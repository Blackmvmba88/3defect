# 🌟 Arquitectura de 7 Niveles / 7-Level Architecture

## 3defect: Sistema Mecánico Escalable y Educativo

**ES:** Un ecosistema fractal donde aprender un nivel te habilita el siguiente. Desde átomos geométricos hasta organismos que evolucionan.

**EN:** A fractal ecosystem where learning one level enables the next. From geometric atoms to evolving organisms.

---

## 📚 La Escalera / The Ladder

### 🔽 NIVEL 1 — GEOMETRÍA (átomos)

**Formas básicas que construyen todo / Basic shapes that build everything**

```python
from defect3d import Cube, Sphere, Cylinder, Cone, Torus

cubo = Cube(size=2.0)
esfera = Sphere(radius=1.5)
cilindro = Cylinder(radius=1.0, height=3.0)
```

**Capacidades / Capabilities:**
- 5 primitivas geométricas / 5 geometric primitives
- Volumen, masa, densidad / Volume, mass, density
- Transformaciones (translate, rotate, scale)
- Composición jerárquica / Hierarchical composition

**📂 Directorio / Directory:** `01_geometry/`
- `README.md` - Documentación completa / Complete documentation
- `example_basic.py` - Ejemplo básico / Basic example
- `example_physics.py` - Test físico / Physics test
- `example_blender.py` - Visualización / Visualization

---

### 🔽 NIVEL 2 — MECANISMOS DE RELOJ (mecánica fina)

**Relojería sistemática / Systematic watchmaking**

```python
from defect3d.clock_mechanisms import Gear, Pendulum, Spring, GearTrain

# Engranaje / Gear
gear = Gear(teeth=30, module=1.0)

# Péndulo / Pendulum  
pendulum = Pendulum(length=1.0, mass=0.5)

# Tren de engranajes / Gear train
train = GearTrain()
train.add_gear(Gear(teeth=60))
train.add_gear(Gear(teeth=30))
ratio = train.total_ratio()  # 2:1
```

**Capacidades / Capabilities:**
- Transmisión de movimiento / Movement transmission
- Precisión temporal / Time precision
- Relación de engranes / Gear ratios
- Torque fino / Fine torque
- Cinemática circular / Circular kinematics

**📂 Directorio / Directory:** `02_clock_mechanisms/`

---

### 🔽 NIVEL 3 — MOTORES (mecánica gruesa)

**Energía → Movimiento / Energy → Motion**

```python
from defect3d import Engine
from defect3d.clock_mechanisms import GearTrain

# Motor / Engine
motor = Engine(cylinders=6)  # 300 HP

# Transmisión / Transmission
transmission = GearTrain()
# ... conectar motor a ruedas / connect engine to wheels
```

**Capacidades / Capabilities:**
- Energía → movimiento / Energy → motion
- Torque alto / High torque
- Consumo y eficiencia / Consumption and efficiency
- Temperatura y materiales / Temperature and materials

**📂 Directorio / Directory:** `03_engines/`

---

### 🔽 NIVEL 4 — VEHÍCULOS (sistemas integrados)

**Mundo compuesto / Composite world**

```python
from defect3d import Car, Motorcycle

# Automóvil / Car
sedan = Car(car_type="sedan")
sports = Car(car_type="sports")
suv = Car(car_type="suv")

# Motocicleta / Motorcycle
sport_bike = Motorcycle(bike_type="sport")
cruiser = Motorcycle(bike_type="cruiser")
touring = Motorcycle(bike_type="touring")
```

**Componentes / Components:**
- Chasis / Chassis
- Ruedas / Wheels
- Suspensión / Suspension
- Dirección / Steering
- Motor integrado / Integrated engine
- Frenos / Brakes

**📂 Directorio / Directory:** `04_vehicles/`

---

### 🔽 NIVEL 5 — SIMULACIÓN (física emocional)

**Historias físicas creíbles / Believable physical stories**

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

sim = PhysicsSimulator(gravity=9.81)
sim.add_object(car, mass=1500, velocity=(10, 0, 0))
sim.apply_force(0, (5000, 0, 0))

