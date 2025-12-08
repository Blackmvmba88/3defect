# 🔽 NIVEL 7 — EVOLUCIÓN (tu cereza) / LEVEL 7 — EVOLUTION (your cherry)

## Descripción / Description

**ES:** La máquina deja de ser estática, se convierte en organismo que aprende. Optimización automática que hace evolucionar tus diseños hacia la perfección.

**EN:** The machine stops being static, it becomes an organism that learns. Automatic optimization that evolves your designs towards perfection.

## Optimización Evolutiva / Evolutionary Optimization

### EvolutionaryOptimizer (Base)

```python
from defect3d.evolutionary import EvolutionaryOptimizer

# Crear optimizador / Create optimizer
optimizer = EvolutionaryOptimizer(
    population_size=20,      # Tamaño de población / Population size
    mutation_rate=0.1,       # Tasa de mutación / Mutation rate
    elite_size=2             # Élite a preservar / Elite to preserve
)

# Definir función de creación / Define creation function
def create_individual(**params):
    # Crear individuo con parámetros / Create individual with parameters
    return MyObject(**params)

# Definir función de aptitud / Define fitness function
def fitness_function(individual):
    # Retornar valor de aptitud (mayor = mejor)
    # Return fitness value (higher = better)
    return individual.calculate_performance()

# Ejecutar optimización / Run optimization
best, fitness, history = optimizer.optimize(
    create_individual=create_individual,
    fitness_function=fitness_function,
    parameter_ranges={'param1': (0, 10), 'param2': (0, 5)},
    generations=50
)
```

## Optimizadores Especializados / Specialized Optimizers

### 1. ClockOptimizer - Precisión de Reloj / Clock Precision

```python
from defect3d.clock_mechanisms import Pendulum
from defect3d.evolutionary import ClockOptimizer

# Crear función de creación de péndulo / Create pendulum creation function
def create_pendulum(length, mass):
    return Pendulum(length=length, mass=mass)

# Optimizar para período de 1 segundo / Optimize for 1 second period
best_pendulum, fitness, history = ClockOptimizer.optimize_for_precision(
    clock_creator=create_pendulum,
    target_period=1.0,
    generations=30
)

print(f"Longitud óptima / Optimal length: {best_pendulum.length:.3f} m")
print(f"Período / Period: {best_pendulum.period:.4f} s")
print(f"Error / Error: {abs(best_pendulum.period - 1.0)*1000:.2f} ms")
```

**Resultado esperado / Expected result:**
- Longitud ~0.248 m para período de 1 segundo
- Length ~0.248 m for 1 second period
- Precisión milimétrica / Millimetric precision

### 2. EngineOptimizer - Eficiencia de Motor / Engine Efficiency

```python
from defect3d import Engine
from defect3d.evolutionary import EngineOptimizer

# Optimizar motor para balance potencia/eficiencia
# Optimize engine for power/efficiency balance

def create_engine(cylinders):
    return Engine(cylinders=int(round(cylinders)))

optimizer = EngineOptimizer()
# (Implementación en desarrollo / Implementation in development)
```

**Objetivos / Objectives:**
- Balance entre potencia y consumo / Balance between power and consumption
- Optimizar curva de torque / Optimize torque curve
- Minimizar peso por HP / Minimize weight per HP

### 3. VehicleOptimizer - Estabilidad de Vehículo / Vehicle Stability

```python
from defect3d import Car
from defect3d.evolutionary import VehicleOptimizer

# Optimizar vehículo para estabilidad
# Optimize vehicle for stability

optimizer = VehicleOptimizer()
# (Implementación en desarrollo / Implementation in development)
```

**Objetivos / Objectives:**
- Centro de masa bajo / Low center of mass
- Relación ancho/largo óptima / Optimal width/length ratio
- Distribución de peso equilibrada / Balanced weight distribution

## Casos de Uso / Use Cases

### Caso 1: Evolucionar Reloj a Precisión Máxima / Evolve Clock to Maximum Precision

```python
from defect3d.clock_mechanisms import Pendulum, GearTrain, Gear
from defect3d.evolutionary import EvolutionaryOptimizer

def create_clock_system(pendulum_length, gear1_teeth, gear2_teeth):
    """Crear sistema de reloj completo / Create complete clock system"""
    pendulum = Pendulum(length=pendulum_length, mass=0.5)
    
    train = GearTrain()
    train.add_gear(Gear(teeth=int(gear1_teeth)))
    train.add_gear(Gear(teeth=int(gear2_teeth)))
    
    return {
        'pendulum': pendulum,
        'train': train
    }

def fitness_clock(system):
    """Evaluar precisión del reloj / Evaluate clock precision"""
    # Período del péndulo / Pendulum period
    period_error = abs(system['pendulum'].period - 2.0)  # Target: 2 segundos
    
    # Relación de engranajes / Gear ratio
    ratio_error = abs(system['train'].total_ratio() - 0.5)  # Target: 0.5
    
    # Mejor fitness = menor error / Better fitness = less error
    return 1.0 / (1.0 + period_error + ratio_error)

optimizer = EvolutionaryOptimizer(population_size=30)

best_clock, best_fitness, history = optimizer.optimize(
    create_individual=create_clock_system,
    fitness_function=fitness_clock,
    parameter_ranges={
        'pendulum_length': (0.5, 2.0),
        'gear1_teeth': (20, 80),
        'gear2_teeth': (10, 40)
    },
    generations=50
)

print(f"✅ Reloj óptimo / Optimal clock:")
print(f"   Período péndulo / Pendulum period: {best_clock['pendulum'].period:.4f} s")
print(f"   Relación engranajes / Gear ratio: {best_clock['train'].total_ratio():.4f}")
```

