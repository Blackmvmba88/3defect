"""
Mecanismos de relojería / Clock Mechanisms

Este módulo implementa los componentes fundamentales de relojería.
This module implements the fundamental clockwork components.
"""

import math
from defect3d import Cylinder, Torus, Sphere, CompositePart
from .geometry import positive, integer, position3, gear_mesh, spring_mesh


class Gear:
    """
    Rueda dentada / Gear wheel

    Una rueda con dientes que transmite movimiento rotacional.
    A wheel with teeth that transmits rotational movement.
    """

    def __init__(self, teeth=20, module=1.0, thickness=0.5, position=(0, 0, 0),
                 *, pressure_angle=20.0, profile_samples=8):
        """
        Crear un engranaje / Create a gear

        Args:
            teeth: Número de dientes / Number of teeth
            module: Módulo del engranaje (tamaño diente) / Gear module (tooth size)
            thickness: Grosor del engranaje / Gear thickness
            position: Posición 3D / 3D position
        """
        integer(teeth, "teeth", 4)
        integer(profile_samples, "profile_samples", 2)
        for value, name in ((module, "module"), (thickness, "thickness")):
            positive(value, name)
        position3(position)
        if not math.isfinite(pressure_angle) or not 10 <= pressure_angle <= 35:
            raise ValueError("pressure_angle must be between 10 and 35 degrees")
        self.pressure_angle = pressure_angle
        self.root_radius = module * (teeth / 2 - 1.25)
        self.addendum_radius = module * (teeth / 2 + 1)
        self.base_radius = module * teeth / 2 * math.cos(math.radians(pressure_angle))
        self.undercut_risk = teeth < 2 / math.sin(math.radians(pressure_angle))**2
        self.teeth = teeth
        self.module = module
        self.thickness = thickness
        self.position = position

        # Calcular diámetro primitivo / Calculate pitch diameter
        self.pitch_diameter = module * teeth
        self.pitch_radius = self.pitch_diameter / 2.0

        # Crear geometría / Create geometry
        self.part = CompositePart(name=f"gear_{teeth}t")

        self.mesh, self._volume = gear_mesh(teeth, module, thickness,
                                           pressure_angle, profile_samples, position)
        self.part.add_part(self.mesh)

    def mesh_validation(self, other):
        """Parameter compatibility; does not certify physical tooth contact."""
        if not math.isclose(self.module, other.module, rel_tol=1e-9):
            raise ValueError("meshing gears need equal modules")
        if not math.isclose(self.pressure_angle, other.pressure_angle):
            raise ValueError("meshing gears need equal pressure angles")
        return self.pitch_radius + other.pitch_radius

    def volume(self):
        """Volumen aproximado / Approximate volume"""
        return self._volume

    def gear_ratio(self, other_gear):
        """
        Calcular relación de engranajes / Calculate gear ratio

        Args:
            other_gear: Otro engranaje / Another gear

        Returns:
            Relación de transmisión / Transmission ratio
        """
        return self.teeth / other_gear.teeth

    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Gear",
            "teeth": self.teeth,
            "module": self.module,
            "pitch_diameter": self.pitch_diameter,
            "pressure_angle": self.pressure_angle,
            "undercut_risk": self.undercut_risk,
            "thickness": self.thickness,
            "position": self.position
        }


class Escapement:
    """
    Escape / Escapement mechanism

    Mecanismo que controla la liberación de energía en pulsos regulares.
    Mechanism that controls the release of energy in regular pulses.
    """

    def __init__(self, frequency=1.0, position=(0, 0, 0)):
        """
        Crear un escape / Create an escapement

        Args:
            frequency: Frecuencia de escape (Hz) / Escapement frequency (Hz)
            position: Posición 3D / 3D position
        """
        self.frequency = frequency
        self.position = position
        self.period = 1.0 / frequency

        # Crear geometría simplificada / Create simplified geometry
        self.part = CompositePart(name="escapement")

        # Rueda de escape / Escape wheel
        escape_wheel = Cylinder(radius=0.3, height=0.1, position=position)
        escape_wheel.set_color(0.8, 0.6, 0.3, 1.0)
        self.part.add_part(escape_wheel)

        # Áncora / Anchor
        anchor_pos = (position[0] + 0.35, position[1], position[2])
        anchor = Cylinder(radius=0.15, height=0.15, position=anchor_pos)
        anchor.set_color(0.7, 0.4, 0.3, 1.0)
        self.part.add_part(anchor)

    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Escapement",
            "frequency": self.frequency,
            "period": self.period,
            "position": self.position
        }


