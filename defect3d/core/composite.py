"""
Composite part system for building complex objects from simple shapes.

This module allows combining multiple 3D shapes into mechanical assemblies
like engines, wheels, chassis, etc.
"""

from typing import List, Dict, Optional
import numpy as np
from .shapes import Shape3D


class CompositePart:
    """
    A composite part made up of multiple 3D shapes.

    This class allows building complex mechanical systems by combining
    simple shapes with relationships and constraints.
    """

    def __init__(self, name: str = "CompositePart"):
        """
        Initialize a composite part.

        Args:
            name: Name identifier for this composite part
        """
        self.name = name
        self.parts: List[Shape3D] = []
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.connections: List[Dict] = []  # Para conexiones mecánicas / For mechanical connections
        self.properties: Dict = {}  # Propiedades personalizadas (masa, material, etc.) / Custom properties (mass, material, etc.)

    def add_part(
            self,
            part: Shape3D,
            relative_position: Optional[tuple] = None):
        """
        Add a part to this composite.

        Args:
            part: The 3D shape to add
            relative_position: Optional position offset from composite center
        """
        if relative_position:
            part.position = np.array(relative_position) + self.position
        self.parts.append(part)

    def remove_part(self, part: Shape3D):
        """Remove a part from this composite."""
        if part in self.parts:
            self.parts.remove(part)

    def translate(self, dx: float, dy: float, dz: float):
        """Move the entire composite part."""
        offset = np.array([dx, dy, dz])
        self.position += offset
        for part in self.parts:
            part.translate(dx, dy, dz)

    def rotate(self, rx: float, ry: float, rz: float):
        """Rotate the entire composite part."""
        self.rotation += np.array([rx, ry, rz])
        # TODO: Implementar rotación adecuada de partes hijas alrededor del centro compuesto
        # TODO: Implement proper rotation of child parts around composite center
        for part in self.parts:
            part.rotate(rx, ry, rz)

    def connect(
            self,
            part1: Shape3D,
            part2: Shape3D,
            connection_type: str = "fixed"):
        """
        Define a connection between two parts.

        Args:
            part1: First part
            part2: Second part
            connection_type: Type of connection (fixed, hinge, slider, etc.)
        """
        self.connections.append({
            "part1": part1,
            "part2": part2,
            "type": connection_type
        })

    def set_property(self, key: str, value):
        """Set a custom property for this composite."""
        self.properties[key] = value

    def get_property(self, key: str, default=None):
        """Get a custom property value."""
        return self.properties.get(key, default)

    def get_bounds(self):
        """Get the bounding box encompassing all parts."""
        if not self.parts:
            return self.position, self.position

        all_mins = []
        all_maxs = []

        for part in self.parts:
            min_bound, max_bound = part.get_bounds()
            all_mins.append(min_bound)
            all_maxs.append(max_bound)

        overall_min = np.min(all_mins, axis=0)
        overall_max = np.max(all_maxs, axis=0)

        return overall_min, overall_max

    def get_part_count(self) -> int:
        """Get the number of parts in this composite."""
        return len(self.parts)

    def to_dict(self) -> dict:
        """Convert composite to dictionary representation."""
        # Manejar tanto arrays numpy como tuplas / Handle both numpy arrays and tuples
        pos = self.position.tolist() if hasattr(
            self.position, 'tolist') else list(
            self.position)
        rot = self.rotation.tolist() if hasattr(
            self.rotation, 'tolist') else list(
            self.rotation)

        return {
            "name": self.name,
            "position": pos,
            "rotation": rot,
            "properties": self.properties,
            "parts": [part.to_dict() for part in self.parts],
            "connections": [
                {
                    "part1": conn["part1"].name,
                    "part2": conn["part2"].name,
                    "type": conn["type"]
                } for conn in self.connections
            ]
        }
