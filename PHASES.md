# 3defect - Phase Implementation Guide

This document describes the phased architecture of the 3defect system, showing how each phase builds upon the previous one.

## 🌑 FASE 0 — FUNDACIÓN & ÓPERA CEREBRAL DEL SISTEMA

**Meta:** Tener un core sólido, entendible, modular, testeable.

### ✅ Implemented Features

#### Core Module Structure
- **`core/primitives.py`** (also `core/shapes.py` for compatibility): Base 3D shape primitives
  - `Cube`: Rectangular boxes with configurable size
  - `Sphere`: Spherical shapes with radius
  - `Cylinder`: Cylindrical shapes with radius and height
  - `Cone`: Conical shapes with base radius and height
  - `Torus`: Donut shapes (perfect for wheels)

#### Composite System
- **`core/composite.py`**: Factory + Composition pattern implementation
  - `CompositePart`: Build complex objects from simple shapes
  - Hierarchical parent-child structure
  - Connection definitions between parts
  - Custom properties system

#### Transformations
- **`core/transformations.py`**: Real transformations module
  - Translation matrices
  - Rotation matrices (X, Y, Z axes)
  - Scale matrices
  - Combined transformation operations
  - Point transformation utilities
  - Position interpolation

#### Serialization
- **`core/serializer.py`**: Universal JSON export (non-graphical)
  - Serialize individual shapes
  - Serialize composite parts (recursive)
  - Export to JSON files
  - Load from JSON files
  - Structured, human-readable format

### Examples
- `examples/json_serialization.py`: Demonstrates JSON export
- `examples/transformations_demo.py`: Demonstrates transformation utilities

### Testing
Create, modify, combine and serialize objects without Blender:
```python
from defect3d import Cube, Sphere
from defect3d.core.serializer import to_json

# Create objects
cube = Cube(size=2.0, position=(0, 0, 0))
sphere = Sphere(radius=1.5, position=(3, 0, 0))

# Modify
cube.translate(1, 0, 0)
cube.rotate(0, 0, 45)
cube.set_scale(2, 2, 2)

# Serialize
json_data = to_json([cube, sphere])
```

---

## 🌒 FASE 1 — ENSAMBLE Y MORFOLOGÍA

**Meta:** Unir piezas para formar objetos complejos.

### ✅ Implemented Features

#### Mechanical Components Library
- **`mechanics/wheels.py`**: Wheel assemblies
  - `Wheel`: Tire + rim composite with realistic proportions

- **`mechanics/engines.py`**: Engine components
  - `Engine`: Configurable cylinder count (2, 4, 6, 8, 12)
  - Realistic engine block and cylinder head geometry

- **`mechanics/frames.py`**: Structural components
  - `Chassis`: Frame with rails and body
  - `Body`: Vehicle body shells (sedan, sports, SUV styles)

#### Transformation System
All objects support:
- `translate(dx, dy, dz)`: Move objects
- `rotate(rx, ry, rz)`: Rotate in degrees
- `set_scale(sx, sy, sz)`: Scale transformations

#### Hierarchical System
- Parent-child relationships via `CompositePart`
- Nested composites (composites can contain composites)
- Relative positioning of parts

### Examples
- `examples/custom_vehicle.py`: Build custom vehicles from components

### Testing
Create a vehicle with properly aligned parts:
```python
from defect3d.mechanics import Wheel, Engine, Chassis

# Create components
chassis = Chassis(length=4.0, width=1.8, height=0.2)
engine = Engine(cylinders=6, position=(1.5, 0, 0.3))
wheel_fl = Wheel(radius=0.35, position=(1.5, 0.9, -0.2))
# ... add more wheels
```

---

## 🌓 FASE 2 — IDIOMA + AUTOMATIZACIÓN

**Meta:** Sistema usable sin programación complicada.

### ✅ Implemented Features

#### Language Detection System
- **`i18n/translator.py`**: Automatic language detection
  - Detects system language (Spanish/English)
  - Environment variable override: `DEFECT3D_LANG=es|en`
  - Bilingual messages and specifications

#### Semantic Presets
High-level vehicle creation:
```python
from defect3d import Car, Motorcycle

# Simple 3-line creation
car = Car(car_type="sedan", color=(0.8, 0.2, 0.2))
bike = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))
specs = car.get_specifications()  # Auto-translated
```

#### Vehicle Types
**Cars:**
- `sedan`: Family car (4.5m, 4 cylinders, 200 HP)
- `sports`: Performance car (4.2m, 6 cylinders, 300 HP)
- `suv`: Large vehicle (5.0m, 6 cylinders, 250 HP)

**Motorcycles:**
- `sport`: High-performance (4 cylinders, 180 HP)
- `cruiser`: Comfortable ride (2 cylinders, 80 HP)
- `touring`: Long-distance (4 cylinders, 120 HP)

#### Parameter Validation
- Type checking on vehicle parameters
- Sensible defaults for all values
- Clear error messages (bilingual)

### Examples
- `examples/create_car.py`: Simple car creation
- `examples/create_motorcycle.py`: Simple motorcycle creation
- `examples/ejemplo_español.py`: Full Spanish example

---

## 🌔 FASE 3 — EXPORTACIÓN VISUAL + BLENDER API

**Meta:** Ser visualizable y útil artísticamente.

### ✅ Implemented Features

