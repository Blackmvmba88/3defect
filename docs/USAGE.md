# 3defect Usage Guide

## Guía de Uso / Usage Guide

Esta guía te ayudará a comenzar con 3defect, un sistema de modelado 3D para crear vehículos y sistemas mecánicos.

This guide will help you get started with 3defect, a 3D modeling system for creating vehicles and mechanical systems.

---

## Instalación / Installation

```bash
# Clonar el repositorio / Clone the repository
git clone https://github.com/Blackmvmba88/3defect.git
cd 3defect

# Instalar dependencias / Install dependencies
pip install -r requirements.txt
```

---

## Ejemplos Básicos / Basic Examples

### 1. Crear un Coche / Create a Car

```python
from defect3d import Car

# Crear un coche deportivo rojo / Create a red sports car
sports_car = Car(
    car_type="sports",
    position=(0, 0, 0),
    color=(0.9, 0.1, 0.1)  # Rojo / Red
)

# Obtener especificaciones / Get specifications
specs = sports_car.get_specifications()
print(f"Motor: {specs['engine']['cylinders']} cilindros")
print(f"Potencia: {specs['engine']['power']} HP")

# Simular movimiento / Simulate movement
sports_car.simulate_movement(distance=10.0)
```

**Tipos de coches disponibles / Available car types:**
- `"sedan"` - Sedán familiar / Family sedan
- `"sports"` - Deportivo / Sports car
- `"suv"` - Vehículo utilitario deportivo / Sport utility vehicle

### 2. Crear una Moto / Create a Motorcycle

```python
from defect3d import Motorcycle

# Crear una moto deportiva azul / Create a blue sport bike
sport_bike = Motorcycle(
    bike_type="sport",
    position=(0, 0, 0),
    color=(0.1, 0.3, 0.9)  # Azul / Blue
)

# Ver especificaciones / View specifications
specs = sport_bike.get_specifications()
print(f"Tipo: {specs['type']}")
print(f"Ruedas: {specs['wheels']}")
```

**Tipos de motos disponibles / Available motorcycle types:**
- `"sport"` - Moto deportiva / Sport bike
- `"cruiser"` - Crucero / Cruiser
- `"touring"` - Turismo / Touring bike

### 3. Exportar a Blender / Export to Blender

```python
from defect3d import Car
from defect3d.blender_integration import export_to_blender

# Crear vehículo / Create vehicle
car = Car(car_type="sedan")

# Exportar / Export
export_to_blender(car, "mi_coche.py", also_json=True)
```

**Para visualizar en Blender / To visualize in Blender:**
1. Abrir Blender / Open Blender
2. Ir a la pestaña "Scripting" / Go to "Scripting" tab
3. Abrir el archivo generado / Open the generated file
4. Ejecutar el script (Alt+P) / Run the script (Alt+P)

### 4. Simulación de Física / Physics Simulation

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

# Crear simulador / Create simulator
sim = PhysicsSimulator(gravity=(0, 0, -9.81))

# Añadir coche / Add car
car = Car(car_type="sedan")
sim.add_object(car, mass=1500, velocity=(0, 0, 0))

# Aplicar fuerza de motor / Apply engine force
sim.apply_force(0, (5000, 0, 0))  # 5000 N

# Simular 2 segundos / Simulate 2 seconds
estados = sim.simulate(duration=2.0, apply_gravity=True)

# Ver resultados / View results
vel = sim.objects[0]['velocity']
print(f"Velocidad final: {vel} m/s")
```

### 5. Vehículo Personalizado / Custom Vehicle

```python
from defect3d.core import CompositePart
from defect3d.vehicles.components import Wheel, Engine, Chassis

# Crear vehículo base / Create base vehicle
mi_vehiculo = CompositePart(name="MiVehiculo")

# Añadir chasis / Add chassis
chasis = Chassis(length=3.0, width=1.5, height=0.2)
mi_vehiculo.add_part(chasis)

# Añadir motor / Add engine
motor = Engine(cylinders=4, position=(1, 0, 0.5))
mi_vehiculo.add_part(motor)

# Añadir ruedas / Add wheels
for x, y in [(1, 0.75), (1, -0.75), (-1, 0.75), (-1, -0.75)]:
    rueda = Wheel(radius=0.35, width=0.25, position=(x, y, 0.3))
    mi_vehiculo.add_part(rueda)

