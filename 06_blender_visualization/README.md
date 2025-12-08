# 🔽 NIVEL 6 — EXPORTACIÓN ARTÍSTICA (Blender + render) / LEVEL 6 — ARTISTIC EXPORT (Blender + render)

## Descripción / Description

**ES:** Cualquier sistema puede renderizarse, animarse, documentarse, convertirse en diseño técnico y presentarse como cine mecánico. Aquí la mecánica se vuelve arte.

**EN:** Any system can be rendered, animated, documented, converted to technical design and presented as mechanical cinema. Here mechanics becomes art.

## Exportación a Blender / Blender Export

### Exportar Script Python / Export Python Script

```python
from defect3d import Car
from defect3d.blender_integration import export_to_blender

# Crear objeto / Create object
coche = Car(car_type="sports", color=(0.9, 0.1, 0.1))

# Exportar a script Blender / Export to Blender script
export_to_blender(coche, "mi_coche.py")

# Luego en Blender / Then in Blender:
# 1. Abrir Blender / Open Blender
# 2. Ir a 'Scripting' / Go to 'Scripting'
# 3. Abrir mi_coche.py / Open mi_coche.py
# 4. Ejecutar (Alt+P) / Run (Alt+P)
```

### Exportar JSON / Export JSON

```python
from defect3d.core.serializer import to_json, save_json

# Exportar a JSON / Export to JSON
json_data = to_json(coche)
save_json(json_data, "mi_coche.json")
```

## Renderizado Fotorrealista / Photorealistic Rendering

### Render Básico / Basic Render

```python
from defect3d import Wheel
from defect3d.blender_integration import BlenderRenderer

# Crear objeto / Create object
rueda = Wheel(radius=0.35, width=0.25)

# Renderizar / Render
renderer = BlenderRenderer()
renderer.render(
    rueda,
    output_file="rueda.png",
    resolution=(1920, 1080),
    samples=128
)
```

### Parámetros de Renderizado / Render Parameters

```python
renderer.render(
    obj=mi_objeto,
    output_file="salida.png",
    resolution=(1920, 1080),  # Full HD
    samples=128,              # Calidad (más = mejor) / Quality (more = better)
    engine='CYCLES'           # Motor de render / Render engine
)
```

## Capacidades / Capabilities

### 1. Renderizarse / Be Rendered

```python
# Generar imagen fotorrealista / Generate photorealistic image
renderer.render(coche, "coche_render.png", samples=256)
```

### 2. Animarse / Be Animated

```python
# Exportar con keyframes (futuro) / Export with keyframes (future)
# export_animation(coche, "coche_animado.py", frames=120)

# Ejemplo de concepto / Concept example:
from defect3d.blender_integration import export_to_blender

# Crear varias poses / Create several poses
poses = []
for i in range(10):
    coche_pose = Car(car_type="sports")
    coche_pose.position = (i * 2, 0, 0)
    poses.append(coche_pose)

# Exportar secuencia / Export sequence
# (Implementación manual por ahora / Manual implementation for now)
```

### 3. Documentarse / Be Documented

```python
# Generar vistas técnicas / Generate technical views
# - Vista frontal / Front view
# - Vista lateral / Side view
# - Vista superior / Top view

from defect3d import Car

coche = Car(car_type="sedan")
specs = coche.get_specifications()

# Guardar especificaciones / Save specifications
import json
with open("especificaciones.json", "w") as f:
    json.dump(specs, f, indent=2)
```

### 4. Convertirse en Diseño Técnico / Become Technical Design

```python
# Planos técnicos con dimensiones / Technical blueprints with dimensions
# (Renderizar con overlays de medidas / Render with measurement overlays)

def create_technical_drawing(vehicle, output="plano.png"):
    """Crear plano técnico / Create technical drawing"""
    # Vista ortográfica / Orthographic view
    # Líneas de dimensión / Dimension lines
    # Anotaciones / Annotations
    pass
```

### 5. Presentarse como Cine Mecánico / Present as Mechanical Cinema

```python
# Secuencia cinematográfica / Cinematic sequence
# - Cámara en movimiento / Moving camera
# - Iluminación dramática / Dramatic lighting
# - Efectos visuales / Visual effects

from defect3d.blender_integration import BlenderRenderer

renderer = BlenderRenderer()

# Render con iluminación cinematográfica / Render with cinematic lighting
renderer.render(
    coche,
    "coche_cinematico.png",
    resolution=(2560, 1440),  # 2K
    samples=512,              # Alta calidad / High quality
)
```

## Formatos de Salida / Output Formats

### Imágenes / Images
- PNG (sin pérdida / lossless)
- JPEG (comprimido / compressed)
- EXR (alta precisión / high precision)

### 3D
- Blender Python Script (.py)
- JSON (estructura de datos / data structure)
- OBJ (futuro / future)
- STL (futuro para impresión 3D / future for 3D printing)

### Animación / Animation
- MP4 (video)
- GIF (animación simple / simple animation)
- Secuencia de imágenes / Image sequence

## Ejemplo Completo de Galería / Complete Gallery Example

```python
from defect3d import Car, Motorcycle
from defect3d.blender_integration import BlenderRenderer
import os

# Crear galería de renders / Create render gallery
vehiculos = [
    ("sedan", Car(car_type="sedan")),
    ("sports", Car(car_type="sports")),
    ("suv", Car(car_type="suv")),
    ("sport_bike", Motorcycle(bike_type="sport")),
    ("cruiser", Motorcycle(bike_type="cruiser")),
]

renderer = BlenderRenderer()
os.makedirs("galeria", exist_ok=True)

for nombre, vehiculo in vehiculos:
    print(f"Renderizando {nombre}...")
    renderer.render(
        vehiculo,
        f"galeria/{nombre}.png",
        resolution=(1920, 1080),
        samples=128
    )

print("✅ Galería completa / Gallery complete!")
```

## Objetivo / Objective

**ES:** Aquí la mecánica se vuelve arte. Tus diseños técnicos se convierten en imágenes hermosas que comunican tanto la función como la forma.

**EN:** Here mechanics becomes art. Your technical designs become beautiful images that communicate both function and form.

## Ver También / See Also

- **Nivel 5 / Level 5:** `05_physics_sim/` - Simular antes de renderizar
- **Nivel 7 / Level 7:** `07_evolutionary_design/` - Optimizar diseños
- **Ejemplos / Examples:**
  - `06_blender_visualization/example_basic.py` - Exportación básica
  - `06_blender_visualization/example_render.py` - Renderizado
  - Referencia: `examples/renderizar_llanta.py` - Render de rueda
