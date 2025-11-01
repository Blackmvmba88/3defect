# Guía de Renderizado / Rendering Guide

## 🎨 Sistema de Renderizado Fotorrealista

El sistema 3defect ahora incluye capacidades de renderizado fotorrealista para generar imágenes de alta calidad de tus modelos 3D.

The 3defect system now includes photorealistic rendering capabilities to generate high-quality images of your 3D models.

---

## 🚀 Inicio Rápido / Quick Start

### Crear y Renderizar una Llanta / Create and Render a Wheel

```bash
# Ejecutar el ejemplo de llanta / Run the wheel example
python examples/renderizar_llanta.py
```

Este ejemplo crea una llanta con rin y proporciona 3 métodos para generar la imagen renderizada.

This example creates a wheel with rim and provides 3 methods to generate the rendered image.

---

## 📋 Métodos de Renderizado / Rendering Methods

### Método 1: Blender GUI (Interfaz Gráfica)

**Ventajas / Advantages:**
- Control total sobre la escena / Full control over the scene
- Ajustes en tiempo real / Real-time adjustments
- Previsualización interactiva / Interactive preview

**Pasos / Steps:**

1. Ejecutar el script de ejemplo:
   ```bash
   python examples/renderizar_llanta.py
   ```

2. Abrir Blender / Open Blender

3. Ir a la pestaña "Scripting" / Go to "Scripting" tab

4. Abrir el archivo generado: `llanta_export.py`

5. Ejecutar el script (Alt+P o botón "Run Script")

6. La llanta aparecerá en la escena

7. Para renderizar:
   - Presionar F12 para renderizar
   - Ir a "Image" > "Save As" para guardar
   - Guardar como: `llanta_renderizada.png`

### Método 2: Línea de Comandos (Blender CLI)

**Ventajas / Advantages:**
- Rápido y automático / Fast and automatic
- No requiere interfaz gráfica / No GUI required
- Ideal para scripts y automatización / Ideal for scripts and automation

**Comando / Command:**

```bash
blender --background --python examples/llanta_export.py --render-output llanta.png -f 1
```

Este comando:
- Ejecuta Blender en segundo plano / Runs Blender in background
- Carga y ejecuta el script / Loads and executes the script
- Renderiza la escena / Renders the scene
- Guarda la imagen como `llanta.png`

### Método 3: Renderizado Automático con Python

**Ventajas / Advantages:**
- Totalmente integrado con Python / Fully integrated with Python
- Control programático completo / Complete programmatic control
- Perfecto para pipelines automatizados / Perfect for automated pipelines

**Código / Code:**

```python
from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import BlenderRenderer

# Crear la llanta / Create the wheel
llanta = Wheel(radius=0.35, width=0.25)

# Crear renderizador / Create renderer
renderer = BlenderRenderer()

# Renderizar / Render
renderer.render(
    llanta,
    "llanta_renderizada.png",
    resolution=(1920, 1080),
    samples=128,
    camera_distance=1.5
)
```

**Ejecutar el script automático / Run the automatic script:**

```bash
python examples/renderizar_llanta_auto.py
```

---

## ⚙️ Configuración de Renderizado / Render Configuration

### Parámetros del Renderizador / Renderer Parameters

```python
renderer.render(
    objects,              # Objeto(s) a renderizar / Object(s) to render
    output_path,          # Ruta de salida / Output path
    resolution=(1920, 1080),  # Resolución (ancho, alto) / Resolution (width, height)
    samples=128,          # Muestras de renderizado / Render samples
    camera_distance=5.0,  # Distancia de cámara / Camera distance
    camera_angle=(60, 0, 45),  # (elevación, azimut, rotación) / (elevation, azimuth, rotation)
    save_blend=True       # Guardar archivo .blend / Save .blend file
)
```

### Calidad de Renderizado / Render Quality

