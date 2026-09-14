"""Tests for the integrated BlackMamba 3D ecosystem registry and planner."""

from defect3d.integrations import (
    all_capabilities,
    capability_matrix,
    get_provider,
    providers_for,
)
from defect3d.pipeline import plan_asset_pipeline


def _manifest():
    return {
        "schema_version": "1.0",
        "asset_id": "BM-INTEGRATION-001",
        "revision": "A",
        "stage": "engineering_design",
        "units": "mm",
        "blueprint": {"id": "BP-INTEGRATION-001", "revision": "A"},
        "parts": [
            {
                "part_id": "P001",
                "name": "body",
                "status": "validated",
                "dimensions": {
                    "length": {
                        "target": 100.0,
                        "tolerance": 0.2,
                        "measured": 100.1,
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
            "render": "unknown",
        },
        "exports": ["glb", "png"],
        "manufacturing": {
            "ready": False,
            "process": None,
            "material_spec": None,
            "evidence": [],
        },
    }


def test_core_provider_is_native_and_active():
    provider = get_provider("core")
    assert provider is not None
    assert provider.repository == "Blackmvmba88/3defect"
    assert provider.integration_mode == "native"
    assert provider.status == "active"


def test_assembly_is_annexed_through_weaponassambly():
    repositories = [provider.repository for provider in providers_for("assembly")]
    assert "Blackmvmba88/weaponassambly" in repositories


def test_registry_annexes_realtime_and_webgl_providers():
    assert any(p.repository == "Blackmvmba88/blender-motion-capture" for p in providers_for("websocket"))
    assert any(p.repository == "Blackmvmba88/3dwave" for p in providers_for("webgl"))
    assert any(p.repository == "Blackmvmba88/Avion" for p in providers_for("threejs"))


def test_capability_matrix_is_deterministic():
    capabilities = all_capabilities()
    assert capabilities == tuple(sorted(capabilities))
    matrix = capability_matrix()
    assert "validation" in matrix
    assert "core" in matrix["validation"]


def test_valid_manifest_builds_cross_repository_plan():
    plan = plan_asset_pipeline(_manifest())
    assert plan["contract_valid"] is True
    step_keys = [step["key"] for step in plan["steps"]]
    assert step_keys[:4] == ["contract", "geometry", "measure", "assemble"]
    assert "runtime" in step_keys

    assemble = next(step for step in plan["steps"] if step["key"] == "assemble")
    assert "assembly" in assemble["providers"]

    measure = next(step for step in plan["steps"] if step["key"] == "measure")
    assert "ocarina" in measure["providers"]


def test_invalid_contract_blocks_downstream_steps():
    data = _manifest()
    data["parts"][0]["dimensions"]["length"]["measured"] = 101.0
    plan = plan_asset_pipeline(data)

    assert plan["contract_valid"] is False
    assert plan["contract_errors"]
    downstream = [step for step in plan["steps"] if step["key"] != "contract"]
    assert downstream
    assert all(step["status"] == "blocked" for step in downstream)
