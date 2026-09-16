import importlib.util
from math import isclose
from pathlib import Path

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "blender_addon"
    / "blackmamba_3d"
    / "control_arm_math.py"
)
SPEC = importlib.util.spec_from_file_location("blackmamba_control_arm_math", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
control_arm_math = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(control_arm_math)
ControlArmSpec = control_arm_math.ControlArmSpec


def test_default_control_arm_is_symmetric():
    spec = ControlArmSpec()
    geometry = spec.geometry()

    assert isclose(spec.front_leg_length, spec.rear_leg_length)
    assert isclose(spec.pivot_span, spec.pivot_spacing)
    assert geometry["front_pivot"][0] == 0.0
    assert geometry["rear_pivot"][0] == 0.0
    assert geometry["upright_joint"][0] == spec.arm_length


def test_upright_z_changes_both_leg_lengths_equally():
    flat = ControlArmSpec(upright_z=0.0)
    raised = ControlArmSpec(upright_z=0.080)

    assert raised.front_leg_length > flat.front_leg_length
    assert isclose(raised.front_leg_length, raised.rear_leg_length)


def test_explicit_interfaces_are_three_distinct_points():
    spec = ControlArmSpec()
    front, rear, upright = spec.points

    assert front != rear
    assert front != upright
    assert rear != upright


@pytest.mark.parametrize(
    "kwargs",
    [
        {"arm_length": 0.0},
        {"pivot_spacing": 0.0},
        {"tube_diameter": 0.0},
        {"tube_diameter": 0.040, "joint_diameter": 0.040},
    ],
)
def test_invalid_control_arm_is_rejected(kwargs):
    with pytest.raises(ValueError):
        ControlArmSpec(**kwargs).geometry()
