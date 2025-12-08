# 🔽 NIVEL 1 — GEOMETRÍA (átomos) / LEVEL 1 — GEOMETRY (atoms)

## Descripción / Description

**ES:** Formas básicas 3D que son los átomos de construcción de toda la mecánica. Estas primitivas geométricas tienen propiedades físicas y pueden combinarse para crear estructuras complejas.

**EN:** Basic 3D shapes that are the building blocks of all mechanics. These geometric primitives have physical properties and can be combined to create complex structures.

## Formas Básicas / Basic Shapes

### Cubo / Cube
```python
from defect3d import Cube

# Crear un cubo / Create a cube
cubo = Cube(size=2.0, position=(0, 0, 0))
cubo.set_color(0.8, 0.2, 0.2, 1.0)  # Rojo / Red
```

### Esfera / Sphere
```python
from defect3d import Sphere

# Crear una esfera / Create a sphere
esfera = Sphere(radius=1.5, position=(3, 0, 0))
esfera.set_color(0.2, 0.8, 0.2, 1.0)  # Verde / Green
```

### Cilindro / Cylinder
```python
from defect3d import Cylinder

# Crear un cilindro / Create a cylinder
cilindro = Cylinder(radius=1.0, height=3.0, position=(6, 0, 0))
cilindro.set_color(0.2, 0.2, 0.8, 1.0)  # Azul / Blue
```

### Cono / Cone
```python
from defect3d import Cone

# Crear un cono / Create a cone
cono = Cone(radius=1.0, height=2.5, position=(9, 0, 0))
cono.set_color(0.8, 0.8, 0.2, 1.0)  # Amarillo / Yellow
```

### Toro / Torus
```python
from defect3d import Torus

# Crear un toro / Create a torus
toro = Torus(major_radius=1.5, minor_radius=0.5, position=(12, 0, 0))
toro.set_color(0.8, 0.2, 0.8, 1.0)  # Magenta
```

## Propiedades / Properties

### Volumen / Volume
Cada forma calcula su volumen geométrico / Each shape calculates its geometric volume:

```python
cubo = Cube(size=2.0)
print(f"Volumen del cubo / Cube volume: {cubo.volume()}")  # 8.0

esfera = Sphere(radius=1.0)
print(f"Volumen de la esfera / Sphere volume: {esfera.volume()}")  # ~4.19
```

### Masa y Densidad / Mass and Density
Las formas pueden tener masa y densidad / Shapes can have mass and density:

```python
# Densidad del acero: 7850 kg/m³ / Steel density: 7850 kg/m³
cubo = Cube(size=1.0)
cubo.density = 7850
masa = cubo.volume() * cubo.density
print(f"Masa / Mass: {masa} kg")
```

### Transformaciones / Transformations
Todas las formas soportan transformaciones / All shapes support transformations:

```python
from defect3d import Cube

cubo = Cube(size=2.0)

# Trasladar / Translate
cubo.translate(5, 0, 0)

# Rotar / Rotate (en grados / in degrees)
cubo.rotate(0, 45, 0)

# Escalar / Scale
cubo.set_scale(2, 1, 1)
```

### Unión y Composición / Union and Composition
Las formas pueden combinarse en partes compuestas / Shapes can be combined into composite parts:

```python
from defect3d import CompositePart, Cube, Cylinder

# Crear una pieza compuesta / Create a composite part
pieza = CompositePart(name="mi_pieza")

base = Cube(size=3.0, position=(0, 0, 0))
columna = Cylinder(radius=0.5, height=5.0, position=(0, 0, 2.5))

pieza.add_part(base)
pieza.add_part(columna)
```

### Tolerancia / Tolerance
El sistema maneja tolerancias en las transformaciones / The system handles tolerances in transformations:

```python
import math

# Comparación con tolerancia / Comparison with tolerance
TOLERANCE = 1e-6

def are_equal(a, b, tolerance=TOLERANCE):
    return abs(a - b) < tolerance
```

## API Completa / Complete API

### Shape3D (Clase Base / Base Class)

Todas las formas heredan de `Shape3D` / All shapes inherit from `Shape3D`:

```python
class Shape3D:
    """Forma 3D base / Base 3D shape"""
    
    # Constructor
    def __init__(self, position=(0, 0, 0)):
        """Inicializar forma / Initialize shape"""
    
    # Propiedades / Properties
    position: tuple[float, float, float]
    rotation: tuple[float, float, float]
    scale: tuple[float, float, float]
    color: tuple[float, float, float, float]
    density: float  # kg/m³
    
    # Métodos / Methods
    def volume(self) -> float:
        """Calcular volumen / Calculate volume"""
    
    def translate(self, dx: float, dy: float, dz: float):
        """Mover la forma / Move the shape"""
    
    def rotate(self, rx: float, ry: float, rz: float):
        """Rotar la forma (grados) / Rotate the shape (degrees)"""
    
    def set_scale(self, sx: float, sy: float, sz: float):
        """Escalar la forma / Scale the shape"""
    
    def set_color(self, r: float, g: float, b: float, a: float = 1.0):
        """Establecer color RGBA / Set RGBA color"""
    
    def to_dict(self) -> dict:
        """Exportar a diccionario / Export to dictionary"""
```

## Objetivo / Objective

**ES:** Tener átomos geométricos bien definidos para construir mecánica real. Estas primitivas son la base de todo: engranajes, ejes, cilindros de motor, ruedas, etc.

**EN:** Have well-defined geometric atoms to build real mechanics. These primitives are the foundation of everything: gears, shafts, engine cylinders, wheels, etc.

## Ver También / See Also

- **Ejemplos / Examples:** `01_geometry/example_basic.py`
- **Ejemplo Blender / Blender Example:** `01_geometry/example_blender.py`
- **Test Físico / Physics Test:** `01_geometry/example_physics.py`
- **Nivel 2 / Level 2:** `02_clock_mechanisms/` - Usar estos átomos para crear engranajes / Use these atoms to create gears
