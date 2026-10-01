# BLACKMAMBA 3D Ecosystem

## Purpose

BlackMamba already has multiple repositories that solve different parts of a 3D pipeline. The goal is **not** to merge everything into one monolith. The goal is to make every repository interoperable through one machine-readable contract.

The standard workflow is:

```text
IDEA
  -> CONCEPT
  -> BLUEPRINT
  -> BOM / PART LIST
  -> DIMENSIONS + TOLERANCES
  -> PART GENERATION
  -> PART VALIDATION
  -> ASSEMBLY VALIDATION
  -> MATERIALS / UV / RIG
  -> RENDER
  -> EXPORT / COMPRESSION / STREAMING
  -> MANUFACTURING GATE (only when explicitly validated)
```

A visually convincing render is **not** equivalent to an engineering-ready or manufacturing-ready asset.

---

## Core rule

Every model must answer these questions before it can be considered complete:

1. What blueprint/revision is authoritative?
2. What parts are required?
3. What are the target dimensions of every part?
4. What tolerances are allowed?
5. What interfaces/sockets must coincide?
6. Which validations passed or failed?
7. What export formats were generated?
8. Is the asset only visual, engineering-oriented, validated, or manufacturing-ready?

If measured geometry is outside tolerance, the part is **FAIL** and must not silently advance to assembly.

---

## Maturity states

```text
concept
prototype
engineering_design
validated
manufacturing_ready
```

### concept
Visual intent only. Dimensions may be approximate.

### prototype
A generated or manually modeled object exists and can be inspected/tested.

### engineering_design
Authoritative dimensions, interfaces, materials and tolerances are defined.

### validated
Automated or documented checks confirm the asset matches its declared contract.

### manufacturing_ready
Allowed only when geometry is closed and the contract includes dimensions, tolerances, material, interfaces, manufacturing process and required validation evidence.

**Never infer `manufacturing_ready` from a render, STL/GLB export, or visual similarity alone.**

---

## Repository map

### 1. `Blackmvmba88/3defect` — proposed orchestration/core 3D layer

Existing strengths:

- primitives and composite parts
- mechanical systems and vehicles
- physics
- Blender integration
- photorealistic rendering
- OBJ / FBX / GLB / glTF export infrastructure

Role in the ecosystem:

- canonical asset contract
- shared validation vocabulary
- common export/render interface
- repository registry and capability map

### 2. `Blackmvmba88/weaponassambly` — deterministic assembly patterns

Existing strengths:

- build manifests
- canonical sockets
- modular assembly
- deterministic planning/resolution
- scene manifest validation
- parametric descriptors
- extensive `Bolt` optimization work around validators/resolvers

Role in the ecosystem:

- source of reusable assembly and deterministic-validation patterns
- socket/interface contract reference
- performance patterns for hot validation paths

This repository remains domain-specific. Generic 3D infrastructure should be extracted as reusable patterns rather than making it the universal 3D core.

### 3. `Blackmvmba88/mamba-architecture` — procedural and organic geometry

Existing strengths:

- parametric design
- fractals and natural growth
- biomimetic/organic models
- mesh export including OBJ/STL/glTF

Role:

- procedural geometry provider
- organic surface and architectural generator

### 4. `Blackmvmba88/ocarine` — dimension-sensitive physical object validation

Existing strengths:

- production GLB path
- Three.js prototype visualization
- Blender/bmesh validation code
- physical/acoustic object workflow

Role:

- reference implementation for real-scale geometry validation
- proving ground for dimensions, holes, interfaces and acoustic/physical constraints

### 5. `Blackmvmba88/circuit` — component-based engineering visualization

Existing strengths:

- Blender scripts
- PCB/component visualization
- STL / OBJ / glTF / FBX export
- assembly-oriented documentation

Role:

- electronic/mechanical component visualization provider
- standardized component-library test case

### 6. `Blackmvmba88/XarvisCore` (`cybercam-blender`) — modular Blender production pipeline

Existing strengths:

- procedural assembly
- LEGO-like parts
- Blender background automation
- glTF/FBX export
- render presets / product shots

Role:

- reference for automated Blender assembly and render pipelines

### 7. `Blackmvmba88/blender-motion-capture` — real-time 3D motion transport

Existing strengths:

- WebSocket architecture
- live/replay session model
- browser 3D dashboard plan
- Blender bridge plan

Role:

- real-time transport layer for transforms, rigs and animation data

### 8. `Blackmvmba88/3dwave` — real-time procedural WebGL geometry

Existing strengths:

- WebGL 2.0
- procedural meshes
- real-time geometry buffers
- camera/light/shadow systems
- high-frequency render loop optimization

Role:

- real-time procedural visualization/render research
- GPU/WebGL optimization reference

### 9. `Blackmvmba88/Avion` — Three.js runtime and renderer

Existing strengths:

- Three.js scene/render loop
- GLB assets
- renderer/resource disposal
- platform feature detection
- network snapshot/compression settings

Role:

- browser/runtime adapter
- Three.js scene integration and runtime optimization reference

### 10. `Blackmvmba88/Patronaje` — 2D-to-3D surface generation

Existing strengths:

