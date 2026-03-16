# 3defect

Un sistema de modelado 3D para crear vehículos y sistemas mecánicos con detección automática de idioma.

**A 3D modeling system for creating vehicles and mechanical systems with automatic language detection.**

## ✨ Características

- **🌍 Detección Automática de Idioma**: El sistema detecta tu idioma y se adapta automáticamente
- **🎨 Formas 3D Primitivas**: Cubo, Esfera, Cilindro, Cono, Toroide
- **🏗️ Partes Compuestas**: Construye ensamblajes mecánicos complejos desde formas simples
- **🚗 Framework de Vehículos**: Modelos pre-construidos de coches (sedán, deportivo, SUV)
- **🏍️ Soporte de Motocicletas**: Motos deportivas, cruceros y de turismo
- **⚙️ Sistemas de Motor**: Motores personalizables con múltiples cilindros
- **🔧 Componentes Mecánicos**: Ruedas, chasis, bastidores y carrocerías
- **🎯 Simulación Física**: Gravedad, fuerzas, velocidad y cálculos de energía
- **🎬 Integración con Blender**: Exporta modelos directamente a Blender para visualización
- **📸 Renderizado Fotorrealista**: Genera imágenes renderizadas de alta calidad automáticamente

> 📸 **[¡Mira el ejemplo de foto renderizada aquí!](docs/EXAMPLE_RENDER.md)** - See the rendered photo example!

## 🚀 Inicio Rápido

### Instalación

```bash
git clone https://github.com/Blackmvmba88/3defect.git
cd 3defect
pip install -r requirements.txt
```

### Crear Tu Primer Coche

```python
from defect3d import Car
from defect3d.blender_integration import export_to_blender

# Crear un coche deportivo
# Create a sports car
deportivo = Car(car_type="sports", color=(0.9, 0.1, 0.1))

# Obtener especificaciones (en tu idioma)
# Get specifications (in your language)
specs = deportivo.get_specifications()
print(f"Motor: {specs['motor']['potencia']} HP")

# Exportar a Blender
# Export to Blender
export_to_blender(deportivo, "mi_coche.py")
```

### Crear una Motocicleta

```python
from defect3d import Motorcycle

# Crear una moto deportiva
# Create a sport bike
moto = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))

# Simular movimiento
# Simulate movement
moto.simulate_movement(distance=10.0)
print(f"Nueva posición: {moto.position}")
```

### Renderizar a Imagen Fotorrealista

```python
from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import BlenderRenderer

# Crear llanta con rin
llanta = Wheel(radius=0.35, width=0.25)

# Renderizar a imagen de alta calidad
renderer = BlenderRenderer()
renderer.render(llanta, "llanta.png", resolution=(1920, 1080), samples=128)
```

**📸 [¡Mira aquí la foto renderizada! / See the rendered photo here →](docs/EXAMPLE_RENDER.md)**

## 🌍 Sistema de Idiomas

### Detección Automática

El sistema detecta automáticamente el idioma de tu sistema operativo:

```python
from defect3d import Car

# El sistema detecta automáticamente español o inglés
# The system automatically detects Spanish or English
coche = Car(car_type="sedan")
specs = coche.get_specifications()

# Si tu sistema está en español, verás:
# If your system is in Spanish, you'll see:
# {'tipo': 'sedan', 'dimensiones': {...}, 'motor': {...}}

# Si tu sistema está en inglés, verás:
# If your system is in English, you'll see:
# {'type': 'sedan', 'dimensions': {...}, 'engine': {...}}
```

### Forzar Idioma Manualmente

```python
from defect3d.i18n import set_language

# Forzar español / Force Spanish
set_language('es')

# Forzar inglés / Force English
set_language('en')
```

### Variable de Entorno

```bash
# Establecer idioma mediante variable de entorno
# Set language via environment variable
export DEFECT3D_LANG=es  # para español / for Spanish
export DEFECT3D_LANG=en  # para inglés / for English
```

## 📚 Ejemplos

Ejecuta los ejemplos incluidos:

```bash
# Crear un coche y exportar a Blender
# Create a car and export to Blender
python examples/create_car.py

# Crear una motocicleta
# Create a motorcycle
python examples/create_motorcycle.py

# Demo de simulación física
# Physics simulation demo
python examples/physics_simulation.py

# Ejemplo completo en español
# Complete example in Spanish
python examples/ejemplo_español.py
```

