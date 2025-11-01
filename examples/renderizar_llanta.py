#!/usr/bin/env python3
"""
Ejemplo: Crear y renderizar una llanta con rin.
Example: Create and render a wheel with rim.

Este es el primer ejercicio: crear una llanta (tire) y rin (rim) y generar
una imagen renderizada fotorrealista.

This is the first exercise: create a tire and rim and generate
a photorealistic rendered image.
"""

import sys
import os

# Agregar directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Forzar idioma español para este ejemplo
from defect3d.i18n import set_language
set_language('es')

from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import export_to_blender


def crear_llanta_personalizada():
    """
    Crea una llanta personalizada con rin y tire.
    Creates a custom wheel with rim and tire.
    """
    print("=" * 70)
    print("EJERCICIO 1: CREAR LLANTA CON RIN")
    print("=" * 70)
    print()

    print("1. Creando llanta con rin...")
    print("   - Radio: 0.35m (35cm)")
    print("   - Ancho: 0.25m (25cm)")
    print()

    # Crear la llanta
    llanta = Wheel(radius=0.35, width=0.25, position=(0, 0, 0))

    print("2. Componentes de la llanta:")
    print(f"   ✓ Tire (Llanta): Color negro, goma")
    print(f"   ✓ Rim (Rin): Color metálico plateado")
    print(f"   ✓ Total de partes: {llanta.get_part_count()}")
    print()

    # Información técnica
    print("3. Especificaciones técnicas:")
    print(f"   • Radio exterior: {llanta.radius:.2f}m")
    print(f"   • Ancho: {llanta.width:.2f}m")
    print(f"   • Diámetro total: {llanta.radius * 2:.2f}m")
    print()

    return llanta


def exportar_para_blender(llanta):
    """
    Exporta la llanta a un archivo de Blender.
    Exports the wheel to a Blender file.
    """
    print("4. Exportando modelo a Blender...")

    # Guardar el script de Blender
    output_file = os.path.join(os.path.dirname(__file__), "llanta_export.py")
    export_to_blender(llanta, output_file, also_json=True)

    print(f"   ✓ Script guardado: {output_file}")
    print(f"   ✓ Datos JSON guardados: {output_file.replace('.py', '.json')}")
    print()


def generar_instrucciones_renderizado():
    """
    Genera instrucciones para renderizar la llanta.
    Generates instructions for rendering the wheel.
    """
    print("=" * 70)
    print("INSTRUCCIONES PARA OBTENER LA IMAGEN RENDERIZADA")
    print("=" * 70)
    print()

    print("MÉTODO 1: Usando Blender GUI (Interfaz Gráfica)")
    print("-" * 70)
    print("1. Abrir Blender")
    print("2. Ir a la pestaña 'Scripting'")
    print("3. Abrir el archivo: llanta_export.py")
    print("4. Ejecutar el script (Alt+P o botón 'Run Script')")
    print("5. La llanta aparecerá en la escena")
    print()
    print("Para renderizar:")
    print("6. Presionar F12 para renderizar")
    print("7. Ir a 'Image' > 'Save As' para guardar la imagen")
    print("   Guardar como: llanta_renderizada.png")
    print()

    print("MÉTODO 2: Usando Blender desde línea de comandos")
    print("-" * 70)
    print("Ejecuta este comando en la terminal:")
    print()
    print("  blender --background --python llanta_export.py --render-output llanta.png -f 1")
    print()
    print("Esto creará automáticamente 'llanta.png' con la imagen renderizada.")
    print()

    print("MÉTODO 3: Renderizado automático (si tienes Blender instalado)")
    print("-" * 70)
    print("Ejecuta el siguiente script Python:")
    print()
    print("  python ejemplos/renderizar_llanta_auto.py")
    print()
    print("Este script generará automáticamente la imagen renderizada.")
    print()

    print("=" * 70)
    print("RESULTADO ESPERADO")
    print("=" * 70)
    print()
    print("La imagen renderizada mostrará:")
    print("  • Una llanta negra (tire) de goma con textura realista")
    print("  • Un rin metálico plateado en el centro")
    print("  • Iluminación profesional de 3 puntos")
    print("  • Sombras y reflejos realistas")
    print("  • Fondo gris neutro con plano de suelo")
    print("  • Resolución: 1920x1080 (Full HD)")
    print()

    print("NOTAS IMPORTANTES:")
    print("  ⚠ Blender debe estar instalado en tu sistema")
    print("  ⚠ El renderizado puede tomar 1-5 minutos dependiendo de tu hardware")
    print("  ⚠ El archivo .blend se guarda para futuras modificaciones")
    print()


def crear_script_renderizado_automatico():
    """
    Crea un script para renderizado automático.
    Creates a script for automatic rendering.
    """
    script_content = '''#!/usr/bin/env python3
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
'''

    script_path = os.path.join(os.path.dirname(__file__), "renderizar_llanta_auto.py")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)

    print(f"✓ Script de renderizado automático creado: {script_path}")
    print()


def main():
    """Función principal."""
    print()

    # Crear la llanta
    llanta = crear_llanta_personalizada()

    # Exportar para Blender
    exportar_para_blender(llanta)

    # Crear script de renderizado automático
    crear_script_renderizado_automatico()

    # Mostrar instrucciones
    generar_instrucciones_renderizado()

    print("=" * 70)
    print("EJERCICIO COMPLETADO")
    print("=" * 70)
    print()
    print("Próximos pasos:")
    print("  1. Revisar el archivo llanta_export.py")
    print("  2. Elegir uno de los 3 métodos para generar la imagen renderizada")
    print("  3. ¡Disfrutar de tu llanta en 3D fotorrealista!")
    print()
    print("¡El archivo de modelado está guardado para futuras modificaciones!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
