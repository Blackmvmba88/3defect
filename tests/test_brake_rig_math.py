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
brake_rig_math = _load("blackmamba_3d.brake_rig_math", "brake_rig_math.py")

DoubleWishboneSpec = double_wishbone_math.DoubleWishboneSpec
BrakeRigSpec = brake_rig_math.BrakeRigSpec
simulate_braking_run = brake_rig_math.simulate_braking_run


def test_load_transfer_matches_basic_longitudinal_formula():
    rig = BrakeRigSpec(
        vehicle_mass_kg=1500.0,
        wheelbase_m=3.0,
        cg_height_m=0.50,
        decel_mps2=6.0,
    )

    expected = 1500.0 * 6.0 * 0.50 / 3.0
    assert isclose(rig.total_load_transfer_n, expected, rel_tol=1e-12)
    assert isclose(rig.front_corner_load_step_n, expected / 2.0, rel_tol=1e-12)


def test_static_compression_matches_force_over_spring_rate():
    rig = BrakeRigSpec(
        vehicle_mass_kg=1200.0,
        wheelbase_m=2.4,
        cg_height_m=0.50,
        decel_mps2=4.8,
        spring_rate_n_per_m=30000.0,
    )

    assert isclose(
        rig.static_corner_compression_m,
        rig.front_corner_load_step_n / 30000.0,
        rel_tol=1e-12,
    )


def test_braking_run_builds_front_compression_and_wishbone_travel():
    suspension = DoubleWishboneSpec()
    rig = BrakeRigSpec(
        initial_speed_mps=25.0,
        decel_mps2=7.0,
        duration_s=0.40,
        sample_hz=120.0,
    )

    samples = simulate_braking_run(suspension, rig)

    assert len(samples) == 49
    assert samples[0].compression_m == 0.0
    assert max(sample.compression_m for sample in samples) > 0.0
    assert max(sample.pose.travel_z for sample in samples) > 0.0
    for sample in samples:
        assert isclose(sample.pose.travel_z, sample.compression_m, abs_tol=2e-6)


def test_stiffer_spring_reduces_brake_dive():
    suspension = DoubleWishboneSpec()
    common = dict(
        initial_speed_mps=30.0,
        decel_mps2=8.0,
        duration_s=0.45,
        sample_hz=120.0,
        damping_n_s_per_m=3200.0,
    )

    soft = simulate_braking_run(
        suspension,
        BrakeRigSpec(spring_rate_n_per_m=25000.0, **common),
    )
    stiff = simulate_braking_run(
        suspension,
        BrakeRigSpec(spring_rate_n_per_m=50000.0, **common),
    )

    assert max(sample.compression_m for sample in stiff) < max(
        sample.compression_m for sample in soft
    )


def test_higher_cg_increases_load_transfer_and_dive():
    suspension = DoubleWishboneSpec()
    common = dict(
        initial_speed_mps=25.0,
        decel_mps2=7.0,
        duration_s=0.35,
        sample_hz=120.0,
    )

    low_cg_rig = BrakeRigSpec(cg_height_m=0.35, **common)
    high_cg_rig = BrakeRigSpec(cg_height_m=0.70, **common)
    low_cg = simulate_braking_run(suspension, low_cg_rig)
    high_cg = simulate_braking_run(suspension, high_cg_rig)

    assert high_cg_rig.total_load_transfer_n > low_cg_rig.total_load_transfer_n
    assert max(sample.compression_m for sample in high_cg) > max(
        sample.compression_m for sample in low_cg
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"vehicle_mass_kg": 0.0},
        {"wheelbase_m": 0.0},
        {"cg_height_m": 0.0},
        {"initial_speed_mps": 0.0},
        {"decel_mps2": 0.0},
        {"spring_rate_n_per_m": 0.0},
        {"damping_n_s_per_m": 0.0},
        {"duration_s": 0.0},
        {"sample_hz": 0.0},
    ],
)
def test_invalid_brake_rig_is_rejected(kwargs):
    with pytest.raises(ValueError):
        BrakeRigSpec(**kwargs).validate()