print(f"Total de partes: {mi_vehiculo.get_part_count()}")
```

---

## Conceptos Avanzados / Advanced Concepts

### Formas 3D Básicas / Basic 3D Shapes

```python
from defect3d.core import Cube, Sphere, Cylinder, Cone

# Cubo / Cube
cubo = Cube(size=1.0, position=(0, 0, 0))
cubo.set_color(1, 0, 0)  # Rojo / Red

# Esfera / Sphere
esfera = Sphere(radius=0.5, position=(2, 0, 0))
esfera.set_color(0, 1, 0)  # Verde / Green

# Cilindro / Cylinder
cilindro = Cylinder(radius=0.3, height=1.0, position=(4, 0, 0))
cilindro.set_color(0, 0, 1)  # Azul / Blue

# Transformaciones / Transformations
cubo.translate(1, 0, 0)  # Mover / Move
cubo.rotate(0, 45, 0)     # Rotar / Rotate
cubo.set_scale(2, 1, 1)   # Escalar / Scale
```

### Partes Compuestas / Composite Parts

```python
from defect3d.core import CompositePart, Cube, Cylinder

# Crear ensamblaje / Create assembly
ensamblaje = CompositePart(name="Ensamblaje")

# Añadir partes / Add parts
base = Cube(size=2.0, position=(0, 0, 0))
base.set_color(0.5, 0.5, 0.5)
ensamblaje.add_part(base)

columna = Cylinder(radius=0.2, height=3.0, position=(0, 0, 1.5))
columna.set_color(0.3, 0.3, 0.8)
ensamblaje.add_part(columna)

# Definir conexiones / Define connections
ensamblaje.connect(base, columna, connection_type="fixed")

# Mover todo el ensamblaje / Move entire assembly
ensamblaje.translate(5, 0, 0)
```

### Propiedades y Límites / Properties and Bounds

```python
from defect3d import Car

car = Car(car_type="sports")

# Establecer propiedades / Set properties
car.set_property("owner", "Juan")
car.set_property("max_speed", 250)

# Obtener propiedades / Get properties
owner = car.get_property("owner")
speed = car.get_property("max_speed", default=200)

# Obtener límites / Get bounds
min_bound, max_bound = car.get_bounds()
dimensions = max_bound - min_bound
print(f"Dimensiones: {dimensions}")
```

---

## Casos de Uso / Use Cases

### 1. Diseño de Vehículos / Vehicle Design

Crea y visualiza diferentes configuraciones de vehículos para:
- Diseño conceptual / Conceptual design
- Prototipado rápido / Rapid prototyping
- Presentaciones / Presentations

### 2. Simulación de Movimiento / Motion Simulation

Simula el comportamiento físico de vehículos para:
- Análisis de rendimiento / Performance analysis
- Pruebas de concepto / Proof of concept
- Educación / Education

### 3. Sistemas Mecánicos / Mechanical Systems

Diseña sistemas mecánicos complejos como:
- Motores / Engines
- Transmisiones / Transmissions
- Suspensiones / Suspensions
- Mecanismos personalizados / Custom mechanisms

### 4. Arte y Visualización / Art and Visualization

Crea escenas artísticas con:
- Múltiples vehículos / Multiple vehicles
- Ambientes personalizados / Custom environments
- Efectos y colores / Effects and colors

---

## Consejos / Tips

1. **Comienza simple / Start simple**: Usa los ejemplos incluidos como base
2. **Experimenta con colores / Experiment with colors**: Los valores RGB van de 0 a 1
3. **Escala correctamente / Scale properly**: Ten en cuenta las unidades (metros)
4. **Usa composites / Use composites**: Organiza piezas complejas en grupos
5. **Prueba en Blender / Test in Blender**: Visualiza tus creaciones para verificar

---

## Solución de Problemas / Troubleshooting

### Error: ModuleNotFoundError: No module named 'numpy'
```bash
pip install numpy
```

### Las formas no aparecen en Blender / Shapes don't appear in Blender
- Verifica que el script se ejecute sin errores / Check script runs without errors
- Asegúrate de que la versión de Blender sea 3.6+ / Ensure Blender version is 3.6+

### Los colores no se ven / Colors don't show
- En Blender, cambia a vista "Solid" o "Material Preview" / In Blender, switch to "Solid" or "Material Preview" view

---

## Recursos Adicionales / Additional Resources

- [Documentación completa](README.md) / [Full documentation](README.md)
- [Ejemplos](examples/) / [Examples](examples/)
- [Blender Documentation](https://docs.blender.org)

---

¡Diviértete creando! / Have fun creating! 🚗🏍️✨
