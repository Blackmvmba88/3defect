#!/usr/bin/env python3
"""
Ejemplo básico de simulación física / Basic physics simulation example

Demuestra la simulación física de objetos y vehículos.
Demonstrates physics simulation of objects and vehicles.
"""

from defect3d import Car, Cube
from defect3d.physics import PhysicsSimulator


def main():
    print("=== NIVEL 5: SIMULACIÓN FÍSICA / LEVEL 5: PHYSICS SIMULATION ===\n")

    # 1. Simulación de caída libre / Free fall simulation
    print("1. Caída Libre / Free Fall\n")

    cubo = Cube(size=1.0, position=(0, 0, 10))

    sim = PhysicsSimulator(gravity=9.81)
    sim.add_object(cubo, mass=100, velocity=(0, 0, 0))

    print(f"   Objeto: cubo de 100 kg a 10m de altura")
    print(f"   Object: 100 kg cube at 10m height")
    print(f"   Gravedad / Gravity: {sim.gravity} m/s²\n")

    # Simular 1.5 segundos / Simulate 1.5 seconds
    states = sim.simulate(duration=1.5, dt=0.1)

    print(f"   t (s) | Altura (m) | Velocidad (m/s) | E_cinética (J) | E_potencial (J)")
    print(f"   " + "-"*75)

    for i, state in enumerate(states[::5]):  # Cada 0.5 segundos
        t = i * 0.5
        obj = state["objects"][0]
        z = obj["position"][2]
        vz = obj["velocity"][2]
        ek = obj["kinetic_energy"]
        ep = obj["potential_energy"]

        print(f"   {t:5.1f} | {z:10.2f} | {abs(vz):15.2f} | {ek:14.1f} | {ep:15.1f}")

    # 2. Vehículo acelerando / Vehicle accelerating
    print("\n2. Vehículo Acelerando / Vehicle Accelerating\n")

    coche = Car(car_type="sports")

    sim2 = PhysicsSimulator(gravity=9.81)
    sim2.add_object(coche, mass=1200, velocity=(0, 0, 0))

    # Aplicar fuerza del motor / Apply engine force
    engine_force = 6000  # N
    sim2.apply_force(0, (engine_force, 0, 0))

    print(f"   Coche deportivo / Sports car: 1200 kg")
    print(f"   Fuerza del motor / Engine force: {engine_force} N")
    print(f"   Aceleración esperada / Expected acceleration: {engine_force/1200:.2f} m/s²\n")

    states2 = sim2.simulate(duration=5.0, dt=0.1)

    print(f"   t (s) | Posición (m) | Velocidad (km/h)")
    print(f"   " + "-"*42)

    for i, state in enumerate(states2[::10]):  # Cada segundo
        t = i * 1.0
        obj = state["objects"][0]
        x = obj["position"][0]
        vx = obj["velocity"][0]
        vx_kmh = vx * 3.6

        print(f"   {t:5.1f} | {x:12.1f} | {vx_kmh:16.1f}")

    # 3. Conservación de energía / Energy conservation
    print("\n3. Conservación de Energía / Energy Conservation\n")

    # Volver a la simulación de caída / Back to fall simulation
    inicial = states[0]["objects"][0]
    final = states[-1]["objects"][0]

    E_inicial = inicial["kinetic_energy"] + inicial["potential_energy"]
    E_final = final["kinetic_energy"] + final["potential_energy"]
    diferencia = abs(E_final - E_inicial)

    print(f"   Energía inicial / Initial energy: {E_inicial:.2f} J")
    print(f"   Energía final / Final energy: {E_final:.2f} J")
    print(f"   Diferencia / Difference: {diferencia:.2f} J")
    print(f"   Conservación / Conservation: {(1 - diferencia/E_inicial)*100:.2f}%")
    print(f"\n   → La energía se conserva (pequeña diferencia = error numérico)")
    print(f"   → Energy is conserved (small difference = numerical error)")

    # 4. Comparar diferentes gravedades / Compare different gravities
    print("\n4. Diferentes Gravedades / Different Gravities\n")

    gravities = [
        ("Tierra / Earth", 9.81),
        ("Luna / Moon", 1.62),
        ("Marte / Mars", 3.71),
        ("Júpiter / Jupiter", 24.79),
    ]

    print(f"   Cuerpo    | Gravedad (m/s²) | Velocidad final (m/s)")
    print(f"   Body      | Gravity         | Final velocity")
    print(f"   " + "-"*56)

    for name, g in gravities:
        sim_g = PhysicsSimulator(gravity=g)
        sim_g.add_object(Cube(size=1.0, position=(0, 0, 10)),
                        mass=100, velocity=(0, 0, 0))

        states_g = sim_g.simulate(duration=1.5, dt=0.1)
        final_velocity = abs(states_g[-1]["objects"][0]["velocity"][2])

        print(f"   {name:10s} | {g:15.2f} | {final_velocity:20.2f}")

    print("\n✅ Nivel 5 completado / Level 5 completed!")
    print("   Tu ecosistema cuenta historias físicas creíbles.")
    print("   Your ecosystem tells believable physical stories.")


if __name__ == "__main__":
    main()
