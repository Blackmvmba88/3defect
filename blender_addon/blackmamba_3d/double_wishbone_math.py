from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, degrees, hypot, radians, sin, sqrt
from typing import Tuple


Point2 = Tuple[float, float]


@dataclass(frozen=True)
class WishbonePose:
    lower_joint: Point2
    upper_joint: Point2
    upright_midpoint: Point2
    upright_lean_deg: float
    travel_z: float
    lower_angle_deg: float


@dataclass(frozen=True)
class DoubleWishboneSpec:
    """Idealized front-view four-bar double-wishbone geometry.

    The model uses the effective pivot axes in the X/Z plane.  The two real
    chassis pivots of each A-arm remain a separate 3D width parameter for the
    Blender generator; the planar solver treats each pair as one hinge axis.
    """

    lower_arm_length: float = 0.340
    upper_arm_length: float = 0.300
    chassis_vertical_separation: float = 0.180
    lower_pivot_spacing: float = 0.200
    upper_pivot_spacing: float = 0.160
    tube_diameter: float = 0.025
    joint_diameter: float = 0.038

    def validate(self) -> None:
        for name, value in (
            ("lower_arm_length", self.lower_arm_length),
            ("upper_arm_length", self.upper_arm_length),
            ("chassis_vertical_separation", self.chassis_vertical_separation),
            ("lower_pivot_spacing", self.lower_pivot_spacing),
            ("upper_pivot_spacing", self.upper_pivot_spacing),
            ("tube_diameter", self.tube_diameter),
            ("joint_diameter", self.joint_diameter),
        ):
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.joint_diameter <= self.tube_diameter:
            raise ValueError("joint_diameter must be greater than tube_diameter")

    @property
    def lower_chassis_axis(self) -> Point2:
        return (0.0, 0.0)

    @property
    def upper_chassis_axis(self) -> Point2:
        return (0.0, self.chassis_vertical_separation)

    @property
    def reference_lower_joint(self) -> Point2:
        return (self.lower_arm_length, 0.0)

    @property
    def reference_upper_joint(self) -> Point2:
        return (self.upper_arm_length, self.chassis_vertical_separation)

    @property
    def upright_length(self) -> float:
        lower = self.reference_lower_joint
        upper = self.reference_upper_joint
        return hypot(upper[0] - lower[0], upper[1] - lower[1])

    @property
    def reference_midpoint(self) -> Point2:
        lower = self.reference_lower_joint
        upper = self.reference_upper_joint
        return ((lower[0] + upper[0]) / 2.0, (lower[1] + upper[1]) / 2.0)

    @property
    def reference_upright_lean_deg(self) -> float:
        dx = self.reference_upper_joint[0] - self.reference_lower_joint[0]
        dz = self.reference_upper_joint[1] - self.reference_lower_joint[1]
        return degrees(atan2(dx, dz))

    def solve(self, lower_angle_deg: float = 0.0) -> WishbonePose:
        self.validate()
        theta = radians(lower_angle_deg)
        lower = (
            self.lower_arm_length * cos(theta),
            self.lower_arm_length * sin(theta),
        )
        upper_axis = self.upper_chassis_axis
        upper = self._circle_intersection(
            lower,
            self.upright_length,
            upper_axis,
            self.upper_arm_length,
        )

        midpoint = ((lower[0] + upper[0]) / 2.0, (lower[1] + upper[1]) / 2.0)
        dx = upper[0] - lower[0]
        dz = upper[1] - lower[1]
        lean = degrees(atan2(dx, dz))
        travel = midpoint[1] - self.reference_midpoint[1]

        return WishbonePose(
            lower_joint=lower,
            upper_joint=upper,
            upright_midpoint=midpoint,
            upright_lean_deg=lean,
            travel_z=travel,
            lower_angle_deg=lower_angle_deg,
        )

    def travel_sweep(
        self,
        min_angle_deg: float = -15.0,
        max_angle_deg: float = 15.0,
        steps: int = 13,
    ) -> tuple[WishbonePose, ...]:
        if steps < 2:
            raise ValueError("steps must be >= 2")
        if max_angle_deg <= min_angle_deg:
            raise ValueError("max_angle_deg must be greater than min_angle_deg")

        poses = []
        for index in range(steps):
            fraction = index / (steps - 1)
            angle = min_angle_deg + (max_angle_deg - min_angle_deg) * fraction
            poses.append(self.solve(angle))
        return tuple(poses)

    def _circle_intersection(
        self,
        center0: Point2,
        radius0: float,
        center1: Point2,
        radius1: float,
    ) -> Point2:
        x0, z0 = center0
        x1, z1 = center1
        dx = x1 - x0
        dz = z1 - z0
        distance = hypot(dx, dz)

        if distance <= 1e-12:
            raise ValueError("wishbone solver reached coincident circle centers")
        if distance > radius0 + radius1 + 1e-9:
            raise ValueError("wishbone geometry cannot close at this lower-arm angle")
        if distance < abs(radius0 - radius1) - 1e-9:
            raise ValueError("wishbone circles are nested and cannot close")

        a = (radius0**2 - radius1**2 + distance**2) / (2.0 * distance)
        h_sq = radius0**2 - a**2
        if h_sq < -1e-9:
            raise ValueError("wishbone solver has no real intersection")
        h = sqrt(max(0.0, h_sq))

        base_x = x0 + a * dx / distance
        base_z = z0 + a * dz / distance
        perp_x = -dz / distance
        perp_z = dx / distance

        candidates = (
            (base_x + h * perp_x, base_z + h * perp_z),
            (base_x - h * perp_x, base_z - h * perp_z),
        )
        reference = self.reference_upper_joint

        def score(point: Point2) -> tuple[float, float]:
            reference_error = hypot(point[0] - reference[0], point[1] - reference[1])
            negative_x_penalty = 1.0 if point[0] < 0 else 0.0
            return negative_x_penalty, reference_error

        return min(candidates, key=score)
