from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from typing import Tuple


Point3 = Tuple[float, float, float]


@dataclass(frozen=True)
class SpringSpec:
    """Parametric helical compression spring envelope in Blender length units.

    ``coil_diameter`` is the centerline diameter of the wire helix.
    ``free_length`` is the overall axial envelope, including wire radius at
    both ends.  The generated curve centerline is shortened by one wire
    diameter so the beveled curve remains inside that requested envelope.
    """

    wire_diameter: float = 0.012
    coil_diameter: float = 0.080
    free_length: float = 0.180
    turns: int = 8
    samples_per_turn: int = 32

    def validate(self) -> None:
        if self.wire_diameter <= 0:
            raise ValueError("wire_diameter must be positive")
        if self.coil_diameter <= self.wire_diameter:
            raise ValueError("coil_diameter must be greater than wire_diameter")
        if self.free_length <= self.wire_diameter:
            raise ValueError("free_length must be greater than wire_diameter")
        if self.turns < 1:
            raise ValueError("turns must be >= 1")
        if self.samples_per_turn < 8:
            raise ValueError("samples_per_turn must be >= 8")

    @property
    def centerline_radius(self) -> float:
        return self.coil_diameter / 2.0

    @property
    def centerline_span(self) -> float:
        return self.free_length - self.wire_diameter

    @property
    def outer_diameter(self) -> float:
        return self.coil_diameter + self.wire_diameter

    @property
    def inner_diameter(self) -> float:
        return self.coil_diameter - self.wire_diameter

    @property
    def pitch(self) -> float:
        return self.centerline_span / self.turns

    def helix_points(self) -> Tuple[Point3, ...]:
        self.validate()
        segments = self.turns * self.samples_per_turn
        radius = self.centerline_radius
        half_span = self.centerline_span / 2.0
        points = []

        for index in range(segments + 1):
            fraction = index / segments
            angle = 2.0 * pi * self.turns * fraction
            z = -half_span + self.centerline_span * fraction
            points.append((radius * cos(angle), radius * sin(angle), z))

        return tuple(points)
