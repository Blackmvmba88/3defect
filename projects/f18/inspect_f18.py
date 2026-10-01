import bpy
if bpy.context.object and bpy.context.object.mode != "OBJECT": bpy.ops.object.mode_set(mode="OBJECT")

from mathutils import Vector
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=1100;s.render.resolution_y=800;s.render.resolution_percentage=100
s.display.shading.light='STUDIO';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True
bpy.ops.object.camera_add(location=(15,-19,18));c=bpy.context.object;c.rotation_euler=(Vector((2,0,4.8))-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=17;s.camera=c
from pathlib import Path
s.render.filepath=str(Path(__file__).resolve().parent/'before.png');bpy.ops.render.render(write_still=True)
