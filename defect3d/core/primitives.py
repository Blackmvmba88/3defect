"""
Basic 3D shape primitives.

This module provides fundamental 3D geometric shapes that can be used
to build more complex objects and mechanical systems.
This is a compatibility alias for shapes.py.
"""

from .shapes import (
    Shape3D,
    Cube,
    Sphere,
    Cylinder,
    Cone,
    Torus
)

__all__ = ['Shape3D', 'Cube', 'Sphere', 'Cylinder', 'Cone', 'Torus']
