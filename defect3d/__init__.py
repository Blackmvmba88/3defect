"""
3defect - A 7-Level Scalable 3D Modeling System

Un sistema escalable de 7 niveles para crear vehículos y sistemas mecánicos.
A 7-level scalable system for creating vehicles and mechanical systems.

NIVEL 1 — GEOMETRÍA / LEVEL 1 — GEOMETRY:
  Formas básicas: Cube, Sphere, Cylinder, Cone, Torus

NIVEL 2 — MECANISMOS DE RELOJ / LEVEL 2 — CLOCK MECHANISMS:
  Engranajes, escape, péndulo, resortes, trenes de engranajes
  Gears, escapement, pendulum, springs, gear trains

NIVEL 3 — MOTORES / LEVEL 3 — ENGINES:
  Motores de combustión interna
  Internal combustion engines

NIVEL 4 — VEHÍCULOS / LEVEL 4 — VEHICLES:
  Automóviles y motocicletas completos
  Complete cars and motorcycles

NIVEL 5 — SIMULACIÓN / LEVEL 5 — SIMULATION:
  Física realista: gravedad, fuerzas, energía
  Realistic physics: gravity, forces, energy

NIVEL 6 — EXPORTACIÓN ARTÍSTICA / LEVEL 6 — ARTISTIC EXPORT:
  Blender integration y renderizado fotorrealista
  Blender integration and photorealistic rendering

NIVEL 7 — EVOLUCIÓN / LEVEL 7 — EVOLUTION:
  Optimización automática mediante algoritmos evolutivos
  Automatic optimization using evolutionary algorithms
"""

__version__ = "0.2.0"

# NIVEL 1: Geometría / Level 1: Geometry
from .core.shapes import Cube, Sphere, Cylinder, Cone, Torus
from .core.composite import CompositePart

# NIVEL 2: Mecanismos de Reloj / Level 2: Clock Mechanisms
from .clock_mechanisms import Gear, Escapement, Pendulum, Spring, GearTrain

# NIVEL 3: Motores / Level 3: Engines
# NIVEL 4: Vehículos / Level 4: Vehicles
from .vehicles.car import Car
from .vehicles.motorcycle import Motorcycle
from .mechanics import Wheel, Engine, Chassis, Body

# NIVEL 5: Simulación / Level 5: Simulation
# Available in defect3d.physics.PhysicsSimulator

# NIVEL 6: Exportación Artística / Level 6: Artistic Export
# Available in defect3d.blender_integration

# NIVEL 7: Evolución / Level 7: Evolution
# Available in defect3d.evolutionary

__all__ = [
    # Nivel 1 / Level 1
    'Cube', 'Sphere', 'Cylinder', 'Cone', 'Torus',
    'CompositePart',
    # Nivel 2 / Level 2
    'Gear', 'Escapement', 'Pendulum', 'Spring', 'GearTrain',
    # Nivel 3 & 4 / Level 3 & 4
    'Car', 'Motorcycle',
    'Wheel', 'Engine', 'Chassis', 'Body',
    # Utilidades / Utilities
    'describe',
]


def describe():
    """Imprime una descripción completa del programa en español e inglés.

    Prints a full bilingual (Spanish/English) description of the program.
    """
    info = f"""
{'='*60}
  3defect — Sistema de Modelado 3D  /  3D Modeling System
  Versión / Version: {__version__}
{'='*60}

¿QUÉ ES ESTE PROGRAMA? / WHAT IS THIS PROGRAM?
-----------------------------------------------
3defect es un sistema Python de modelado 3D escalable de 7 niveles
diseñado para crear vehículos y sistemas mecánicos con integración
directa con Blender.

3defect is a 7-level scalable Python 3D modeling system designed to
create vehicles and mechanical systems with direct Blender integration.

NIVELES / LEVELS:
  Nivel 1 — Geometría      : Formas básicas (Cubo, Esfera, Cilindro, Cono, Toroide)
  Level 1 — Geometry       : Basic shapes (Cube, Sphere, Cylinder, Cone, Torus)

  Nivel 2 — Mecanismos     : Engranajes, escape, péndulo, resortes
  Level 2 — Mechanisms     : Gears, escapement, pendulum, springs

  Nivel 3 — Motores        : Motores de combustión interna
  Level 3 — Engines        : Internal combustion engines

  Nivel 4 — Vehículos      : Automóviles y motocicletas completos
  Level 4 — Vehicles       : Complete cars and motorcycles

  Nivel 5 — Simulación     : Física realista (gravedad, fuerzas, energía)
  Level 5 — Simulation     : Realistic physics (gravity, forces, energy)

  Nivel 6 — Exportación    : Integración con Blender, renderizado fotorrealista
  Level 6 — Artistic Export: Blender integration, photorealistic rendering

  Nivel 7 — Evolución      : Optimización automática con algoritmos evolutivos
  Level 7 — Evolution      : Automatic optimization using evolutionary algorithms

CARACTERÍSTICAS PRINCIPALES / KEY FEATURES:
  ✓ Formas 3D primitivas / 3D primitive shapes
  ✓ Partes compuestas jerárquicas / Hierarchical composite parts
  ✓ Coches y motocicletas pre-construidos / Pre-built cars and motorcycles
  ✓ Simulación física newtoniana / Newtonian physics simulation
  ✓ Exportación a Blender / Blender export
  ✓ Detección automática de idioma / Automatic language detection
  ✓ Optimización evolutiva / Evolutionary optimization

USO RÁPIDO / QUICK START:
  from defect3d import Car
  coche = Car(car_type="sports", color=(0.9, 0.1, 0.1))
  specs = coche.get_specifications()

  from defect3d import Motorcycle
  moto = Motorcycle(bike_type="sport")
  moto.simulate_movement(distance=10.0)

DOCUMENTACIÓN / DOCUMENTATION:
  README.md, README_ES.md, docs/

{'='*60}
"""
    print(info)
