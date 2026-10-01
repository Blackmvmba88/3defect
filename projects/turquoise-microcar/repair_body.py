"""Repair the saved model without regenerating or discarding manual edits."""
from pathlib import Path
import bpy,json,math,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from integrate_body import integrate_shell
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Turquoise_Microcar.blend'))
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
from complete_skirts import complete_skirts
report=integrate_shell();report.update(complete_skirts());collection=bpy.data.collections['MICROCAR • editable components']
report.update({'components':len(collection.objects),'finite_geometry':all(math.isfinite(c) for o in collection.objects if o.type=='MESH' for v in o.data.vertices for c in v.co),'user_source_preserved':True})
assert report['finite_geometry'];(ROOT/'validation.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Turquoise_Microcar.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in collection.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'Turquoise_Microcar.glb'),use_selection=True,export_apply=True)
scene=bpy.context.scene;scene.cycles.caustics_refractive=False;scene.cycles.caustics_reflective=False;scene.render.filepath=str(ROOT/'Turquoise_Microcar.png');scene.cycles.samples=48;bpy.ops.render.render(write_still=True)
print('INTEGRATED_BODY_VALID',report)
