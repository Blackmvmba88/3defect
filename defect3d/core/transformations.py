"""
Transformation utilities for 3D objects.

This module provides helper functions for common 3D transformations
including scaling, rotation, translation, and matrix operations.
"""

import numpy as np
from typing import Tuple


def create_translation_matrix(dx: float, dy: float, dz: float) -> np.ndarray:
    """
    Create a 4x4 translation matrix.

    Args:
        dx: Translation along X axis
        dy: Translation along Y axis
        dz: Translation along Z axis

    Returns:
        4x4 translation matrix
    """
    matrix = np.eye(4)
    matrix[0:3, 3] = [dx, dy, dz]
    return matrix


def create_rotation_matrix_x(angle_deg: float) -> np.ndarray:
    """
    Create a 4x4 rotation matrix around X axis.

    Args:
        angle_deg: Rotation angle in degrees

    Returns:
        4x4 rotation matrix
    """
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    matrix = np.eye(4)
    matrix[1, 1] = cos_a
    matrix[1, 2] = -sin_a
    matrix[2, 1] = sin_a
    matrix[2, 2] = cos_a
    return matrix


def create_rotation_matrix_y(angle_deg: float) -> np.ndarray:
    """
    Create a 4x4 rotation matrix around Y axis.

    Args:
        angle_deg: Rotation angle in degrees

    Returns:
        4x4 rotation matrix
    """
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    matrix = np.eye(4)
    matrix[0, 0] = cos_a
    matrix[0, 2] = sin_a
    matrix[2, 0] = -sin_a
    matrix[2, 2] = cos_a
    return matrix


def create_rotation_matrix_z(angle_deg: float) -> np.ndarray:
    """
    Create a 4x4 rotation matrix around Z axis.

    Args:
        angle_deg: Rotation angle in degrees

    Returns:
        4x4 rotation matrix
    """
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    matrix = np.eye(4)
    matrix[0, 0] = cos_a
    matrix[0, 1] = -sin_a
    matrix[1, 0] = sin_a
    matrix[1, 1] = cos_a
    return matrix


def create_scale_matrix(sx: float, sy: float, sz: float) -> np.ndarray:
    """
    Create a 4x4 scale matrix.

    Args:
        sx: Scale factor along X axis
        sy: Scale factor along Y axis
        sz: Scale factor along Z axis

    Returns:
        4x4 scale matrix
    """
    matrix = np.eye(4)
    matrix[0, 0] = sx
    matrix[1, 1] = sy
    matrix[2, 2] = sz
    return matrix


def apply_transform(
        position: Tuple[float, float, float],
        rotation: Tuple[float, float, float],
        scale: Tuple[float, float, float]) -> np.ndarray:
    """
    Create a complete transformation matrix from position, rotation, and scale.

    Args:
        position: (x, y, z) translation
        rotation: (rx, ry, rz) rotation in degrees
        scale: (sx, sy, sz) scale factors

    Returns:
        4x4 transformation matrix
    """
    # Build transformation matrix: T * Rz * Ry * Rx * S
    mat_translate = create_translation_matrix(*position)
    mat_rotate_x = create_rotation_matrix_x(rotation[0])
    mat_rotate_y = create_rotation_matrix_y(rotation[1])
    mat_rotate_z = create_rotation_matrix_z(rotation[2])
    mat_scale = create_scale_matrix(*scale)

    # Combine transformations
    transform = mat_translate @ mat_rotate_z @ mat_rotate_y @ mat_rotate_x @ mat_scale
    return transform


def transform_point(
        point: Tuple[float, float, float],
        matrix: np.ndarray) -> np.ndarray:
    """
    Apply a transformation matrix to a 3D point.

    Args:
        point: (x, y, z) coordinates
        matrix: 4x4 transformation matrix

    Returns:
        Transformed point as numpy array
    """
    point_homogeneous = np.array([point[0], point[1], point[2], 1.0])
    transformed = matrix @ point_homogeneous
    return transformed[0:3]


def interpolate_transform(
        start_pos: Tuple[float, float, float],
        end_pos: Tuple[float, float, float],
        t: float) -> Tuple[float, float, float]:
    """
    Linear interpolation between two positions.

    Args:
        start_pos: Starting position
        end_pos: Ending position
        t: Interpolation factor (0.0 to 1.0)

    Returns:
        Interpolated position
    """
    t = max(0.0, min(1.0, t))  # Clamp to [0, 1]
    result = tuple(
        start_pos[i] + (end_pos[i] - start_pos[i]) * t
        for i in range(3)
    )
    return result
