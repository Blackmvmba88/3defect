#!/usr/bin/env python3
"""
Ejemplo básico de visualización Blender / Basic Blender visualization example

Demuestra la exportación y renderizado de objetos a Blender.
Demonstrates export and rendering of objects to Blender.
"""

from defect3d import Car, Motorcycle, Cube, Sphere
from defect3d.blender_integration import export_to_blender, BlenderRenderer
from defect3d import CompositePart


def main():
    print("=== NIVEL 6: EXPORTACIÓN ARTÍSTICA / LEVEL 6: ARTISTIC EXPORT ===\n")
    
    # 1. Exportar vehículos a Blender / Export vehicles to Blender
    print("1. Exportando Vehículos / Exporting Vehicles\n")
    
    # Crear vehículos / Create vehicles
    sedan = Car(car_type="sedan", color=(0.3, 0.3, 0.8))
    sports = Car(car_type="sports", color=(0.9, 0.1, 0.1))
    bike = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))
    
    vehicles = [
        ("sedan", sedan),
        ("sports_car", sports),
        ("sport_bike", bike),
    ]
    
    for name, vehicle in vehicles:
        filename = f"06_{name}.py"
        export_to_blender(vehicle, filename)
        print(f"   ✅ Exportado / Exported: {filename}")
    
    # 2. Crear escena compuesta / Create composite scene
    print("\n2. Creando Escena Compuesta / Creating Composite Scene\n")
    
    escena = CompositePart(name="garage")
    
    # Piso / Floor
    piso = Cube(size=20.0, position=(0, 0, -0.5))
    piso.set_color(0.4, 0.4, 0.4, 1.0)
    piso.set_scale(1, 1, 0.05)
    escena.add_part(piso)
    
    # Vehículos en posiciones / Vehicles at positions
    sedan_scene = Car(car_type="sedan")
    sedan_scene.position = (-5, 0, 0)
    escena.add_part(sedan_scene)
    
    sports_scene = Car(car_type="sports")
    sports_scene.position = (0, 0, 0)
    escena.add_part(sports_scene)
    
    bike_scene = Motorcycle(bike_type="sport")
    bike_scene.position = (5, 0, 0)
    escena.add_part(bike_scene)
    
    # Luces (esferas brillantes) / Lights (bright spheres)
    for x in [-8, 8]:
        luz = Sphere(radius=0.5, position=(x, 0, 5))
        luz.set_color(1.0, 1.0, 0.8, 1.0)
        escena.add_part(luz)
    
    print(f"   Objetos en la escena / Objects in scene: {len(escena.parts)}")
    
    filename_scene = "06_garage_scene.py"
    export_to_blender(escena, filename_scene)
    print(f"   ✅ Escena exportada / Scene exported: {filename_scene}")
    
    # 3. Información de renderizado / Rendering information
    print("\n3. Renderizado (requiere Blender instalado)")
    print("   Rendering (requires Blender installed)\n")
    
    print("   Para renderizar con BlenderRenderer:")
    print("   To render with BlenderRenderer:")
    print()
    print("   from defect3d.blender_integration import BlenderRenderer")
    print("   renderer = BlenderRenderer()")
    print("   renderer.render(vehicle, 'output.png', resolution=(1920, 1080))")
    print()
    print("   Nota: Requiere Blender en PATH del sistema")
    print("   Note: Requires Blender in system PATH")
    
    # 4. Diferentes formatos / Different formats
    print("\n4. Formatos de Exportación / Export Formats\n")
    
    from defect3d.core.serializer import to_json, save_json
    
    # JSON
    json_data = to_json(sedan)
    save_json(json_data, "06_sedan.json")
    print("   ✅ JSON exportado / JSON exported: 06_sedan.json")
    
    # Blender Python
    export_to_blender(sedan, "06_sedan_blender.py")
    print("   ✅ Blender Python exportado / Blender Python exported: 06_sedan_blender.py")
    
    print("\n" + "="*70)
    print("INSTRUCCIONES PARA BLENDER / INSTRUCTIONS FOR BLENDER:")
    print("="*70)
    print()
    print("1. Abrir Blender / Open Blender")
    print("2. Cambiar a workspace 'Scripting' / Switch to 'Scripting' workspace")
    print("3. Abrir cualquiera de los archivos .py / Open any of the .py files:")
    for name, _ in vehicles:
        print(f"   • 06_{name}.py")
    print(f"   • {filename_scene}")
    print("4. Ejecutar el script (Alt+P) / Run the script (Alt+P)")
    print("5. ¡Ver tu modelo en 3D! / See your 3D model!")
    print()
    print("Para renderizar / To render:")
    print("6. Cambiar a workspace 'Shading' / Switch to 'Shading' workspace")
    print("7. Ajustar materiales y luces / Adjust materials and lights")
    print("8. F12 para renderizar / F12 to render")
    print("="*70)
    
    print("\n✅ Nivel 6 completado / Level 6 completed!")
    print("   La mecánica se vuelve arte.")
    print("   Mechanics becomes art.")


if __name__ == "__main__":
    main()
