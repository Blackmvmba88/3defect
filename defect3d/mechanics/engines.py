"""
Engine components for vehicles.

This module provides engine blocks and powertrain components
with realistic proportions and configurations.
"""

from typing import Tuple
from ..core.composite import CompositePart
from ..core.shapes import Cylinder, Cube


class Engine(CompositePart):
    """A vehicle engine block."""

    def __init__(self, cylinders: int = 4,
                 position: Tuple[float, float, float] = (0, 0, 0)):
        """
        Create an engine.

        Args:
            cylinders: Number of cylinders (typically 2, 4, 6, 8, or 12)
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
            offset = (i - cylinders / 2) * 0.15
            cylinder = Cylinder(
                radius=0.08,
                height=0.3,
                position=(
                    position[0] +
                    offset,
                    position[1],
                    position[2] +
                    0.4))
            cylinder.name = f"Cylinder_{i + 1}"
            cylinder.set_color(0.4, 0.4, 0.4)
            self.add_part(cylinder)

        self.set_property("cylinders", cylinders)
        # Simplified power calculation (HP per cylinder)
        self.set_property("power", cylinders * 50)
