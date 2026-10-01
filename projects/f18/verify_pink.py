import bpy,hashlib,json,math
from pathlib import Path
p=Path(__file__).resolve().parent
def signature(o):
 return hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(f.vertices) for f in o.data.polygons],list(map(tuple,o.matrix_world)))).encode()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(p/'F18_continuado.blend'))
before={o.name:signature(o) for o in bpy.data.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(p/'F18_rosa_serigrafiado.blend'))
changed=[n for n,h in before.items() if n not in bpy.data.objects or signature(bpy.data.objects[n])!=h]
decals=bpy.data.collections['SERIGRAFIA_ROSA • editable'].objects
assert len(decals)==66
assert all(math.isfinite(c) for o in decals for v in o.data.vertices for c in v.co)
r={'original_meshes_and_transforms_unchanged':len(before)-len(changed),'changed_original_objects':changed,'original_preservation_passed':not changed,'screenprinted_elements':len(decals),'finite_geometry':True,'file_reopened':True}
(p/'pink_validation.json').write_text(json.dumps(r,indent=2));print(r)

if changed:
 raise SystemExit("Original preservation check failed: " + ", ".join(changed))
