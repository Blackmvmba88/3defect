# 🔽 NIVEL 3 — MOTORES (mecánica gruesa) / LEVEL 3 — ENGINES (heavy mechanics)

## Descripción / Description

**ES:** Motores y sistemas de transmisión de potencia que convierten energía en movimiento. Aquí puedes energetizar tus engranajes del reloj y transformarlos en máquinas vivientes.

**EN:** Engines and power transmission systems that convert energy into motion. Here you can energize your clock gears and transform them into living machines.

## Componentes / Components

### Motor / Engine

```python
from defect3d import Engine

# Crear un motor / Create an engine
motor = Engine(
    cylinders=4,        # Número de cilindros / Number of cylinders
    position=(0, 0, 0)
)

# El motor ya está implementado en defect3d.mechanics.engines
# The engine is already implemented in defect3d.mechanics.engines
```

### Conceptos Clave / Key Concepts

Este nivel añade / This level adds:

#### 1. Energía → Movimiento / Energy → Movement
- Combustión interna convierte energía química en movimiento
- Internal combustion converts chemical energy into motion
- Torque y potencia / Torque and power

#### 2. Torque Alto / High Torque
- Mayor fuerza de rotación que mecanismos de reloj
- Greater rotational force than clock mechanisms
- Ideal para mover vehículos / Ideal for moving vehicles

#### 3. Consumo y Eficiencia / Consumption and Efficiency
- Relación potencia/combustible / Power/fuel ratio
- Curvas de torque / Torque curves
- Rendimiento térmico / Thermal efficiency

#### 4. Temperatura y Materiales / Temperature and Materials
- Motores operan a altas temperaturas
- Engines operate at high temperatures
- Materiales resistentes al calor
- Heat-resistant materials

## Componentes Mecánicos / Mechanical Components

### Cilindros / Cylinders
```python
# Los cilindros ya están en el motor
# Cylinders are already in the engine
motor = Engine(cylinders=6)
# Crea 6 cilindros automáticamente / Creates 6 cylinders automatically
```

### Cigüeñal / Crankshaft
```python
# El cigüeñal convierte movimiento lineal (pistón) en rotacional
# The crankshaft converts linear motion (piston) to rotational
# Ya implementado implícitamente en Engine
# Already implemented implicitly in Engine
```

### Pistones / Pistons
```python
# Los pistones se mueven dentro de los cilindros
# Pistons move inside cylinders
# Parte del sistema Engine
# Part of the Engine system
```

### Diferencial / Differential
```python
# Permite que las ruedas giren a diferentes velocidades
# Allows wheels to rotate at different speeds
# En el futuro: defect3d.mechanics.differential
# Future: defect3d.mechanics.differential
```

### Embrague / Clutch
```python
# Conecta/desconecta el motor de la transmisión
# Connects/disconnects engine from transmission
# En el futuro: defect3d.mechanics.clutch
# Future: defect3d.mechanics.clutch
```

## Ejemplo de Uso / Usage Example

```python
from defect3d import Engine, Car

# Motor standalone / Standalone engine
motor_v6 = Engine(cylinders=6, position=(0, 0, 0))

# Motor en un vehículo / Engine in a vehicle
coche = Car(car_type="sports")  # Tiene motor de 6 cilindros / Has 6-cylinder engine
specs = coche.get_specifications()
print(specs['engine'])  # Información del motor / Engine information
```

## Relación con Nivel 2 / Relationship with Level 2

**ES:** Los engranajes del Nivel 2 transmiten el movimiento del motor. Un motor sin engranajes solo gira; con engranajes se convierte en una máquina útil.

**EN:** Level 2 gears transmit the engine's motion. An engine without gears just spins; with gears it becomes a useful machine.

```python
from defect3d import Engine
from defect3d.clock_mechanisms import GearTrain, Gear

# Motor / Engine
motor = Engine(cylinders=4)

# Transmisión (tren de engranajes) / Transmission (gear train)
transmision = GearTrain(name="transmission")
transmision.add_gear(Gear(teeth=20))  # Entrada del motor / Engine input
transmision.add_gear(Gear(teeth=60))  # Salida a ruedas / Output to wheels

# El motor gira rápido, los engranajes reducen velocidad y aumentan torque
# Engine spins fast, gears reduce speed and increase torque
input_rpm = 3000  # RPM del motor / Engine RPM
output_rpm = transmision.output_speed(input_rpm)
print(f"Motor: {input_rpm} RPM → Ruedas: {output_rpm} RPM")
```

## Especificaciones de Motores / Engine Specifications

### Motor 2 Cilindros / 2-Cylinder Engine
- Potencia / Power: ~80 HP
- Uso / Use: Motocicletas / Motorcycles

### Motor 4 Cilindros / 4-Cylinder Engine
- Potencia / Power: ~150-200 HP
- Uso / Use: Automóviles sedan

### Motor 6 Cilindros / 6-Cylinder Engine
- Potencia / Power: ~250-300 HP
- Uso / Use: Automóviles deportivos / Sports cars

### Motor 8 Cilindros / 8-Cylinder Engine
- Potencia / Power: ~400+ HP
- Uso / Use: Vehículos de alto rendimiento / High-performance vehicles

## Objetivo / Objective

**ES:** Aquí ya puedes energetizar tus engranes del reloj y transformarlos en máquinas vivientes. El motor proporciona la potencia, los engranajes la controlan.

**EN:** Here you can energize your clock gears and transform them into living machines. The engine provides power, the gears control it.

## Ver También / See Also

- **Nivel 2 / Level 2:** `02_clock_mechanisms/` - Engranajes que transmiten la potencia del motor
- **Nivel 4 / Level 4:** `04_vehicles/` - Integrar motores en vehículos completos
- **Ejemplos / Examples:**
  - `03_engines/example_basic.py` - Ejemplos de motores
  - `03_engines/example_blender.py` - Visualización
  - `03_engines/example_physics.py` - Física del motor