#### Blender Integration
- **`blender_integration/exporter.py`**: Blender Python script generation
  - Export any object to Blender-executable Python
  - Automatic material setup
  - Camera and lighting configuration
  - JSON export option

#### Rendering System
- **`blender_integration/renderer.py`**: Photorealistic rendering
  - `BlenderRenderer.render()`: Generate high-quality images
  - Configurable resolution and samples
  - Material presets

#### Export Formats
- Blender Python scripts (.py)
- JSON data (.json)
- Support for nested composites

### Examples
- All vehicle examples include Blender export
- `examples/renderizar_llanta.py`: Render a wheel to image

### Testing
Export and visualize in Blender:
```python
from defect3d import Car
from defect3d.blender_integration import export_to_blender

car = Car(car_type="sports")
export_to_blender(car, "my_car.py")
# Open in Blender, run script (Alt+P)
```

---

## 🌕 FASE 4 — FÍSICA SIMBÓLICA & SIMULACIÓN

**Meta:** Comportamiento dinámico básico.

### ✅ Implemented Features

#### Physics Simulator
- **`physics/simulator.py`**: Newtonian mechanics
  - `PhysicsSimulator`: Multi-object physics engine
  - Gravity simulation (configurable, default Earth gravity)
  - Force application
  - Velocity and acceleration
  - Kinetic and potential energy calculations

#### Simulation Features
- Time-stepped simulation (~60 FPS)
- Multiple object support
- State history export
- Mass and velocity tracking

### Examples
- `examples/physics_simulation.py`: Complete physics demo

### Testing
Simulate movement and forces:
```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

car = Car(car_type="sedan")
sim = PhysicsSimulator()
sim.add_object(car, mass=1500, velocity=(10, 0, 0))
sim.apply_force(0, (5000, 0, 0))  # Driving force

states = sim.simulate(duration=2.0)
# Object moves, accelerates, physics calculated
```

---

## 🔥 FASE 5 — MOTOR ARTÍSTICO & RENDER PRO

**Meta:** Uso creativo real y showcase profesional.

### ✅ Implemented Features

#### Photorealistic Rendering
- **`BlenderRenderer`**: High-quality image generation
  - Configurable samples (quality)
  - Resolution control
  - Material setup
  - Lighting configuration

#### Material System
- Default materials in shape definitions
- Color/RGBA support
- Material properties in JSON export

### Examples
- `examples/renderizar_llanta.py`: Render wheel to image
- `examples/renderizar_llanta_auto.py`: Automated rendering

### Future Enhancements (Phase 5 Extensions)
- Extended material library (metal, plastic, rubber, glass, fiber)
- Advanced lighting presets
- Mini-gallery export system
- Post-processing effects

---

## 🧠 FASE 6 — IA GEOMÉTRICA (OPTIONAL FUTURE)

**Meta:** Sugerencias inteligentes.

### Future Vision
- Natural language vehicle generation
- Automatic dimensional correction
- Procedural generation
- Style transfer

---

## 📂 Current Directory Structure

```
3defect/
├── core/                      # FASE 0: Foundation
│   ├── primitives.py         # 3D shape primitives
│   ├── shapes.py             # (backward compatibility)
│   ├── transformations.py    # Transformation utilities
│   ├── composite.py          # Composition pattern
│   └── serializer.py         # JSON export
├── mechanics/                 # FASE 1: Assembly
│   ├── wheels.py             # Wheel components
│   ├── engines.py            # Engine components
│   └── frames.py             # Chassis and body components
├── vehicles/                  # FASE 2: Automation
│   ├── car.py                # Car presets
│   ├── motorcycle.py         # Motorcycle presets
│   └── components.py         # (backward compatibility)
├── i18n/                      # FASE 2: Language
│   └── translator.py         # Language detection
├── physics/                   # FASE 4: Physics
│   └── simulator.py          # Physics engine
├── blender_integration/       # FASE 3 & 5: Visualization
│   ├── exporter.py           # Blender export
│   └── renderer.py           # Photorealistic rendering
└── examples/                  # Usage demonstrations
```

---

## 🚦 Golden Rule

**"Si una función genera frustración, se demueve, documenta o simplifica."**

The system is designed to be:
- **Understandable**: Clear module separation
- **Testable**: Each phase can be tested independently
- **Modular**: Components can be used separately
- **Documented**: Comprehensive examples and docstrings
- **Frustration-free**: Simple APIs, sensible defaults

---

## Quick Start by Phase

### Phase 0: Create basic shapes
```python
from defect3d import Cube, Sphere, Cylinder
cube = Cube(size=2.0)
```

### Phase 1: Build assemblies
```python
from defect3d.mechanics import Wheel, Engine
wheel = Wheel(radius=0.4)
engine = Engine(cylinders=6)
```

### Phase 2: Use presets
```python
from defect3d import Car
car = Car(car_type="sports")
```

### Phase 3: Export to Blender
```python
from defect3d.blender_integration import export_to_blender
export_to_blender(car, "my_car.py")
```

### Phase 4: Simulate physics
```python
from defect3d.physics import PhysicsSimulator
sim = PhysicsSimulator()
sim.add_object(car, mass=1500)
states = sim.simulate(duration=2.0)
```

### Phase 5: Render images
```python
from defect3d.blender_integration import BlenderRenderer
renderer = BlenderRenderer()
renderer.render(car, "car.png", resolution=(1920, 1080))
```

---

**Made with ❤️ following a clear, phased architecture**