### Caso 2: Evolucionar Motor a Eficiencia / Evolve Engine to Efficiency

```python
from defect3d import Engine
from defect3d.evolutionary import EvolutionaryOptimizer

def create_engine_config(cylinders, displacement_per_cyl):
    """Crear configuración de motor / Create engine configuration"""
    engine = Engine(cylinders=int(round(cylinders)))
    engine.displacement = displacement_per_cyl * cylinders
    return engine

def fitness_engine(engine):
    """Evaluar eficiencia / Evaluate efficiency"""
    # Potencia estimada / Estimated power
    power = engine.cylinders * 50  # HP aproximado
    
    # Peso estimado / Estimated weight
    weight = engine.cylinders * 20  # kg aproximado
    
    # Consumo estimado / Estimated consumption
    consumption = engine.cylinders * 0.5  # L/100km aproximado
    
    # Fitness = potencia / (peso + consumo)
    # Higher power, lower weight and consumption = better
    return power / (weight * 0.1 + consumption)

optimizer = EvolutionaryOptimizer(population_size=20, mutation_rate=0.15)

best_engine, best_fitness, history = optimizer.optimize(
    create_individual=create_engine_config,
    fitness_function=fitness_engine,
    parameter_ranges={
        'cylinders': (2, 8),
        'displacement_per_cyl': (0.3, 0.8)  # Litros
    },
    generations=40
)

print(f"✅ Motor óptimo / Optimal engine:")
print(f"   Cilindros / Cylinders: {best_engine.cylinders}")
print(f"   Desplazamiento / Displacement: {best_engine.displacement:.2f} L")
```

### Caso 3: Evolucionar Moto a Estabilidad / Evolve Motorcycle to Stability

```python
from defect3d import Motorcycle
from defect3d.evolutionary import EvolutionaryOptimizer

def create_bike_config(wheelbase, seat_height, weight_dist):
    """Crear configuración de moto / Create motorcycle configuration"""
    bike = Motorcycle(bike_type="sport")
    bike.wheelbase = wheelbase
    bike.seat_height = seat_height
    bike.weight_distribution = weight_dist  # 0=adelante, 1=atrás / 0=front, 1=rear
    return bike

def fitness_bike(bike):
    """Evaluar estabilidad / Evaluate stability"""
    # Distancia entre ejes ideal / Ideal wheelbase
    wheelbase_score = 1.0 / (1.0 + abs(bike.wheelbase - 1.4))
    
    # Altura de asiento baja = más estable / Low seat = more stable
    seat_score = 1.0 / (1.0 + abs(bike.seat_height - 0.75))
    
    # Distribución de peso equilibrada / Balanced weight distribution
    weight_score = 1.0 / (1.0 + abs(bike.weight_distribution - 0.5))
    
    return wheelbase_score + seat_score + weight_score

optimizer = EvolutionaryOptimizer(population_size=25, mutation_rate=0.12)

best_bike, best_fitness, history = optimizer.optimize(
    create_individual=create_bike_config,
    fitness_function=fitness_bike,
    parameter_ranges={
        'wheelbase': (1.2, 1.6),
        'seat_height': (0.6, 0.9),
        'weight_dist': (0.3, 0.7)
    },
    generations=35
)

print(f"✅ Moto óptima / Optimal motorcycle:")
print(f"   Distancia entre ejes / Wheelbase: {best_bike.wheelbase:.3f} m")
print(f"   Altura asiento / Seat height: {best_bike.seat_height:.3f} m")
print(f"   Distribución peso / Weight dist: {best_bike.weight_distribution:.3f}")
```

## Algoritmo Evolutivo / Evolutionary Algorithm

### Proceso / Process

1. **Población Inicial / Initial Population**
   - Crear N individuos con parámetros aleatorios
   - Create N individuals with random parameters

2. **Evaluación / Evaluation**
   - Calcular fitness de cada individuo
   - Calculate fitness of each individual

3. **Selección / Selection**
   - Seleccionar mejores individuos (élite)
   - Select best individuals (elite)
   - Selección por torneo para reproducción
   - Tournament selection for reproduction

4. **Reproducción / Reproduction**
   - Cruzamiento de padres / Parent crossover
   - Mutación aleatoria / Random mutation

5. **Nueva Generación / New Generation**
   - Repetir hasta alcanzar generaciones objetivo
   - Repeat until reaching target generations

### Parámetros Clave / Key Parameters

- **population_size**: Más grande = mejor exploración, más lento
- **mutation_rate**: Alta = más exploración, baja = más explotación  
- **elite_size**: Preservar mejores soluciones
- **generations**: Más generaciones = mejor optimización

## Objetivo / Objective

**ES:** La máquina deja de ser estática, se convierte en organismo que aprende. Tus diseños evolucionan automáticamente hacia la perfección sin intervención manual.

**EN:** The machine stops being static, it becomes an organism that learns. Your designs automatically evolve towards perfection without manual intervention.

## Ver También / See Also

- **Nivel 2 / Level 2:** `02_clock_mechanisms/` - Relojes a optimizar
- **Nivel 3 / Level 3:** `03_engines/` - Motores a optimizar
- **Nivel 4 / Level 4:** `04_vehicles/` - Vehículos a optimizar
- **Ejemplos / Examples:**
  - `07_evolutionary_design/example_clock_precision.py` - Optimizar reloj
  - `07_evolutionary_design/example_engine_efficiency.py` - Optimizar motor
  - `07_evolutionary_design/example_vehicle_stability.py` - Optimizar vehículo
