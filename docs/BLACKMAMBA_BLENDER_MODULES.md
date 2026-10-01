# BLACKMAMBA Blender Modular Layer

## Goal

Turn Blender into a BlackMamba modular construction surface: select an object, apply a module, edit parameters, preview the result immediately, save a preset, and continue composing larger systems.

The user-facing rule is simple:

```text
CREATE -> MATERIAL -> FORM -> MECHANICS -> ASSEMBLY -> ANIMATION -> PHYSICS -> WORLD -> OUTPUT
```

This layer is not a replacement for the BlackMamba 3D asset contract. It is the interactive authoring layer that feeds it.

## Object / system / world hierarchy

### Object

A reusable part such as a cube, wheel, spring, bolt, gear, panel or crystal.

### System

A functional composition such as a suspension, drivetrain, door, robot mechanism or steering assembly.

### World

A scene-scale composition such as a garage, castle, road, city, forest, laboratory or stage.

Keeping these levels separate prevents the UI from collapsing into thousands of unrelated buttons.

---

## Canonical modules

### `create`

Primitive and reusable part creation.

Initial actions:

- cube
- sphere
- cylinder
- plane
- tube
- spring
- bolt
- gear

### `material`

Instant visual treatment of the selected object.

Initial presets:

- metallic
- brushed metal
- chrome
- pearlescent
- iridescent
- holographic
- transparent
- glass
- plastic
- rubber
- carbon fiber
- wood
- stone
- water
- emissive / neon

Every material implementation should expose a common editable surface where applicable:

```text
base_color
roughness
metallic
transmission
ior
emission
normal_strength
scale
opacity
```

The expected interaction is deliberately direct:

```text
select cube
-> Material
-> Iridescent
-> Apply
-> immediate preview
```

### `form`

Non-destructive shape refinement and deformation.

- bevel
- smooth
- subdivision
- solidify
- mirror
- array
- boolean
- twist
- bend
- taper

### `mechanics`

Mechanical subsystems. The first canonical family is suspension.

```text
mechanics
├── suspension
├── drivetrain
├── motion
└── structure
```

### `assembly`

Composition and interface operations.

- parent
- constraint
- align
- snap
- bolt join
- interface match
- tolerance verification

### `animation`

Reusable movement behaviors.

- rotate
- translate
- oscillate
- bounce
- compression
- loop
- keyframe
- driver
- camera orbit

### `physics`

- gravity
- collision
- rigid body
- soft body
- cloth
- fluid
- particles
- spring/damper behavior

### `world`

Scene templates and environments.

- technical floor
- studio
- industrial room
- garage
- track
- castle
- sci-fi lab
- anime scene

### `output`

- preview render
- turntable
- final render
- wireframe
- exploded view
- blueprint view
- GLB
- FBX
- OBJ
- STL

---

## Suspension module

Suspension is a system module, not one button.

```text
Suspension
├── Architecture
├── Spring
├── Damper
├── Arms
├── Steering
├── Wheel Hub
├── Constraints
├── Motion
├── Test
└── Blueprint
```

Initial architecture presets:

- MacPherson
- double wishbone
- multilink
- trailing arm
- pushrod
- hydraulic
- pneumatic

Suggested editable parameters:

```text
track_width
ride_height
spring_length
spring_radius
damper_length
upper_arm_length
lower_arm_length
travel
steering_angle
compression_limit
extension_limit
```

The implementation must preserve the distinction between a visual suspension preset and an engineering-validated suspension. Dimensional and manufacturing claims continue to pass through the ecosystem validation gates.

---

## Module contract

Every BlackMamba Blender module should satisfy five properties:

1. **Clear action** — it creates or modifies something explicit.
2. **Editable parameters** — the result is not a dead asset when parametric behavior is appropriate.
3. **Immediate preview** — the user can see the effect quickly.
4. **Preset support** — useful configurations can be saved and reapplied.
5. **Composition** — the result can be consumed by other modules.

Visibility must be controllable independently when practical:

```text
👁 Material
👁 Suspension
👁 Armature
👁 FX
👁 Lights
```

Turning a module off for inspection must not silently delete its underlying data.

---

## UI direction

The Blender sidebar should expose the module tree instead of Blender implementation details:

```text
BLACKMAMBA
├── Create
├── Material
├── Form
├── Mechanics
├── Assembly
├── Animation
├── Physics
├── World
└── Output
```

Example material panel:

```text
Preset        [ Iridescent v ]
Base Color    [ ... ]
Roughness     [-----o---]
Metallic      [-------o-]
Transmission  [--o------]
Scale         [----o----]

[ Apply ] [ Random ] [ Save Preset ]
```

Example suspension panel:

```text
Type              [ Double Wishbone v ]
Track Width       [ 1380 mm ]
Travel            [ 160 mm ]
Spring Length     [ 320 mm ]
Damper Length     [ 360 mm ]
Steering Angle    [ 32 deg ]

[ Generate ] [ Update ] [ Motion Test ]
```

---

## Preset naming

Presets are reusable BlackMamba assets, not hidden UI state.

Example material presets:

```text
BM Metal Black
BM Iridescent Oil
BM Pearl White
BM Toxic Neon
BM Glass Green
```

Example suspension presets:

```text
BM Street Sport
BM Formula
BM Baja
BM Monster
BM Lowrider Hydraulic
```

Presets should eventually serialize to a stable format so the same settings can be consumed by Blender, web UI and automation agents.

---

## Implementation order

### Phase 1 — visible payoff

- Create: cube, sphere, cylinder
- Material: metallic, pearlescent, iridescent, transparent
- Form: bevel, subdivision, smooth
- module sidebar
- preset serialization

### Phase 2 — mechanical primitives

- spring generator
- damper generator
- control-arm generator
- interface/snap primitives

### Phase 3 — first complete system

- double-wishbone suspension
- steering links
- travel constraints
- motion test
- blueprint/inspection view

### Phase 4 — ecosystem expansion

- drivetrains
- vehicles
- buildings
- castles
- cute cars
- motorcycles
- robots
- anime tools
- VFX

---

## Architectural boundary

The module vocabulary lives in `defect3d/blender_integration/module_registry.py` and intentionally does not import `bpy`.

Blender-specific operators can implement those module identifiers behind the registry. This lets tests, web interfaces and orchestration code understand the same BlackMamba vocabulary without requiring Blender to be installed.

The contract is therefore:

```text
UI / Agent / Web
      ↓
BlackMamba module_id + parameters
      ↓
Module registry
      ↓
Blender adapter / generator / validator
      ↓
BlackMamba 3D asset contract
```

That keeps the user experience simple while preserving the existing engineering/validation boundary.