- 2D points to 3D mesh generation
- OBJ/STL/glTF-oriented export surface

Role:

- pattern/surface conversion provider

### 11. `Blackmvmba88/js-3d-area-explorer` — geospatial 3D environment viewer

Existing strengths:

- photorealistic 3D tiles
- Cesium camera/orbit controls
- large environment visualization

Role:

- environment/geospatial visualization adapter
- not a canonical mesh-authoring core

### 12. `Blackmvmba88/MasterSong` — mixed repository with Blender generators to extract

Detected useful 3D material:

- Blender/bmesh generation scripts
- architecture/terrain generation
- procedural landscape code

Role:

- migration source only
- reusable 3D scripts should be extracted into the appropriate 3D module rather than expanded inside a music repository

### Additional candidates

- `BlackMamba-Rod-Forge` — Blender blockout/modeling code
- `circuits-D` — planned GLTF/GLB output
- `rainboe` / `rainbow-wave-visualizer` / `Rockhero` — WebGL/Three.js visual systems that may provide rendering/shader patterns

These should remain adjacent until their reusable 3D responsibilities are explicitly identified.

---

## Canonical BlackMamba 3D asset contract

Every interoperable project should be able to emit or consume an object equivalent to:

```json
{
  "schema_version": "1.0",
  "asset_id": "BM-EXAMPLE-001",
  "revision": "A",
  "stage": "engineering_design",
  "units": "mm",
  "blueprint": {
    "id": "BP-BM-EXAMPLE-001",
    "revision": "A"
  },
  "parts": [
    {
      "part_id": "P001",
      "name": "example_part",
      "status": "validated",
      "material": "aluminum_6061",
      "dimensions": {
        "x": {"target": 120.0, "tolerance": 0.2},
        "y": {"target": 40.0, "tolerance": 0.2},
        "z": {"target": 12.0, "tolerance": 0.1}
      },
      "interfaces": ["IFACE_A"],
      "source": "generated"
    }
  ],
  "validation": {
    "dimensions": "pass",
    "interfaces": "pass",
    "closed_geometry": "unknown",
    "assembly": "pass"
  },
  "exports": ["glb"],
  "manufacturing": {
    "ready": false,
    "process": null
  }
}
```

---

## Required validation gates

### Gate A — Blueprint

- blueprint exists
- revision is explicit
- global scale/units are explicit

### Gate B — BOM

- every required part has a stable `part_id`
- no required part is silently missing
- revision/status is visible

### Gate C — Dimensions

For every critical dimension:

```text
abs(measured - target) <= tolerance
```

Anything outside tolerance is a deterministic failure.

### Gate D — Interfaces

For every connection:

- mating interface exists
- origin/axis convention matches
- position is within tolerance
- orientation is within angular tolerance
- clearance/interference rule is declared when relevant

### Gate E — Assembly

- all mandatory parts present
- no unresolved collisions where prohibited
- transforms/sockets resolve deterministically

### Gate F — Render/export

Rendering and exports are outputs, not proof of engineering validity.

Recommended targets:

- `.blend` authoring/master scene
- `.glb/.gltf` web/runtime
- `.fbx` DCC/game interchange when needed
- `.stl` mesh fabrication/prototyping only when appropriate
- render PNG/EXR

### Gate G — Manufacturing

`manufacturing.ready = true` is forbidden unless the manufacturing-specific checks for the declared process have passed.

---

## Compression and optimization layer

Optimization must be stage-specific:

```text
MASTER GEOMETRY (authoritative, loss-minimized)
    -> VALIDATED ENGINEERING COPY
    -> RUNTIME COPY / LODs
    -> COMPRESSED DELIVERY ASSET
```

Do not validate engineering dimensions against an aggressively decimated or lossy runtime mesh.

Planned runtime optimization adapters may include:

- mesh simplification / LOD generation
- quantization
- texture compression
- GLB packing
- mesh compression where supported
- instancing
- shared materials
- deterministic cache keys

Performance work from `Bolt` should be reused where semantics are preserved and benchmark evidence exists.

---

## Render standard

Every important asset should be able to produce:

1. orthographic front
2. orthographic side
3. orthographic top
4. 3/4 product view
5. exploded view when multipart
6. dimension/inspection view
7. material preview
8. final presentation render

The final render is compared against the visual concept; dimensional validation is compared against the engineering contract. They are separate checks.

---

## Migration strategy

Do not bulk-copy repositories into `3defect`.

Instead:

1. inventory reusable capability
2. define its input/output contract
3. wrap it with an adapter
4. add a fixture
5. validate deterministic output
6. then extract shared code only when duplication is proven

This keeps every project usable while gradually making the ecosystem interoperable.

---

## North-star pipeline

```text
prompt / concept image
        ↓
blueprint + dimensions
        ↓
BOM
        ↓
parametric part descriptors
        ↓
generator adapters
        ↓
geometry
        ↓
automated dimensional/interface validation
        ↓
assembly
        ↓
Blender master scene
        ↓
materials / animation / render
        ↓
GLB/FBX/STL adapters
        ↓
runtime optimization / streaming
        ↓
optional manufacturing gate
```

The goal is simple: **generate spectacular 3D assets without confusing a beautiful image with verified engineering.**
