# 3defect Documentation

## Overview

**3defect** is a Python-based 3D modeling system designed for creating vehicles and mechanical systems. It provides an intuitive API for building complex 3D objects from simple geometric primitives and includes integration with Blender for visualization.

## 📚 Documentation Index

- **[API Reference](API_REFERENCE.md)** - Complete API documentation for all modules
- **[Phase Guide](../PHASES.md)** - Detailed phased architecture implementation
- **[Language Support](LANGUAGE_SUPPORT.md)** - Internationalization guide
- **[Rendering Guide](RENDERING.md)** - Blender integration and rendering
- **[Usage Guide](../USAGE.md)** - Comprehensive usage examples

## Features

- **Basic 3D Shapes**: Cube, Sphere, Cylinder, Cone, Torus
- **Composite Parts**: Build complex objects from simple shapes
- **Vehicle Framework**: Pre-built car and motorcycle models
- **Physics Simulation**: Basic Newtonian physics with gravity and forces
- **Blender Integration**: Export models to Blender for visualization
- **Component Library**: Reusable parts like wheels, engines, chassis

## Installation

### Prerequisites

- Python 3.8 or higher
- NumPy
- Blender 3.6+ (optional, for visualization)

### Install from source

```bash
git clone https://github.com/Blackmvmba88/3defect.git
cd 3defect
pip install -e .
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Creating a Car

```python
from defect3d import Car
from defect3d.blender_integration import export_to_blender

# Create a sports car
sports_car = Car(car_type="sports", position=(0, 0, 0), color=(0.9, 0.1, 0.1))

# Get specifications
specs = sports_car.get_specifications()
print(f"Engine: {specs['engine']['cylinders']} cylinders")

# Export to Blender
export_to_blender(sports_car, "my_car.py")
```

### Creating a Motorcycle

```python
from defect3d import Motorcycle

# Create a sport bike
bike = Motorcycle(bike_type="sport", position=(0, 0, 0))

# Simulate movement
bike.simulate_movement(distance=10.0)
```

### Physics Simulation

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

# Create car and simulator
car = Car(car_type="sedan")
sim = PhysicsSimulator()
sim.add_object(car, mass=1500, velocity=(10, 0, 0))

# Apply force and simulate
sim.apply_force(0, (5000, 0, 0))  # Forward force
states = sim.simulate(duration=2.0)
```

## Core Concepts

### Shapes

All 3D objects inherit from the `Shape3D` base class:

- **Position**: (x, y, z) coordinates
- **Rotation**: (rx, ry, rz) in degrees
- **Scale**: (sx, sy, sz) scale factors
- **Material**: Color and appearance properties

### Composite Parts

Use `CompositePart` to build complex objects:

```python
from defect3d.core import CompositePart, Cube, Cylinder

# Create a custom object
my_object = CompositePart(name="CustomObject")
base = Cube(size=1.0, position=(0, 0, 0))
top = Cylinder(radius=0.5, height=1.0, position=(0, 0, 1))

my_object.add_part(base)
my_object.add_part(top)
```

### Vehicle Components

Pre-built components for vehicles:

- **Wheel**: Tire and rim assembly
- **Engine**: Engine block with cylinders
- **Chassis**: Vehicle frame
- **Body**: Vehicle body shell

## Examples

See the `examples/` directory for complete examples:

- `create_car.py` - Create and export a car
- `create_motorcycle.py` - Create and export a motorcycle
- `physics_simulation.py` - Physics simulation examples
- `custom_vehicle.py` - Build a custom vehicle from components

## Blender Integration

### Exporting to Blender

```python
from defect3d.blender_integration import export_to_blender

export_to_blender(my_object, "blender_script.py", also_json=True)
```

### Using in Blender

1. Open Blender
2. Switch to the Scripting workspace
3. Open the generated Python script
4. Run the script (Alt+P or click "Run Script")

The script will create all objects with proper materials and colors.

## API Reference

### Core Classes

#### `Shape3D`
Base class for all 3D shapes.

**Methods:**
- `translate(dx, dy, dz)` - Move the shape
- `rotate(rx, ry, rz)` - Rotate the shape
- `set_scale(sx, sy, sz)` - Scale the shape
- `set_color(r, g, b, a)` - Set RGBA color

#### `CompositePart`
Container for multiple shapes.

**Methods:**
- `add_part(part, relative_position)` - Add a part
- `remove_part(part)` - Remove a part
- `connect(part1, part2, type)` - Define connection between parts
- `get_bounds()` - Get bounding box

### Vehicle Classes

#### `Car`
Complete car model with 4 wheels, engine, chassis, and body.

**Parameters:**
- `car_type`: "sedan", "sports", or "suv"
- `position`: (x, y, z) position
- `color`: (r, g, b) color tuple

**Methods:**
- `get_specifications()` - Get car specs
- `simulate_movement(distance, direction)` - Move the car

#### `Motorcycle`
Complete motorcycle model with 2 wheels, engine, frame, and body.

**Parameters:**
- `bike_type`: "sport", "cruiser", or "touring"
- `position`: (x, y, z) position
- `color`: (r, g, b) color tuple

### Physics Classes

#### `PhysicsSimulator`
Simulates Newtonian physics.

**Methods:**
- `add_object(obj, mass, velocity)` - Add object to simulation
- `apply_force(obj_index, force)` - Apply force to object
- `simulate(duration, apply_gravity)` - Run simulation
- `get_kinetic_energy(obj_index)` - Calculate kinetic energy
- `get_potential_energy(obj_index)` - Calculate potential energy

## Advanced Usage

### Custom Components

Create your own reusable components:

```python
from defect3d.core import CompositePart, Cube, Cylinder

class CustomEngine(CompositePart):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(name="CustomEngine")
        # Add your parts here
        block = Cube(size=0.5, position=position)
        self.add_part(block)
```

### Mechanical Connections

Define connections between parts:

```python
composite = CompositePart("Assembly")
part1 = Cube(size=1.0)
part2 = Cylinder(radius=0.5, height=1.0)

composite.add_part(part1)
composite.add_part(part2)
composite.connect(part1, part2, connection_type="hinge")
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source. See the repository for license details.

## Acknowledgments

Built with support from GitHub Copilot and the development community.
