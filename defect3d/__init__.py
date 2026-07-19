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


def _check_module(module_path: str) -> bool:
    """Intenta importar un sub-módulo y devuelve True si tiene éxito.

    Tries to import a sub-module and returns True on success.
    """
    import importlib
    try:
        importlib.import_module(module_path)
        return True
    except Exception:  # noqa: BLE001
        return False


def describe():
    """Imprime una descripción completa y dinámica del programa en español e inglés.

    Prints a full bilingual (Spanish/English) description of the program,
    including a live status check of each sub-module.
    """
    # --- live module status -------------------------------------------
    _modules = [
        ("defect3d.core",               "Nivel 1  Geometría      / Level 1  Geometry"),
        ("defect3d.clock_mechanisms",   "Nivel 2  Mecanismos     / Level 2  Mechanisms"),
        ("defect3d.mechanics",          "Nivel 3  Motores        / Level 3  Engines"),
        ("defect3d.vehicles",           "Nivel 4  Vehículos      / Level 4  Vehicles"),
        ("defect3d.physics",            "Nivel 5  Simulación     / Level 5  Simulation"),
        ("defect3d.blender_integration","Nivel 6  Exportación    / Level 6  Artistic Export"),
        ("defect3d.evolutionary",       "Nivel 7  Evolución      / Level 7  Evolution"),
    ]
    status_lines = "\n".join(
        f"  {'✓' if _check_module(mod) else '✗'} {label}"
        for mod, label in _modules
    )

    # --- optional dependency status -----------------------------------
    _deps = [("numpy", "numpy"), ("scipy", "scipy"), ("mathutils", "mathutils (Blender)")]
    dep_lines = "\n".join(
        f"  {'✓' if _check_module(dep) else '✗  (opcional / optional)'} {label}"
        for dep, label in _deps
    )

    info = f"""
{'='*62}
  3defect — Sistema de Modelado 3D  /  3D Modeling System
  Versión / Version: {__version__}
{'='*62}

¿QUÉ ES ESTE PROGRAMA? / WHAT IS THIS PROGRAM?
-----------------------------------------------
3defect es un sistema Python de modelado 3D escalable de 7 niveles
diseñado para crear vehículos y sistemas mecánicos con integración
directa con Blender.

3defect is a 7-level scalable Python 3D modeling system designed to
create vehicles and mechanical systems with direct Blender integration.

ESTADO DE MÓDULOS / MODULE STATUS:
{status_lines}

DEPENDENCIAS / DEPENDENCIES:
{dep_lines}

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

LÍNEA DE COMANDOS / COMMAND LINE:
  python -m defect3d              → esta pantalla / this screen
  python -m defect3d --version    → sólo la versión / version only
  python -m defect3d --list       → lista de clases disponibles / available classes

DOCUMENTACIÓN / DOCUMENTATION:
  README.md, README_ES.md, docs/

{'='*62}
"""
    print(info)
