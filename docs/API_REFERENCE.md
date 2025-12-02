# API Reference - 3defect

Complete API reference for the 3defect 3D modeling system.

## Core Module (`defect3d.core`)

### Primitives (`defect3d.core.primitives` or `defect3d.core.shapes`)

Base 3D shape classes for building models.

#### `Shape3D` (Base Class)

Base class for all 3D shapes.

**Constructor:**
```python
Shape3D(position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
```

**Attributes:**
- `position`: numpy array [x, y, z]
- `rotation`: numpy array [rx, ry, rz] in degrees
- `scale`: numpy array [sx, sy, sz]
- `name`: string identifier
- `material`: dict with 'color' key (RGBA tuple)

**Methods:**
- `translate(dx, dy, dz)`: Move shape by offset
- `rotate(rx, ry, rz)`: Rotate shape by angles in degrees
- `set_scale(sx, sy, sz)`: Set scale factors
- `set_color(r, g, b, a=1.0)`: Set RGBA color (0-1 range)
- `get_bounds()`: Get bounding box as (min_point, max_point)
- `to_dict()`: Convert to dictionary representation

#### `Cube(Shape3D)`

Rectangular box primitive.

```python
cube = Cube(size=1.0, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
```

**Parameters:**
- `size`: float - Side length of the cube

#### `Sphere(Shape3D)`

Spherical primitive.

```python
sphere = Sphere(radius=1.0, position=(0, 0, 0))
```

**Parameters:**
- `radius`: float - Radius of the sphere

#### `Cylinder(Shape3D)`

Cylindrical primitive.

```python
cylinder = Cylinder(radius=1.0, height=2.0, position=(0, 0, 0))
```

**Parameters:**
- `radius`: float - Radius of the cylinder
- `height`: float - Height of the cylinder

#### `Cone(Shape3D)`

Conical primitive.

```python
cone = Cone(radius=1.0, height=2.0, position=(0, 0, 0))
```

**Parameters:**
- `radius`: float - Base radius
- `height`: float - Height of the cone

#### `Torus(Shape3D)`

Donut-shaped primitive (useful for wheels).

```python
torus = Torus(major_radius=1.0, minor_radius=0.25, position=(0, 0, 0))
```

**Parameters:**
- `major_radius`: float - Distance from center to tube center
- `minor_radius`: float - Radius of the tube

### Composite (`defect3d.core.composite`)

System for building complex objects from simple shapes.

#### `CompositePart`

A composite part made up of multiple 3D shapes.

**Constructor:**
```python
composite = CompositePart(name="MyPart")
```

**Attributes:**
- `name`: string identifier
- `parts`: list of Shape3D objects
- `position`: numpy array [x, y, z]
- `rotation`: numpy array [rx, ry, rz]
- `connections`: list of connection definitions
- `properties`: dict of custom properties

**Methods:**
```python
# Add parts
composite.add_part(shape, relative_position=(x, y, z))
composite.remove_part(shape)

# Transformations
composite.translate(dx, dy, dz)
composite.rotate(rx, ry, rz)

# Connections
composite.connect(part1, part2, connection_type="fixed")

# Properties
composite.set_property(key, value)
value = composite.get_property(key, default=None)

# Utilities
min_bounds, max_bounds = composite.get_bounds()
count = composite.count_parts()
dict_data = composite.to_dict()
```

### Transformations (`defect3d.core.transformations`)

Matrix-based transformation utilities.

**Functions:**

```python
# Create transformation matrices
matrix = create_translation_matrix(dx, dy, dz)
matrix = create_rotation_matrix_x(angle_deg)
matrix = create_rotation_matrix_y(angle_deg)
matrix = create_rotation_matrix_z(angle_deg)
matrix = create_scale_matrix(sx, sy, sz)

# Apply transformations
matrix = apply_transform(position, rotation, scale)
new_point = transform_point(point, matrix)

# Interpolation
interpolated = interpolate_transform(start_pos, end_pos, t)
```

### Serialization (`defect3d.core.serializer`)

Universal JSON export for 3D objects.

**Functions:**

```python
# Serialize to dictionary
data = serialize_shape(shape)
data = serialize_composite(composite)
data = serialize_object(obj)  # Works with any object

# Export to JSON
json_string = to_json(obj, pretty=True)
json_string = to_json([obj1, obj2, obj3], pretty=True)  # Multiple objects

# File operations
save_to_json(obj, "output.json", pretty=True)
data = load_from_json("input.json")  # Returns dict
```

