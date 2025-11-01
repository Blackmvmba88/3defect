"""
Common vehicle components.

This module provides reusable vehicle parts like wheels, engines, chassis, etc.
"""

from typing import Tuple
from ..core.composite import CompositePart
from ..core.shapes import Cylinder, Cube


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
        tire.set_color(0.1, 0.1, 0.1)  # Black rubber
        self.add_part(tire)

        # Rim (inner cylinder)
        rim = Cylinder(radius=radius * 0.7, height=width * 0.8,
                      position=position, rotation=(0, 90, 0))
        rim.name = "Rim"
        rim.set_color(0.7, 0.7, 0.8)  # Metallic
        self.add_part(rim)

        self.set_property("radius", radius)
        self.set_property("width", width)


class Engine(CompositePart):
    """A vehicle engine block."""

    def __init__(self, cylinders: int = 4,
                 position: Tuple[float, float, float] = (0, 0, 0)):
        """
        Create an engine.

        Args:
            cylinders: Number of cylinders
            position: Position in 3D space
        """
        super().__init__(name="Engine")
        self.cylinders = cylinders

        # Engine block (main body)
        block = Cube(size=0.5, position=position)
        block.name = "EngineBlock"
        block.set_color(0.3, 0.3, 0.3)  # Dark gray
        block.set_scale(1.2, 0.8, 0.6)
        self.add_part(block)

        # Cylinder heads
        for i in range(cylinders):
            offset = (i - cylinders/2) * 0.15
            cylinder = Cylinder(radius=0.08, height=0.3,
                              position=(position[0] + offset, position[1], position[2] + 0.4))
            cylinder.name = f"Cylinder_{i+1}"
            cylinder.set_color(0.4, 0.4, 0.4)
            self.add_part(cylinder)

        self.set_property("cylinders", cylinders)
        self.set_property("power", cylinders * 50)  # Simplified power calculation


class Chassis(CompositePart):
    """A vehicle chassis/frame."""

    def __init__(self, length: float = 2.0, width: float = 1.0, height: float = 0.2,
                 position: Tuple[float, float, float] = (0, 0, 0)):
        """
        Create a chassis.

        Args:
            length: Chassis length
            width: Chassis width
            height: Chassis height
            position: Position in 3D space
        """
        super().__init__(name="Chassis")

        # Main chassis body
        body = Cube(size=1.0, position=position)
        body.name = "ChassisBody"
        body.set_scale(length, width, height)
        body.set_color(0.5, 0.5, 0.6)  # Light gray metal
        self.add_part(body)

        # Frame rails
        rail_height = height * 2
        for side in [-1, 1]:
            rail = Cube(size=0.1, position=(position[0],
                                           position[1] + side * width * 0.4,
                                           position[2]))
            rail.set_scale(length * 0.9, 0.1, rail_height)
            rail.name = f"Rail_{side}"
            rail.set_color(0.3, 0.3, 0.3)
            self.add_part(rail)

        self.set_property("length", length)
        self.set_property("width", width)
        self.set_property("height", height)


class Body(CompositePart):
    """A vehicle body/shell."""

    def __init__(self, style: str = "sedan",
                 position: Tuple[float, float, float] = (0, 0, 0)):
        """
        Create a vehicle body.

        Args:
            style: Body style (sedan, sports, suv, etc.)
            position: Position in 3D space
        """
        super().__init__(name=f"Body_{style}")

        if style == "sedan":
            # Lower body
            lower = Cube(size=1.0, position=position)
            lower.set_scale(2.0, 1.2, 0.5)
            lower.name = "LowerBody"
            lower.set_color(0.8, 0.2, 0.2)  # Red
            self.add_part(lower)

            # Cabin
            cabin = Cube(size=1.0, position=(position[0], position[1], position[2] + 0.6))
            cabin.set_scale(1.2, 1.0, 0.6)
            cabin.name = "Cabin"
            cabin.set_color(0.7, 0.7, 0.8)  # Windows
            self.add_part(cabin)

        elif style == "sports":
            # Sleeker, lower profile
            lower = Cube(size=1.0, position=position)
            lower.set_scale(2.2, 1.3, 0.4)
            lower.name = "LowerBody"
            lower.set_color(0.9, 0.7, 0.1)  # Yellow
            self.add_part(lower)

            cabin = Cube(size=1.0, position=(position[0], position[1], position[2] + 0.4))
            cabin.set_scale(1.0, 1.1, 0.4)
            cabin.name = "Cabin"
            cabin.set_color(0.2, 0.2, 0.2)
            self.add_part(cabin)

        self.set_property("style", style)
