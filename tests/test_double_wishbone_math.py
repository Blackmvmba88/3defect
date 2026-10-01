import importlib.util
from math import hypot, isclose
from pathlib import Path

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "blender_addon"
    / "blackmamba_3d"
    / "double_wishbone_math.py"
)
SPEC = importlib.util.spec_from_file_location("blackmamba_double_wishbone_math", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
double_wishbone_math = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(double_wishbone_math)
DoubleWishboneSpec = double_wishbone_math.DoubleWishboneSpec


def _distance(a, b):
    return hypot(b[0] - a[0], b[1] - a[1])


def test_reference_pose_closes_exactly():
    spec = DoubleWishboneSpec()
    pose = spec.solve(0.0)

    assert isclose(pose.lower_joint[0], spec.reference_lower_joint[0], abs_tol=1e-9)
    assert isclose(pose.lower_joint[1], spec.reference_lower_joint[1], abs_tol=1e-9)
    assert isclose(pose.upper_joint[0], spec.reference_upper_joint[0], abs_tol=1e-9)
    assert isclose(pose.upper_joint[1], spec.reference_upper_joint[1], abs_tol=1e-9)
    assert isclose(pose.travel_z, 0.0, abs_tol=1e-9)
    assert isclose(pose.upright_lean_deg, spec.reference_upright_lean_deg, abs_tol=1e-9)


def test_link_lengths_remain_constant_through_travel():
    spec = DoubleWishboneSpec()

    for angle in (-12.0, -6.0, 0.0, 6.0, 12.0):
        pose = spec.solve(angle)
        assert isclose(
            _distance(spec.lower_chassis_axis, pose.lower_joint),
            spec.lower_arm_length,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )
        assert isclose(
            _distance(spec.upper_chassis_axis, pose.upper_joint),
            spec.upper_arm_length,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )
        assert isclose(
            _distance(pose.lower_joint, pose.upper_joint),
            spec.upright_length,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )


def test_travel_sweep_is_deterministic_and_includes_endpoints():
    spec = DoubleWishboneSpec()
    poses = spec.travel_sweep(-10.0, 14.0, 7)

    assert len(poses) == 7
    assert isclose(poses[0].lower_angle_deg, -10.0)
    assert isclose(poses[-1].lower_angle_deg, 14.0)
    assert all(pose.lower_joint[0] > 0.0 for pose in poses)


def test_travel_changes_hub_height_and_upright_lean():
    spec = DoubleWishboneSpec()
    low = spec.solve(-10.0)
    high = spec.solve(10.0)

    assert high.upright_midpoint[1] > low.upright_midpoint[1]
    assert not isclose(high.upright_lean_deg, low.upright_lean_deg, abs_tol=1e-6)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"lower_arm_length": 0.0},
        {"upper_arm_length": 0.0},
        {"chassis_vertical_separation": 0.0},
        {"lower_pivot_spacing": 0.0},
        {"upper_pivot_spacing": 0.0},
        {"tube_diameter": 0.0},
        {"tube_diameter": 0.04, "joint_diameter": 0.03},
    ],
)
def test_invalid_wishbone_spec_is_rejected(kwargs):
    with pytest.raises(ValueError):
        DoubleWishboneSpec(**kwargs).solve()


def test_invalid_travel_sweep_is_rejected():
    spec = DoubleWishboneSpec()

    with pytest.raises(ValueError):
        spec.travel_sweep(-5.0, 5.0, 1)
    with pytest.raises(ValueError):
        spec.travel_sweep(5.0, -5.0, 5)
