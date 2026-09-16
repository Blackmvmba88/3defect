# BlackMamba 3D Blender Add-on

This folder contains the first directly installable runtime slice of the BlackMamba modular Blender layer.

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
- automatic switch to Material Preview after applying a material
- idempotent named modifiers (`BM_Bevel`, `BM_Subdivision`) so repeated clicks update instead of stacking accidental duplicates

## Install

Zip the `blackmamba_3d` directory itself so the archive contains:

```text
blackmamba_3d/
├── __init__.py
└── materials.py
```

Then in Blender use the Add-ons/Extensions install-from-disk workflow for your Blender version and select the ZIP.

After enabling it:

```text
3D View -> N sidebar -> BLACKMAMBA
```

## First smoke test

1. Click `Cube`.
2. Click `Iridescent`.
3. The viewport should switch to Material Preview and the cube should show an angle-dependent rainbow surface.
4. Click `Bevel` and adjust Bevel Width / Segments.
5. Click `Subdivision`.

## Architecture

The installable add-on is intentionally a thin Blender runtime adapter. The canonical ecosystem vocabulary and engineering boundaries remain documented in:

- `docs/BLACKMAMBA_3D_ECOSYSTEM.md`
- `docs/BLACKMAMBA_BLENDER_MODULES.md`
- `defect3d/blender_integration/module_registry.py`

The next runtime slice is the first mechanics implementation: spring + damper primitives, followed by double-wishbone suspension composition and travel testing.