## 🎯 Lo Que Puedes Construir

- 🚗 **Coches**: Sedanes, deportivos, SUVs con colores personalizables
- 🏍️ **Motocicletas**: Motos deportivas, cruceros, motos de turismo
- ⚙️ **Motores**: Motores de 2, 4, 6 cilindros con proporciones realistas
- 🛞 **Vehículos Personalizados**: Construye desde componentes (ruedas, chasis, bastidores)
- 🎢 **Sistemas Mecánicos**: Ensamblajes con conexiones y restricciones
- 📊 **Simulaciones Físicas**: Movimiento, gravedad, fuerzas y energía

## 🔬 Simulación Física

```python
from defect3d import Car
from defect3d.physics import PhysicsSimulator

# Crear coche y añadir a simulación
# Create car and add to simulation
coche = Car(car_type="sedan")
sim = PhysicsSimulator()
sim.add_object(coche, mass=1500, velocity=(10, 0, 0))

# Aplicar fuerza de motor
# Apply driving force
sim.apply_force(0, (5000, 0, 0))

# Ejecutar simulación
# Run simulation
estados = sim.simulate(duration=2.0)
```

## 🎬 Visualización en Blender

1. Ejecuta cualquier script de ejemplo para generar archivo de exportación
2. Abre Blender
3. Cambia al espacio de trabajo Scripting
4. Abre el archivo `.py` generado
5. Ejecuta el script (Alt+P)
6. ¡Tu modelo 3D aparecerá!

## 📖 Documentación

Documentación completa disponible en:

- [Documentación Completa](docs/README.md) (inglés/español)
- [Guía de Uso](docs/USAGE.md) (bilingüe)
- Referencia de API
- Ejemplos de Uso Avanzado

## 🏗️ Estructura del Proyecto

```
3defect/
├── defect3d/                  # Paquete principal
│   ├── core/                  # Formas 3D y composites
│   ├── vehicles/              # Implementaciones de coches y motos
│   ├── physics/               # Simulación física
│   ├── blender_integration/   # Funcionalidad de exportación
│   └── i18n/                  # Sistema de internacionalización
├── examples/                  # Scripts de ejemplo
├── docs/                      # Documentación
└── requirements.txt           # Dependencias
```

## 🌟 Características de Idioma

El sistema es completamente bilingüe (español/inglés) con:

- ✅ Detección automática del idioma del sistema
- ✅ Todas las salidas adaptadas al idioma
- ✅ Especificaciones de vehículos localizadas
- ✅ Mensajes de error y advertencias traducidos
- ✅ Ejemplos en ambos idiomas
- ✅ Documentación bilingüe
- ✅ Configuración manual del idioma
- ✅ Variable de entorno para control

## 🔧 Calidad de Código y Validación

Este proyecto incluye una herramienta completa de validación y reparación para mantener alta calidad de código.

### Validación Rápida
```bash
# Verificar calidad del código
python validate_and_fix.py --check-only

# Reparar problemas automáticamente
python validate_and_fix.py --fix
```

### Estado Actual
- ✅ 0 Errores de sintaxis
- ✅ 0 Problemas de estilo (flake8)
- ✅ 9.87/10 puntuación pylint (¡Excelente!)
- ✅ 0 Problemas de seguridad

**📚 Para guía detallada:** Ver [docs/VALIDATION.md](docs/VALIDATION.md) y [docs/QUICKSTART_VALIDATION.md](docs/QUICKSTART_VALIDATION.md)

## 🤝 Contribuir

Las contribuciones son bienvenidas! Siéntete libre de:

- Reportar bugs
- Sugerir características
- Enviar pull requests
- Mejorar documentación
- Añadir más traducciones
- Ejecutar `python validate_and_fix.py --fix` antes de hacer commit

## 🎉 Agradecimientos

Construido con pasión y soporte de:
- GitHub Copilot
- La comunidad de código abierto
- Fundación Blender

## 📄 Licencia

Licencia MIT - Libre de usar, modificar y distribuir

---

**Hecho con ❤️ para desarrolladores de habla hispana y la comunidad 3D**

**Made with ❤️ for Spanish-speaking developers and the 3D community**

¡Diviértete creando! / Have fun creating! 🚗🏍️✨
