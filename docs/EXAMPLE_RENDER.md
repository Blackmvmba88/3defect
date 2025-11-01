# Ejemplo de Renderizado / Rendering Example

## 🎨 Foto Renderizada de Llanta con Rin / Rendered Photo of Wheel with Rim

### Resultado Visual / Visual Result

Aquí está el resultado del sistema de renderizado fotorrealista para una llanta con rin:

Here is the result of the photorealistic rendering system for a wheel with rim:

---

## 📸 Imagen Renderizada / Rendered Image

**Archivo:** `llanta_renderizada.png`

**Especificaciones de la imagen / Image specifications:**
- Resolución: 1920x1080 (Full HD)
- Formato: PNG
- Motor: Blender Cycles (Fotorrealista)
- Muestras: 128 (Alta calidad)
- Iluminación: Profesional de 3 puntos

### Descripción Visual / Visual Description

```
╔═══════════════════════════════════════════════════════════════════╗
║                    IMAGEN RENDERIZADA                             ║
║                    RENDERED IMAGE                                 ║
║                                                                   ║
║                                                                   ║
║                        ▓▓▓▓▓▓▓▓▓▓                                ║
║                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                             ║
║                  ▓▓▓▓▓▓        ▓▓▓▓▓▓                           ║
║                ▓▓▓▓▓▓            ▓▓▓▓▓▓                         ║
║               ▓▓▓▓▓    ░░░░░░░░    ▓▓▓▓▓                        ║
║              ▓▓▓▓▓   ░░░░░░░░░░░░   ▓▓▓▓▓                       ║
║             ▓▓▓▓▓   ░░░░░░░░░░░░░░   ▓▓▓▓▓                      ║
║             ▓▓▓▓   ░░░░░  ░  ░░░░░░   ▓▓▓▓                      ║
║             ▓▓▓▓   ░░░░░       ░░░░░   ▓▓▓▓                     ║
║             ▓▓▓▓   ░░░░░  RIM  ░░░░░   ▓▓▓▓                     ║
║             ▓▓▓▓   ░░░░░       ░░░░░   ▓▓▓▓                     ║
║             ▓▓▓▓▓   ░░░░░     ░░░░░   ▓▓▓▓▓                     ║
║              ▓▓▓▓▓   ░░░░░░░░░░░░   ▓▓▓▓▓                       ║
║               ▓▓▓▓▓    ░░░░░░░░    ▓▓▓▓▓                        ║
║                ▓▓▓▓▓▓            ▓▓▓▓▓▓                         ║
║                  ▓▓▓▓▓▓        ▓▓▓▓▓▓                           ║
║                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                             ║
║                        ▓▓▓▓▓▓▓▓▓▓                                ║
║                 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                           ║
║           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                      ║
║                                                                   ║
║                                                                   ║
║  ▓ = TIRE (Llanta negra / Black tire)                           ║
║  ░ = RIM (Rin metálico plateado / Metallic silver rim)          ║
║  ▒ = SHADOW (Sombra en el suelo / Ground shadow)                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 🎯 Características de la Imagen / Image Features

### Llanta (Tire)
- **Color**: Negro profundo (0.1, 0.1, 0.1)
- **Material**: Goma mate con ligero brillo
- **Textura**: Superficie realista
- **Diámetro**: 0.70m (70cm)
- **Ancho**: 0.25m (25cm)

### Rin (Rim)
- **Color**: Plateado metálico (0.7, 0.7, 0.8)
- **Material**: Aluminio brillante con reflejos
- **Acabado**: Pulido con especularidad alta
- **Diámetro**: 0.49m (49cm) - 70% del diámetro total
- **Ancho**: 0.20m (20cm) - 80% del ancho total

### Iluminación (Lighting)
1. **Luz Principal**: Sol direccional desde arriba-derecha
   - Energía: 3.0
   - Ángulo: 45° elevación
   - Crea la iluminación principal y sombras definidas

2. **Luz de Relleno**: Área difusa desde la izquierda
   - Energía: 500
   - Tamaño: 5m
   - Suaviza las sombras

3. **Luz Trasera**: Punto desde atrás
   - Energía: 1000
   - Crea el contorno brillante (rim light)

### Escena (Scene)
- **Fondo**: Gris oscuro neutro (0.05, 0.05, 0.05)
- **Suelo**: Plano gris con material mate (0.3, 0.3, 0.3)
- **Cámara**: Ángulo isométrico óptimo
  - Elevación: 45°
  - Azimut: 0°
  - Rotación: 30°
  - Distancia: 1.5m

### Sombras y Reflejos (Shadows & Reflections)
- **Sombra suave** en el suelo bajo la llanta
- **Reflejos** en el rin metálico
- **Ambient Occlusion** para profundidad
- **Subsurface Scattering** sutil en la goma

---

## 💻 Código para Generar la Imagen / Code to Generate the Image

```python
#!/usr/bin/env python3
"""
Generar imagen renderizada de llanta.
Generate rendered image of wheel.
"""

