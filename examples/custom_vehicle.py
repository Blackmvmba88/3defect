#!/usr/bin/env python3
"""
Example: Create a custom vehicle from components.

This script demonstrates how to build a custom vehicle by combining
individual components.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d.core import CompositePart, Cube, Cylinder
from defect3d.vehicles.components import Wheel, Engine, Chassis
from defect3d.blender_integration import export_to_blender


def create_custom_buggy():
    """Create a custom dune buggy vehicle."""
    print("Building a custom dune buggy...")

    # Create the main vehicle composite
    buggy = CompositePart(name="DuneBuggy")

    # Add chassis
    chassis = Chassis(length=2.5, width=1.5, height=0.15, position=(0, 0, 0.4))
    buggy.add_part(chassis)

    # Add engine (smaller, positioned at rear)
    engine = Engine(cylinders=2, position=(-0.8, 0, 0.6))
    for part in engine.parts:
        part.set_scale(0.7, 0.7, 0.7)  # Scale down
    buggy.add_part(engine)

    # Add 4 large off-road wheels
    wheel_positions = [
        (0.9, 0.75, 0.35),   # Front right
        (0.9, -0.75, 0.35),  # Front left
        (-0.9, 0.75, 0.35),  # Rear right
        (-0.9, -0.75, 0.35), # Rear left
    ]

    wheels = []
    for i, pos in enumerate(wheel_positions):
        wheel = Wheel(radius=0.4, width=0.3, position=pos)
        wheel.name = f"OffRoadWheel_{i+1}"
        wheels.append(wheel)
        buggy.add_part(wheel)

    # Add roll cage (safety bars)
    print("  Adding roll cage...")
    cage_parts = [
        # Vertical posts
        (0.8, 0.6, 1.0),
        (0.8, -0.6, 1.0),
        (-0.3, 0.6, 1.0),
        (-0.3, -0.6, 1.0),
    ]

    for i, pos in enumerate(cage_parts):
        post = Cylinder(radius=0.03, height=0.8, position=pos)
        post.name = f"RollCage_Post_{i+1}"
        post.set_color(0.9, 0.9, 0.1)  # Yellow
        buggy.add_part(post)

    # Add horizontal bars
    top_bar = Cylinder(radius=0.03, height=1.2, position=(0.25, 0, 1.35), rotation=(0, 90, 0))
    top_bar.name = "RollCage_TopBar"
    top_bar.set_color(0.9, 0.9, 0.1)
    buggy.add_part(top_bar)

    # Add seats
    for i, y_pos in enumerate([0.3, -0.3]):
        seat = Cube(size=0.3, position=(0.2, y_pos, 0.7))
        seat.name = f"Seat_{i+1}"
        seat.set_color(0.1, 0.1, 0.1)  # Black
        seat.set_scale(0.4, 0.4, 0.3)
        buggy.add_part(seat)

    # Set properties
    buggy.set_property("type", "dune_buggy")
    buggy.set_property("wheels", len(wheels))
    buggy.set_property("max_speed", 80)  # km/h

    print(f"  Total parts: {buggy.get_part_count()}")

    return buggy


def main():
    print("Custom Vehicle Builder")
    print("=" * 50)

    # Create custom buggy
    buggy = create_custom_buggy()

    # Get bounds
    min_bounds, max_bounds = buggy.get_bounds()
    dimensions = max_bounds - min_bounds
    print(f"\nVehicle dimensions:")
    print(f"  Length: {dimensions[0]:.2f}m")
    print(f"  Width: {dimensions[1]:.2f}m")
    print(f"  Height: {dimensions[2]:.2f}m")

    # Export to Blender
    print("\nExporting to Blender...")
    output_file = os.path.join(os.path.dirname(__file__), "custom_buggy_export.py")
    export_to_blender(buggy, output_file, also_json=True)

    print(f"\nDone! To visualize in Blender:")
    print(f"  1. Open Blender")
    print(f"  2. Go to Scripting tab")
    print(f"  3. Open the file: {output_file}")
    print(f"  4. Run the script (Alt+P or click 'Run Script')")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
