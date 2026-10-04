"""Parametric reference-matched widebody sports car.

The goal is not to hard-code one dead mesh. The model stores master
dimensions plus visual exaggeration controls so Blender exporters and future
reference-fit tooling can reconstruct the silhouette consistently.

Coordinates follow the 3defect vehicle convention:
X = longitudinal, Y = lateral, Z = vertical.
"""

from dataclasses import asdict, dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class ReferenceRatios:
    """Normalized visual ratios measured against wheelbase == 1.0."""

    wheelbase: float = 1.0
    wheel_diameter: float = 0.285
    total_height: float = 0.545
    hood_height: float = 0.285
    beltline_height: float = 0.390
    roof_start: float = 0.295
    roof_length: float = 0.465


@dataclass
class P911ReferenceParams:
    """Master parameters for the P911_REF_001 reference profile."""

    length: float = 4.00
    width: float = 1.86
    height: float = 1.23
    wheelbase: float = 2.27
    front_track: float = 1.60
    rear_track: float = 1.64
    ground_clearance: float = 0.075

    wheel_radius_front: float = 0.315
    wheel_radius_rear: float = 0.330
    wheel_width_front: float = 0.245
    wheel_width_rear: float = 0.285

    front_overhang: float = 0.77
    rear_overhang: float = 0.96

    body_scale_x: float = 1.00
    body_scale_y: float = 1.08
    body_scale_z: float = 0.94

    cabin_scale_x: float = 0.94
    cabin_scale_y: float = 0.92
    cabin_scale_z: float = 1.00

    front_fender_bulge: float = 0.115
    rear_fender_bulge: float = 0.155

    headlight_radius: float = 0.155

    splitter_depth: float = 0.145
    splitter_height: float = 0.035

    wing_width: float = 1.54
    wing_depth: float = 0.29
    wing_height: float = 0.34

    reference_match: float = 1.0
    body_widening: float = 1.08
    roof_compression: float = 0.94
    wheel_exaggeration: float = 1.05
    fender_exaggeration: float = 1.18
    stance: float = 0.92
    front_visual_weight: float = 1.06
    rear_visual_weight: float = 1.08

    body_color: Tuple[float, float, float] = (0.86, 0.025, 0.055)

    def validate(self) -> None:
        positive = (
            "length", "width", "height", "wheelbase",
            "front_track", "rear_track", "wheel_radius_front",
            "wheel_radius_rear", "wheel_width_front", "wheel_width_rear",
        )
        for name in positive:
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be > 0")

        if not 0.0 <= self.reference_match <= 1.0:
            raise ValueError("reference_match must be between 0.0 and 1.0")

        if self.wheelbase >= self.length:
            raise ValueError("wheelbase must be smaller than total length")


class P911Reference:
    """Parametric description of the supplied red widebody reference car."""

    model_id = "P911_REF_001"

    def __init__(self, params: P911ReferenceParams | None = None):
        self.params = params or P911ReferenceParams()
        self.params.validate()
        self.ratios = ReferenceRatios()

    @staticmethod
    def _lerp(realistic: float, reference: float, amount: float) -> float:
        return realistic + ((reference - realistic) * amount)

    def resolved(self) -> Dict[str, float | Tuple[float, float, float]]:
        p = self.params
        m = p.reference_match

        wheel_scale = self._lerp(1.0, p.wheel_exaggeration, m)
        body_y = self._lerp(1.0, p.body_scale_y, m)
        body_z = self._lerp(1.0, p.body_scale_z, m)
        fender_scale = self._lerp(1.0, p.fender_exaggeration, m)
        stance = self._lerp(1.0, p.stance, m)

        return {
            "length": p.length * p.body_scale_x,
            "width": p.width * body_y,
            "height": p.height * body_z,
            "wheelbase": p.wheelbase,
            "front_track": p.front_track,
            "rear_track": p.rear_track,
            "ground_clearance": p.ground_clearance * stance,
            "wheel_radius_front": p.wheel_radius_front * wheel_scale,
            "wheel_radius_rear": p.wheel_radius_rear * wheel_scale,
            "wheel_width_front": p.wheel_width_front,
            "wheel_width_rear": p.wheel_width_rear,
            "front_fender_bulge": p.front_fender_bulge * fender_scale,
            "rear_fender_bulge": p.rear_fender_bulge * fender_scale,
            "headlight_radius": p.headlight_radius,
            "splitter_depth": p.splitter_depth,
            "splitter_height": p.splitter_height,
            "wing_width": p.wing_width,
            "wing_depth": p.wing_depth,
            "wing_height": p.wing_height,
            "body_color": p.body_color,
        }

    def wheel_centers(self) -> Dict[str, Tuple[float, float, float]]:
        r = self.resolved()
        x_front = r["wheelbase"] / 2.0
        x_rear = -x_front
        z_front = r["wheel_radius_front"]
        z_rear = r["wheel_radius_rear"]

        return {
            "FL": (x_front, r["front_track"] / 2.0, z_front),
            "FR": (x_front, -r["front_track"] / 2.0, z_front),
            "RL": (x_rear, r["rear_track"] / 2.0, z_rear),
            "RR": (x_rear, -r["rear_track"] / 2.0, z_rear),
        }

    def part_graph(self) -> Dict[str, object]:
        return {
            "BODY": [
                "main_shell", "hood", "roof", "windshield_frame",
                "rear_shell", "rocker_panels",
            ],
            "FENDERS": ["FL", "FR", "RL", "RR"],
            "FRONT": [
                "bumper", "center_intake", "brake_duct_L",
                "brake_duct_R", "splitter",
            ],
            "LIGHTS": ["headlight_L", "headlight_R"],
            "WINDOWS": ["windshield", "side_L", "side_R", "rear_window"],
            "WHEELS": ["FL", "FR", "RL", "RR"],
            "AERO": ["rear_wing", "wing_support_L", "wing_support_R"],
        }

    def to_dict(self) -> Dict[str, object]:
        return {
            "model_id": self.model_id,
            "parameters": asdict(self.params),
            "reference_ratios": asdict(self.ratios),
            "resolved": self.resolved(),
            "wheel_centers": self.wheel_centers(),
            "part_graph": self.part_graph(),
        }
