# BlackMamba 3D Blender Add-on

This folder contains the directly installable runtime slice of the BlackMamba modular Blender layer.

## Included now

- BLACKMAMBA sidebar in the 3D View
- Create: Cube, Sphere, Cylinder
- Material one-click presets:
  - Metallic
  - Pearlescent
  - Iridescent
  - Transparent
- Form:
  - Bevel with editable width/segments
  - Smooth
  - Subdivision with editable level
- Mechanics > Suspension > Spring:
  - wire diameter
  - coil centerline diameter
  - free length
  - turns
  - generated as a real 3D beveled curve
  - BlackMamba component metadata stored on the object for later assembly/validation
- automatic switch to Material Preview after applying a material
- idempotent named modifiers (`BM_Bevel`, `BM_Subdivision`) so repeated clicks update instead of stacking accidental duplicates

## Spring dimension contract

The spring runtime uses explicit dimensions rather than a visual-only scale guess:

- `wire_diameter`: physical wire thickness
- `coil_diameter`: helix centerline diameter
- `free_length`: overall axial envelope including the wire radius at both ends
- `turns`: complete helical revolutions

From those inputs the runtime derives:

- inner diameter = coil diameter - wire diameter
- outer diameter = coil diameter + wire diameter
- centerline span = free length - wire diameter
- pitch = centerline span / turns

The generated object is still maturity=`concept`. It is not automatically manufacturing-ready; material, tolerances, end-coil design, loads, spring rate, fatigue and process validation remain separate engineering gates.

## Install

Zip the `blackmamba_3d` directory itself so the archive contains:

```text
blackmamba_3d/
├── __init__.py
├── materials.py
├── mechanics.py
└── spring_math.py
```

Then in Blender use the Add-ons/Extensions install-from-disk workflow for your Blender version and select the ZIP.

After enabling it:

```text
3D View -> N sidebar -> BLACKMAMBA
```

## Smoke test

1. Click `Cube`.
2. Click `Iridescent`.
3. The viewport should switch to Material Preview and the cube should show an angle-dependent rainbow surface.
4. Click `Bevel` and adjust Bevel Width / Segments.
5. Click `Subdivision`.
6. Under `Mechanics > Suspension > Spring`, set dimensions and click `Add Spring`.
7. Confirm a `BM_Spring` curve is created and that changing dimensions on the next generated spring changes its measurable envelope.

## Architecture

The installable add-on is intentionally a thin Blender runtime adapter. The canonical ecosystem vocabulary and engineering boundaries remain documented in:

- `docs/BLACKMAMBA_3D_ECOSYSTEM.md`
- `docs/BLACKMAMBA_BLENDER_MODULES.md`
- `defect3d/blender_integration/module_registry.py`

The next runtime slice after the spring is the damper generator, followed by control arms, double-wishbone composition and suspension travel testing.
