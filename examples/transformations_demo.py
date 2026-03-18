#!/usr/bin/env python3
"""
Example demonstrating transformation utilities.

This example shows how to use the transformation module for
matrix operations, rotations, translations, and interpolations.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d import Cube
from defect3d.core.transformations import (
    create_translation_matrix,
    create_rotation_matrix_z,
    create_scale_matrix,
    apply_transform,
    transform_point,
    interpolate_transform
)


def main():
    print("3defect - Transformation Utilities Example\n")

    # Create a cube
    cube = Cube(size=1.0, position=(0, 0, 0))
    cube.name = "TransformCube"
    print(f"Initial cube position: {cube.position}")

    # Example 1: Translation matrix
    print("\n1. Translation Matrix Example")
    trans_matrix = create_translation_matrix(5, 3, 2)
    print(f"Translation matrix created for moving (5, 3, 2)")
    original_point = (0, 0, 0)
    transformed_point = transform_point(original_point, trans_matrix)
    print(f"Point {original_point} transformed to {transformed_point}")

    # Example 2: Rotation matrix
    print("\n2. Rotation Matrix Example")
    rot_matrix = create_rotation_matrix_z(90)  # 90 degrees around Z axis
    print("Rotation matrix created for 90° around Z axis")
    point = (1, 0, 0)
    rotated_point = transform_point(point, rot_matrix)
    print(f"Point {point} rotated to {rotated_point}")

    # Example 3: Scale matrix
    print("\n3. Scale Matrix Example")
    scale_matrix = create_scale_matrix(2, 2, 2)
    print("Scale matrix created for 2x scaling")
    point = (1, 1, 1)
    scaled_point = transform_point(point, scale_matrix)
    print(f"Point {point} scaled to {scaled_point}")

    # Example 4: Combined transformation
    print("\n4. Combined Transformation Example")
    position = (3, 2, 1)
    rotation = (0, 0, 45)  # 45 degrees around Z
    scale = (1.5, 1.5, 1.5)
    combined_matrix = apply_transform(position, rotation, scale)
    print(f"Combined transformation matrix created:")
    print(f"  Position: {position}")
    print(f"  Rotation: {rotation}")
    print(f"  Scale: {scale}")

    # Example 5: Interpolation
    print("\n5. Position Interpolation Example")
    start = (0, 0, 0)
    end = (10, 5, 3)
    print(f"Interpolating from {start} to {end}")

    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        interpolated = interpolate_transform(start, end, t)
        print(f"  t={t:.2f}: {interpolated}")

    # Example 6: Apply transformations to cube
    print("\n6. Applying Transformations to Cube")
    cube.translate(5, 3, 2)
    print(f"After translation: {cube.position}")

    cube.rotate(0, 0, 45)
    print(f"After rotation: rotation = {cube.rotation}")

    cube.set_scale(2, 2, 2)
    print(f"After scaling: scale = {cube.scale}")

    print("\n✅ Transformation utilities example completed!")


if __name__ == "__main__":
    main()
