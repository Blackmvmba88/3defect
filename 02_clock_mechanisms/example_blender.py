#!/usr/bin/env python3
"""
Ejemplo Blender de mecanismos de reloj / Blender example of clock mechanisms

Exporta mecanismos de reloj a Blender para visualización.
Exports clock mechanisms to Blender for visualization.
"""

from defect3d.clock_mechanisms import Gear, Pendulum, Spring, GearTrain
from defect3d.blender_integration import export_to_blender
from defect3d import CompositePart


def main():
    print("=== NIVEL 2: MECANISMOS DE RELOJ - Blender ===\n")

    # 1. Tren de engranajes visual / Visual gear train
    print("1. Creando tren de engranajes / Creating gear train")

    train = GearTrain(name="gear_display")

    # Crear engranajes escalonados / Create stepped gears
    positions = [(0, 0, 0), (2, 0, 0), (4, 0, 0), (6, 0, 0)]
    teeth_counts = [40, 30, 20, 15]

    for i, (pos, teeth) in enumerate(zip(positions, teeth_counts)):
        gear = Gear(teeth=teeth, module=0.8, thickness=0.3, position=pos)
        train.add_gear(gear, connects_to=i-1 if i > 0 else None)

    print(f"   Engranajes creados / Gears created: {len(train.gears)}")
    print(f"   Relación total / Total ratio: {train.total_ratio():.2f}:1")

    # Exportar tren / Export train
    output1 = "02_gear_train.py"
    export_to_blender(train.part, output1)
    print(f"   ✅ Exportado / Exported: {output1}")

    # 2. Sistema de péndulo / Pendulum system
    print("\n2. Creando sistema de péndulo / Creating pendulum system")

    pendulum_system = CompositePart(name="pendulum_clock")

    # Péndulo principal / Main pendulum
    pendulum = Pendulum(length=1.5, mass=0.3, position=(0, 0, 2))
    pendulum_system.add_part(pendulum.part)

    # Base del reloj / Clock base
    from defect3d import Cube
    base = Cube(size=1.0, position=(0, 0, 0.5))
    base.set_color(0.4, 0.3, 0.2, 1.0)
    pendulum_system.add_part(base)

    print(f"   Período del péndulo / Pendulum period: {pendulum.period:.3f} s")

    output2 = "02_pendulum_clock.py"
    export_to_blender(pendulum_system, output2)
    print(f"   ✅ Exportado / Exported: {output2}")

    # 3. Resorte en compresión / Spring under compression
    print("\n3. Creando resorte / Creating spring")

    spring_assembly = CompositePart(name="spring_mechanism")

    spring = Spring(coils=15, wire_diameter=0.08, coil_diameter=0.6,
                   free_length=2.0, stiffness=200.0, position=(0, 0, 0))
    spring_assembly.add_part(spring.part)

    # Plataformas superior e inferior / Upper and lower platforms
    from defect3d import Cylinder
    platform_top = Cylinder(radius=0.5, height=0.1, position=(0, 0, 2.2))
    platform_top.set_color(0.6, 0.6, 0.6, 1.0)
    spring_assembly.add_part(platform_top)

    platform_bottom = Cylinder(radius=0.5, height=0.1, position=(0, 0, -0.2))
    platform_bottom.set_color(0.6, 0.6, 0.6, 1.0)
    spring_assembly.add_part(platform_bottom)

    print(f"   Espiras / Coils: {spring.coils}")
    print(f"   Rigidez / Stiffness: {spring.stiffness} N/m")

    output3 = "02_spring_mechanism.py"
    export_to_blender(spring_assembly, output3)
    print(f"   ✅ Exportado / Exported: {output3}")

    # 4. Reloj mecánico completo / Complete mechanical clock
    print("\n4. Creando reloj mecánico completo / Creating complete mechanical clock")

    clock = CompositePart(name="mechanical_clock")

    # Caja del reloj / Clock case
    case = Cube(size=2.0, position=(0, 0, 1))
    case.set_color(0.3, 0.2, 0.15, 1.0)
    clock.add_part(case)

    # Engranajes internos / Internal gears
    internal_train = GearTrain(name="clock_train")
    g1 = Gear(teeth=60, module=0.3, thickness=0.2, position=(-0.5, 0, 1.5))
    g2 = Gear(teeth=30, module=0.3, thickness=0.2, position=(0, 0, 1.5))
    g3 = Gear(teeth=20, module=0.3, thickness=0.2, position=(0.4, 0, 1.5))

    internal_train.add_gear(g1)
    internal_train.add_gear(g2, connects_to=0)
    internal_train.add_gear(g3, connects_to=1)

    clock.add_part(internal_train.part)

    # Péndulo del reloj / Clock pendulum
    clock_pendulum = Pendulum(length=1.2, mass=0.2, position=(0, -0.8, 2))
    clock.add_part(clock_pendulum.part)

    # Resorte motor / Motor spring
    motor_spring = Spring(coils=8, wire_diameter=0.05, coil_diameter=0.3,
                         free_length=0.8, position=(0.7, 0, 1))
    clock.add_part(motor_spring.part)

    print(f"   Componentes / Components: {len(clock.parts)}")

    output4 = "02_complete_clock.py"
    export_to_blender(clock, output4)
    print(f"   ✅ Exportado / Exported: {output4}")

    print("\n" + "="*70)
    print("INSTRUCCIONES PARA BLENDER / INSTRUCTIONS FOR BLENDER:")
    print("="*70)
    print("1. Abrir Blender / Open Blender")
    print("2. Cambiar a 'Scripting' / Switch to 'Scripting'")
    print("3. Abrir cualquiera de estos archivos / Open any of these files:")
    for f in [output1, output2, output3, output4]:
        print(f"   • {f}")
    print("4. Ejecutar (Alt+P) / Run (Alt+P)")
    print("="*70)

    print("\n✅ Mecanismos de reloj exportados / Clock mechanisms exported!")


if __name__ == "__main__":
    main()
