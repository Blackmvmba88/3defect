"""Tests for the P911_REF_001 parameter model."""

import pytest

from defect3d.vehicles.reference import P911Reference, P911ReferenceParams


def test_reference_profile_resolves_expected_dimensions():
    car = P911Reference()
    resolved = car.resolved()

    assert resolved["wheelbase"] == pytest.approx(2.27)
    assert resolved["width"] > car.params.width
    assert resolved["ground_clearance"] < car.params.ground_clearance


def test_wheel_centers_are_symmetric():
    centers = P911Reference().wheel_centers()

    assert centers["FL"][0] == pytest.approx(-centers["RL"][0])
    assert centers["FR"][0] == pytest.approx(-centers["RR"][0])
    assert centers["FL"][1] == pytest.approx(-centers["FR"][1])
    assert centers["RL"][1] == pytest.approx(-centers["RR"][1])


def test_reference_match_is_bounded():
    with pytest.raises(ValueError):
        P911Reference(P911ReferenceParams(reference_match=1.1))
