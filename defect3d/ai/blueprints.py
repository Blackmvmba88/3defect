"""
Librería de planos maestros (blueprints) para la IA.
Blueprint library for AI assistance.
"""

from typing import Dict, Any, List
from ..core.composite import CompositePart
from ..core.shapes import Cube, Cylinder, Torus

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
