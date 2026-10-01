"""Cross-repository contract test for the annexed BM-OC-002 ocarina."""

import json
from pathlib import Path

from defect3d.asset_contract import validate_asset_contract
from defect3d.pipeline import plan_asset_pipeline


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "examples" / "mamba3d_ocarina_bm_oc_002.json"


def _load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_annexed_ocarina_contract_is_structurally_valid():
    data = _load()
    assert validate_asset_contract(data) == []


def test_annexed_ocarina_remains_unvalidated_until_measurements_exist():
    data = _load()
    assert data["validation"]["dimensions"] == "unknown"
    assert data["manufacturing"]["ready"] is False


def test_annexed_ocarina_gets_integrated_provider_plan():
    plan = plan_asset_pipeline(_load())
    assert plan["contract_valid"] is True

    measure = next(step for step in plan["steps"] if step["key"] == "measure")
    assert "ocarina" in measure["providers"]

    dcc = next(step for step in plan["steps"] if step["key"] == "dcc")
    assert "xarvis_blender" in dcc["providers"]
