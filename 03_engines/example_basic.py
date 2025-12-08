#!/usr/bin/env python3
"""
Ejemplo básico de motores / Basic engines example

Demuestra la creación y uso de motores.
Demonstrates creation and usage of engines.
"""

from defect3d import Engine


def main():
    print("=== NIVEL 3: MOTORES / LEVEL 3: ENGINES ===\n")
    
    # 1. Crear diferentes tipos de motores / Create different engine types
    print("1. Tipos de Motores / Engine Types\n")
    
    engines = [
        ("Moto pequeña / Small bike", Engine(cylinders=2)),
        ("Sedan familiar / Family sedan", Engine(cylinders=4)),
        ("Deportivo / Sports car", Engine(cylinders=6)),
        ("Súper deportivo / Super sports", Engine(cylinders=8)),
    ]
    
    for name, engine in engines:
        power_estimate = engine.cylinders * 50  # HP aproximado
        print(f"   {name}:")
        print(f"     Cilindros / Cylinders: {engine.cylinders}")
        print(f"     Potencia estimada / Estimated power: ~{power_estimate} HP")
        print()
    
    # 2. Integración con engranajes / Integration with gears
    print("2. Motor + Transmisión / Engine + Transmission\n")
    
    from defect3d.clock_mechanisms import GearTrain, Gear
    
    motor = Engine(cylinders=4)
    transmision = GearTrain(name="4_speed_transmission")
    
    # Crear caja de cambios / Create gearbox
    transmision.add_gear(Gear(teeth=20, module=0.5))  # Entrada motor / Engine input
    transmision.add_gear(Gear(teeth=60, module=0.5))  # Salida a ruedas / Output to wheels
    
    motor_rpm = 3000  # RPM del motor / Engine RPM
    wheel_rpm = transmision.output_speed(motor_rpm)
    
    print(f"   Motor / Engine: {motor.cylinders} cilindros a {motor_rpm} RPM")
    print(f"   Transmisión / Transmission: ratio {transmision.total_ratio():.2f}:1")
    print(f"   Velocidad ruedas / Wheel speed: {wheel_rpm:.1f} RPM")
    print(f"   → Reducción de velocidad, aumento de torque")
    print(f"   → Speed reduction, torque increase")
    
    # 3. Energía y potencia / Energy and power
    print("\n3. Energía y Potencia / Energy and Power\n")
    
    # Potencia = Torque × Velocidad angular / Power = Torque × Angular velocity
    # P (kW) = T (N⋅m) × ω (rad/s) / 1000
    
    torque = 200  # N⋅m
    rpm = 3000
    omega = rpm * 2 * 3.14159 / 60  # rad/s
    power_kw = (torque * omega) / 1000
    power_hp = power_kw * 1.341  # Convertir a HP / Convert to HP
    
    print(f"   Torque del motor / Engine torque: {torque} N⋅m")
    print(f"   Velocidad / Speed: {rpm} RPM ({omega:.1f} rad/s)")
    print(f"   Potencia / Power: {power_kw:.1f} kW ({power_hp:.1f} HP)")
    
    # 4. Eficiencia térmica / Thermal efficiency
    print("\n4. Eficiencia Térmica / Thermal Efficiency\n")
    
    # Eficiencia = Potencia útil / Energía combustible
    # Efficiency = Useful power / Fuel energy
    
    fuel_energy_rate = 100  # kW (energía del combustible / fuel energy)
    useful_power = 35  # kW (potencia útil / useful power)
    efficiency = (useful_power / fuel_energy_rate) * 100
    
    print(f"   Energía combustible / Fuel energy: {fuel_energy_rate} kW")
    print(f"   Potencia útil / Useful power: {useful_power} kW")
    print(f"   Eficiencia / Efficiency: {efficiency:.1f}%")
    print(f"   → Motor típico de gasolina / Typical gasoline engine: ~35%")
    print(f"   → Motor diesel / Diesel engine: ~40-45%")
    
    print("\n✅ Nivel 3 completado / Level 3 completed!")
    print("   Ahora puedes energetizar tus engranajes y crear máquinas vivientes.")
    print("   Now you can energize your gears and create living machines.")


if __name__ == "__main__":
    main()
