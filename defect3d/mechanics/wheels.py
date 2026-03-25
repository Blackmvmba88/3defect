"""
Wheel components for vehicles.

This module provides wheel and tire assemblies that can be used
in various vehicle types.
"""

from typing import Tuple
from ..core.composite import CompositePart
from ..core.shapes import Cylinder


class Wheel(CompositePart):
    """A vehicle wheel with tire and rim."""

    def __init__(self, radius: float = 0.3, width: float = 0.2,
                 position: Tuple[float, float, float] = (0, 0, 0)):
        """
        Create a wheel.

        Args:
            radius: Wheel radius
            width: Wheel width
            position: Position in 3D space
        """
        super().__init__(name="Wheel")
        self.radius = radius
        self.width = width

        # Tire (outer cylinder)
        tire = Cylinder(radius=radius, height=width,
                        position=position, rotation=(0, 90, 0))
        tire.name = "Tire"
        tire.add_tag("rubber")
        tire.add_tag("traction")
        tire.set_color(0.1, 0.1, 0.1)  # Black rubber
        self.add_part(tire)

        # Rim (inner cylinder)
        rim = Cylinder(radius=radius * 0.7, height=width * 0.8,
                       position=position, rotation=(0, 90, 0))
        rim.name = "Rim"
        rim.add_tag("metallic")
        rim.add_tag("structural")
        rim.set_color(0.7, 0.7, 0.8)  # Metallic
        self.add_part(rim)

        self.set_property("radius", radius)
        self.set_property("width", width)
