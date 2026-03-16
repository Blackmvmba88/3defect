#!/usr/bin/env python3
"""
Ejemplo básico de vehículos / Basic vehicles example

Demuestra la creación de vehículos completos.
Demonstrates creation of complete vehicles.
"""

from defect3d import Car, Motorcycle


def main():
    print("=== NIVEL 4: VEHÍCULOS / LEVEL 4: VEHICLES ===\n")

    # 1. Crear diferentes tipos de automóviles / Create different car types
    print("1. Automóviles / Cars\n")

    cars = [
        Car(car_type="sedan", color=(0.3, 0.3, 0.8)),
        Car(car_type="sports", color=(0.9, 0.1, 0.1)),
        Car(car_type="suv", color=(0.2, 0.5, 0.2)),
    ]

    for car in cars:
        specs = car.get_specifications()

        # Manejar tanto español como inglés / Handle both Spanish and English
        car_type = specs.get('tipo', specs.get('type', 'unknown'))
        dims = specs.get('dimensiones', specs.get('dimensions', {}))
        engine = specs.get('motor', specs.get('engine', {}))

        length = dims.get('longitud', dims.get('length', 0))
        power = engine.get('potencia', engine.get('power', 0))
        cyls = engine.get('cilindros', engine.get('cylinders', 0))

        print(f"   {car_type.upper()}:")
        print(f"     Longitud / Length: {length} m")
        print(f"     Motor / Engine: {cyls} cilindros, {power} HP")
        print()

    # 2. Crear diferentes tipos de motocicletas / Create different motorcycle types
    print("2. Motocicletas / Motorcycles\n")

    bikes = [
        Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9)),
        Motorcycle(bike_type="cruiser", color=(0.1, 0.1, 0.1)),
        Motorcycle(bike_type="touring", color=(0.6, 0.2, 0.2)),
    ]

    for bike in bikes:
        specs = bike.get_specifications()

        bike_type = specs.get('tipo', specs.get('type', 'unknown'))
        engine = specs.get('motor', specs.get('engine', {}))

        power = engine.get('potencia', engine.get('power', 0))
        cyls = engine.get('cilindros', engine.get('cylinders', 0))

        print(f"   {bike_type.upper()}:")
        print(f"     Motor / Engine: {cyls} cilindros, {power} HP")
        print()

    # 3. Jerarquía de componentes / Component hierarchy
    print("3. Componentes del Vehículo / Vehicle Components\n")

    from defect3d import Chassis, Wheel, Engine

    print("   Construyendo vehículo desde componentes...")
    print("   Building vehicle from components...\n")

    # Chasis / Chassis
    chasis = Chassis(length=4.5, width=1.8, height=0.3)
    print(f"   ✓ Chasis / Chassis: {4.5}m × {1.8}m")

    # Motor / Engine
    motor = Engine(cylinders=4)
    print(f"   ✓ Motor / Engine: {motor.cylinders} cilindros")

    # Ruedas / Wheels
    ruedas = [Wheel(radius=0.35, width=0.25) for _ in range(4)]
    print(f"   ✓ Ruedas / Wheels: 4× (radio/radius=0.35m)")

    print("\n   → Vehículo completo ensamblado / Complete vehicle assembled")

    # 4. Simulación simple / Simple simulation
    print("\n4. Simulación de Movimiento / Movement Simulation\n")

    coche = Car(car_type="sports")

    # Simular aceleración / Simulate acceleration
    posicion = [0, 0, 0]
    velocidad = 0  # m/s
    aceleracion = 4  # m/s² (deportivo típico / typical sports car)

    print(f"   Coche deportivo acelerando / Sports car accelerating:")
    print(f"   Aceleración / Acceleration: {aceleracion} m/s²\n")
    print(f"   Tiempo (s) | Velocidad (km/h) | Posición (m)")
    print(f"   Time       | Speed            | Position")
    print(f"   " + "-"*48)

    for t in range(0, 11, 2):
        velocidad = aceleracion * t
        velocidad_kmh = velocidad * 3.6
        posicion[0] = 0.5 * aceleracion * t**2
        print(f"   {t:10d} | {velocidad_kmh:16.1f} | {posicion[0]:12.1f}")

    print("\n✅ Nivel 4 completado / Level 4 completed!")
    print("   Ya no solo mueves un engrane: mueves un mundo compuesto.")
    print("   You no longer just move a gear: you move a composite world.")


if __name__ == "__main__":
    main()
