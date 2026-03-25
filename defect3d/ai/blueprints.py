"""
Librería de planos maestros (blueprints) para la IA.
Blueprint library for AI assistance.
"""

from typing import Dict, Any, List
from ..core.composite import CompositePart
from ..core.shapes import Cube, Cylinder, Torus
from ..clock_mechanisms import Gear, Pendulum, Spring, Escapement, GearTrain

class BlueprintLibrary:
    """Librería que contiene recetas complejas para construcción asistida."""

    @staticmethod
    def create_mechanical_arm(segments=3) -> CompositePart:
        """Crea un brazo mecánico articulado."""
        arm = CompositePart(name="Mechanical_Arm")
        arm.add_tag("mechanical")
        arm.add_tag("robotic_arm")

        current_z = 0
        for i in range(segments):
            # Articulación / Joint
            joint = Cylinder(radius=0.3, height=0.4, position=(0, 0, current_z))
            joint.add_tag("joint")
            joint.add_tag(f"joint_{i}")
            arm.add_part(joint)

            # Segmento / Link
            link_height = 2.0 / (i + 1)
            link = Cylinder(radius=0.15, height=link_height, position=(0, 0, current_z + 0.2 + link_height/2))
            link.add_tag("link")
            link.add_tag(f"link_{i}")
            arm.add_part(link)

            current_z += 0.4 + link_height

        return arm

    @staticmethod
    def create_thruster(power=1.0) -> CompositePart:
        """Crea un motor de propulsión."""
        thruster = CompositePart(name="Thruster")
        thruster.add_tag("propulsion")
        thruster.add_tag("engine")

        # Cuerpo / Body
        body = Cylinder(radius=0.5 * power, height=1.5 * power)
        body.add_tag("housing")
        thruster.add_part(body)

        # Boquilla / Nozzle
        nozzle = Cylinder(radius=0.7 * power, height=0.5 * power, position=(0, 0, -0.8 * power))
        nozzle.add_tag("nozzle")
        thruster.add_part(nozzle)

        return thruster

    @staticmethod
    def create_clock_system(precision=1.0) -> CompositePart:
        """Crea un sistema de reloj mecánico completo."""
        clock = CompositePart(name="Mechanical_Clock")
        clock.add_tag("clockwork")
        clock.add_tag("precision_instrument")

        # 1. Péndulo / Pendulum
        pendulum = Pendulum(length=0.248 * (1.0/precision), mass=0.5, position=(0, 0, 0))
        pendulum.part.add_tag("regulator")
        clock.add_part(pendulum.part)

        # 2. Escape / Escapement
        escape = Escapement(frequency=1.0/pendulum.period, position=(0.5, 0, 0))
        escape.part.add_tag("escapement")
        clock.add_part(escape.part)

        # 3. Almacenamiento de energía (Resorte) / Energy storage (Spring)
        energy_source = Spring(coils=15, stiffness=500.0, position=(1.0, 0, -0.5))
        energy_source.part.add_tag("energy_source")
        clock.add_part(energy_source.part)

        return clock

    @staticmethod
    def create_transmission_system(ratio=2.0) -> CompositePart:
        """Crea un sistema de transmisión por engranajes."""
        transmission = CompositePart(name="Transmission_System")
        transmission.add_tag("transmission")
        transmission.add_tag("mechanical_power")

        train = GearTrain(name="gear_box")

        # Engranaje conductor / Drive gear
        g1 = Gear(teeth=40, module=0.5, position=(0, 0, 0))
        g1.part.add_tag("drive_gear")

        # Engranaje conducido / Driven gear
        g2_teeth = int(max(10, 40 / ratio))
        g2 = Gear(teeth=g2_teeth, module=0.5, position=(1.5, 0, 0))
        g2.part.add_tag("driven_gear")

        train.add_gear(g1)
        train.add_gear(g2, connects_to=0)

        transmission.add_part(train.part)
        transmission.set_property("total_ratio", train.total_ratio())

        return transmission
