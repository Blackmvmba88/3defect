#!/usr/bin/env python3
"""
Example: Create a motorcycle and export it to Blender.

This script demonstrates how to create a motorcycle model using the 3defect library
and export it to a Blender Python script.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d import Motorcycle
from defect3d.blender_integration import export_to_blender


def main():
    print("Creating a sport motorcycle...")
    
    # Create a sport motorcycle
    sport_bike = Motorcycle(bike_type="sport", position=(0, 0, 0), color=(0.1, 0.1, 0.9))
    
    # Get specifications
    specs = sport_bike.get_specifications()
    print(f"\nMotorcycle Specifications:")
    print(f"  Type: {specs['type']}")
    print(f"  Dimensions: {specs['dimensions']['length']:.2f}m x {specs['dimensions']['width']:.2f}m")
    print(f"  Seat Height: {specs['dimensions']['seat_height']:.2f}m")
    print(f"  Wheels: {specs['wheels']}")
    print(f"  Engine: {specs['engine']['cylinders']} cylinders, {specs['engine']['power']} HP")
    print(f"  Total parts: {specs['parts_count']}")
    
    # Simulate some movement
    print("\nSimulating movement...")
    sport_bike.simulate_movement(distance=10.0, direction=(1, 0, 0))
    print(f"  New position: {sport_bike.position}")
    
    # Export to Blender
    print("\nExporting to Blender...")
    output_file = os.path.join(os.path.dirname(__file__), "motorcycle_export.py")
    export_to_blender(sport_bike, output_file, also_json=True)
    
    print(f"\nDone! To visualize in Blender:")
    print(f"  1. Open Blender")
    print(f"  2. Go to Scripting tab")
    print(f"  3. Open the file: {output_file}")
    print(f"  4. Run the script (Alt+P or click 'Run Script')")


if __name__ == "__main__":
    main()
