"""Tests for the BlackMamba 3D asset contract validator."""

from defect3d.asset_contract import (
    dimension_within_tolerance,
    validate_asset_contract,
)


def _manifest():
    return {
        "schema_version": "1.0",
        "asset_id": "BM-DEMO-001",
        "revision": "A",
        "stage": "engineering_design",
        "units": "mm",
        "blueprint": {"id": "BP-001", "revision": "A"},
        "parts": [
            {
                "part_id": "P001",
                "name": "body",
                "status": "validated",
                "dimensions": {
                    "length": {
                        "target": 120.0,
                        "tolerance": 0.2,
                        "measured": 120.1,
                        "status": "pass",
                    }
                },
                "interfaces": [],
            }
        ],
        "validation": {
            "dimensions": "pass",
            "interfaces": "pass",
            "closed_geometry": "unknown",
            "assembly": "pass",
        },
        "manufacturing": {
            "ready": False,
            "process": None,
            "material_spec": None,
            "evidence": [],
        },
    }


def test_dimension_within_tolerance_accepts_boundary():
    assert dimension_within_tolerance(10.0, 10.2, 0.2)


def test_valid_engineering_manifest_passes():
    assert validate_asset_contract(_manifest()) == []


def test_out_of_tolerance_measurement_fails():
    data = _manifest()
    dimension = data["parts"][0]["dimensions"]["length"]
    dimension["measured"] = 120.5

    errors = validate_asset_contract(data)

    assert any("out of tolerance" in error for error in errors)
    assert any("contradicts measured geometry" in error for error in errors)


def test_duplicate_part_ids_fail():
    data = _manifest()
    data["parts"].append(dict(data["parts"][0]))

    errors = validate_asset_contract(data)

    assert "duplicate part_id: P001" in errors


def test_manufacturing_ready_requires_engineering_evidence():
    data = _manifest()
    data["stage"] = "manufacturing_ready"
    data["manufacturing"]["ready"] = True

    errors = validate_asset_contract(data)

    assert any("non-empty process" in error for error in errors)
    assert any("non-empty material_spec" in error for error in errors)
    assert any("evidence item" in error for error in errors)
    assert any("closed_geometry=pass" in error for error in errors)


def test_manufacturing_ready_can_pass_when_all_gates_pass():
    data = _manifest()
    data["stage"] = "manufacturing_ready"
    data["validation"]["closed_geometry"] = "pass"
    data["manufacturing"] = {
        "ready": True,
        "process": "cnc_milling",
        "material_spec": "aluminum_6061-t6",
        "evidence": ["inspection/BM-DEMO-001-A.json"],
    }

    assert validate_asset_contract(data) == []
