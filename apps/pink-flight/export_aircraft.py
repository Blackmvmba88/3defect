import bpy
from mathutils import Matrix,Vector
from pathlib import Path
bpy.ops.wm.open_mainfile(filepath=str(Path(__file__).resolve().parents[2]/'projects/f18/F18_rosa_serigrafiado.blend'))
frame=bpy.data.objects['Fuselage_continued'].matrix_world.inverted();dg=bpy.context.evaluated_depsgraph_get()
rotation=Matrix(((0,-1,0),(0,0,1),(-1,0,0)))
buckets={}
for o in list(bpy.context.scene.objects):
 if o.type!='MESH' or o.name.startswith('Cylinder'):continue
 ev=o.evaluated_get(dg);me=ev.to_mesh()
 for face in me.polygons:
  mat=me.materials[face.material_index] if me.materials else None
  name=mat.name if mat else 'default';b=buckets.setdefault(name,{'v':[],'f':[],'mat':mat});base=len(b['v'])
  b['v'].extend([rotation@(frame@o.matrix_world@me.vertices[i].co-Vector((1.77,0,.8)))*.23 for i in face.vertices]);b['f'].append(tuple(range(base,base+len(face.vertices))))
 ev.to_mesh_clear()
bpy.ops.object.select_all(action='DESELECT')
for name,b in buckets.items():
 me=bpy.data.meshes.new('Game_'+name);me.from_pydata(b['v'],[],b['f']);me.update();o=bpy.data.objects.new('Game_'+name,me);bpy.context.scene.collection.objects.link(o);o.select_set(True)
 m=bpy.data.materials.new('PBR_'+name);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=b['mat'].diffuse_color if b['mat'] else (.8,.1,.5,1)
 n.inputs['Metallic'].default_value=.5;n.inputs['Roughness'].default_value=.29
 if 'Canopy' in name:n.inputs['Base Color'].default_value=(.36,.025,.016,1);n.inputs['Metallic'].default_value=.85;n.inputs['Roughness'].default_value=.17
 me.materials.append(m)
 for p in me.polygons:p.use_smooth='INK' not in name
bpy.ops.export_scene.gltf(filepath=str(Path(__file__).resolve().parent/'public/models/f18-pink.glb'),export_format='GLB',use_selection=True,export_yup=False)
print('EXPORTED',len(buckets),'material batches')
