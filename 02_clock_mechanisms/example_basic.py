#!/usr/bin/env python3
"""
Ejemplo básico de mecanismos de reloj / Basic clock mechanisms example

Demuestra engranajes, escapes, péndulos, resortes y trenes de engranajes.
Demonstrates gears, escapements, pendulums, springs and gear trains.
"""

from defect3d.clock_mechanisms import Gear, Escapement, Pendulum, Spring, GearTrain


def main():
    print("=== NIVEL 2: MECANISMOS DE RELOJ / LEVEL 2: CLOCK MECHANISMS ===\n")

    # 1. Engranajes individuales / Individual gears
    print("1. Engranajes / Gears")

    gear1 = Gear(teeth=30, module=1.0, thickness=0.5)
    gear2 = Gear(teeth=15, module=1.0, thickness=0.5)

    print(f"   Engranaje 1 / Gear 1: {gear1.teeth} dientes/teeth, "
          f"diámetro/diameter={gear1.pitch_diameter:.2f}")
    print(f"   Engranaje 2 / Gear 2: {gear2.teeth} dientes/teeth, "
          f"diámetro/diameter={gear2.pitch_diameter:.2f}")

    ratio = gear1.gear_ratio(gear2)
    print(f"   Relación / Ratio: {ratio:.2f}:1")
    print(f"   → Si gear1 gira a 60 RPM, gear2 gira a {60/ratio:.1f} RPM")
    print(f"   → If gear1 rotates at 60 RPM, gear2 rotates at {60/ratio:.1f} RPM")

    # 2. Escape / Escapement
    print("\n2. Escape / Escapement")

    escape = Escapement(frequency=1.0)
    print(f"   Frecuencia / Frequency: {escape.frequency} Hz")
    print(f"   Período / Period: {escape.period} segundos/seconds")
    print(f"   → Hace {escape.frequency} 'tic' por segundo / Makes {escape.frequency} 'tick' per second")

    # 3. Péndulo / Pendulum
    print("\n3. Péndulo / Pendulum")

    # Péndulo de 1 metro / 1 meter pendulum
    pendulum1m = Pendulum(length=1.0, mass=0.5)
    print(f"   Longitud / Length: {pendulum1m.length} m")
    print(f"   Período / Period: {pendulum1m.period:.3f} s")
    print(f"   Frecuencia / Frequency: {pendulum1m.frequency:.3f} Hz")

    # Péndulo de reloj de pared (más largo, más lento)
    # Wall clock pendulum (longer, slower)
    pendulum2m = Pendulum(length=2.0, mass=1.0)
    print(f"\n   Péndulo más largo / Longer pendulum: {pendulum2m.length} m")
    print(f"   Período / Period: {pendulum2m.period:.3f} s")
    print(f"   → {pendulum1m.period/pendulum2m.period:.2f}x más rápido que el corto")
    print(f"   → {pendulum1m.period/pendulum2m.period:.2f}x faster than the short one")

    # 4. Resorte / Spring
    print("\n4. Resorte / Spring")

    spring = Spring(coils=12, stiffness=100.0, free_length=0.2)

    compressions = [0.01, 0.02, 0.05]  # 1cm, 2cm, 5cm
    print(f"   Rigidez / Stiffness: {spring.stiffness} N/m")
    print(f"   Longitud libre / Free length: {spring.free_length} m")
    print(f"\n   Compresión (m) | Fuerza (N) | Energía (J)")
    print(f"   Compression    | Force      | Energy")
    print(f"   " + "-"*47)

    for comp in compressions:
        force = spring.force(comp)
        energy = spring.energy(comp)
        print(f"   {comp:13.3f} | {force:10.2f} | {energy:10.3f}")

    # 5. Tren de engranajes / Gear train
    print("\n5. Tren de Engranajes / Gear Train")

    train = GearTrain(name="reloj_mecanico")

    # Crear un tren de reducción / Create a reduction train
    # Motor -> Minutos -> Segundos / Motor -> Minutes -> Seconds
    motor_gear = Gear(teeth=60, module=0.5, position=(0, 0, 0))
    minute_gear = Gear(teeth=30, module=0.5, position=(1.5, 0, 0))
    second_gear = Gear(teeth=15, module=0.5, position=(2.5, 0, 0))

    train.add_gear(motor_gear)
    train.add_gear(minute_gear, connects_to=0)
    train.add_gear(second_gear, connects_to=1)

    print(f"   Engranajes en el tren / Gears in train: {len(train.gears)}")
    print(f"   Relación total / Total ratio: {train.total_ratio():.2f}:1")

    input_speed = 60  # RPM
    output_speed = train.output_speed(input_speed)

    print(f"\n   Velocidad entrada / Input speed: {input_speed} RPM")
    print(f"   Velocidad salida / Output speed: {output_speed:.2f} RPM")
    print(f"   → Reducción de velocidad, aumento de torque")
    print(f"   → Speed reduction, torque increase")

    # 6. Sistema completo de reloj / Complete clock system
    print("\n6. Sistema de Reloj Completo / Complete Clock System")

    print("\n   Componentes / Components:")
    print(f"   • Resorte / Spring: almacena {spring.energy(0.05):.2f} J")
    print(f"   • Escape / Escapement: libera energía a {escape.frequency} Hz")
    print(f"   • Péndulo / Pendulum: oscila con período {pendulum1m.period:.3f} s")
    print(f"   • Tren de engranajes / Gear train: reduce velocidad {train.total_ratio():.1f}x")

    print("\n   Flujo de energía / Energy flow:")
    print("   Resorte → Tren → Escape → Péndulo")
    print("   Spring  → Train → Escapement → Pendulum")

    print("\n✅ Nivel 2 completado / Level 2 completed!")
    print("   Ya tienes relojería sistemática / You now have systematic watchmaking")
    print("   Siguiente / Next: 03_engines - Convertir estos mecanismos en motores")
    print("                                   Convert these mechanisms into engines")


if __name__ == "__main__":
    main()
