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
- Mechanics > Suspension > Damper:
  - body diameter and length
  - rod diameter
  - stroke
  - mount outer/bore diameters and width
  - extension preview from 0 to 100%
  - grouped body, rod and mount geometry under one BlackMamba root object
  - collapsed/current/extended eye-to-eye dimensions stored as metadata
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

## Damper dimension contract

The damper runtime is a telescopic concept assembly with an explicit travel state:

- `body_diameter`, `body_length`
- `rod_diameter`
- `stroke`
- `mount_outer_diameter`, `mount_bore_diameter`, `mount_width`
- `extension_fraction` in the closed interval 0..1

It derives:

- travel = stroke × extension fraction
- collapsed eye-to-eye center distance
- current eye-to-eye center distance
- extended eye-to-eye center distance
- current exposed rod length

The body is centered on local Z; the two mount centers define the primary damper interface line for later suspension assembly and travel testing.

Both Spring and Damper objects remain maturity=`concept`. They are not automatically manufacturing-ready. Material, tolerances, loads, rates/valving, seals, fatigue, end geometry and fabrication process remain separate engineering gates.

## Install

Zip the `blackmamba_3d` directory itself so the archive contains:

```text
blackmamba_3d/
├── __init__.py
├── damper_math.py
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
7. Confirm a `BM_Spring` curve is created and that changing dimensions changes its measurable envelope.
8. Under `Mechanics > Suspension > Damper`, set body/rod/stroke/mount dimensions and move the Extension slider.
9. Click `Add Damper` and confirm a grouped `BM_Damper` assembly appears at the 3D cursor.
10. Generate the damper again at 0% and 100% extension and verify the eye-to-eye delta equals the requested stroke.

## Architecture

The installable add-on is intentionally a thin Blender runtime adapter. The canonical ecosystem vocabulary and engineering boundaries remain documented in:

- `docs/BLACKMAMBA_3D_ECOSYSTEM.md`
- `docs/BLACKMAMBA_BLENDER_MODULES.md`
- `defect3d/blender_integration/module_registry.py`

The next runtime slice is the control-arm generator, followed by double-wishbone composition and suspension travel testing.
