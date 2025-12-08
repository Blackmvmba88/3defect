#!/usr/bin/env python3
"""
Ejemplo de integración de los 7 niveles / Integration example of all 7 levels

Demuestra cómo todos los niveles trabajan juntos en un sistema completo.
Demonstrates how all levels work together in a complete system.
"""

import sys


def main():
    print("="*80)
    print(" 3defect: DEMOSTRACIÓN DE ARQUITECTURA DE 7 NIVELES")
    print(" 3defect: 7-LEVEL ARCHITECTURE DEMONSTRATION")
    print("="*80)
    print()
    
    # NIVEL 1: GEOMETRÍA / LEVEL 1: GEOMETRY
    print("🔽 NIVEL 1 — GEOMETRÍA / LEVEL 1 — GEOMETRY")
    print("-" * 80)
    
    from defect3d import Cube, Sphere, Cylinder
    
    cube = Cube(size=1.0)
    sphere = Sphere(radius=0.5)
    cylinder = Cylinder(radius=0.3, height=2.0)
    print(f"✓ Creadas formas básicas / Created basic shapes")
    print(f"  • Cubo / Cube: size=1.0")
    print(f"  • Esfera / Sphere: radius=0.5")
    print(f"  • Cilindro / Cylinder: radius=0.3, height=2.0")
    print()
    
    # NIVEL 2: MECANISMOS DE RELOJ / LEVEL 2: CLOCK MECHANISMS
    print("🔽 NIVEL 2 — MECANISMOS DE RELOJ / LEVEL 2 — CLOCK MECHANISMS")
    print("-" * 80)
    
    from defect3d.clock_mechanisms import Gear, Pendulum, Spring, GearTrain
    
    # Crear tren de engranajes / Create gear train
    transmission = GearTrain(name="vehicle_transmission")
    transmission.add_gear(Gear(teeth=40, module=0.5))
    transmission.add_gear(Gear(teeth=20, module=0.5))
    
    # Crear péndulo para regulación / Create pendulum for regulation
    regulator = Pendulum(length=0.248, mass=0.5)
    
    # Crear resorte para suspensión / Create spring for suspension
    suspension = Spring(coils=8, stiffness=10000.0)
    
    print(f"✓ Creados mecanismos de relojería / Created clock mechanisms")
    print(f"  • Transmisión con ratio / Transmission with ratio: {transmission.total_ratio():.2f}:1")
    print(f"  • Péndulo con período / Pendulum with period: {regulator.period:.3f} s")
    print(f"  • Resorte suspensión / Suspension spring: {suspension.stiffness} N/m")
    print()
    
    # NIVEL 3: MOTORES / LEVEL 3: ENGINES
    print("🔽 NIVEL 3 — MOTORES / LEVEL 3 — ENGINES")
    print("-" * 80)
    
    from defect3d import Engine
    
    engine = Engine(cylinders=6)
    engine_rpm = 3000
    wheel_rpm = transmission.output_speed(engine_rpm)
    
    print(f"✓ Motor creado y conectado / Engine created and connected")
    print(f"  • Motor de / Engine with: {engine.cylinders} cilindros (~{engine.cylinders*50} HP)")
    print(f"  • Velocidad motor / Engine speed: {engine_rpm} RPM")
    print(f"  • Velocidad ruedas / Wheel speed: {wheel_rpm:.1f} RPM (vía transmisión)")
    print()
    
    # NIVEL 4: VEHÍCULOS / LEVEL 4: VEHICLES
    print("🔽 NIVEL 4 — VEHÍCULOS / LEVEL 4 — VEHICLES")
    print("-" * 80)
    
    from defect3d import Car, Motorcycle
    
    sports_car = Car(car_type="sports", color=(0.9, 0.1, 0.1))
    sport_bike = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))
    
    car_specs = sports_car.get_specifications()
    bike_specs = sport_bike.get_specifications()
    
    print(f"✓ Vehículos completos ensamblados / Complete vehicles assembled")
    print(f"  • Coche deportivo / Sports car:")
    car_engine = car_specs.get('motor', car_specs.get('engine', {}))
    print(f"    Motor: {car_engine.get('cilindros', car_engine.get('cylinders', 0))} cilindros, "
          f"{car_engine.get('potencia', car_engine.get('power', 0))} HP")
    
    print(f"  • Moto deportiva / Sport bike:")
    bike_engine = bike_specs.get('motor', bike_specs.get('engine', {}))
    print(f"    Motor: {bike_engine.get('cilindros', bike_engine.get('cylinders', 0))} cilindros, "
          f"{bike_engine.get('potencia', bike_engine.get('power', 0))} HP")
    print()
    
    # NIVEL 5: SIMULACIÓN / LEVEL 5: SIMULATION
    print("🔽 NIVEL 5 — SIMULACIÓN / LEVEL 5 — SIMULATION")
    print("-" * 80)
    
    from defect3d.physics import PhysicsSimulator
    
    # Simular coche acelerando / Simulate car accelerating
    sim = PhysicsSimulator(gravity=(0, 0, -9.81))
    sim.add_object(sports_car, mass=1200, velocity=(0, 0, 0))
    sim.apply_force(0, (6000, 0, 0))  # Fuerza del motor / Engine force
    
    states = sim.simulate(duration=3.0)
    
    final_state = states[-1]["objects"][0]
    final_velocity_kmh = final_state["velocity"][0] * 3.6
    final_position = final_state["position"][0]
    
    print(f"✓ Simulación física completa / Physics simulation complete")
    print(f"  • Duración / Duration: 3.0 segundos / seconds")
    print(f"  • Velocidad final / Final velocity: {final_velocity_kmh:.1f} km/h")
    print(f"  • Distancia recorrida / Distance traveled: {final_position:.1f} m")
    print(f"  • Aceleración / Acceleration: {6000/1200:.2f} m/s²")
    print()
    
    # NIVEL 6: EXPORTACIÓN ARTÍSTICA / LEVEL 6: ARTISTIC EXPORT
    print("🔽 NIVEL 6 — EXPORTACIÓN ARTÍSTICA / LEVEL 6 — ARTISTIC EXPORT")
    print("-" * 80)
    
    from defect3d.blender_integration import export_to_blender
    from defect3d.core.serializer import to_json
    
    # Exportar a Blender / Export to Blender
    export_to_blender(sports_car, "demo_sports_car.py")
    export_to_blender(sport_bike, "demo_sport_bike.py")
    
    # Exportar a JSON / Export to JSON
    json_data = to_json(sports_car)
    
    print(f"✓ Vehículos exportados / Vehicles exported")
    print(f"  • Blender Python: demo_sports_car.py, demo_sport_bike.py")
    print(f"  • JSON: Datos estructurados disponibles / Structured data available")
    print(f"  • Para renderizar / To render: BlenderRenderer().render(...)")
    print()
    
    # NIVEL 7: EVOLUCIÓN / LEVEL 7: EVOLUTION
    print("🔽 NIVEL 7 — EVOLUCIÓN / LEVEL 7 — EVOLUTION")
    print("-" * 80)
    
    from defect3d.evolutionary import ClockOptimizer
    
    # Optimizar péndulo para precisión / Optimize pendulum for precision
    def create_pendulum(length, mass):
        return Pendulum(length=length, mass=mass)
    
    print(f"  Optimizando péndulo para período de 1 segundo...")
    print(f"  Optimizing pendulum for 1 second period...")
    
    best_pendulum, best_fitness, history = ClockOptimizer.optimize_for_precision(
        clock_creator=create_pendulum,
        target_period=1.0,
        generations=20
    )
    
    improvement = ((history[-1] - history[0]) / history[0]) * 100 if history[0] > 0 else 0
    
    print(f"✓ Optimización evolutiva completa / Evolutionary optimization complete")
    print(f"  • Generaciones / Generations: 20")
    print(f"  • Longitud óptima / Optimal length: {best_pendulum.length:.3f} m")
    print(f"  • Período / Period: {best_pendulum.period:.4f} s")
    print(f"  • Error / Error: {abs(best_pendulum.period - 1.0)*1000:.2f} ms")
    print(f"  • Mejora / Improvement: {improvement:.1f}%")
    print()
    
    # RESUMEN FINAL / FINAL SUMMARY
    print("="*80)
    print(" RESUMEN DE INTEGRACIÓN / INTEGRATION SUMMARY")
    print("="*80)
    print()
    print("✅ Los 7 niveles trabajando juntos / All 7 levels working together:")
    print()
    print("   1️⃣  Geometría define formas básicas / Geometry defines basic shapes")
    print("   2️⃣  Mecanismos transmiten movimiento / Mechanisms transmit motion")
    print("   3️⃣  Motores generan potencia / Engines generate power")
    print("   4️⃣  Vehículos integran todo / Vehicles integrate everything")
    print("   5️⃣  Simulación valida física / Simulation validates physics")
    print("   6️⃣  Exportación crea arte / Export creates art")
    print("   7️⃣  Evolución optimiza diseño / Evolution optimizes design")
    print()
    print("="*80)
    print()
    print("🌟 Ecosistema Fractal Completo / Complete Fractal Ecosystem")
    print()
    print("   pequeño reloj → gran motor → movilidad → universo")
    print("   small clock → big engine → mobility → universe")
    print()
    print("   'La relojería es el ADN de la movilidad'")
    print("   'Clockwork is the DNA of mobility'")
    print()
    print("="*80)
    print()
    print("Para explorar cada nivel / To explore each level:")
    print("  • python 01_geometry/example_basic.py")
    print("  • python 02_clock_mechanisms/example_basic.py")
    print("  • python 03_engines/example_basic.py")
    print("  • python 04_vehicles/example_basic.py")
    print("  • python 05_physics_sim/example_basic.py")
    print("  • python 06_blender_visualization/example_basic.py")
    print("  • python 07_evolutionary_design/example_basic.py")
    print()
    print("Ver documentación completa / See complete documentation:")
    print("  • 7_LEVEL_ARCHITECTURE.md")
    print()


if __name__ == "__main__":
    main()