---

## Mechanics Module (`defect3d.mechanics`)

Pre-built mechanical components for vehicles.

### `Wheel`

Vehicle wheel with tire and rim.

```python
from defect3d.mechanics import Wheel

wheel = Wheel(radius=0.3, width=0.2, position=(0, 0, 0))
```

**Parameters:**
- `radius`: float - Wheel radius (default: 0.3)
- `width`: float - Wheel width (default: 0.2)
- `position`: tuple - 3D position

**Properties:**
- Contains tire (outer cylinder) and rim (inner cylinder)
- Properties: `radius`, `width`

### `Engine`

Vehicle engine block with cylinders.

```python
from defect3d.mechanics import Engine

engine = Engine(cylinders=4, position=(0, 0, 0))
```

**Parameters:**
- `cylinders`: int - Number of cylinders (default: 4)
- `position`: tuple - 3D position

**Properties:**
- `cylinders`: Number of cylinders
- `power`: Horsepower (calculated as cylinders * 50)

### `Chassis`

Vehicle chassis/frame with rails.

```python
from defect3d.mechanics import Chassis

chassis = Chassis(length=2.0, width=1.0, height=0.2, position=(0, 0, 0))
```

**Parameters:**
- `length`: float - Chassis length
- `width`: float - Chassis width  
- `height`: float - Chassis height
- `position`: tuple - 3D position

**Properties:**
- `length`, `width`, `height`
- Contains main body and side rails

### `Body`

Vehicle body shell.

```python
from defect3d.mechanics import Body

body = Body(style="sedan", position=(0, 0, 0))
```

**Parameters:**
- `style`: str - Body style ("sedan" or "sports")
- `position`: tuple - 3D position

**Properties:**
- `style`: Body style identifier

---

## Vehicles Module (`defect3d.vehicles`)

High-level vehicle presets.

### `Car`

Complete car with all components.

```python
from defect3d import Car

car = Car(car_type="sedan", position=(0, 0, 0), color=(0.8, 0.2, 0.2))
```

**Car Types:**
- `"sedan"`: Family car (4.5m, 4 cylinders, 200 HP)
- `"sports"`: Performance car (4.2m, 6 cylinders, 300 HP)
- `"suv"`: Large vehicle (5.0m, 6 cylinders, 250 HP)

**Methods:**
```python
specs = car.get_specifications()  # Returns dict with all specs
car.translate(dx, dy, dz)
car.simulate_movement(distance, direction=(1, 0, 0))
```

### `Motorcycle`

Complete motorcycle with all components.

```python
from defect3d import Motorcycle

bike = Motorcycle(bike_type="sport", position=(0, 0, 0), color=(0.1, 0.3, 0.9))
```

**Motorcycle Types:**
- `"sport"`: High-performance (4 cylinders, 180 HP)
- `"cruiser"`: Comfortable (2 cylinders, 80 HP)
- `"touring"`: Long-distance (4 cylinders, 120 HP)

**Methods:**
```python
specs = bike.get_specifications()
bike.translate(dx, dy, dz)
bike.simulate_movement(distance, direction=(1, 0, 0))
```

---

## Physics Module (`defect3d.physics`)

Newtonian physics simulation.

### `PhysicsSimulator`

Multi-object physics engine.

```python
from defect3d.physics import PhysicsSimulator

sim = PhysicsSimulator(gravity=(0, 0, -9.81))
```

**Methods:**

```python
# Add objects
obj_id = sim.add_object(obj, mass=1000, velocity=(0, 0, 0))

# Apply forces
sim.apply_force(obj_id, force=(100, 0, 0))

# Run simulation
states = sim.simulate(duration=2.0, dt=1/60)

# Get state
state = sim.get_state(obj_id)
# Returns: {
#   'position': array,
#   'velocity': array,
#   'acceleration': array,
#   'kinetic_energy': float,
#   'potential_energy': float,
#   'total_energy': float
# }

# Reset
sim.reset()
```

---

## Blender Integration (`defect3d.blender_integration`)

Export and rendering for Blender.

### `export_to_blender`

Export object to Blender Python script.

```python
from defect3d.blender_integration import export_to_blender

export_to_blender(obj, "output.py", json_export=True)
```

