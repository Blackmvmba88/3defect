"""
Biomimetic Architecture Example / Ejemplo de Arquitectura Biomimética

Demuestra la creación de edificios biomiméticos en diferentes escalas.
Demonstrates creation of biomimetic buildings at different scales.
"""

import os
from defect3d.architecture import (
    BuildingScale,
    BiomimeticMesh,
    get_scale_config,
    get_all_scales
)
from defect3d.architecture.exporters import export_mesh
from defect3d.architecture.blender_integration import BlenderBiomimeticExporter


def print_available_scales():
    """
    Muestra las escalas disponibles / Shows available scales
    """
    print("\n" + "="*60)
    print("ESCALAS DISPONIBLES / AVAILABLE SCALES")
    print("="*60)
    
    scales = get_all_scales()
    
    for key, (name_es, name_en, height_range) in scales.items():
        print(f"\n{key} — {name_es}")
        print(f"    {name_en}")
        print(f"    Altura / Height: {height_range[0]}-{height_range[1]} m")


def create_biomimetic_building(scale: BuildingScale, output_dir: str = "output"):
    """
    Crea un edificio biomimético completo.
    Creates a complete biomimetic building.
    
    Args:
        scale: Escala del edificio / Building scale
        output_dir: Directorio de salida / Output directory
    """
    print(f"\n{'='*60}")
    print(f"Creando edificio biomimético / Creating biomimetic building")
    print(f"Escala / Scale: {scale.value}")
    print(f"{'='*60}\n")
    
    # Crear directorio de salida / Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generar malla maestra / Generate master mesh
    print("1. Generando malla maestra / Generating master mesh...")
    building = BiomimeticMesh(scale)
    mesh = building.get_mesh()
    
    # Mostrar especificaciones / Show specifications
    specs = building.get_specifications()
    print("\nEspecificaciones / Specifications:")
    for key, value in specs.items():
        print(f"  {key}: {value}")
    
    # 2. Exportar a formatos 3D / Export to 3D formats
    print("\n2. Exportando a formatos 3D / Exporting to 3D formats...")
    
    # OBJ
    obj_path = os.path.join(output_dir, f"biomimetic_{scale.value}.obj")
    export_mesh(mesh, obj_path, format="obj", include_materials=True)
    print(f"   ✓ OBJ: {obj_path}")
    
    # FBX
    fbx_path = os.path.join(output_dir, f"biomimetic_{scale.value}.fbx")
    export_mesh(mesh, fbx_path, format="fbx")
    print(f"   ✓ FBX: {fbx_path}")
    
    # GLB
    glb_path = os.path.join(output_dir, f"biomimetic_{scale.value}.glb")
    export_mesh(mesh, glb_path, format="glb")
    print(f"   ✓ GLB/glTF: {glb_path}")
    
    # 3. Generar archivo Blender / Generate Blender file
    print("\n3. Generando archivo Blender / Generating Blender file...")
    config = get_scale_config(scale)
    blender_exporter = BlenderBiomimeticExporter(mesh, config)
    
    blend_path = os.path.join(output_dir, f"biomimetic_{scale.value}.py")
    blender_exporter.export(
        blend_path,
        include_animation=True,
        include_geometry_nodes=True
    )
    print(f"   ✓ Blender script: {blend_path}")
    print(f"     Para usar / To use: Abre Blender > Scripting > Abre el archivo > Ejecuta")
    print(f"                        Open Blender > Scripting > Open file > Run")
    
    # 4. Generar LODs / Generate LODs
    print("\n4. Generando niveles de detalle / Generating LOD levels...")
    for lod in ["LOD0", "LOD1", "LOD2"]:
        lod_mesh = building.get_lod(lod)
        lod_path = os.path.join(output_dir, f"biomimetic_{scale.value}_{lod}.obj")
        export_mesh(lod_mesh, lod_path, format="obj")
        print(f"   ✓ {lod}: {lod_path}")
    
    print(f"\n{'='*60}")
    print(f"✓ Edificio completado / Building completed: {scale.value}")
    print(f"  Archivos en / Files in: {output_dir}/")
    print(f"{'='*60}\n")
    
    return building


def main():
    """
    Función principal / Main function
    """
    print("\n" + "="*60)
    print("GENERADOR DE ARQUITECTURA BIOMIMÉTICA")
    print("BIOMIMETIC ARCHITECTURE GENERATOR")
    print("="*60)
    
    # Mostrar escalas disponibles / Show available scales
    print_available_scales()
    
    # Crear ejemplos de cada escala / Create examples of each scale
    print("\n\nCreando edificios de ejemplo / Creating example buildings...")
    
    examples = [
        (BuildingScale.S, "output/pavilion"),
        (BuildingScale.M, "output/cultural_center"),
        # Escalas grandes comentadas para no generar demasiados archivos
        # Large scales commented to not generate too many files
        # (BuildingScale.L, "output/tower"),
        # (BuildingScale.XL, "output/megastructure"),
    ]
    
    for scale, output_dir in examples:
        try:
            building = create_biomimetic_building(scale, output_dir)
            print(f"✓ Éxito / Success: {scale.value}\n")
        except Exception as e:
            print(f"✗ Error en / Error in {scale.value}: {e}\n")
    
    print("\n" + "="*60)
    print("RESUMEN / SUMMARY")
    print("="*60)
    print("\nArchivos generados / Generated files:")
    print("  • Master Reference Mesh (.obj + .fbx + .glb)")
    print("  • Blender Version (.py script con/with Geometry Nodes)")
    print("  • LOD Levels (LOD0, LOD1, LOD2)")
    print("  • Material Slots (Skin, Ribs, Vegetation, Glass)")
    print("\nCaracterísticas implementadas / Implemented features:")
    print("  ✓ Forma biomimética (coral + hueso + concha)")
    print("  ✓ Exoesqueleto estructural tipo ribs fractales")
    print("  ✓ Canalizaciones para ventilación tipo termitero")
    print("  ✓ Piel reactiva con panales hexagonales")
    print("  ✓ UVs limpios y edge flow optimizado")
    print("  ✓ Material slots configurados")
    print("\nPróximos pasos / Next steps:")
    print("  1. Abrir archivos .obj en tu software 3D favorito")
    print("     Open .obj files in your favorite 3D software")
    print("  2. Ejecutar scripts .py en Blender para ver animación")
    print("     Run .py scripts in Blender to see animation")
    print("  3. Importar archivos .glb en motores de juego")
    print("     Import .glb files in game engines")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
