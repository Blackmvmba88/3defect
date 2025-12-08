# 🔽 NIVEL 2 — MECANISMOS DE RELOJ (mecánica fina) / LEVEL 2 — CLOCK MECHANISMS (fine mechanics)

## Descripción / Description

**ES:** Componentes de relojería que permiten transmisión precisa de movimiento, control de tiempo y almacenamiento de energía. Aquí naces como relojería sistemática.

**EN:** Clockwork components that enable precise movement transmission, time control and energy storage. Here you are born as systematic watchmaking.

## Componentes / Components

### Engranajes / Gears

```python
from defect3d.clock_mechanisms import Gear

# Crear un engranaje / Create a gear
engranaje = Gear(
    teeth=30,           # Número de dientes / Number of teeth
    module=1.0,         # Módulo (tamaño) / Module (size)
    thickness=0.5,      # Grosor / Thickness
    position=(0, 0, 0)
)

# Calcular diámetro / Calculate diameter
print(f"Diámetro / Diameter: {engranaje.pitch_diameter}")

# Relación con otro engranaje / Ratio with another gear
engranaje2 = Gear(teeth=15, module=1.0)
ratio = engranaje.gear_ratio(engranaje2)
print(f"Relación / Ratio: {ratio}")  # 30/15 = 2.0
```

### Escape / Escapement

```python
from defect3d.clock_mechanisms import Escapement

# Crear un escape / Create an escapement
escape = Escapement(
    frequency=1.0,      # 1 Hz (1 tick por segundo / 1 tick per second)
    position=(0, 0, 0)
)

print(f"Período / Period: {escape.period} segundos / seconds")
```

### Péndulo / Pendulum

```python
from defect3d.clock_mechanisms import Pendulum

# Crear un péndulo / Create a pendulum
pendulo = Pendulum(
    length=1.0,         # Longitud / Length (metros / meters)
    mass=0.5,           # Masa / Mass (kg)
    position=(0, 0, 2)  # Posición del pivote / Pivot position
)

print(f"Período / Period: {pendulo.period:.3f} s")
print(f"Frecuencia / Frequency: {pendulo.frequency:.3f} Hz")
```

### Resorte / Spring

```python
from defect3d.clock_mechanisms import Spring

# Crear un resorte / Create a spring
resorte = Spring(
    coils=10,               # Espiras / Coils
    wire_diameter=0.05,     # Diámetro del alambre / Wire diameter
    coil_diameter=0.5,      # Diámetro de la espira / Coil diameter
    free_length=1.0,        # Longitud libre / Free length
    stiffness=100.0,        # Rigidez (N/m) / Stiffness (N/m)
    position=(0, 0, 0)
)

# Calcular energía almacenada / Calculate stored energy
compression = 0.1  # 10 cm de compresión / 10 cm compression
energia = resorte.energy(compression)
fuerza = resorte.force(compression)

print(f"Energía / Energy: {energia} J")
print(f"Fuerza / Force: {fuerza} N")
```

### Tren de Engranajes / Gear Train

```python
from defect3d.clock_mechanisms import Gear, GearTrain

# Crear un tren de engranajes / Create a gear train
tren = GearTrain(name="reloj_simple")

# Agregar engranajes / Add gears
gear1 = Gear(teeth=60, module=0.5, position=(0, 0, 0))
gear2 = Gear(teeth=30, module=0.5, position=(1.5, 0, 0))
gear3 = Gear(teeth=15, module=0.5, position=(2.5, 0, 0))

tren.add_gear(gear1)
tren.add_gear(gear2, connects_to=0)
tren.add_gear(gear3, connects_to=1)

# Calcular relación total / Calculate total ratio
print(f"Relación total / Total ratio: {tren.total_ratio()}")

# Velocidad de salida / Output speed
input_rpm = 60  # 1 rev/segundo / 1 rev/second
output_rpm = tren.output_speed(input_rpm)
print(f"Entrada / Input: {input_rpm} RPM")
print(f"Salida / Output: {output_rpm} RPM")
```

## Capacidades / Capabilities

Este nivel te da / This level gives you:

### 1. Transmisión de Movimiento / Movement Transmission
```python
# Un engranaje puede mover otro / A gear can move another
gear_driver = Gear(teeth=40)
gear_driven = Gear(teeth=20)
ratio = gear_driver.gear_ratio(gear_driven)  # 2:1
```

### 2. Precisión / Precision
```python
# El escape controla liberación precisa de energía
# The escapement controls precise energy release
escapement = Escapement(frequency=2.0)  # 2 ticks por segundo / 2 ticks per second
```

### 3. Relación de Engranes / Gear Ratio
```python
# Modificar velocidad y torque / Modify speed and torque
tren = GearTrain()
tren.add_gear(Gear(teeth=60))
tren.add_gear(Gear(teeth=20))
# Ratio 3:1 - más torque, menos velocidad / 3:1 ratio - more torque, less speed
```

### 4. Torque Fino / Fine Torque
```python
# Resortes proporcionan torque controlado / Springs provide controlled torque
spring = Spring(stiffness=50.0)
force = spring.force(0.05)  # Fuerza a 5cm de compresión / Force at 5cm compression
```

### 5. Cinemática Circular / Circular Kinematics
```python
# Péndulos y ruedas giratorias / Pendulums and rotating wheels
pendulum = Pendulum(length=0.5)
period = pendulum.period  # Período de oscilación / Oscillation period
```

## API Completa / Complete API

### Gear
```python
Gear(teeth, module, thickness, position)
  .pitch_diameter: float
  .pitch_radius: float
  .volume() -> float
  .gear_ratio(other_gear) -> float
  .to_dict() -> dict
```

### Escapement
```python
Escapement(frequency, position)
  .frequency: float
  .period: float
  .to_dict() -> dict
```

### Pendulum
```python
Pendulum(length, mass, position)
  .period: float
  .frequency: float
  .to_dict() -> dict
```

### Spring
```python
Spring(coils, wire_diameter, coil_diameter, free_length, stiffness, position)
  .energy(compression) -> float
  .force(compression) -> float
  .to_dict() -> dict
```

### GearTrain
```python
GearTrain(name)
  .add_gear(gear, connects_to)
  .total_ratio() -> float
  .output_speed(input_speed) -> float
  .to_dict() -> dict
```

## Objetivo / Objective

**ES:** Aquí naces como relojería sistemática. Puedes crear mecanismos precisos que controlan el tiempo, transmiten movimiento con exactitud y almacenan energía de forma predecible.

**EN:** Here you are born as systematic watchmaking. You can create precise mechanisms that control time, transmit movement accurately and store energy predictably.

## Ver También / See Also

- **Nivel 1 / Level 1:** `01_geometry/` - Los átomos que construyen estos engranajes / The atoms that build these gears
- **Nivel 3 / Level 3:** `03_engines/` - Energetizar estos engranajes en motores / Energize these gears into engines
- **Ejemplos / Examples:** 
  - `02_clock_mechanisms/example_basic.py` - Ejemplos básicos / Basic examples
  - `02_clock_mechanisms/example_blender.py` - Visualización / Visualization
  - `02_clock_mechanisms/example_physics.py` - Test físico / Physics test
