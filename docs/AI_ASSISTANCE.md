# 🔽 NIVEL 8 — ASISTENCIA DE IA (Diseño Semántico) / LEVEL 8 — AI ASSISTANCE (Semantic Design)

## Descripción / Description

**ES:** El nivel más alto del sistema 3defect. Utiliza etiquetas semánticas y planos maestros (blueprints) para permitir que modelos de IA y prompts de lenguaje natural generen piezas mecánicas complejas sin necesidad de especificar coordenadas manuales.

**EN:** The highest level of the 3defect system. It uses semantic tags and blueprints to allow AI models and natural language prompts to generate complex mechanical parts without the need for manual coordinate specification.

## Componentes Clave / Key Components

### 1. Etiquetas Semánticas / Semantic Tags
Todas las formas y piezas ahora pueden tener etiquetas que describen su función.
All shapes and parts can now have tags describing their function.

```python
from defect3d import Cube
box = Cube()
box.add_tag("housing")
box.add_tag("protective_layer")
```

### 2. Arquitecto de IA / AI Architect
El puente entre conceptos y geometría.
The bridge between concepts and geometry.

```python
from defect3d.ai import AIArchitect

architect = AIArchitect()
# Crear mediante concepto semántico / Create via semantic concept
arm = architect.design("mechanical arm", segments=4)
```

### 3. Búsqueda Semántica / Semantic Search
Encontrar partes por su función, no por su nombre de variable.
Finding parts by their function, not by variable name.

```python
# Encontrar todas las articulaciones / Find all joints
joints = architect.get_parts_by_tag(arm, "joint")
```

## Flujo de Trabajo / Workflow

1.  **Prompt**: "Diseña un brazo robótico de 3 segmentos".
2.  **Architect**: Traduce el prompt a la llamada `create_mechanical_arm(segments=3)`.
3.  **Blueprints**: Proporcionan la receta geométrica con etiquetas semánticas.
4.  **Output**: Un objeto `CompositePart` listo para simulación o exportación.

## Ejemplo de Uso / Usage Example

```bash
python examples/ai_assisted_design.py
```

## Objetivo / Objective

**ES:** Hacer que el diseño 3D sea accesible mediante lenguaje natural, permitiendo que la IA sea un co-diseñador activo en el proceso de ingeniería.

**EN:** Make 3D design accessible via natural language, allowing AI to be an active co-designer in the engineering process.
