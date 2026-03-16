#!/usr/bin/env python3
"""
Ejemplo de visualización en Blender / Blender visualization example

Exporta formas básicas a Blender para visualización.
Exports basic shapes to Blender for visualization.
"""

from defect3d import Cube, Sphere, Cylinder, Cone, Torus, CompositePart
from defect3d.blender_integration import export_to_blender


def main():
    print("=== NIVEL 1: GEOMETRÍA - Exportación Blender / LEVEL 1: GEOMETRY - Blender Export ===\n")

    # Crear una galería de formas / Create a gallery of shapes
    print("1. Creando galería de formas básicas / Creating gallery of basic shapes")

    galeria = CompositePart(name="geometria_basica")

    # Cubo / Cube
    cubo = Cube(size=2.0, position=(0, 0, 0))
    cubo.set_color(0.8, 0.2, 0.2, 1.0)
    galeria.add_part(cubo)

    # Esfera / Sphere
    esfera = Sphere(radius=1.2, position=(4, 0, 0))
    esfera.set_color(0.2, 0.8, 0.2, 1.0)
    galeria.add_part(esfera)

    # Cilindro / Cylinder
    cilindro = Cylinder(radius=0.8, height=3.0, position=(8, 0, 1.5))
    cilindro.set_color(0.2, 0.2, 0.8, 1.0)
    galeria.add_part(cilindro)

    # Cono / Cone
    cono = Cone(radius=1.0, height=2.5, position=(12, 0, 1.25))
    cono.set_color(0.8, 0.8, 0.2, 1.0)
    galeria.add_part(cono)

    # Toro / Torus
    toro = Torus(major_radius=1.2, minor_radius=0.4, position=(16, 0, 0))
    toro.set_color(0.8, 0.2, 0.8, 1.0)
    galeria.add_part(toro)

    print(f"   Formas creadas / Shapes created: {len(galeria.parts)}")

    # Exportar a Blender / Export to Blender
    print("\n2. Exportando a Blender / Exporting to Blender")
    output_file = "01_geometry_gallery.py"
    export_to_blender(galeria, output_file)
    print(f"   ✅ Archivo exportado / File exported: {output_file}")

    # Crear una estructura compuesta / Create a composite structure
    print("\n3. Creando estructura compuesta / Creating composite structure")

    estructura = CompositePart(name="torre_geometrica")

    # Base (cubo grande) / Base (large cube)
    base = Cube(size=4.0, position=(0, 0, 0))
    base.set_color(0.5, 0.5, 0.5, 1.0)
    estructura.add_part(base)

    # Columnas (cilindros) / Columns (cylinders)
    for i, pos in enumerate([(-1.5, -1.5), (-1.5, 1.5), (1.5, -1.5), (1.5, 1.5)]):
        columna = Cylinder(radius=0.3, height=6.0, position=(pos[0], pos[1], 3.0))
        columna.set_color(0.7, 0.3, 0.3, 1.0)
        estructura.add_part(columna)

    # Techo (esfera) / Roof (sphere)
    techo = Sphere(radius=2.5, position=(0, 0, 8.0))
    techo.set_color(0.3, 0.3, 0.7, 1.0)
    estructura.add_part(techo)

    # Decoración (toros) / Decoration (tori)
    for angle in [0, 90, 180, 270]:
        import math
        rad = math.radians(angle)
        x = 2.0 * math.cos(rad)
        y = 2.0 * math.sin(rad)
        toro_dec = Torus(major_radius=0.5, minor_radius=0.15, position=(x, y, 6.0))
        toro_dec.set_color(0.9, 0.7, 0.2, 1.0)
        estructura.add_part(toro_dec)

    print(f"   Partes en la estructura / Parts in structure: {len(estructura.parts)}")

    # Exportar estructura / Export structure
    output_file2 = "01_geometry_tower.py"
    export_to_blender(estructura, output_file2)
    print(f"   ✅ Archivo exportado / File exported: {output_file2}")

    print("\n" + "="*70)
    print("INSTRUCCIONES PARA BLENDER / INSTRUCTIONS FOR BLENDER:")
    print("="*70)
    print("1. Abrir Blender / Open Blender")
    print("2. Cambiar a espacio de trabajo 'Scripting' / Switch to 'Scripting' workspace")
    print(f"3. Abrir el archivo / Open file: {output_file}")
    print("   o / or: {output_file2}")
    print("4. Ejecutar script (Alt+P) / Run script (Alt+P)")
    print("5. ¡Ver tu geometría en 3D! / See your geometry in 3D!")
    print("="*70)

    print("\n✅ Ejemplos exportados / Examples exported!")
    print("   Ahora puedes visualizar las formas básicas en Blender.")
    print("   Now you can visualize the basic shapes in Blender.")


if __name__ == "__main__":
    main()