class Pendulum:
    """
    Péndulo / Pendulum

    Oscilador que regula el tiempo mediante oscilación gravitacional.
    Oscillator that regulates time through gravitational oscillation.
    """

    def __init__(self, length=1.0, mass=0.5, position=(0, 0, 0)):
        """
        Crear un péndulo / Create a pendulum

        Args:
            length: Longitud del péndulo / Pendulum length
            mass: Masa de la lenteja / Bob mass
            position: Posición del pivote / Pivot position
        """
        self.length = length
        self.mass = mass
        self.position = position

        # Calcular período / Calculate period (T = 2π√(L/g))
        g = 9.81  # m/s²
        self.period = 2 * math.pi * math.sqrt(length / g)
        self.frequency = 1.0 / self.period

        # Crear geometría / Create geometry
        self.part = CompositePart(name="pendulum")

        # Varilla / Rod
        rod_pos = (position[0], position[1], position[2] - length/2)
        rod = Cylinder(radius=0.02, height=length, position=rod_pos)
        rod.set_color(0.5, 0.5, 0.5, 1.0)
        self.part.add_part(rod)

        # Lenteja (masa) / Bob (mass)
        bob_radius = (mass * 0.3) ** (1/3)  # Aproximación / Approximation
        bob_pos = (position[0], position[1], position[2] - length)
        bob = Sphere(radius=bob_radius, position=bob_pos)
        bob.set_color(0.8, 0.6, 0.2, 1.0)
        self.part.add_part(bob)

        # Pivote / Pivot
        pivot = Sphere(radius=0.05, position=position)
        pivot.set_color(0.3, 0.3, 0.3, 1.0)
        self.part.add_part(pivot)

    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Pendulum",
            "length": self.length,
            "mass": self.mass,
            "period": self.period,
            "frequency": self.frequency,
            "position": self.position
        }


class Spring:
    """
    Resorte / Spring

    Almacena energía mediante deformación elástica.
    Stores energy through elastic deformation.
    """

    def __init__(self, coils=10, wire_diameter=0.05, coil_diameter=0.5,
                 free_length=1.0, stiffness=100.0, position=(0, 0, 0), *, samples_per_coil=32):
        """
        Crear un resorte / Create a spring

        Args:
            coils: Número de espiras / Number of coils
            wire_diameter: Diámetro del alambre / Wire diameter
            coil_diameter: Diámetro de la espira / Coil diameter
            free_length: Longitud libre / Free length
            stiffness: Rigidez (N/m) / Stiffness (N/m)
            position: Posición 3D / 3D position
        """
        for value, name in ((coils, "coils"), (wire_diameter, "wire_diameter"),
                            (coil_diameter, "coil_diameter"), (free_length, "free_length"),
                            (stiffness, "stiffness")):
            positive(value, name)
        integer(samples_per_coil, "samples_per_coil", 8)
        position3(position)
        if wire_diameter >= coil_diameter:
            raise ValueError("wire must be thinner than mean coil diameter")
        self.coils = coils
        self.wire_diameter = wire_diameter
        self.coil_diameter = coil_diameter
        self.free_length = free_length
        self.stiffness = stiffness
        self.position = position

        # Energía almacenada (con compresión x) / Stored energy (with compression x)
        # E = 0.5 * k * x²

        # Crear geometría simplificada / Create simplified geometry
        self.part = CompositePart(name="spring")

        self.mesh, self.centerline = spring_mesh(coils, wire_diameter, coil_diameter,
                                                free_length, samples_per_coil, position)
        self.part.add_part(self.mesh)
        self.coil_overlap_risk = free_length / coils <= wire_diameter

    def energy(self, compression):
        """
        Energía almacenada / Stored energy

        Args:
            compression: Compresión del resorte / Spring compression

        Returns:
            Energía en Joules / Energy in Joules
        """
        if not math.isfinite(compression):
            raise ValueError("compression must be finite")
        return 0.5 * self.stiffness * compression**2

    def force(self, compression):
        """
        Fuerza ejercida / Force exerted

        Args:
            compression: Compresión del resorte / Spring compression

        Returns:
            Fuerza en Newtons / Force in Newtons
        """
        if not math.isfinite(compression):
            raise ValueError("compression must be finite")
        return self.stiffness * compression

    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Spring",
            "coils": self.coils,
            "wire_diameter": self.wire_diameter,
            "coil_diameter": self.coil_diameter,
            "free_length": self.free_length,
            "stiffness": self.stiffness,
            "position": self.position
        }


