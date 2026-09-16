import importlib.util
from math import isclose, hypot
from pathlib import Path

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "blender_addon"
    / "blackmamba_3d"
    / "spring_math.py"
)
SPEC = importlib.util.spec_from_file_location("blackmamba_spring_math", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
spring_math = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(spring_math)
SpringSpec = spring_math.SpringSpec


def test_default_spring_geometry_respects_requested_envelope():
    spec = SpringSpec()
    points = spec.helix_points()

    assert len(points) == spec.turns * spec.samples_per_turn + 1
    assert isclose(points[0][2], -spec.centerline_span / 2.0)
    assert isclose(points[-1][2], spec.centerline_span / 2.0)

    for x, y, _z in (points[0], points[len(points) // 2], points[-1]):
        assert isclose(hypot(x, y), spec.centerline_radius, rel_tol=1e-9)

    assert isclose(spec.outer_diameter, spec.coil_diameter + spec.wire_diameter)
    assert isclose(spec.inner_diameter, spec.coil_diameter - spec.wire_diameter)
    assert isclose(spec.pitch, spec.centerline_span / spec.turns)


def test_integer_turns_finish_at_same_angular_phase():
    spec = SpringSpec(turns=6, samples_per_turn=16)
    first = spec.helix_points()[0]
    last = spec.helix_points()[-1]

    assert isclose(first[0], last[0], rel_tol=1e-9, abs_tol=1e-9)
    assert isclose(first[1], last[1], rel_tol=1e-9, abs_tol=1e-9)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"wire_diameter": 0.0},
        {"wire_diameter": 0.02, "coil_diameter": 0.02},
        {"wire_diameter": 0.02, "free_length": 0.02},
        {"turns": 0},
        {"samples_per_turn": 4},
    ],
)
def test_invalid_spring_spec_is_rejected(kwargs):
    with pytest.raises(ValueError):
        SpringSpec(**kwargs).helix_points()
