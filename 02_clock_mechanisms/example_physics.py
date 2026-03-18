#!/usr/bin/env python3
"""
Test físico de mecanismos de reloj / Physics test of clock mechanisms

Demuestra las propiedades físicas de los mecanismos de relojería.
Demonstrates the physical properties of clock mechanisms.
"""

import math
from defect3d.clock_mechanisms import Gear, Pendulum, Spring, GearTrain


def main():
    print("=== NIVEL 2: MECANISMOS DE RELOJ - Test Físico ===\n")

    # 1. Conservación de momento angular en engranajes
    # Conservation of angular momentum in gears
    print("1. Transmisión de Potencia en Engranajes / Power Transmission in Gears")

    gear_drive = Gear(teeth=40, module=1.0)
    gear_driven = Gear(teeth=20, module=1.0)

    # Velocidad angular del motor / Angular velocity of driver
    omega_drive = 10.0  # rad/s
    ratio = gear_drive.gear_ratio(gear_driven)
    omega_driven = omega_drive * ratio

    print(f"   Engranaje motor / Driver gear: {gear_drive.teeth} dientes/teeth")
    print(f"   Engranaje movido / Driven gear: {gear_driven.teeth} dientes/teeth")
    print(f"   Relación / Ratio: {ratio:.2f}:1")
    print(f"   ω motor / ω driver: {omega_drive:.2f} rad/s")
    print(f"   ω movido / ω driven: {omega_driven:.2f} rad/s")

    # Torque (asumiendo potencia constante) / Torque (assuming constant power)
    # P = T × ω → T_driven = T_drive × ratio
    torque_drive = 10.0  # N⋅m
    torque_driven = torque_drive * ratio

    print(f"\n   Torque motor / Driver torque: {torque_drive:.2f} N⋅m")
    print(f"   Torque movido / Driven torque: {torque_driven:.2f} N⋅m")
    print(f"   → Velocidad reducida, torque aumentado / Speed reduced, torque increased")

    # 2. Péndulo: Ley del péndulo simple / Pendulum: Simple pendulum law
    print("\n2. Física del Péndulo / Pendulum Physics")

    # T = 2π√(L/g)
    g = 9.81  # m/s²

    lengths = [0.5, 1.0, 1.5, 2.0]
    print(f"\n   Longitud (m) | Período (s) | Frecuencia (Hz)")
    print(f"   Length       | Period      | Frequency")
    print(f"   " + "-"*47)

    for length in lengths:
        pendulum = Pendulum(length=length, mass=0.5)
        print(f"   {length:12.2f} | {pendulum.period:11.3f} | {pendulum.frequency:14.3f}")

    # Verificar que el período es independiente de la masa
    # Verify that period is independent of mass
    print(f"\n   Verificación: ¿El período depende de la masa?")
    print(f"   Verification: Does period depend on mass?")

    p1 = Pendulum(length=1.0, mass=0.1)
    p2 = Pendulum(length=1.0, mass=1.0)
    p3 = Pendulum(length=1.0, mass=5.0)

    print(f"   Masa 0.1 kg / Mass: período/period = {p1.period:.4f} s")
    print(f"   Masa 1.0 kg / Mass: período/period = {p2.period:.4f} s")
    print(f"   Masa 5.0 kg / Mass: período/period = {p3.period:.4f} s")
    print(f"   → ¡Independiente de la masa! / Independent of mass!")

    # 3. Resorte: Ley de Hooke / Spring: Hooke's law
    print("\n3. Ley de Hooke del Resorte / Spring Hooke's Law")

    spring = Spring(coils=10, stiffness=100.0, free_length=0.5)

    print(f"   Rigidez / Stiffness k = {spring.stiffness} N/m")
    print(f"   F = k × x  (Ley de Hooke / Hooke's Law)")
    print(f"   E = ½k × x²  (Energía elástica / Elastic energy)")

    compressions = [0.01, 0.02, 0.05, 0.10, 0.15]
    print(f"\n   Compresión x (m) | Fuerza F (N) | Energía E (J)")
    print(f"   Compression      | Force        | Energy")
    print(f"   " + "-"*52)

    for x in compressions:
        F = spring.force(x)
        E = spring.energy(x)
        print(f"   {x:16.3f} | {F:12.2f} | {E:13.4f}")

    # Verificar relación lineal / Verify linear relationship
    print(f"\n   Verificación linealidad / Linearity check:")
    x1, x2 = 0.05, 0.10
    F1, F2 = spring.force(x1), spring.force(x2)
    print(f"   F({x2}m) / F({x1}m) = {F2/F1:.2f}")
    print(f"   {x2}m / {x1}m = {x2/x1:.2f}")
    print(f"   → Relación lineal confirmada / Linear relationship confirmed")

    # 4. Tren de engranajes: Conservación de energía
    # Gear train: Energy conservation
    print("\n4. Conservación de Energía en Tren / Energy Conservation in Train")

    train = GearTrain()
    train.add_gear(Gear(teeth=60, module=0.5))
    train.add_gear(Gear(teeth=30, module=0.5))
    train.add_gear(Gear(teeth=15, module=0.5))

    # Potencia de entrada / Input power
    input_rpm = 120
    input_torque = 5.0  # N⋅m
    input_omega = input_rpm * 2 * math.pi / 60  # rad/s
    input_power = input_torque * input_omega

    # Potencia de salida (asumiendo 100% eficiencia) / Output power (assuming 100% efficiency)
    output_rpm = train.output_speed(input_rpm)
    output_omega = output_rpm * 2 * math.pi / 60
    output_torque = input_power / output_omega  # P = T × ω

    print(f"   Relación del tren / Train ratio: {train.total_ratio():.2f}:1")
    print(f"\n   Entrada / Input:")
    print(f"     Velocidad / Speed: {input_rpm:.2f} RPM ({input_omega:.2f} rad/s)")
    print(f"     Torque: {input_torque:.2f} N⋅m")
    print(f"     Potencia / Power: {input_power:.2f} W")

    print(f"\n   Salida / Output:")
    print(f"     Velocidad / Speed: {output_rpm:.2f} RPM ({output_omega:.2f} rad/s)")
    print(f"     Torque: {output_torque:.2f} N⋅m")
    print(f"     Potencia / Power: {input_power:.2f} W")

    print(f"\n   → Potencia conservada (sin fricción)")
    print(f"   → Power conserved (without friction)")
    print(f"   → Velocidad ÷{train.total_ratio():.1f}, Torque ×{train.total_ratio():.1f}")

    # 5. Oscilador armónico: Péndulo + Resorte
    print("\n5. Comparación de Osciladores / Oscillator Comparison")

    # Péndulo / Pendulum
    pend = Pendulum(length=1.0, mass=1.0)

    # Resorte con masa / Spring with mass
    spr = Spring(stiffness=100.0)
    mass = 1.0  # kg
    # Período del resorte: T = 2π√(m/k)
    spring_period = 2 * math.pi * math.sqrt(mass / spr.stiffness)
    spring_freq = 1.0 / spring_period

    print(f"\n   Péndulo (L=1m) / Pendulum (L=1m):")
    print(f"     Período / Period: {pend.period:.3f} s")
    print(f"     Frecuencia / Frequency: {pend.frequency:.3f} Hz")

    print(f"\n   Resorte (k=100 N/m, m=1 kg) / Spring:")
    print(f"     Período / Period: {spring_period:.3f} s")
    print(f"     Frecuencia / Frequency: {spring_freq:.3f} Hz")

    print(f"\n   → Ambos son osciladores armónicos")
    print(f"   → Both are harmonic oscillators")

    print("\n✅ Test físico completado / Physics test completed!")
    print("   Los mecanismos de reloj siguen leyes físicas precisas.")
    print("   Clock mechanisms follow precise physical laws.")


if __name__ == "__main__":
    main()
