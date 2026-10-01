import bpy,json,math,bmesh
from pathlib import Path
p=Path(__file__).resolve().parent
assert len(bpy.data.collections['ORIGINAL_BACKUP'].objects)==2
assert bpy.data.collections['ORIGINAL_BACKUP'].hide_render
report={'meshes':0,'vertices':0,'new_closed_meshes':{},'original_backup':True,'reference_packed':any(i.packed_file for i in bpy.data.images),'glb_bytes':(p/'F18_continuado.glb').stat().st_size}
for o in bpy.data.objects:
 if o.type!='MESH' or o.name.startswith('Cylinder'):continue
 assert all(math.isfinite(x) for v in o.data.vertices for x in v.co)
 report['meshes']+=1;report['vertices']+=len(o.data.vertices)
 if o.name in ['Fuselage_continued','Canopy','Engine_fairing_L','Engine_fairing_R','Radome']:
  bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);bm.free();assert bad==0,(o.name,bad);report['new_closed_meshes'][o.name]=True
(p/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
