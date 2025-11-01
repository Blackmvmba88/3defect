#!/usr/bin/env python3
"""
Ejemplo: Crear un coche y exportarlo a Blender.
Example: Create a car and export it to Blender.

Este script demuestra cómo crear un modelo de coche usando la biblioteca 3defect
y exportarlo a un script Python de Blender.
This script demonstrates how to create a car model using the 3defect library
and export it to a Blender Python script.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d import Car
from defect3d.blender_integration import export_to_blender
from defect3d.i18n import get_language


def main():
    lang = get_language()

    if lang == 'es':
        print("Creando un coche deportivo...")
    else:
        print("Creating a sports car...")

    # Create a sports car
    sports_car = Car(car_type="sports", position=(0, 0, 0), color=(0.9, 0.1, 0.1))

    # Get specifications
    specs = sports_car.get_specifications()

    if lang == 'es':
        print(f"\nEspecificaciones del Coche:")
        tipo_key = 'tipo'
        dim_key = 'dimensiones'
        long_key = 'longitud'
        ancho_key = 'ancho'
        alt_key = 'altura'
        ruedas_key = 'ruedas'
        motor_key = 'motor'
        cil_key = 'cilindros'
        pot_key = 'potencia'
        parts_key = 'total_partes'
        print(f"  Tipo: {specs[tipo_key]}")
        print(f"  Dimensiones: {specs[dim_key][long_key]:.2f}m x {specs[dim_key][ancho_key]:.2f}m x {specs[dim_key][alt_key]:.2f}m")
        print(f"  Ruedas: {specs[ruedas_key]}")
        print(f"  Motor: {specs[motor_key][cil_key]} cilindros, {specs[motor_key][pot_key]} HP")
        print(f"  Partes totales: {specs[parts_key]}")

        print("\nSimulando movimiento...")
        sports_car.simulate_movement(distance=5.0, direction=(1, 0, 0))
        print(f"  Nueva posición: {sports_car.position}")

        print("\nExportando a Blender...")
        output_file = os.path.join(os.path.dirname(__file__), "car_export.py")
        export_to_blender(sports_car, output_file, also_json=True)

        print(f"\n¡Hecho! Para visualizar en Blender:")
        print(f"  1. Abrir Blender")
        print(f"  2. Ir a la pestaña de Scripting")
        print(f"  3. Abrir el archivo: {output_file}")
        print(f"  4. Ejecutar el script (Alt+P o clic en 'Run Script')")
    else:
        print(f"\nCar Specifications:")
        print(f"  Type: {specs['type']}")
        print(f"  Dimensions: {specs['dimensions']['length']:.2f}m x {specs['dimensions']['width']:.2f}m x {specs['dimensions']['height']:.2f}m")
        print(f"  Wheels: {specs['wheels']}")
        print(f"  Engine: {specs['engine']['cylinders']} cylinders, {specs['engine']['power']} HP")
        print(f"  Total parts: {specs['parts_count']}")

        print("\nSimulating movement...")
        sports_car.simulate_movement(distance=5.0, direction=(1, 0, 0))
        print(f"  New position: {sports_car.position}")

        print("\nExporting to Blender...")
        output_file = os.path.join(os.path.dirname(__file__), "car_export.py")
        export_to_blender(sports_car, output_file, also_json=True)

        print(f"\nDone! To visualize in Blender:")
        print(f"  1. Open Blender")
        print(f"  2. Go to Scripting tab")
        print(f"  3. Open the file: {output_file}")
        print(f"  4. Run the script (Alt+P or click 'Run Script')")


if __name__ == "__main__":
    main()
