"""Validation gates for the Chibi Kei Hot-Rod P0 silhouette."""
import bpy, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
car = bpy.data.collections.get('CHIBI KEI HOTROD • P0 silhouette')
assert car is not None, 'Missing vehicle collection'

meshes = [o for o in car.objects if o.type == 'MESH']
assert meshes, 'No mesh objects found'

finite = all(math.isfinite(c) for o in meshes for v in o.data.vertices for c in v.co)
assert finite, 'Non-finite geometry detected'

required = {
    'Body mass',
    'Front vertical nose',
    'Rear thick mass',
    'Cabin lower',
    'Roof cap',
    'Windshield mass',
    'Front splitter',
    'Rear mini spoiler',
    'Front grille',
}
names = {o.name for o in car.objects}
missing = sorted(required - names)
assert not missing, f'Missing required silhouette objects: {missing}'

# Bounding-box gate: compact but tall.
coords = []
for o in meshes:
    for corner in o.bound_box:
        p = o.matrix_world @ __import__('mathutils').Vector(corner)
        coords.append(p)
xs=[p.x for p in coords]; ys=[p.y for p in coords]; zs=[p.z for p in coords]
dims = {
    'length': max(xs)-min(xs),
    'width': max(ys)-min(ys),
    'height': max(zs)-min(zs),
}
ratios = {
    'height_to_length': dims['height']/dims['length'],
    'width_to_length': dims['width']/dims['length'],
}
assert ratios['height_to_length'] > .48, ratios
assert ratios['width_to_length'] > .50, ratios

report = {
    'status':'passed',
    'mesh_objects':len(meshes),
    'finite_geometry':finite,
    'dimensions':dims,
    'ratios':ratios,
    'required_objects':sorted(required),
}
(ROOT/'verify_report.json').write_text(json.dumps(report, indent=2))
print('CHIBI_KEI_HOTROD_VERIFY', json.dumps(report))
