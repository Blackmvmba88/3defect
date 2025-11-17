"""
3defect - A 3D modeling system for creating vehicles and mechanical systems.

This package provides tools for:
- Creating and manipulating 3D shapes
- Building composite mechanical parts
- Simulating physics and movement
- Integrating with Blender for visualization
"""

__version__ = "0.1.0"

from .core.shapes import Cube, Sphere, Cylinder, Cone, Torus
from .core.composite import CompositePart
from .vehicles.car import Car
from .vehicles.motorcycle import Motorcycle
from .mechanics import Wheel, Engine, Chassis, Body

__all__ = [
    'Cube', 'Sphere', 'Cylinder', 'Cone', 'Torus',
    'CompositePart',
    'Car', 'Motorcycle',
    'Wheel', 'Engine', 'Chassis', 'Body',
]