| Samples | Calidad / Quality | Tiempo / Time | Uso / Use |
|---------|------------------|---------------|-----------|
| 32      | Borrador / Draft | ~30 segundos  | Pruebas rápidas / Quick tests |
| 64      | Media / Medium   | ~1 minuto     | Previsualizaciones / Previews |
| 128     | Alta / High      | ~2-3 minutos  | Uso general / General use |
| 256     | Muy Alta / Very High | ~5-10 minutos | Presentaciones / Presentations |
| 512+    | Producción / Production | 15+ minutos | Imágenes finales / Final images |

### Resoluciones Comunes / Common Resolutions

```python
# HD
resolution=(1280, 720)

# Full HD (Recomendado / Recommended)
resolution=(1920, 1080)

# 2K
resolution=(2560, 1440)

# 4K
resolution=(3840, 2160)
```

---

## 📸 Configuración de Cámara / Camera Configuration

### Ángulos de Cámara / Camera Angles

```python
# Vista frontal / Front view
camera_angle=(0, 0, 0)

# Vista isométrica (Recomendado) / Isometric view (Recommended)
camera_angle=(45, 0, 30)

# Vista superior / Top view
camera_angle=(90, 0, 0)

# Vista lateral / Side view
camera_angle=(0, 90, 0)
```

### Distancia de Cámara / Camera Distance

```python
# Primer plano / Close-up
camera_distance=1.0

# Medio / Medium (Recomendado para llantas / Recommended for wheels)
camera_distance=1.5

# Alejado / Far
camera_distance=3.0

# Vista completa / Full view
camera_distance=5.0
```

---

## 💡 Iluminación / Lighting

El sistema incluye iluminación profesional de 3 puntos automática:

The system includes automatic 3-point professional lighting:

1. **Luz Principal / Main Light**: Luz solar intensa / Intense sun light
2. **Luz de Relleno / Fill Light**: Luz de área suave / Soft area light
3. **Luz Trasera / Back Light**: Luz puntual para contornos / Point light for contours

### Personalizar Iluminación / Custom Lighting

Edita el script generado para ajustar:

Edit the generated script to adjust:

```python
# Luz principal / Main light
main_light.data.energy = 3.0  # Aumentar para más brillante / Increase for brighter

# Luz de relleno / Fill light
fill_light.data.energy = 500  # Ajustar suavidad / Adjust softness

# Luz trasera / Back light
back_light.data.energy = 1000  # Ajustar contorno / Adjust rim lighting
```

---

## 🎨 Materiales y Texturas / Materials and Textures

### Materiales Predefinidos / Predefined Materials

El sistema incluye materiales realistas:

The system includes realistic materials:

- **Goma / Rubber**: Negro mate para llantas / Matte black for tires
- **Metal / Metal**: Plateado brillante para rines / Shiny silver for rims
- **Pintura / Paint**: Colores personalizables para carrocerías / Customizable colors for bodies

### Personalizar Colores / Custom Colors

```python
from defect3d.vehicles.components import Wheel

# Crear llanta / Create wheel
llanta = Wheel(radius=0.35, width=0.25)

# Cambiar color del rin / Change rim color
for part in llanta.parts:
    if part.name == "Rim":
        part.set_color(1.0, 0.8, 0.0)  # Dorado / Gold
```

---

## 🖼️ Formatos de Salida / Output Formats

### Formato de Imagen / Image Format

Por defecto: PNG (sin pérdida, transparencia)

Default: PNG (lossless, transparency)

Otros formatos disponibles editando el script:

Other formats available by editing the script:

```python
# En el script de Blender / In the Blender script
bpy.context.scene.render.image_settings.file_format = 'PNG'  # PNG
bpy.context.scene.render.image_settings.file_format = 'JPEG'  # JPEG
bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'  # EXR (HDR)
```

---

## 🔧 Requisitos del Sistema / System Requirements

### Software Requerido / Required Software

1. **Blender 3.6 o superior** / **Blender 3.6 or higher**
   - Descargar de: https://www.blender.org/download/
   - Versión recomendada: 4.0+

2. **Python 3.8+**
   - Con NumPy instalado / With NumPy installed

### Hardware Recomendado / Recommended Hardware

