"""Core 3D modeling functionality."""

from .shapes import Cube, Sphere, Cylinder, Cone, Torus, Shape3D
from .primitives import Cube, Sphere, Cylinder, Cone, Torus, Shape3D
from .composite import CompositePart
from .transformations import (
    create_translation_matrix,
    create_rotation_matrix_x,
    create_rotation_matrix_y,
    create_rotation_matrix_z,
    create_scale_matrix,
    apply_transform,
    transform_point,
    interpolate_transform
)
from .serializer import (
    serialize_shape,
    serialize_composite,
    serialize_object,
    to_json,
    save_to_json,
    load_from_json
)

__all__ = [
    # Shapes/Primitives
    'Cube', 'Sphere', 'Cylinder', 'Cone', 'Torus', 'Shape3D',
    # Composite
    'CompositePart',
    # Transformations
    'create_translation_matrix', 'create_rotation_matrix_x',
    'create_rotation_matrix_y', 'create_rotation_matrix_z',
    'create_scale_matrix', 'apply_transform', 'transform_point',
    'interpolate_transform',
    # Serialization
    'serialize_shape', 'serialize_composite', 'serialize_object',
    'to_json', 'save_to_json', 'load_from_json'
]