class GearTrain:
    """
    Tren de engranajes / Gear train

    Sistema de múltiples engranajes que modifica velocidad y torque.
    System of multiple gears that modifies speed and torque.
    """

    def __init__(self, name="gear_train"):
        """Crear un tren de engranajes / Create a gear train"""
        self.name = name
        self.gears = []
        self.part = CompositePart(name=name)

    def add_gear(self, gear, connects_to=None):
        """
        Agregar un engranaje al tren / Add a gear to the train

        Args:
            gear: Engranaje a agregar / Gear to add
            connects_to: Índice del engranaje con el que conecta / Index of gear it connects to
        """
        if not isinstance(gear, Gear):
            raise TypeError("gear must be a Gear")
        if connects_to is None and self.gears:
            connects_to = len(self.gears) - 1
        if connects_to is not None:
            integer(connects_to, "connects_to", 0)
            if connects_to >= len(self.gears):
                raise ValueError("connection must reference an existing gear")
            self.gears[connects_to]["gear"].mesh_validation(gear)
        self.gears.append({
            "gear": gear,
            "connects_to": connects_to
        })
        self.part.add_part(gear.part)

    def total_ratio(self):
        """
        Relación de transmisión total / Total transmission ratio

        Returns:
            Relación de entrada/salida / Input/output ratio
        """
        if len(self.gears) < 2:
            return 1.0

        return 1.0 / abs(self.speed_factors()[-1])

    def speed_factors(self):
        """Signed output/input angular speed for each external mesh."""
        factors = []
        for entry in self.gears:
            parent = entry['connects_to']
            factors.append(1.0 if parent is None else
                           -factors[parent] * self.gears[parent]['gear'].teeth / entry['gear'].teeth)
        return factors

    def signed_output_speed(self, input_speed):
        return input_speed * (self.speed_factors()[-1] if self.gears else 1.0)

    def simulate(self, duration, input_speed=1.0, dt=0.01):
        """Ideal constant-speed snapshots. Speed in rad/s; angles in radians."""
        positive(dt, 'dt')
        if not math.isfinite(duration) or duration < 0 or not math.isfinite(input_speed):
            raise ValueError('duration must be nonnegative and speed finite')
        factors = self.speed_factors()
        count = math.ceil(duration / dt)
        times = [min(i * dt, duration) for i in range(count + 1)]
        return [{'time': t, 'angles': [t*input_speed*f for f in factors],
                 'angular_velocities': [input_speed*f for f in factors]} for t in times]

    def output_speed(self, input_speed):
        """
        Velocidad de salida / Output speed

        Args:
            input_speed: Velocidad de entrada (RPM) / Input speed (RPM)

        Returns:
            Velocidad de salida (RPM) / Output speed (RPM)
        """
        return input_speed / self.total_ratio()

    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "GearTrain",
            "name": self.name,
            "gears": [g["gear"].to_dict() for g in self.gears],
            "total_ratio": self.total_ratio(),
            "connections": [g["connects_to"] for g in self.gears]
        }


__all__ = ['Gear', 'Escapement', 'Pendulum', 'Spring', 'GearTrain']