| Componente | Mínimo / Minimum | Recomendado / Recommended |
|------------|------------------|---------------------------|
| CPU | Dual-core | Quad-core+ |
| RAM | 4 GB | 8 GB+ |
| GPU | Integrada / Integrated | NVIDIA/AMD dedicada |
| Disco / Disk | 2 GB libre / free | 5 GB+ libre / free |

### Configuración de Blender / Blender Configuration

**Para usar GPU (más rápido) / To use GPU (faster):**

1. Abrir Blender / Open Blender
2. Edit > Preferences > System
3. Cycles Render Devices > seleccionar GPU
4. Guardar preferencias / Save preferences

---

## 📝 Ejemplos Completos / Complete Examples

### Ejemplo 1: Llanta Simple / Simple Wheel

```python
from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import render_to_image

llanta = Wheel(radius=0.35, width=0.25)
render_to_image(llanta, "mi_llanta.png")
```

### Ejemplo 2: Coche Completo / Complete Car

```python
from defect3d import Car
from defect3d.blender_integration import BlenderRenderer

coche = Car(car_type="sports", color=(0.9, 0.1, 0.1))

renderer = BlenderRenderer()
renderer.render(
    coche,
    "coche_deportivo.png",
    resolution=(2560, 1440),
    samples=256,
    camera_distance=8.0,
    camera_angle=(30, 0, 45)
)
```

### Ejemplo 3: Múltiples Vistas / Multiple Views

```python
from defect3d.vehicles.components import Wheel
from defect3d.blender_integration import BlenderRenderer

llanta = Wheel(radius=0.35, width=0.25)
renderer = BlenderRenderer()

# Vista frontal / Front view
renderer.render(llanta, "llanta_frontal.png", 
                camera_angle=(0, 0, 0))

# Vista lateral / Side view
renderer.render(llanta, "llanta_lateral.png", 
                camera_angle=(0, 90, 0))

# Vista isométrica / Isometric view
renderer.render(llanta, "llanta_isometrica.png", 
                camera_angle=(45, 0, 30))
```

---

## ⚠️ Solución de Problemas / Troubleshooting

### Blender no encontrado / Blender not found

**Problema:** "Blender no encontrado"

**Solución:**

1. Instalar Blender desde https://www.blender.org
2. Añadir Blender al PATH del sistema
3. O especificar la ruta manualmente:

```python
renderer = BlenderRenderer(blender_path="/ruta/a/blender")
```

### Renderizado muy lento / Rendering too slow

**Soluciones:**

1. Reducir samples: `samples=64` o `samples=32`
2. Reducir resolución: `resolution=(1280, 720)`
3. Usar GPU en las preferencias de Blender
4. Cerrar otras aplicaciones

### Imagen muy oscura / Image too dark

**Solución:**

Aumentar la energía de las luces en el script:

```python
main_light.data.energy = 5.0  # Valor por defecto: 3.0
```

### Imagen muy clara / Image too bright

**Solución:**

Reducir la energía de las luces:

```python
main_light.data.energy = 1.5  # Valor por defecto: 3.0
```

---

## 🎓 Mejores Prácticas / Best Practices

1. **Usar resolución Full HD** para un buen balance calidad/velocidad
   **Use Full HD resolution** for a good quality/speed balance

2. **Empezar con 64-128 samples** para pruebas
   **Start with 64-128 samples** for tests

3. **Guardar el archivo .blend** para ediciones futuras
   **Save the .blend file** for future edits

4. **Probar diferentes ángulos de cámara** para encontrar la mejor vista
   **Try different camera angles** to find the best view

5. **Ajustar distancia de cámara** según el tamaño del objeto
   **Adjust camera distance** based on object size

---

## 📚 Recursos Adicionales / Additional Resources

- [Documentación de Blender](https://docs.blender.org)
- [Tutorial de Cycles Render](https://docs.blender.org/manual/en/latest/render/cycles/)
- [Blender Python API](https://docs.blender.org/api/current/)

---

**¡Disfruta creando imágenes fotorrealistas de tus modelos 3D!**

**Enjoy creating photorealistic images of your 3D models!**

🎨✨🚗🏍️
