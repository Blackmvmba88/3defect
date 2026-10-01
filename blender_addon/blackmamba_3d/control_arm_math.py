from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Tuple


Point3 = Tuple[float, float, float]


def _distance(a: Point3, b: Point3) -> float:
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


@dataclass(frozen=True)
class ControlArmSpec:
    """Parametric A-arm with two chassis pivots and one upright joint.

    Local axes:
    - X: lateral/outboard direction
    - Y: longitudinal direction
    - Z: vertical direction
    """

    arm_length: float = 0.320
    pivot_spacing: float = 0.180
    upright_z: float = 0.0
    tube_diameter: float = 0.025
    joint_diameter: float = 0.038

    def validate(self) -> None:
        if self.arm_length <= 0:
            raise ValueError("arm_length must be positive")
        if self.pivot_spacing <= 0:
            raise ValueError("pivot_spacing must be positive")
        if self.tube_diameter <= 0:
            raise ValueError("tube_diameter must be positive")
        if self.joint_diameter <= self.tube_diameter:
            raise ValueError("joint_diameter must be greater than tube_diameter")

    @property
    def front_pivot(self) -> Point3:
        return (0.0, self.pivot_spacing / 2.0, 0.0)

    @property
    def rear_pivot(self) -> Point3:
        return (0.0, -self.pivot_spacing / 2.0, 0.0)

    @property
    def upright_joint(self) -> Point3:
        return (self.arm_length, 0.0, self.upright_z)

    @property
    def front_leg_length(self) -> float:
        return _distance(self.front_pivot, self.upright_joint)

    @property
    def rear_leg_length(self) -> float:
        return _distance(self.rear_pivot, self.upright_joint)

    @property
    def pivot_span(self) -> float:
        return _distance(self.front_pivot, self.rear_pivot)

    @property
    def points(self) -> tuple[Point3, Point3, Point3]:
        self.validate()
        return self.front_pivot, self.rear_pivot, self.upright_joint

    def geometry(self) -> dict[str, object]:
        self.validate()
        return {
            "front_pivot": self.front_pivot,
            "rear_pivot": self.rear_pivot,
            "upright_joint": self.upright_joint,
            "front_leg_length": self.front_leg_length,
            "rear_leg_length": self.rear_leg_length,
            "pivot_span": self.pivot_span,
            "tube_radius": self.tube_diameter / 2.0,
            "joint_radius": self.joint_diameter / 2.0,
        }
