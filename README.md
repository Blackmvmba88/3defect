# 3defect

Un sistema de modelado 3D para crear vehículos y sistemas mecánicos con **detección automática de idioma**.

A 3D modeling system based on basic geometric shapes, using Blender as an artistic communication interface with **automatic language detection**.

> 🌍 **¡Ahora en Español! / Now in Spanish!** - El sistema detecta automáticamente tu idioma y se adapta completamente. [Ver README en Español](README_ES.md)

## ✨ Features

- **🌍 Automatic Language Detection**: Detects your system language and adapts completely (Spanish/English)
- **🎨 3D Shape Primitives**: Cube, Sphere, Cylinder, Cone, Torus
- **🏗️ Composite Parts**: Build complex mechanical assemblies from simple shapes
- **🚗 Vehicle Framework**: Pre-built car models (sedan, sports, SUV)
- **🏍️ Motorcycle Support**: Sport bikes, cruisers, and touring motorcycles
- **⚙️ Engine Systems**: Customizable engines with multiple cylinders
- **🔧 Mechanical Components**: Wheels, chassis, frames, and body parts
- **🎯 Physics Simulation**: Gravity, forces, velocity, and energy calculations
- **🎬 Blender Integration**: Export models directly to Blender for visualization
- **📸 Photorealistic Rendering**: Generate high-quality rendered images automatically
- **🌍 Real-world Physics**: Simulate movement with Earth's gravitational forces

> 📸 **[Ver ejemplo de foto renderizada / See rendered photo example](docs/EXAMPLE_RENDER.md)** - ¡Mira el resultado del sistema de renderizado!

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

### Render to Photorealistic Image

```python
from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import BlenderRenderer

# Create wheel with tire and rim
wheel = Wheel(radius=0.35, width=0.25)

# Render to high-quality image
renderer = BlenderRenderer()
renderer.render(wheel, "wheel.png", resolution=(1920, 1080), samples=128)
```

**📸 [See the rendered result / Ver el resultado renderizado →](docs/EXAMPLE_RENDER.md)**

## 🌍 Language Support / Soporte de Idiomas

The system **automatically detects your system language** and adapts all outputs, messages, and specifications accordingly.

**El sistema detecta automáticamente el idioma de tu sistema** y adapta todas las salidas, mensajes y especificaciones.

### Automatic Detection / Detección Automática

```python
from defect3d import Car

# System automatically detects language
# El sistema detecta automáticamente el idioma
car = Car(car_type="sedan")
specs = car.get_specifications()

# Spanish system shows / Sistema en español muestra:
# {'tipo': 'sedan', 'dimensiones': {...}, 'motor': {...}}

# English system shows / Sistema en inglés muestra:
# {'type': 'sedan', 'dimensions': {...}, 'engine': {...}}
```

### Manual Language Control / Control Manual del Idioma

```python
from defect3d.i18n import set_language

# Force Spanish / Forzar español
set_language('es')

# Force English / Forzar inglés
set_language('en')
```

### Environment Variable / Variable de Entorno

```bash
# Set via environment / Establecer mediante variable
export DEFECT3D_LANG=es  # Spanish / Español
export DEFECT3D_LANG=en  # English / Inglés
```

## 📚 Examples / Ejemplos

Run the included examples:

```bash
# Create a car and export to Blender (auto-detects language)
python examples/create_car.py

# Create a motorcycle (auto-detects language)
python examples/create_motorcycle.py

# Physics simulation demo
python examples/physics_simulation.py

# Build a custom vehicle
python examples/custom_vehicle.py

# Complete example in Spanish / Ejemplo completo en español
python examples/ejemplo_español.py

# Run all levels demo
python examples/demo_7_levels.py
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

## 🔧 Code Quality & Validation

This project includes a comprehensive validation and repair tool to maintain high code quality.

### Quick Validation
```bash
# Check code quality
python validate_and_fix.py --check-only

# Fix issues automatically
python validate_and_fix.py --fix
```

### Current Status
- ✅ 0 Syntax errors
- ✅ 0 Style issues (flake8)
- ✅ 9.87/10 pylint score (Excellent!)
- ✅ 0 Security issues

**📚 For detailed guide:** See [VALIDATION.md](docs/VALIDATION.md) and [QUICKSTART_VALIDATION.md](docs/QUICKSTART_VALIDATION.md)

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation
- Run `python validate_and_fix.py --fix` before committing

## 🎉 Acknowledgments

Built with passion and support from:
- GitHub Copilot
- The open-source community
- Blender Foundation

¡Diviértete creando! / Have fun creating!

---

**Made with ❤️ for the 3D modeling community**
