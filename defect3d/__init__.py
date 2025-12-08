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
]
