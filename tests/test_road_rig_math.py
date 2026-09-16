import importlib.util
from math import isclose
from pathlib import Path
import sys

import pytest


PKG_DIR = Path(__file__).resolve().parents[1] / "blender_addon" / "blackmamba_3d"


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, PKG_DIR / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


double_wishbone_math = _load(
    "blackmamba_3d.double_wishbone_math", "double_wishbone_math.py"
)
road_rig_math = _load("blackmamba_3d.road_rig_math", "road_rig_math.py")

DoubleWishboneSpec = double_wishbone_math.DoubleWishboneSpec
RoadProfileSpec = road_rig_math.RoadProfileSpec
RoadRigSpec = road_rig_math.RoadRigSpec
simulate_road_run = road_rig_math.simulate_road_run


def test_flat_road_is_valid_baseline_even_at_high_speed():
    suspension = DoubleWishboneSpec()
    road = RoadProfileSpec(kind="flat")
    rig = RoadRigSpec(speed=83.3333333333, duration_s=0.2, sample_hz=100.0)

    samples = simulate_road_run(suspension, road, rig)

    assert len(samples) == 21
    assert all(isclose(sample.road_z, 0.0, abs_tol=1e-12) for sample in samples)
    assert all(isclose(sample.pose.travel_z, 0.0, abs_tol=1e-6) for sample in samples)


def test_speed_changes_excitation_frequency_not_profile_amplitude():
    suspension = DoubleWishboneSpec()
    road = RoadProfileSpec(kind="sine", amplitude=0.005, wavelength=1.0)

    slow = simulate_road_run(
        suspension,
        road,
        RoadRigSpec(speed=10.0, duration_s=0.1, sample_hz=100.0),
    )
    fast = simulate_road_run(
        suspension,
        road,
        RoadRigSpec(speed=20.0, duration_s=0.1, sample_hz=100.0),
    )

    assert max(abs(sample.road_z) for sample in slow) <= road.amplitude + 1e-12
    assert max(abs(sample.road_z) for sample in fast) <= road.amplitude + 1e-12
    assert not isclose(slow[5].road_z, fast[5].road_z, abs_tol=1e-9)


def test_local_bump_has_zero_slope_style_endpoints_and_peak():
    road = RoadProfileSpec(kind="bump", amplitude=0.02, center=2.0, feature_length=1.0)

    assert isclose(road.height_at(1.5), 0.0, abs_tol=1e-12)
    assert isclose(road.height_at(2.0), 0.02, abs_tol=1e-12)
    assert isclose(road.height_at(2.5), 0.0, abs_tol=1e-12)
    assert isclose(road.height_at(0.0), 0.0, abs_tol=1e-12)


def test_road_height_maps_back_to_wishbone_travel():
    suspension = DoubleWishboneSpec()
    road = RoadProfileSpec(kind="sine", amplitude=0.004, wavelength=2.0)
    rig = RoadRigSpec(speed=8.0, duration_s=0.25, sample_hz=40.0)

    samples = simulate_road_run(suspension, road, rig)

    for sample in samples:
        assert isclose(sample.pose.travel_z, sample.road_z, abs_tol=2e-6)


def test_road_input_outside_travel_envelope_fails_closed():
    suspension = DoubleWishboneSpec()
    road = RoadProfileSpec(kind="bump", amplitude=0.50, center=0.1, feature_length=0.2)
    rig = RoadRigSpec(speed=1.0, duration_s=0.2, sample_hz=20.0)

    with pytest.raises(ValueError, match="travel envelope"):
        simulate_road_run(suspension, road, rig)


@pytest.mark.parametrize(
    "profile",
    [
        RoadProfileSpec(amplitude=-0.1),
        RoadProfileSpec(wavelength=0.0),
        RoadProfileSpec(feature_length=0.0),
    ],
)
def test_invalid_road_profile_is_rejected(profile):
    with pytest.raises(ValueError):
        profile.height_at(0.0)
