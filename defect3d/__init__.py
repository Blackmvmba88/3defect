"""
3defect - A 3D modeling system for creating vehicles and mechanical systems.

This package provides tools for:
- Creating and manipulating 3D shapes
- Building composite mechanical parts
- Simulating physics and movement
- Integrating with Blender for visualization
"""

__version__ = "0.1.0"

from .core.shapes import Cube, Sphere, Cylinder, Cone
from .core.composite import CompositePart
from .vehicles.car import Car
from .vehicles.motorcycle import Motorcycle

__all__ = [
    'Cube', 'Sphere', 'Cylinder', 'Cone',
    'CompositePart',
    'Car', 'Motorcycle',
]
