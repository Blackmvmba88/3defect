# 🔽 NIVEL 4 — VEHÍCULOS (sistemas integrados) / LEVEL 4 — VEHICLES (integrated systems)

## Descripción / Description

**ES:** Vehículos completos que integran todos los niveles anteriores: geometría, mecanismos, motores. Aquí ya no solo mueves un engrane: mueves un mundo compuesto.

**EN:** Complete vehicles that integrate all previous levels: geometry, mechanisms, engines. Here you no longer just move a gear: you move a composite world.

## Vehículos Disponibles / Available Vehicles

### Automóviles / Cars

```python
from defect3d import Car

# Sedan (familiar) / Sedan (family car)
sedan = Car(car_type="sedan", color=(0.3, 0.3, 0.8))

# Deportivo / Sports car
sports = Car(car_type="sports", color=(0.9, 0.1, 0.1))

# SUV (todoterreno) / SUV (off-road)
suv = Car(car_type="suv", color=(0.2, 0.5, 0.2))

# Obtener especificaciones / Get specifications
specs = sedan.get_specifications()
print(specs)
```

### Motocicletas / Motorcycles

```python
from defect3d import Motorcycle

# Deportiva / Sport bike
sport_bike = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))

# Cruiser (paseo) / Cruiser (touring)
cruiser = Motorcycle(bike_type="cruiser", color=(0.1, 0.1, 0.1))

# Touring (viaje) / Touring (travel)
touring = Motorcycle(bike_type="touring", color=(0.6, 0.2, 0.2))
```

## Componentes de un Vehículo / Vehicle Components

### 1. Chasis / Chassis
```python
from defect3d import Chassis

# Base estructural del vehículo / Structural base of vehicle
chasis = Chassis(length=4.5, width=1.8, height=0.3)
```

### 2. Ruedas / Wheels
```python
from defect3d import Wheel

# Rueda con llanta y rin / Wheel with tire and rim
rueda = Wheel(radius=0.35, width=0.25)
```

### 3. Suspensión / Suspension
```python
# La suspensión absorbe impactos / Suspension absorbs impacts
# Implementada con resortes del Nivel 2 / Implemented with Level 2 springs
from defect3d.clock_mechanisms import Spring

suspension = Spring(coils=8, stiffness=10000.0)
```

### 4. Dirección / Steering
```python
# Sistema de dirección / Steering system
# Controla el ángulo de las ruedas delanteras
# Controls front wheel angle
```

### 5. Motor Integrado / Integrated Engine
```python
# Todos los vehículos tienen motor / All vehicles have engines
coche = Car(car_type="sedan")
# Motor de 4 cilindros, 200 HP / 4-cylinder engine, 200 HP
```

### 6. Frenos / Brakes
```python
# Sistema de frenado / Braking system
# Reduce velocidad mediante fricción
# Reduces speed through friction
```

## Jerarquía de Construcción / Construction Hierarchy

```
Vehículo / Vehicle
├── Chasis / Chassis (Nivel 1: Cubo + Cilindros / Level 1: Cube + Cylinders)
├── Motor / Engine (Nivel 3: Motor / Level 3: Engine)
│   └── Cilindros (Nivel 1: Cilindros / Cylinders)
├── Transmisión / Transmission (Nivel 2: Engranajes / Level 2: Gears)
├── Ruedas / Wheels (Nivel 1: Cilindros + Toros / Cylinders + Tori)
├── Suspensión / Suspension (Nivel 2: Resortes / Level 2: Springs)
└── Carrocería / Body (Nivel 1: Geometría compuesta / Composite geometry)
```

## Especificaciones por Tipo / Specifications by Type

### Sedan
- Longitud / Length: 4.5 m
- Motor / Engine: 4 cilindros, 200 HP
- Uso / Use: Familiar / Family

### Sports
- Longitud / Length: 4.2 m
- Motor / Engine: 6 cilindros, 300 HP
- Uso / Use: Alto rendimiento / High performance

### SUV
- Longitud / Length: 5.0 m
- Motor / Engine: 6 cilindros, 250 HP
- Uso / Use: Todoterreno / Off-road

### Sport Motorcycle
- Motor / Engine: 4 cilindros, 180 HP
- Velocidad máx / Max speed: Alto / High

### Cruiser Motorcycle
- Motor / Engine: 2 cilindros, 80 HP
- Confort / Comfort: Alto / High

### Touring Motorcycle
- Motor / Engine: 4 cilindros, 120 HP
- Autonomía / Range: Alta / High

## Simulación de Movimiento / Movement Simulation

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

# Crear vehículo / Create vehicle
coche = Car(car_type="sports")

# Crear simulador / Create simulator
sim = PhysicsSimulator()

# Agregar al simulador / Add to simulator
sim.add_object(coche, mass=1200, velocity=(20, 0, 0))  # 20 m/s inicial

# Aplicar fuerza del motor / Apply engine force
sim.apply_force(0, (3000, 0, 0))  # 3000 N

# Simular / Simulate
states = sim.simulate(duration=5.0)
```

## Objetivo / Objective

**ES:** Aquí ya no solo mueves un engrane: mueves un mundo compuesto. El vehículo es la integración de todos los niveles anteriores en un sistema funcional completo.

**EN:** Here you no longer just move a gear: you move a composite world. The vehicle is the integration of all previous levels into a complete functional system.

## Ver También / See Also

- **Nivel 1 / Level 1:** `01_geometry/` - Formas básicas que construyen el vehículo
- **Nivel 2 / Level 2:** `02_clock_mechanisms/` - Engranajes en la transmisión
- **Nivel 3 / Level 3:** `03_engines/` - Motor que impulsa el vehículo
- **Nivel 5 / Level 5:** `05_physics_sim/` - Simular el movimiento del vehículo
- **Ejemplos / Examples:**
  - `04_vehicles/example_basic.py` - Crear vehículos
  - `04_vehicles/example_blender.py` - Visualizar vehículos
  - `04_vehicles/example_physics.py` - Simular vehículos
