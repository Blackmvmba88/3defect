# 🔽 NIVEL 5 — SIMULACIÓN (física emocional) / LEVEL 5 — SIMULATION (emotional physics)

## Descripción / Description

**ES:** Física realista que hace que los sistemas cobren vida. Tu ecosistema empieza a contar historias físicas creíbles.

**EN:** Realistic physics that brings systems to life. Your ecosystem begins to tell believable physical stories.

## Sistemas Físicos / Physical Systems

### PhysicsSimulator

```python
from defect3d.physics import PhysicsSimulator

# Crear simulador / Create simulator
sim = PhysicsSimulator(gravity=9.81)  # Gravedad terrestre / Earth gravity

# Agregar objeto / Add object
sim.add_object(my_object, mass=1000, velocity=(10, 0, 0))

# Aplicar fuerzas / Apply forces
sim.apply_force(0, (5000, 0, 0))  # Fuerza en X

# Simular / Simulate
states = sim.simulate(duration=2.0, dt=0.016)  # 60 FPS
```

## Fuerzas y Efectos / Forces and Effects

### 1. Gravedad / Gravity
```python
# Gravedad configurable / Configurable gravity
sim = PhysicsSimulator(gravity=9.81)  # Tierra / Earth
sim_moon = PhysicsSimulator(gravity=1.62)  # Luna / Moon
sim_jupiter = PhysicsSimulator(gravity=24.79)  # Júpiter / Jupiter
```

### 2. Colisiones / Collisions
```python
# Detección de colisiones (futuro) / Collision detection (future)
# sim.enable_collisions()
# sim.add_collision_pair(obj1, obj2)
```

### 3. Fricción / Friction
```python
# Fricción del aire (futuro) / Air friction (future)
# sim.set_air_resistance(coefficient=0.5)

# Fricción de rodadura (futuro) / Rolling friction (future)
# wheel.set_friction(coefficient=0.7)
```

### 4. Aceleración / Acceleration
```python
# La aceleración se calcula automáticamente: a = F/m
# Acceleration is calculated automatically: a = F/m

sim.add_object(car, mass=1500, velocity=(0, 0, 0))
sim.apply_force(0, (6000, 0, 0))  # 6000 N

# Aceleración / Acceleration: 6000/1500 = 4 m/s²
```

### 5. Curvas de Torque / Torque Curves
```python
# Torque del motor varía con RPM / Engine torque varies with RPM
# (Implementación futura / Future implementation)

def torque_curve(rpm):
    """Curva de torque realista / Realistic torque curve"""
    if rpm < 1000:
        return rpm * 0.5
    elif rpm < 5000:
        return 500 + (rpm - 1000) * 0.1
    else:
        return 900 - (rpm - 5000) * 0.05
```

### 6. Resistencia del Aire / Air Resistance
```python
# Fuerza de arrastre: F = ½ρv²CdA / Drag force: F = ½ρv²CdA
# (Implementación futura / Future implementation)

def air_drag(velocity, drag_coefficient=0.3, area=2.0):
    """Calcular resistencia del aire / Calculate air resistance"""
    rho = 1.225  # kg/m³ (densidad del aire / air density)
    v_squared = velocity[0]**2 + velocity[1]**2 + velocity[2]**2
    force_magnitude = 0.5 * rho * v_squared * drag_coefficient * area
    # Dirección opuesta a la velocidad / Direction opposite to velocity
    return (-force_magnitude, 0, 0)
```

### 7. Estabilidad / Stability
```python
# Centro de masa y estabilidad / Center of mass and stability
# Un vehículo con centro de masa bajo es más estable
# A vehicle with low center of mass is more stable

# (Implementación futura / Future implementation)
```

### 8. Carga Estructural / Structural Load
```python
# Fuerzas sobre el chasis y componentes
# Forces on chassis and components
# Análisis de estrés (futuro) / Stress analysis (future)
```

## Energía / Energy

### Energía Cinética / Kinetic Energy
```python
# E_k = ½mv²
# Ya implementado en PhysicsSimulator
# Already implemented in PhysicsSimulator

state = sim.simulate(duration=1.0)[-1]
kinetic_energy = state["objects"][0]["kinetic_energy"]
print(f"Energía cinética / Kinetic energy: {kinetic_energy} J")
```

### Energía Potencial / Potential Energy
```python
# E_p = mgh
# Ya implementado en PhysicsSimulator
# Already implemented in PhysicsSimulator

potential_energy = state["objects"][0]["potential_energy"]
print(f"Energía potencial / Potential energy: {potential_energy} J")
```

### Conservación de Energía / Energy Conservation
```python
# En un sistema aislado sin fricción:
# In an isolated system without friction:
# E_total = E_k + E_p = constante / constant

initial_state = states[0]
final_state = states[-1]

E_initial = sum(obj["kinetic_energy"] + obj["potential_energy"] 
                for obj in initial_state["objects"])
E_final = sum(obj["kinetic_energy"] + obj["potential_energy"] 
              for obj in final_state["objects"])

print(f"Energía inicial / Initial: {E_initial:.2f} J")
print(f"Energía final / Final: {E_final:.2f} J")
```

## Ejemplo Completo / Complete Example

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

# Crear vehículo / Create vehicle
coche = Car(car_type="sports")

# Crear simulador / Create simulator
sim = PhysicsSimulator(gravity=9.81)

# Condiciones iniciales / Initial conditions
masa = 1200  # kg
velocidad_inicial = (0, 0, 0)  # Partiendo del reposo / Starting from rest
sim.add_object(coche, mass=masa, velocity=velocidad_inicial)

# Aplicar fuerza del motor / Apply engine force
fuerza_motor = 5000  # N
sim.apply_force(0, (fuerza_motor, 0, 0))

# Simular aceleración / Simulate acceleration
print("Simulando aceleración 0-100 km/h...")
duration = 5.0  # segundos / seconds
states = sim.simulate(duration=duration, dt=0.01)

# Analizar resultados / Analyze results
for i, state in enumerate(states[::10]):  # Cada 0.1 segundos / Every 0.1 seconds
    t = i * 0.1
    vel = state["objects"][0]["velocity"]
    speed_kmh = vel[0] * 3.6  # m/s a km/h / m/s to km/h
    print(f"t={t:.1f}s: velocidad={speed_kmh:.1f} km/h")
```

## Objetivo / Objective

**ES:** Tu ecosistema empieza a contar historias físicas creíbles. Los vehículos no solo existen, se mueven con física realista que puedes sentir.

**EN:** Your ecosystem begins to tell believable physical stories. Vehicles don't just exist, they move with realistic physics that you can feel.

## Ver También / See Also

- **Nivel 4 / Level 4:** `04_vehicles/` - Vehículos a simular
- **Nivel 6 / Level 6:** `06_blender_visualization/` - Visualizar la simulación
- **Ejemplos / Examples:**
  - `05_physics_sim/example_basic.py` - Simulación básica
  - `05_physics_sim/example_advanced.py` - Simulación avanzada
  - Referencia: `examples/physics_simulation.py` - Ejemplo original
