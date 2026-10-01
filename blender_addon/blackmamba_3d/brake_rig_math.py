from __future__ import annotations

from dataclasses import dataclass

from .double_wishbone_math import DoubleWishboneSpec, WishbonePose
from .road_rig_math import _solve_angle_for_travel


@dataclass(frozen=True)
class BrakeRigSpec:
    """Simple front-corner longitudinal braking response model.

    SI units:
    - mass: kg
    - distance: m
    - speed: m/s
    - acceleration: m/s^2
    - spring rate: N/m
    - damping: N*s/m

    Braking transfers load forward by m*a*h/L. Half of that transfer is
    assigned to one front corner. The corner then follows a linear
    spring-damper response so the visible wishbone compresses over time rather
    than jumping directly to a static pose.
    """

    vehicle_mass_kg: float = 1500.0
    wheelbase_m: float = 2.70
    cg_height_m: float = 0.55
    initial_speed_mps: float = 27.78
    decel_mps2: float = 8.0
    front_corner_sprung_mass_kg: float = 375.0
    spring_rate_n_per_m: float = 35000.0
    damping_n_s_per_m: float = 3200.0
    duration_s: float = 2.0
    sample_hz: float = 120.0
    min_angle_deg: float = -20.0
    max_angle_deg: float = 20.0

    def validate(self) -> None:
        positive = {
            "vehicle_mass_kg": self.vehicle_mass_kg,
            "wheelbase_m": self.wheelbase_m,
            "cg_height_m": self.cg_height_m,
            "initial_speed_mps": self.initial_speed_mps,
            "decel_mps2": self.decel_mps2,
            "front_corner_sprung_mass_kg": self.front_corner_sprung_mass_kg,
            "spring_rate_n_per_m": self.spring_rate_n_per_m,
            "damping_n_s_per_m": self.damping_n_s_per_m,
            "duration_s": self.duration_s,
            "sample_hz": self.sample_hz,
        }
        for name, value in positive.items():
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.min_angle_deg >= self.max_angle_deg:
            raise ValueError("min_angle_deg must be below max_angle_deg")

    @property
    def total_load_transfer_n(self) -> float:
        self.validate()
        return (
            self.vehicle_mass_kg
            * self.decel_mps2
            * self.cg_height_m
            / self.wheelbase_m
        )

    @property
    def front_corner_load_step_n(self) -> float:
        return self.total_load_transfer_n / 2.0

    @property
    def static_corner_compression_m(self) -> float:
        return self.front_corner_load_step_n / self.spring_rate_n_per_m

    @property
    def stop_time_s(self) -> float:
        return self.initial_speed_mps / self.decel_mps2


@dataclass(frozen=True)
class BrakeRigSample:
    time_s: float
    speed_mps: float
    longitudinal_g: float
    load_transfer_n: float
    corner_force_n: float
    compression_m: float
    compression_velocity_mps: float
    lower_angle_deg: float
    pose: WishbonePose


def simulate_braking_run(
    suspension: DoubleWishboneSpec,
    rig: BrakeRigSpec,
) -> tuple[BrakeRigSample, ...]:
    """Integrate one front corner's brake-dive response over time.

    Positive ``compression_m`` means the chassis has moved downward relative
    to the wheel. In the suspension coordinate frame this is equivalent to an
    upward hub travel target of the same magnitude.
    """

    suspension.validate()
    rig.validate()

    sample_count = max(2, int(round(rig.duration_s * rig.sample_hz)) + 1)
    dt = rig.duration_s / (sample_count - 1)

    compression = 0.0
    velocity = 0.0
    samples = []

    for index in range(sample_count):
        time_s = index * dt
        braking_active = time_s <= rig.stop_time_s
        decel = rig.decel_mps2 if braking_active else 0.0
        speed = max(0.0, rig.initial_speed_mps - rig.decel_mps2 * time_s)
        total_transfer = (
            rig.vehicle_mass_kg * decel * rig.cg_height_m / rig.wheelbase_m
        )
        corner_force = total_transfer / 2.0

        if index > 0:
            spring_force = rig.spring_rate_n_per_m * compression
            damping_force = rig.damping_n_s_per_m * velocity
            acceleration = (
                corner_force - spring_force - damping_force
            ) / rig.front_corner_sprung_mass_kg
            velocity += acceleration * dt
            compression += velocity * dt

        angle = _solve_angle_for_travel(
            suspension,
            compression,
            min_angle_deg=rig.min_angle_deg,
            max_angle_deg=rig.max_angle_deg,
        )
        pose = suspension.solve(angle)

        samples.append(
            BrakeRigSample(
                time_s=time_s,
                speed_mps=speed,
                longitudinal_g=decel / 9.80665,
                load_transfer_n=total_transfer,
                corner_force_n=corner_force,
                compression_m=compression,
                compression_velocity_mps=velocity,
                lower_angle_deg=angle,
                pose=pose,
            )
        )

    return tuple(samples)
