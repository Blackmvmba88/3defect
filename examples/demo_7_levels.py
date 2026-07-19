#!/usr/bin/env python3
"""
Demo de 7 Niveles / 7-Level Demo

Demostración completa del sistema 3defect que muestra todos los niveles,
desde geometría básica hasta optimización evolutiva.

Complete demonstration of the 3defect system showing all levels,
from basic geometry to evolutionary optimization.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d import (
    Cube, Sphere, Cylinder, Cone, Torus, CompositePart,
    Gear, Escapement, Pendulum, Spring, GearTrain,
    Car, Motorcycle,
    Wheel, Engine, Chassis,
)
from defect3d.physics import PhysicsSimulator
from defect3d.blender_integration import export_to_blender
from defect3d.evolutionary import ClockOptimizer


def _get_vehicle_length_and_power(specs):
    """Extract length and power from a bilingual vehicle spec dict."""
    dims = specs.get('dimensions', specs.get('dimensiones', {}))
    length = dims.get('length', dims.get('longitud', 0))
    engine = specs.get('engine', specs.get('motor', {}))
    power = engine.get('power', engine.get('potencia', 0))
    return length, power


def demo_nivel_1():
    """NIVEL 1: Geometría / LEVEL 1: Geometry"""
    print("\n" + "=" * 60)
    print("NIVEL 1 — GEOMETRÍA / LEVEL 1 — GEOMETRY")
    print("=" * 60)

    cubo = Cube(size=2.0, position=(0, 0, 0))
    cubo.set_color(0.8, 0.2, 0.2, 1.0)

    esfera = Sphere(radius=1.5, position=(3, 0, 0))
    esfera.set_color(0.2, 0.8, 0.2, 1.0)

    cilindro = Cylinder(radius=1.0, height=3.0, position=(6, 0, 0))
    cilindro.set_color(0.2, 0.2, 0.8, 1.0)

    cono = Cone(radius=1.0, height=2.5, position=(9, 0, 0))
    cono.set_color(0.8, 0.8, 0.2, 1.0)

    toro = Torus(major_radius=1.5, minor_radius=0.5, position=(12, 0, 0))
    toro.set_color(0.8, 0.2, 0.8, 1.0)

    print(f"  Cubo    / Cube:     volume={cubo.volume():.2f} m³")
    print(f"  Esfera  / Sphere:   volume={esfera.volume():.2f} m³")
    print(f"  Cilindro/ Cylinder: volume={cilindro.volume():.2f} m³")
    print(f"  Cono    / Cone:     volume={cono.volume():.2f} m³")
    print(f"  Toro    / Torus:    volume={toro.volume():.2f} m³")

    pieza = CompositePart(name="ensamblaje_demo")
    pieza.add_part(cubo)
    pieza.add_part(esfera)
    print(f"\n  Pieza compuesta / Composite part: {len(pieza.parts)} shapes")
    print("  ✅ Nivel 1 completado / Level 1 complete")


def demo_nivel_2():
    """NIVEL 2: Mecanismos de Reloj / LEVEL 2: Clock Mechanisms"""
    print("\n" + "=" * 60)
    print("NIVEL 2 — MECANISMOS DE RELOJ / LEVEL 2 — CLOCK MECHANISMS")
    print("=" * 60)

    # Engranajes / Gears
    engranaje_grande = Gear(teeth=60, module=1.0, position=(0, 0, 0))
    engranaje_pequeno = Gear(teeth=20, module=1.0, position=(4, 0, 0))
    ratio = engranaje_grande.gear_ratio(engranaje_pequeno)
    print(f"  Engranaje / Gear: {engranaje_grande.teeth}T → {engranaje_pequeno.teeth}T, "
          f"ratio={ratio:.2f}")

    # Tren de engranajes / Gear train
    tren = GearTrain(name="transmision")
    tren.add_gear(Gear(teeth=60))
    tren.add_gear(Gear(teeth=30))
    tren.add_gear(Gear(teeth=15))
    print(f"  Tren de engranajes / Gear train: ratio total = {tren.total_ratio():.2f}")
    print(f"  100 RPM entrada → {tren.output_speed(100):.1f} RPM salida/output")

    # Péndulo / Pendulum
    pendulo = Pendulum(length=0.994, mass=0.5)
    print(f"  Péndulo / Pendulum: L={pendulo.length:.3f}m, "
          f"T={pendulo.period:.4f}s")

    # Resorte / Spring
    resorte = Spring(coils=10, stiffness=150.0)
    print(f"  Resorte / Spring: stiffness={resorte.stiffness} N/m, "
          f"energia(5cm)={resorte.energy(0.05):.3f} J")

    # Escape / Escapement
    escape = Escapement(frequency=1.0)
    print(f"  Escape / Escapement: {escape.frequency} Hz, "
          f"período/period={escape.period:.2f}s")

    print("  ✅ Nivel 2 completado / Level 2 complete")


def demo_nivel_3():
    """NIVEL 3: Motores / LEVEL 3: Engines"""
    print("\n" + "=" * 60)
    print("NIVEL 3 — MOTORES / LEVEL 3 — ENGINES")
    print("=" * 60)

    for cylinders in [2, 4, 6, 8]:
        motor = Engine(cylinders=cylinders)
        power = motor.get_property("power", cylinders * 50)
        print(f"  Motor {cylinders} cil. / Engine {cylinders} cyl.: ~{power} HP")

    # Motor + transmisión / Engine + transmission
    motor = Engine(cylinders=4)
    tren = GearTrain(name="transmision")
    tren.add_gear(Gear(teeth=20, module=0.5))
    tren.add_gear(Gear(teeth=60, module=0.5))
    rpm_motor = 3000
    rpm_ruedas = tren.output_speed(rpm_motor)
    print(f"\n  Motor 4 cil. a {rpm_motor} RPM → ruedas/wheels: {rpm_ruedas:.0f} RPM "
          f"(ratio {tren.total_ratio():.1f}:1)")
    print("  ✅ Nivel 3 completado / Level 3 complete")


def demo_nivel_4():
    """NIVEL 4: Vehículos / LEVEL 4: Vehicles"""
    print("\n" + "=" * 60)
    print("NIVEL 4 — VEHÍCULOS / LEVEL 4 — VEHICLES")
    print("=" * 60)

    # Coches / Cars
    for car_type in ["sedan", "sports", "suv"]:
        coche = Car(car_type=car_type)
        length, power = _get_vehicle_length_and_power(coche.get_specifications())
        print(f"  {car_type.upper()} Car: {length:.2f}m long, {power} HP")

    # Motocicleta / Motorcycle
    moto = Motorcycle(bike_type="sport")
    length, power = _get_vehicle_length_and_power(moto.get_specifications())
    print(f"  SPORT Motorcycle: {length:.2f}m long, {power} HP")

    # Simular movimiento / Simulate movement
    coche = Car(car_type="sports", position=(0, 0, 0))
    coche.simulate_movement(distance=10.0, direction=(1, 0, 0))
    print(f"\n  Deportivo movido 10m / Sports car moved 10m → position: {coche.position}")
    print("  ✅ Nivel 4 completado / Level 4 complete")


def demo_nivel_5():
    """NIVEL 5: Simulación Física / LEVEL 5: Physics Simulation"""
    print("\n" + "=" * 60)
    print("NIVEL 5 — SIMULACIÓN FÍSICA / LEVEL 5 — PHYSICS SIMULATION")
    print("=" * 60)

    # Caída libre / Free fall
    esfera = Sphere(radius=0.5, position=(0, 0, 10))
    sim = PhysicsSimulator(gravity=(0, 0, -9.81))
    sim.add_object(esfera, mass=1.0, velocity=(0, 0, 0))

    altura_inicial = esfera.position[2]
    sim.simulate(duration=1.0, apply_gravity=True)
    altura_final = esfera.position[2]

    print(f"  Caída libre / Free fall: {altura_inicial:.1f}m → {altura_final:.2f}m "
          f"(caída / fell {altura_inicial - altura_final:.2f}m en/in 1s)")

    # Movimiento de coche / Car movement
    sim.reset()
    coche = Car(car_type="sedan", position=(0, 0, 0))
    sim.add_object(coche, mass=1500, velocity=(0, 0, 0))

    for _ in range(30):
        sim.apply_force(0, (5000, 0, 0))
        sim.step()

    velocidad = sim.objects[0]['velocity']
    rapidez = sum(v**2 for v in velocidad) ** 0.5
    ke = sim.get_kinetic_energy(0)

    print(f"  Coche / Car: rapidez/speed={rapidez:.2f} m/s "
          f"({rapidez * 3.6:.1f} km/h), KE={ke:.0f} J")
    print("  ✅ Nivel 5 completado / Level 5 complete")


def demo_nivel_6():
    """NIVEL 6: Exportación Artística / LEVEL 6: Artistic Export"""
    print("\n" + "=" * 60)
    print("NIVEL 6 — EXPORTACIÓN ARTÍSTICA / LEVEL 6 — ARTISTIC EXPORT")
    print("=" * 60)

    coche = Car(car_type="sports", color=(0.9, 0.1, 0.1))
    output_file = os.path.join(os.path.dirname(__file__), "demo_7_levels_export.py")
    export_to_blender(coche, output_file)

    print(f"  Script de Blender exportado / Blender script exported:")
    print(f"    → {output_file}")
    print("  Para visualizar / To visualize:")
    print("    1. Abrir Blender / Open Blender")
    print("    2. Scripting tab → Open file → Run (Alt+P)")
    print("  ✅ Nivel 6 completado / Level 6 complete")


def demo_nivel_7():
    """NIVEL 7: Evolución / LEVEL 7: Evolution"""
    print("\n" + "=" * 60)
    print("NIVEL 7 — EVOLUCIÓN / LEVEL 7 — EVOLUTION")
    print("=" * 60)

    print("  Optimizando péndulo para período de 1s...")
    print("  Optimizing pendulum for 1-second period...")

    def crear_pendulo(length, mass):
        return Pendulum(length=length, mass=mass)

    mejor, fitness, historial = ClockOptimizer.optimize_for_precision(
        clock_creator=crear_pendulo,
        target_period=1.0,
        generations=20
    )

    error_ms = abs(mejor.period - 1.0) * 1000
    print(f"\n  Resultado / Result:")
    print(f"    Longitud óptima / Optimal length: {mejor.length:.4f} m")
    print(f"    Período / Period: {mejor.period:.4f} s")
    print(f"    Error: {error_ms:.2f} ms")
    print(f"    Fitness: {fitness:.6f}")

    mejora_absoluta = historial[-1] - historial[0]
    print(f"    Mejora absoluta / Absolute improvement: {mejora_absoluta:+.6f}")
    print("  ✅ Nivel 7 completado / Level 7 complete")


def main():
    """Ejecutar demo completo de 7 niveles / Run complete 7-level demo"""
    print("\n" + "=" * 60)
    print("3DEFECT — DEMO COMPLETO 7 NIVELES / COMPLETE 7-LEVEL DEMO")
    print("Sistema Escalable de Modelado 3D / Scalable 3D Modeling System")
    print("=" * 60)

    demo_nivel_1()
    demo_nivel_2()
    demo_nivel_3()
    demo_nivel_4()
    demo_nivel_5()
    demo_nivel_6()
    demo_nivel_7()

    print("\n" + "=" * 60)
    print("¡DEMO COMPLETADO! / DEMO COMPLETE!")
    print("=" * 60)
    print("\n  Niveles demostrados / Levels demonstrated:")
    print("    1. Geometría básica / Basic geometry")
    print("    2. Mecanismos de reloj / Clock mechanisms")
    print("    3. Motores / Engines")
    print("    4. Vehículos / Vehicles")
    print("    5. Simulación física / Physics simulation")
    print("    6. Exportación artística (Blender) / Artistic export")
    print("    7. Optimización evolutiva / Evolutionary optimization")
    print("\n  ¡Diviértete creando! / Have fun creating! 🚗🏍️✨\n")


if __name__ == "__main__":
    main()
