"""Tests for the Blender script emitted by the P911 reference profile."""

from defect3d.blender_integration.reference_vehicle import (
    generate_p911_reference_script,
)
from defect3d.vehicles.reference import P911Reference


def test_generated_script_contains_semantic_parts():
    script = generate_p911_reference_script(P911Reference())

    assert "BODY_main_shell" in script
    assert "FENDER_FL" in script
    assert "WHEEL_RR" in script
    assert "FRONT_splitter" in script
    assert "AERO_rear_wing" in script


def test_generated_script_is_self_contained():
    script = generate_p911_reference_script(P911Reference())

    assert "import bpy" in script
    assert "import mathutils" in script
    assert "def build():" in script
    assert 'if __name__ == "__main__":' in script


def test_generated_script_builds_loft_body_and_front_openings():
    script = generate_p911_reference_script(P911Reference())

    assert "SECTIONS = DATA[\"body_sections\"]" in script
    assert "def add_loft_body" in script
    assert "BodySubdivision" in script
    assert "FRONT_center_intake" in script
    assert "FRONT_brake_duct" in script
