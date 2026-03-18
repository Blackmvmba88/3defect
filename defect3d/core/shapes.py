"""
Basic 3D shape primitives.

This module provides fundamental 3D geometric shapes that can be used
to build more complex objects and mechanical systems.
"""

import math
import numpy as np
from typing import Tuple


class Shape3D:
    """Base class for all 3D shapes."""

    def __init__(self, position: Tuple[float, float, float] = (0, 0, 0),
                 rotation: Tuple[float, float, float] = (0, 0, 0),
                 scale: Tuple[float, float, float] = (1, 1, 1)):
        """
        Initialize a 3D shape.

        Args:
            position: (x, y, z) coordinates
            rotation: (rx, ry, rz) rotation in degrees
            scale: (sx, sy, sz) scale factors
        """
        self.position = np.array(position, dtype=float)
        self.rotation = np.array(rotation, dtype=float)
        self.scale = np.array(scale, dtype=float)
        self.name = ""
        self.tags = []  # Etiquetas semánticas para IA / Semantic tags for AI
        self.material = {"color": (0.8, 0.8, 0.8, 1.0)}  # Gris por defecto / Default gray

    def add_tag(self, tag: str):
        """Add a semantic tag to the shape."""
        if tag not in self.tags:
            self.tags.append(tag)

    def translate(self, dx: float, dy: float, dz: float):
        """Move the shape by the given offset."""
        self.position += np.array([dx, dy, dz])

    def rotate(self, rx: float, ry: float, rz: float):
        """Rotate the shape by the given angles (in degrees)."""
        self.rotation += np.array([rx, ry, rz])

    def set_scale(self, sx: float, sy: float, sz: float):
        """Set the scale of the shape."""
        self.scale = np.array([sx, sy, sz])

    def set_color(self, r: float, g: float, b: float, a: float = 1.0):
        """Set the color of the shape (RGBA values 0-1)."""
        self.material["color"] = (r, g, b, a)

    def volume(self) -> float:
        """Calculate the volume of the shape."""
        # Default implementation, override in subclasses
        return 0.0

    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get the bounding box of the shape."""
        # Implementación por defecto, sobrescribir en subclases / Default implementation, override in subclasses
        return self.position - self.scale, self.position + self.scale

    def to_dict(self) -> dict:
        """Convert shape to dictionary representation."""
        return {
            "type": self.__class__.__name__,
            "position": self.position.tolist(),
            "rotation": self.rotation.tolist(),
            "scale": self.scale.tolist(),
            "name": self.name,
            "tags": self.tags,
            "material": self.material
        }


class Cube(Shape3D):
    """A cube/box primitive."""

    def __init__(self, size: float = 1.0, **kwargs):
        """
        Create a cube.

        Args:
            size: Length of each side
            **kwargs: Additional arguments for Shape3D
        """
        super().__init__(**kwargs)
        self.size = size
        self.name = "Cube"

    def volume(self) -> float:
        return self.size**3

    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        half_size = (self.size * self.scale) / 2
        return self.position - half_size, self.position + half_size


class Sphere(Shape3D):
    """A sphere primitive."""

    def __init__(self, radius: float = 1.0, **kwargs):
        """
        Create a sphere.

        Args:
            radius: Radius of the sphere
            **kwargs: Additional arguments for Shape3D
        """
        super().__init__(**kwargs)
        self.radius = radius
        self.name = "Sphere"

    def volume(self) -> float:
        return (4 / 3) * math.pi * (self.radius**3)

    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        scaled_radius = self.radius * self.scale
        return self.position - scaled_radius, self.position + scaled_radius


class Cylinder(Shape3D):
    """A cylinder primitive."""

    def __init__(self, radius: float = 1.0, height: float = 2.0, **kwargs):
        """
        Create a cylinder.

        Args:
            radius: Radius of the cylinder
            height: Height of the cylinder
            **kwargs: Additional arguments for Shape3D
        """
        super().__init__(**kwargs)
        self.radius = radius
        self.height = height
        self.name = "Cylinder"

    def volume(self) -> float:
        return math.pi * (self.radius**2) * self.height

    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        scaled_radius = self.radius * self.scale[0]
        half_height = (self.height * self.scale[2]) / 2
        min_bounds = self.position - \
            np.array([scaled_radius, scaled_radius, half_height])
        max_bounds = self.position + \
            np.array([scaled_radius, scaled_radius, half_height])
        return min_bounds, max_bounds


class Cone(Shape3D):
    """A cone primitive."""

    def __init__(self, radius: float = 1.0, height: float = 2.0, **kwargs):
        """
        Create a cone.

        Args:
            radius: Radius of the base
            height: Height of the cone
            **kwargs: Additional arguments for Shape3D
        """
        super().__init__(**kwargs)
        self.radius = radius
        self.height = height
        self.name = "Cone"

    def volume(self) -> float:
        return (1 / 3) * math.pi * (self.radius**2) * self.height

    def get_bounds(self) -> Tuple[np.ndarray, np.ndarray]:
        scaled_radius = self.radius * self.scale[0]
        scaled_height = self.height * self.scale[2]
        min_bounds = self.position + \
            np.array([-scaled_radius, -scaled_radius, 0])
        max_bounds = self.position + \
            np.array([scaled_radius, scaled_radius, scaled_height])
        return min_bounds, max_bounds


class Torus(Shape3D):
    """A torus (donut) primitive - useful for wheels."""

    def __init__(
            self,
            major_radius: float = 1.0,
            minor_radius: float = 0.25,
            **kwargs):
        """
        Create a torus.

        Args:
            major_radius: Distance from center to tube center
            minor_radius: Radius of the tube
            **kwargs: Additional arguments for Shape3D
        """
        super().__init__(**kwargs)
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.name = "Torus"

    def volume(self) -> float:
        # V = (πr²)(2πR) = 2π²Rr²
        return 2 * (math.pi**2) * self.major_radius * (self.minor_radius**2)
