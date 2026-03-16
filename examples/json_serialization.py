#!/usr/bin/env python3
"""
Example demonstrating JSON serialization of 3D objects.

This example shows how to use the universal JSON serializer to export
3D objects and composite parts to structured JSON format.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d import Cube, Sphere, Cylinder
from defect3d.mechanics import Wheel, Engine
from defect3d.core.serializer import to_json, save_to_json


def main():
    print("3defect - JSON Serialization Example\n")

    # Create some basic shapes
    print("1. Creating basic shapes...")
    cube = Cube(size=2.0, position=(0, 0, 0))
    cube.name = "BasicCube"
    cube.set_color(0.8, 0.2, 0.2)

    sphere = Sphere(radius=1.5, position=(3, 0, 0))
    sphere.name = "BasicSphere"
    sphere.set_color(0.2, 0.8, 0.2)

    # Create a composite part (wheel)
    print("2. Creating composite part (wheel)...")
    wheel = Wheel(radius=0.4, width=0.25, position=(0, 0, 2))

    # Create an engine
    print("3. Creating engine...")
    engine = Engine(cylinders=4, position=(6, 0, 0))

    # Serialize individual objects
    print("\n4. Serializing objects to JSON...")

    # Serialize cube to JSON string
    cube_json = to_json(cube)
    print("\nCube JSON:")
    print(cube_json)

    # Serialize wheel (composite) to JSON string
    wheel_json = to_json(wheel)
    print("\nWheel JSON:")
    print(wheel_json)

    # Save multiple objects to JSON file
    print("\n5. Saving multiple objects to file...")
    objects = [cube, sphere, wheel, engine]
    output_file = os.path.join(os.path.dirname(__file__), "serialized_objects.json")
    save_to_json(objects, output_file)
    print(f"Objects saved to: {output_file}")

    print("\n✅ Serialization example completed!")
    print("\nYou can:")
    print("  - Open the JSON file to inspect the structure")
    print("  - Use the JSON for storage, transfer, or analysis")
    print("  - Parse the JSON in other languages or systems")


if __name__ == "__main__":
    main()
