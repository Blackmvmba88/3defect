from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


Point3 = Tuple[float, float, float]


@dataclass(frozen=True)
class DamperSpec:
    """Parametric telescopic suspension damper envelope.

    The body is centered on the local Z axis. ``extension_fraction`` previews
    the mechanism between the collapsed and extended states without claiming
    real damping force, pressure, valving, fatigue life, or manufacturing
    readiness.
    """

    body_diameter: float = 0.045
    body_length: float = 0.120
    rod_diameter: float = 0.012
    stroke: float = 0.080
    mount_outer_diameter: float = 0.030
    mount_bore_diameter: float = 0.014
    mount_width: float = 0.018
    extension_fraction: float = 0.50

    def validate(self) -> None:
        if self.body_diameter <= 0:
            raise ValueError("body_diameter must be positive")
        if self.body_length <= 0:
            raise ValueError("body_length must be positive")
        if self.rod_diameter <= 0 or self.rod_diameter >= self.body_diameter:
            raise ValueError("rod_diameter must be positive and smaller than body_diameter")
        if self.stroke <= 0:
            raise ValueError("stroke must be positive")
        if self.mount_outer_diameter <= 0:
            raise ValueError("mount_outer_diameter must be positive")
        if not (0 < self.mount_bore_diameter < self.mount_outer_diameter):
            raise ValueError("mount_bore_diameter must be inside mount_outer_diameter")
        if self.mount_width <= 0:
            raise ValueError("mount_width must be positive")
        if not 0.0 <= self.extension_fraction <= 1.0:
            raise ValueError("extension_fraction must be between 0 and 1")

    @property
    def body_radius(self) -> float:
        return self.body_diameter / 2.0

    @property
    def rod_radius(self) -> float:
        return self.rod_diameter / 2.0

    @property
    def mount_major_radius(self) -> float:
        return (self.mount_outer_diameter + self.mount_bore_diameter) / 4.0

    @property
    def mount_minor_radius(self) -> float:
        return (self.mount_outer_diameter - self.mount_bore_diameter) / 4.0

    @property
    def travel(self) -> float:
        return self.stroke * self.extension_fraction

    @property
    def rod_exposed_length(self) -> float:
        return self.mount_outer_diameter / 2.0 + self.travel

    @property
    def collapsed_center_distance(self) -> float:
        return self.body_length + self.mount_outer_diameter

    @property
    def extended_center_distance(self) -> float:
        return self.collapsed_center_distance + self.stroke

    @property
    def current_center_distance(self) -> float:
        return self.collapsed_center_distance + self.travel

    @property
    def bottom_mount_center(self) -> Point3:
        z = -(self.body_length / 2.0 + self.mount_outer_diameter / 2.0)
        return (0.0, 0.0, z)

    @property
    def top_mount_center(self) -> Point3:
        z = self.body_length / 2.0 + self.rod_exposed_length
        return (0.0, 0.0, z)

    @property
    def rod_center(self) -> Point3:
        body_top = self.body_length / 2.0
        return (0.0, 0.0, body_top + self.rod_exposed_length / 2.0)

    def geometry(self) -> dict[str, object]:
        self.validate()
        return {
            "body_center": (0.0, 0.0, 0.0),
            "body_depth": self.body_length,
            "body_radius": self.body_radius,
            "rod_center": self.rod_center,
            "rod_depth": self.rod_exposed_length,
            "rod_radius": self.rod_radius,
            "bottom_mount_center": self.bottom_mount_center,
            "top_mount_center": self.top_mount_center,
            "mount_major_radius": self.mount_major_radius,
            "mount_minor_radius": self.mount_minor_radius,
            "mount_width": self.mount_width,
        }
