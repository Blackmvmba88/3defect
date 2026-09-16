import importlib.util
from math import isclose
from pathlib import Path

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "blender_addon"
    / "blackmamba_3d"
    / "damper_math.py"
)
SPEC = importlib.util.spec_from_file_location("blackmamba_damper_math", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
damper_math = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(damper_math)
DamperSpec = damper_math.DamperSpec


def test_default_damper_geometry_matches_requested_travel():
    spec = DamperSpec(extension_fraction=0.5)
    geometry = spec.geometry()

    assert isclose(spec.travel, spec.stroke * 0.5)
    assert isclose(
        spec.current_center_distance,
        spec.collapsed_center_distance + spec.stroke * 0.5,
    )
    assert isclose(
        spec.extended_center_distance - spec.collapsed_center_distance,
        spec.stroke,
    )
    assert geometry["body_depth"] == spec.body_length
    assert geometry["rod_depth"] == spec.rod_exposed_length


def test_mount_centers_match_current_center_distance():
    spec = DamperSpec(extension_fraction=0.75)
    bottom_z = spec.bottom_mount_center[2]
    top_z = spec.top_mount_center[2]

    assert isclose(top_z - bottom_z, spec.current_center_distance)


def test_torus_radii_reconstruct_mount_diameters():
    spec = DamperSpec(mount_outer_diameter=0.040, mount_bore_diameter=0.020)

    outer_radius = spec.mount_major_radius + spec.mount_minor_radius
    inner_radius = spec.mount_major_radius - spec.mount_minor_radius

    assert isclose(outer_radius * 2.0, spec.mount_outer_diameter)
    assert isclose(inner_radius * 2.0, spec.mount_bore_diameter)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"body_diameter": 0.0},
        {"body_length": 0.0},
        {"rod_diameter": 0.045},
        {"stroke": 0.0},
        {"mount_outer_diameter": 0.0},
        {"mount_bore_diameter": 0.030, "mount_outer_diameter": 0.030},
        {"mount_width": 0.0},
        {"extension_fraction": -0.01},
        {"extension_fraction": 1.01},
    ],
)
def test_invalid_damper_spec_is_rejected(kwargs):
    with pytest.raises(ValueError):
        DamperSpec(**kwargs).geometry()