**Parameters:**
- `obj`: Object to export (Shape3D or CompositePart)
- `filename`: Output .py file path
- `json_export`: bool - Also export JSON (default: True)

### `BlenderRenderer`

Photorealistic rendering.

```python
from defect3d.blender_integration import BlenderRenderer

renderer = BlenderRenderer()
renderer.render(obj, "output.png", resolution=(1920, 1080), samples=128)
```

**Parameters:**
- `obj`: Object to render
- `output_path`: Output image file path
- `resolution`: tuple (width, height)
- `samples`: int - Ray tracing samples (quality)

---

## Internationalization (`defect3d.i18n`)

Language detection and translation.

```python
from defect3d.i18n import set_language, get_language

# Auto-detect (default)
lang = get_language()  # Returns 'es' or 'en'

# Force language
set_language('es')  # Spanish
set_language('en')  # English

# Environment variable
# export DEFECT3D_LANG=es
```

---

## Usage Examples

### Basic Shapes

```python
from defect3d import Cube, Sphere, Cylinder

# Create shapes
cube = Cube(size=2.0, position=(0, 0, 0))
cube.set_color(0.8, 0.2, 0.2)

sphere = Sphere(radius=1.5, position=(3, 0, 0))
sphere.set_color(0.2, 0.8, 0.2)

# Transform
cube.translate(1, 0, 0)
cube.rotate(0, 0, 45)
cube.set_scale(1.5, 1.5, 1.5)
```

### Composite Parts

```python
from defect3d.core import CompositePart
from defect3d import Cube, Cylinder

# Create composite
vehicle = CompositePart(name="SimpleVehicle")

# Add parts
chassis = Cube(size=1.0, position=(0, 0, 0))
vehicle.add_part(chassis)

wheel1 = Cylinder(radius=0.3, height=0.2, position=(0.5, 0.5, -0.5))
wheel2 = Cylinder(radius=0.3, height=0.2, position=(0.5, -0.5, -0.5))
vehicle.add_part(wheel1)
vehicle.add_part(wheel2)

# Set properties
vehicle.set_property("mass", 1000)
```

### Vehicles

```python
from defect3d import Car, Motorcycle

# Create car
car = Car(car_type="sports", color=(0.9, 0.1, 0.1))
specs = car.get_specifications()
print(f"Power: {specs['engine']['power']} HP")

# Create motorcycle
bike = Motorcycle(bike_type="cruiser", color=(0.1, 0.1, 0.1))
bike.simulate_movement(distance=10.0)
```

### Physics Simulation

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

# Create car and simulator
car = Car(car_type="sedan")
sim = PhysicsSimulator()

# Add to simulation
car_id = sim.add_object(car, mass=1500, velocity=(10, 0, 0))

# Apply force
sim.apply_force(car_id, force=(5000, 0, 0))

# Simulate
states = sim.simulate(duration=2.0)

# Check final state
final_state = sim.get_state(car_id)
print(f"Final position: {final_state['position']}")
print(f"Final velocity: {final_state['velocity']}")
```

### Export & Rendering

```python
from defect3d import Car
from defect3d.blender_integration import export_to_blender, BlenderRenderer

car = Car(car_type="sports")

# Export to Blender
export_to_blender(car, "my_car.py", json_export=True)

# Render to image (requires Blender)
renderer = BlenderRenderer()
renderer.render(car, "car.png", resolution=(1920, 1080), samples=128)
```

### Serialization

```python
from defect3d import Cube, Sphere
from defect3d.core.serializer import to_json, save_to_json

# Create objects
cube = Cube(size=2.0)
sphere = Sphere(radius=1.5)

# Serialize to JSON string
json_str = to_json([cube, sphere], pretty=True)
print(json_str)

# Save to file
save_to_json([cube, sphere], "objects.json")
```

---

## Type Hints

All modules use Python type hints for better IDE support:

```python
from typing import Tuple, List, Dict, Optional
import numpy as np

def my_function(
    position: Tuple[float, float, float],
    parts: List[Shape3D],
    properties: Dict[str, any],
    name: Optional[str] = None
) -> np.ndarray:
    ...
```

---

## See Also

- [README.md](../README.md) - Project overview
- [PHASES.md](../PHASES.md) - Phase implementation guide
- [USAGE.md](../USAGE.md) - Comprehensive usage guide
- [examples/](../examples/) - Working examples
