from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from typing import Literal

from .double_wishbone_math import DoubleWishboneSpec, WishbonePose


RoadKind = Literal["flat", "sine", "bump", "dip"]


@dataclass(frozen=True)
class RoadProfileSpec:
    """Deterministic longitudinal road-height profile.

    Distances and heights use the same length unit as the suspension geometry.
    The road varies along vehicle-local Y while the wishbone solve remains in
    the front-view X/Z plane.
    """

    kind: RoadKind = "sine"
    amplitude: float = 0.010
    wavelength: float = 1.50
    center: float = 4.0
    feature_length: float = 0.60

    def validate(self) -> None:
        if self.kind not in {"flat", "sine", "bump", "dip"}:
            raise ValueError("unsupported road profile kind")
        if self.amplitude < 0:
            raise ValueError("amplitude must be non-negative")
        if self.wavelength <= 0:
            raise ValueError("wavelength must be positive")
        if self.feature_length <= 0:
            raise ValueError("feature_length must be positive")

    def height_at(self, distance: float) -> float:
        self.validate()
        if self.kind == "flat" or self.amplitude == 0:
            return 0.0
        if self.kind == "sine":
            return self.amplitude * sin(2.0 * pi * distance / self.wavelength)

        half = self.feature_length / 2.0
        offset = distance - self.center
        if abs(offset) > half:
            return 0.0

        # Raised-cosine feature: zero slope at the start, peak and end.
        normalized = offset / half
        shape = 0.5 * (1.0 + cos(pi * normalized))
        sign = 1.0 if self.kind == "bump" else -1.0
        return sign * self.amplitude * shape


@dataclass(frozen=True)
class RoadRigSample:
    time_s: float
    distance: float
    road_z: float
    lower_angle_deg: float
    pose: WishbonePose


@dataclass(frozen=True)
class RoadRigSpec:
    speed: float = 30.0
    duration_s: float = 1.0
    sample_hz: float = 60.0
    min_angle_deg: float = -20.0
    max_angle_deg: float = 20.0

    def validate(self) -> None:
        if self.speed < 0:
            raise ValueError("speed must be non-negative")
        if self.duration_s <= 0:
            raise ValueError("duration_s must be positive")
        if self.sample_hz <= 0:
            raise ValueError("sample_hz must be positive")
        if self.min_angle_deg >= self.max_angle_deg:
            raise ValueError("min_angle_deg must be below max_angle_deg")


def _solve_angle_for_travel(
    suspension: DoubleWishboneSpec,
    target_travel_z: float,
    *,
    min_angle_deg: float,
    max_angle_deg: float,
    tolerance: float = 1e-7,
    iterations: int = 64,
) -> float:
    """Invert the local monotonic wishbone travel curve by bisection."""

    low_angle = float(min_angle_deg)
    high_angle = float(max_angle_deg)
    low_pose = suspension.solve(low_angle)
    high_pose = suspension.solve(high_angle)
    low_value = low_pose.travel_z
    high_value = high_pose.travel_z

    lower_bound = min(low_value, high_value)
    upper_bound = max(low_value, high_value)
    if target_travel_z < lower_bound - tolerance or target_travel_z > upper_bound + tolerance:
        raise ValueError(
            "road input exceeds the configured wishbone travel envelope"
        )

    increasing = high_value >= low_value
    for _ in range(iterations):
        mid_angle = (low_angle + high_angle) / 2.0
        mid_value = suspension.solve(mid_angle).travel_z
        error = mid_value - target_travel_z
        if abs(error) <= tolerance:
            return mid_angle

        if increasing:
            if mid_value < target_travel_z:
                low_angle = mid_angle
            else:
                high_angle = mid_angle
        else:
            if mid_value > target_travel_z:
                low_angle = mid_angle
            else:
                high_angle = mid_angle

    return (low_angle + high_angle) / 2.0


def simulate_road_run(
    suspension: DoubleWishboneSpec,
    road: RoadProfileSpec,
    rig: RoadRigSpec,
) -> tuple[RoadRigSample, ...]:
    """Drive a road profile under a fixed chassis and solve wheel travel.

    The first kinematic rig assumes the tire/contact point follows the road
    height exactly and maps that vertical input to the wishbone hub travel.
    No mass, tire compliance, spring force or damping force is modeled here.
    """

    suspension.validate()
    road.validate()
    rig.validate()

    sample_count = max(2, int(round(rig.duration_s * rig.sample_hz)) + 1)
    samples = []
    for index in range(sample_count):
        time_s = rig.duration_s * index / (sample_count - 1)
        distance = rig.speed * time_s
        road_z = road.height_at(distance)
        angle = _solve_angle_for_travel(
            suspension,
            road_z,
            min_angle_deg=rig.min_angle_deg,
            max_angle_deg=rig.max_angle_deg,
        )
        pose = suspension.solve(angle)
        samples.append(
            RoadRigSample(
                time_s=time_s,
                distance=distance,
                road_z=road_z,
                lower_angle_deg=angle,
                pose=pose,
            )
        )

    return tuple(samples)