states = sim.simulate(duration=2.0)
```

**Capacidades / Capabilities:**
- Gravedad / Gravity
- Colisiones / Collisions
- Fricción / Friction
- Aceleración / Acceleration
- Curvas de torque / Torque curves
- Resistencia del aire / Air resistance
- Estabilidad / Stability
- Carga estructural / Structural load

**📂 Directorio / Directory:** `05_physics_sim/`

---

### 🔽 NIVEL 6 — EXPORTACIÓN ARTÍSTICA (Blender + render)

**La mecánica se vuelve arte / Mechanics becomes art**

```python
from defect3d.blender_integration import export_to_blender, BlenderRenderer

# Exportar a Blender / Export to Blender
export_to_blender(car, "mi_coche.py")

# Renderizar / Render
renderer = BlenderRenderer()
renderer.render(car, "coche.png", resolution=(1920, 1080), samples=128)
```

**Capacidades / Capabilities:**
- Renderizarse / Be rendered
- Animarse / Be animated
- Documentarse / Be documented
- Convertirse en diseño técnico / Become technical design
- Presentarse como cine mecánico / Present as mechanical cinema

**📂 Directorio / Directory:** `06_blender_visualization/`

---

### 🔽 NIVEL 7 — EVOLUCIÓN

**Organismos que aprenden / Organisms that learn**

```python
from defect3d.evolutionary import ClockOptimizer, EvolutionaryOptimizer
from defect3d.clock_mechanisms import Pendulum

# Optimizar péndulo para precisión / Optimize pendulum for precision
def create_pendulum(length, mass):
    return Pendulum(length=length, mass=mass)

best, fitness, history = ClockOptimizer.optimize_for_precision(
    clock_creator=create_pendulum,
    target_period=1.0,
    generations=30
)

print(f"Longitud óptima / Optimal length: {best.length:.3f} m")
print(f"Período / Period: {best.period:.4f} s")
```

**Capacidades / Capabilities:**
- Optimización automática / Automatic optimization
- Reloj → precisión / Clock → precision
- Motor → eficiencia / Engine → efficiency
- Moto → estabilidad / Motorcycle → stability
- Algoritmos evolutivos / Evolutionary algorithms

**📂 Directorio / Directory:** `07_evolutionary_design/`

---

### 🔽 NIVEL 8 — ASISTENCIA DE IA (la nueva frontera)

**Diseño semántico y lenguaje natural / Semantic design and natural language**

```python
from defect3d.ai import AIArchitect

