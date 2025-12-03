# Biomimetic Architecture Module

## Descripción / Description

Sistema completo de arquitectura biomimética inspirada en formas orgánicas naturales.
Complete biomimetic architecture system inspired by natural organic forms.

## Características / Features

### 1. Master Reference Mesh

Formatos exportables / Export formats:
- **.obj** - Wavefront OBJ con materiales MTL
- **.fbx** - Autodesk FBX (especificación)
- **.glb / .gltf** - glTF 2.0 con materiales PBR

Características del diseño / Design features:
- ✓ Forma biomimética inspirada en coral + hueso + concha
- ✓ Exoesqueleto estructural tipo "ribs" fractales
- ✓ Canalizaciones internas para ventilación tipo termitero
- ✓ Piel reactiva (panales hexagonales inspirados en hojas)
- ✓ UVs limpios y edge flow optimizado
- ✓ LOD0 + LOD1 + LOD2
- ✓ Material slots: Skin, Ribs, Vegetation, Glass

### 2. Blender Integration

Archivo generado / Generated file: **.py** (script de Python para Blender)

Incluye / Includes:
- Geometry Nodes para crecimiento fractal
- Extrusión orgánica
- Patrón fotosintético
- Shader procedural que simula:
  - Humedad
  - Recuperación solar
  - Patrón de células vivas
- Animación del "respiramiento" del edificio
- Luces atmosféricas
- Render preset (Cycles + Eevee)

### 3. Escalas Disponibles / Available Scales

| Escala | Descripción ES | Description EN | Altura / Height |
|--------|----------------|----------------|-----------------|
| **S** | Pabellón Biomimético | Biomimetic Pavilion | 8-12m |
| **M** | Centro Cultural/Museo | Cultural Center/Museum | 40-60m |
| **L** | Torre Orgánica | Organic Tower | 120-200m |
| **XL** | Megaestructura Fractal | Fractal Megastructure | 300-800m |

## Uso / Usage

### Ejemplo Básico / Basic Example

```python
from defect3d.architecture import BuildingScale, BiomimeticMesh
from defect3d.architecture.exporters import export_mesh

# Crear un edificio de escala M (Centro cultural)
# Create an M-scale building (Cultural center)
building = BiomimeticMesh(BuildingScale.M)

# Obtener especificaciones / Get specifications
specs = building.get_specifications()
print(specs)

# Exportar a OBJ / Export to OBJ
mesh = building.get_mesh()
export_mesh(mesh, "my_building.obj", format="obj")

# Exportar a GLB / Export to GLB
export_mesh(mesh, "my_building.glb", format="glb")
```

### Exportar a Blender / Export to Blender

```python
from defect3d.architecture import BuildingScale, BiomimeticMesh, get_scale_config
from defect3d.architecture.blender_integration import BlenderBiomimeticExporter

# Crear edificio / Create building
building = BiomimeticMesh(BuildingScale.L)
mesh = building.get_mesh()
config = get_scale_config(BuildingScale.L)

# Exportar script de Blender / Export Blender script
exporter = BlenderBiomimeticExporter(mesh, config)
exporter.export(
    "my_tower.py",
    include_animation=True,
    include_geometry_nodes=True
)

# Usar en Blender / Use in Blender:
# 1. Abrir Blender / Open Blender
# 2. Ir a Scripting workspace
# 3. Abrir el archivo .py / Open the .py file
# 4. Ejecutar con Alt+P / Run with Alt+P
```

### Generar LODs

```python
# Obtener diferentes niveles de detalle
# Get different levels of detail
lod0 = building.get_lod("LOD0")  # Máximo detalle / Maximum detail
lod1 = building.get_lod("LOD1")  # Detalle medio / Medium detail
lod2 = building.get_lod("LOD2")  # Bajo detalle / Low detail

# Exportar LODs / Export LODs
export_mesh(lod0, "building_LOD0.obj", format="obj")
export_mesh(lod1, "building_LOD1.obj", format="obj")
export_mesh(lod2, "building_LOD2.obj", format="obj")
```

### Ejecutar Ejemplo Completo / Run Complete Example

```bash
cd examples
python create_biomimetic_building.py
```

Esto generará / This will generate:
- Edificios en escalas S y M / Buildings in S and M scales
- Archivos OBJ, FBX, GLB para cada uno
- Scripts de Blender con animación
- 3 niveles LOD para cada edificio

## Estructura del Módulo / Module Structure

```
defect3d/architecture/
├── __init__.py              # Módulo principal / Main module
├── scales.py                # Configuración de escalas / Scale configuration
├── biomimetic_mesh.py       # Generador de malla principal / Main mesh generator
├── exoskeleton.py           # Sistema de exoesqueleto fractal / Fractal exoskeleton
├── ventilation.py           # Sistema de ventilación / Ventilation system
├── reactive_skin.py         # Piel fotosintética reactiva / Reactive photosynthetic skin
├── exporters.py             # Exportadores (OBJ/FBX/GLB) / Exporters
└── blender_integration.py   # Integración con Blender / Blender integration
```

## Características del Diseño Biomimético / Biomimetic Design Features

### Inspiración en Coral / Coral Inspiration
- Estructura ramificada y porosa
- Patrones fractales de crecimiento
- Canales internos para flujo

### Inspiración en Hueso / Bone Inspiration
- Exoesqueleto estructural resistente
- Geometría optimizada para carga
- Ligereza y resistencia combinadas

### Inspiración en Concha / Shell Inspiration
- Forma helicoidal natural
- Superficies curvas y orgánicas
- Protección y belleza estética

### Inspiración en Termiteros / Termite Mound Inspiration
- Sistema de ventilación natural
- Canales de circulación de aire
- Regulación térmica pasiva

### Inspiración en Hojas / Leaf Inspiration
- Paneles fotosintéticos hexagonales
- Superficie reactiva a la luz solar
- Capacidad de adaptación ambiental

## Materiales Incluidos / Included Materials

1. **Skin** - Piel externa biomimética
   - Roughness: 0.4
   - Metallic: 0.1
   - Color: Beige orgánico

2. **Ribs** - Costillas estructurales
   - Roughness: 0.6
   - Metallic: 0.0
   - Color: Hueso blanco

3. **Vegetation** - Paneles fotosintéticos
   - Roughness: 0.8
   - Metallic: 0.0
   - Color: Verde fotosintético
   - Subsurface: 0.3 (scattering orgánico)

4. **Glass** - Elementos transparentes
   - Roughness: 0.0
   - Metallic: 0.0
   - Transmission: 0.95
   - Color: Azul cristalino

## Próximas Funcionalidades / Future Features

- [ ] Fusion 360 parametric version (.f3d)
- [ ] Godot 4 version with shaders
- [ ] Unity HDRP version with AI
- [ ] Análisis estructural FEA
- [ ] Simulación de ventilación CFD
- [ ] Renderizado fotorrealista
- [ ] Sistema de iluminación día/noche
- [ ] VR/AR support

## Licencia / License

MIT License - Ver LICENSE en el directorio raíz / See LICENSE in root directory

## Créditos / Credits

Desarrollado con / Developed with:
- GitHub Copilot
- Inspiración en patrones naturales / Inspiration from natural patterns
- Principios de biomimética / Biomimicry principles
