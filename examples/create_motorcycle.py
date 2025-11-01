#!/usr/bin/env python3
"""
Ejemplo: Crear una motocicleta y exportarla a Blender.
Example: Create a motorcycle and export it to Blender.

Este script demuestra cómo crear un modelo de motocicleta usando la biblioteca 3defect
y exportarlo a un script Python de Blender.
This script demonstrates how to create a motorcycle model using the 3defect library
and export it to a Blender Python script.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d import Motorcycle
from defect3d.blender_integration import export_to_blender
from defect3d.i18n import get_language


def main():
    lang = get_language()

    if lang == 'es':
        print("Creando una motocicleta deportiva...")
    else:
        print("Creating a sport motorcycle...")

    # Create a sport motorcycle
    sport_bike = Motorcycle(bike_type="sport", position=(0, 0, 0), color=(0.1, 0.1, 0.9))

    # Get specifications
    specs = sport_bike.get_specifications()

    if lang == 'es':
        print(f"\nEspecificaciones de la Motocicleta:")
        print(f"  Tipo: {specs['tipo']}")
        print(f"  Dimensiones: {specs['dimensiones']['longitud']:.2f}m x {specs['dimensiones']['ancho']:.2f}m")
        print(f"  Altura del asiento: {specs['dimensiones']['altura_asiento']:.2f}m")
        print(f"  Ruedas: {specs['ruedas']}")
        print(f"  Motor: {specs['motor']['cilindros']} cilindros, {specs['motor']['potencia']} HP")
        print(f"  Partes totales: {specs['total_partes']}")

        print("\nSimulando movimiento...")
        sport_bike.simulate_movement(distance=10.0, direction=(1, 0, 0))
        print(f"  Nueva posición: {sport_bike.position}")

        print("\nExportando a Blender...")
        output_file = os.path.join(os.path.dirname(__file__), "motorcycle_export.py")
        export_to_blender(sport_bike, output_file, also_json=True)

        print(f"\n¡Hecho! Para visualizar en Blender:")
        print(f"  1. Abrir Blender")
        print(f"  2. Ir a la pestaña de Scripting")
        print(f"  3. Abrir el archivo: {output_file}")
        print(f"  4. Ejecutar el script (Alt+P o clic en 'Run Script')")
    else:
        print(f"\nMotorcycle Specifications:")
        print(f"  Type: {specs['type']}")
        print(f"  Dimensions: {specs['dimensions']['length']:.2f}m x {specs['dimensions']['width']:.2f}m")
        print(f"  Seat Height: {specs['dimensions']['seat_height']:.2f}m")
        print(f"  Wheels: {specs['wheels']}")
        print(f"  Engine: {specs['engine']['cylinders']} cylinders, {specs['engine']['power']} HP")
        print(f"  Total parts: {specs['parts_count']}")

        print("\nSimulating movement...")
        sport_bike.simulate_movement(distance=10.0, direction=(1, 0, 0))
        print(f"  New position: {sport_bike.position}")

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