architect = AIArchitect()
# Crear mediante concepto semántico / Create via semantic concept
arm = architect.design("mechanical arm", segments=4)
```

**Capacidades / Capabilities:**
- Diseño basado en conceptos / Concept-based design
- Etiquetas semánticas / Semantic tagging
- Búsqueda funcional / Functional search
- Blueprints complejos / Complex blueprints
- Puente IA-API / AI-API Bridge

**📂 Directorio / Directory:** `docs/AI_ASSISTANCE.md`

---

## 🎯 Cómo se Conecta Todo / How Everything Connects

### De Abajo Hacia Arriba / Bottom-Up

1. **Geometría** crea engranajes / creates gears
2. **Engranajes** crean relojería / create clockwork
3. **Relojería** crea motores / creates engines
4. **Motores** crean vehículos / create vehicles
5. **Vehículos** crean simulación / create simulation
6. **Simulación** crea cine mecánico / creates mechanical cinema
7. **Evolución** crea optimización / creates optimization
8. **IA** crea diseño semántico / creates semantic design

### Ecosistema Fractal / Fractal Ecosystem

> El mismo reloj que late en tu muñeca puede ser el mismo tren de engranes que anima un motor.
>
> The same clock that beats on your wrist can be the same gear train that drives an engine.

**La relojería es el ADN de la movilidad / Clockwork is the DNA of mobility**

---

## ⭐ Consistencia Sistémica / Systemic Consistency

Si tu usuario sabe diseñar un engrane preciso...
también puede diseñar un cigüeñal, un embrague y un diferencial.

If your user knows how to design a precise gear...
they can also design a crankshaft, clutch, and differential.

**3defect = Escuela de ingeniería escalable**
**3defect = Scalable engineering school**

Donde aprender un nivel te habilita el siguiente.
Where learning one level enables the next.

---

## 🚀 Quick Start por Nivel / Quick Start by Level

### Nivel 1: Crear formas básicas / Create basic shapes
```bash
python 01_geometry/example_basic.py
```

### Nivel 2: Construir mecanismos de reloj / Build clock mechanisms
```bash
python 02_clock_mechanisms/example_basic.py
```

### Nivel 3: Crear motores / Create engines
```bash
python 03_engines/example_basic.py
```

### Nivel 4: Ensamblar vehículos / Assemble vehicles
```bash
python 04_vehicles/example_basic.py
```

### Nivel 5: Simular física / Simulate physics
```bash
python 05_physics_sim/example_basic.py
```

### Nivel 6: Exportar a Blender / Export to Blender
```bash
python 06_blender_visualization/example_basic.py
```

### Nivel 7: Evolucionar diseños / Evolve designs
```bash
python 07_evolutionary_design/example_basic.py
```

### Nivel 8: Asistencia de IA / AI Assistance
```bash
python examples/ai_assisted_design.py
```

---

## 📊 Estructura Completa / Complete Structure

```
3defect/
├── 01_geometry/              # NIVEL 1: Átomos geométricos
│   ├── README.md
│   ├── example_basic.py
│   ├── example_physics.py
│   └── example_blender.py
│
├── 02_clock_mechanisms/      # NIVEL 2: Relojería
│   ├── README.md
│   ├── example_basic.py
│   ├── example_physics.py
│   └── example_blender.py
│
├── 03_engines/               # NIVEL 3: Motores
│   ├── README.md
│   └── example_basic.py
│
├── 04_vehicles/              # NIVEL 4: Vehículos
│   ├── README.md
│   └── example_basic.py
│
├── 05_physics_sim/           # NIVEL 5: Simulación
│   ├── README.md
│   └── example_basic.py
│
├── 06_blender_visualization/ # NIVEL 6: Arte
│   ├── README.md
│   └── example_basic.py
│
├── 07_evolutionary_design/   # NIVEL 7: Evolución
│   ├── README.md
│   └── example_basic.py
│
└── defect3d/                 # Código fuente / Source code
    ├── core/                 # Geometría / Geometry
    ├── clock_mechanisms/     # Mecanismos de reloj / Clock mechanisms
    ├── mechanics/            # Componentes mecánicos / Mechanical components
    ├── vehicles/             # Vehículos / Vehicles
    ├── physics/              # Simulador físico / Physics simulator
    ├── blender_integration/  # Exportación Blender / Blender export
    └── evolutionary/         # Optimización evolutiva / Evolutionary optimization
```

---

## 🎓 Filosofía de Aprendizaje / Learning Philosophy

### Progresión Natural / Natural Progression

Cada nivel construye sobre el anterior:
Each level builds on the previous:

1. **Entender** las formas básicas / **Understand** basic shapes
2. **Combinar** en mecanismos / **Combine** into mechanisms  
3. **Energetizar** con motores / **Energize** with engines
4. **Integrar** en vehículos / **Integrate** into vehicles
5. **Simular** con física / **Simulate** with physics
6. **Visualizar** como arte / **Visualize** as art
7. **Optimizar** mediante evolución / **Optimize** through evolution

### Sin Frustración / Frustration-Free

> "Si una función genera frustración, se demueve, documenta o simplifica."
>
> "If a function generates frustration, it is demoted, documented or simplified."

- API simple en cada nivel / Simple API at each level
- Ejemplos mínimos funcionales / Minimal working examples
- Tests físicos verificables / Verifiable physics tests
- Visualización inmediata / Immediate visualization

---

## 🌍 El Último Nivel / The Final Level

El último nivel no es un auto...
The final level is not a car...

Es un **reloj que es vehículo del tiempo**
It's a **clock that is a vehicle of time**

Un **motor que late**
An **engine that beats**

Una **moto que respira torque**
A **motorcycle that breathes torque**

Una **física que canta**
A **physics that sings**

---

## 📖 Ver También / See Also

- [README.md](../README.md) - Introducción general / General introduction
- [PHASES.md](PHASES.md) - Fases de implementación / Implementation phases
- [USAGE.md](USAGE.md) - Guía de uso / Usage guide

---

**Made with ❤️ for the engineering community**

*Un sistema donde pequeño reloj → gran motor → movilidad → universo*
*A system where small clock → big engine → mobility → universe*
