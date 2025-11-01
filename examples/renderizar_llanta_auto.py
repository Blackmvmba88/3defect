#!/usr/bin/env python3
"""
Script automático para renderizar la llanta.
Automatic script to render the wheel.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d.i18n import set_language
set_language('es')

from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import BlenderRenderer

def main():
    print("Renderizando llanta automáticamente...")
    print()

    # Crear la llanta
    llanta = Wheel(radius=0.35, width=0.25, position=(0, 0, 0))

    # Crear renderizador
    renderer = BlenderRenderer()

    # Configurar salida
    output_path = os.path.join(os.path.dirname(__file__), "llanta_renderizada.png")

    print(f"Generando imagen renderizada en: {output_path}")
    print("Esto puede tomar unos minutos...")
    print()

    # Renderizar con configuración de alta calidad
    success = renderer.render(
        llanta,
        output_path,
        resolution=(1920, 1080),  # Full HD
        samples=128,  # Buena calidad
        camera_distance=1.5,  # Más cerca para ver detalles
        camera_angle=(45, 0, 30)  # Ángulo óptimo para la llanta
    )

    if success:
        print("✓ ¡Renderizado completado exitosamente!")
        print(f"✓ Imagen guardada en: {output_path}")
        print()
        print("Puedes abrir la imagen con cualquier visor de imágenes.")
    else:
        print("✗ Error al renderizar.")
        print("Asegúrate de que Blender esté instalado y en el PATH del sistema.")

if __name__ == "__main__":
    main()