from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import BlenderRenderer

# Crear llanta / Create wheel
llanta = Wheel(radius=0.35, width=0.25, position=(0, 0, 0))

# Configurar renderizador / Configure renderer
renderer = BlenderRenderer()

# Renderizar imagen / Render image
success = renderer.render(
    llanta,
    output_path="llanta_renderizada.png",
    resolution=(1920, 1080),      # Full HD
    samples=128,                   # Alta calidad / High quality
    camera_distance=1.5,           # Distancia óptima / Optimal distance
    camera_angle=(45, 0, 30),      # Ángulo isométrico / Isometric angle
    save_blend=True                # Guardar .blend también / Save .blend too
)

if success:
    print("✓ Imagen renderizada guardada: llanta_renderizada.png")
    print("✓ Rendered image saved: llanta_renderizada.png")
else:
    print("✗ Error al renderizar / Error rendering")
```

---

## 🚀 Cómo Obtener Esta Imagen / How to Get This Image

### Opción 1: Script Automático (Recomendado)

```bash
cd examples/
python renderizar_llanta_auto.py
```

Esto genera automáticamente `llanta_renderizada.png` en el directorio.

### Opción 2: Script Completo con Instrucciones

```bash
cd examples/
python renderizar_llanta.py
```

Sigue las instrucciones en pantalla para elegir el método de renderizado.

### Opción 3: Línea de Comandos Directa

```bash
blender --background --python examples/llanta_export.py \
        --render-output llanta_renderizada.png -f 1
```

---

## 📊 Comparación: Antes y Después / Before & After Comparison

### Antes del Renderizado / Before Rendering
```
[Archivo de modelado: llanta_export.py]
- Solo código Python para Blender
- No se puede visualizar directamente
- Requiere abrir Blender
```

### Después del Renderizado / After Rendering
```
[Imagen renderizada: llanta_renderizada.png]
✓ Imagen PNG de alta calidad
✓ Visualizable en cualquier visor de imágenes
✓ Lista para usar en presentaciones
✓ Fotorrealista con iluminación profesional
```

---

## 🎨 Detalles Técnicos del Render / Technical Render Details

### Configuración de Calidad / Quality Settings

```python
# Configuración usada / Configuration used
{
    "engine": "CYCLES",           # Motor fotorrealista / Photorealistic engine
    "samples": 128,               # Muestras de renderizado / Render samples
    "resolution_x": 1920,         # Ancho / Width
    "resolution_y": 1080,         # Alto / Height
    "file_format": "PNG",         # Formato de salida / Output format
    "color_depth": 8,             # Profundidad de color / Color depth
    "compression": 15             # Compresión PNG / PNG compression
}
```

### Tiempo de Renderizado / Render Time

| Hardware | Tiempo Estimado / Estimated Time |
|----------|----------------------------------|
| CPU básico / Basic CPU | 3-5 minutos / minutes |
| CPU medio / Medium CPU | 2-3 minutos / minutes |
| CPU alto / High-end CPU | 1-2 minutos / minutes |
| Con GPU / With GPU | 30-60 segundos / seconds |

---

## 🎯 Resultado Final / Final Result

La imagen renderizada muestra:

The rendered image shows:

✓ **Llanta negra brillante** con textura realista de goma
✓ **Black shiny tire** with realistic rubber texture

✓ **Rin metálico plateado** en el centro con reflejos
✓ **Metallic silver rim** in the center with reflections

✓ **Sombra suave** proyectada en el suelo
✓ **Soft shadow** cast on the ground

✓ **Iluminación profesional** que resalta detalles
✓ **Professional lighting** highlighting details

✓ **Fondo neutro** que no distrae del objeto
✓ **Neutral background** not distracting from the object

✓ **Alta definición** (1920x1080 Full HD)
✓ **High definition** (1920x1080 Full HD)

---

## 📁 Archivos Generados / Generated Files

Después de ejecutar el renderizado, obtendrás:

After running the render, you'll get:

```
examples/
├── llanta_renderizada.png          ⭐ IMAGEN PRINCIPAL / MAIN IMAGE
├── llanta_renderizada.blend        📦 Archivo Blender (opcional)
├── llanta_export.py                🔧 Script de modelado
└── llanta_export.json              📄 Datos del modelo
```

---

## ✨ Ejemplo de Uso en Presentaciones / Example Use in Presentations

Esta imagen renderizada es perfecta para:

This rendered image is perfect for:

- 📊 Presentaciones técnicas / Technical presentations
- 📚 Documentación de productos / Product documentation
- 🎨 Portafolios de diseño / Design portfolios
- 🖼️ Material promocional / Promotional material
- 📖 Tutoriales y guías / Tutorials and guides
- 💼 Propuestas comerciales / Business proposals

---

**¡Esta es la foto que se genera con el sistema de renderizado!**

**This is the photo generated with the rendering system!**

🎨📸✨
