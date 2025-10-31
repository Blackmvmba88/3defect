# 3defect

Un sistema de modelado 3D para crear vehículos y sistemas mecánicos.

A 3D modeling system based on basic geometric shapes, using Blender as an artistic communication interface.

## ✨ Features

- **🎨 3D Shape Primitives**: Cube, Sphere, Cylinder, Cone, Torus
- **🏗️ Composite Parts**: Build complex mechanical assemblies from simple shapes
- **🚗 Vehicle Framework**: Pre-built car models (sedan, sports, SUV)
- **🏍️ Motorcycle Support**: Sport bikes, cruisers, and touring motorcycles
- **⚙️ Engine Systems**: Customizable engines with multiple cylinders
- **🔧 Mechanical Components**: Wheels, chassis, frames, and body parts
- **🎯 Physics Simulation**: Gravity, forces, velocity, and energy calculations
- **🎬 Blender Integration**: Export models directly to Blender for visualization
- **🌍 Real-world Physics**: Simulate movement with Earth's gravitational forces

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Blackmvmba88/3defect.git
cd 3defect
pip install -r requirements.txt
```

### Create Your First Car

```python
from defect3d import Car
from defect3d.blender_integration import export_to_blender

# Create a sports car
sports_car = Car(car_type="sports", color=(0.9, 0.1, 0.1))

# Get specifications
specs = sports_car.get_specifications()
print(f"Engine: {specs['engine']['power']} HP")

# Export to Blender
export_to_blender(sports_car, "my_car.py")
```

### Create a Motorcycle

```python
from defect3d import Motorcycle

# Create a sport bike
bike = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))

# Simulate movement
bike.simulate_movement(distance=10.0)
print(f"New position: {bike.position}")
```

## 📚 Examples

Run the included examples:

```bash
# Create a car and export to Blender
python examples/create_car.py

# Create a motorcycle
python examples/create_motorcycle.py

# Physics simulation demo
python examples/physics_simulation.py

# Build a custom vehicle
python examples/custom_vehicle.py
```

## 🎯 What You Can Build

- 🚗 **Cars**: Sedans, sports cars, SUVs with customizable colors
- 🏍️ **Motorcycles**: Sport bikes, cruisers, touring bikes
- ⚙️ **Engines**: 2, 4, 6 cylinder engines with realistic proportions
- 🛞 **Custom Vehicles**: Build from components (wheels, chassis, frames)
- 🎢 **Mechanical Systems**: Assemblies with connections and constraints
- 📊 **Physics Simulations**: Movement, gravity, forces, and energy

## 🔬 Physics Simulation

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

# Create car and add to simulation
car = Car(car_type="sedan")
sim = PhysicsSimulator()
sim.add_object(car, mass=1500, velocity=(10, 0, 0))

# Apply driving force
sim.apply_force(0, (5000, 0, 0))

# Run simulation
states = sim.simulate(duration=2.0)
```

## 🎬 Blender Visualization

1. Run any example script to generate a Blender export file
2. Open Blender
3. Switch to the Scripting workspace
4. Open the generated `.py` file
5. Run the script (Alt+P)
6. Your 3D model will appear!

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Full Documentation](docs/README.md)
- API Reference
- Advanced Usage Examples
- Component Library

## 🏗️ Project Structure

```
3defect/
├── defect3d/                  # Main package
│   ├── core/                  # Core 3D shapes and composites
│   ├── vehicles/              # Car and motorcycle implementations
│   ├── physics/               # Physics simulation
│   └── blender_integration/   # Blender export functionality
├── examples/                  # Example scripts
├── docs/                      # Documentation
└── requirements.txt           # Dependencies
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 🎉 Acknowledgments

Built with passion and support from:
- GitHub Copilot
- The open-source community
- Blender Foundation

¡Diviértete creando! / Have fun creating!

---

**Made with ❤️ for the 3D modeling community**
