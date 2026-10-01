import bpy, math, os
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(n,c,metal=0):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=.68; return m
coral=mat('Coral enamel',(.85,.20,.12)); orange=mat('Expedition orange',(1,.43,.06)); dark=mat('Graphite',(.075,.065,.075)); rubber=mat('Tire rubber',(.11,.095,.09)); steel=mat('Steel',(.26,.29,.32),.65); glass=mat('Smoked blue glass',(.10,.19,.23),.3); cream=mat('Ivory',(.88,.85,.73)); lamp=mat('Headlight',(.75,.84,.85)); sand=mat('Sand',(.64,.52,.37)); strap=mat('Canvas straps',(.26,.23,.19))
def cube(n,loc,size,m,bev=.05):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=n; o.dimensions=size; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if bev: mod=o.modifiers.new('Soft manufactured edges','BEVEL'); mod.width=bev; mod.segments=3; o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def cyl(n,loc,r,depth,m,axis='Z',verts=32):
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=loc); o=bpy.context.object; o.name=n
 if axis=='Y': o.rotation_euler[0]=math.pi/2
 if axis=='X': o.rotation_euler[1]=math.pi/2
 o.data.materials.append(m); mod=o.modifiers.new('Edge bevel','BEVEL'); mod.width=.025; mod.segments=2; o.modifiers.new('Weighted normals','WEIGHTED_NORMAL'); return o
def rod(n,a,b,r,m):
 a,b=Vector(a),Vector(b); o=cyl(n,(a+b)/2,r,(b-a).length,m); o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o
# Front points toward negative X; four wheels with individual tread blocks.
cube('Ladder chassis',(0,0,.95),(4.7,1.55,.25),dark)
for x in [-1.55,1.5]:
 cyl('Axle',(x,0,.86),.13,2.6,steel,'Y')
 for y in [-1.18,1.18]:
  cyl('Oversize tire',(x,y,.85),.85,.55,rubber,'Y',48)
  for j in range(28):
   t=j*math.tau/28
   for offset in [-.15,.15]:
    o=cube('Chunky tread',(x+.82*math.sin(t),y+offset,.85+.82*math.cos(t)),(.25,.26,.13),rubber,.025); o.rotation_euler[1]=t; o.rotation_euler[2]=.18 if offset>0 else -.18
  side=y+(.29 if y>0 else -.29)
  cyl('Orange wheel rim',(x,side,.85),.57,.05,orange,'Y'); cyl('Steel wheel hub',(x,side+(.035 if y>0 else -.035),.85),.29,.07,steel,'Y'); cyl('Hub cap',(x,side+(.08 if y>0 else -.08),.85),.12,.08,dark,'Y')
  for j in range(6):
   t=j*math.tau/6; cyl('Wheel bolt',(x+.2*math.sin(t),side+(.08 if y>0 else -.08),.85+.2*math.cos(t)),.035,.04,dark,'Y',12)
cube('Lower body',(.35,0,1.7),(3.5,1.85,.9),coral,.12)
cube('Hood',(-1.55,0,2.03),(1.45,1.86,.45),coral,.1)
cube('Front grille',(-2.3,0,1.82),(.15,1.85,.74),coral)
for y in [-.48,-.32,-.16,0,.16,.32,.48]: cube('Grille slot',(-2.39,y,1.84),(.025,.075,.44),dark,.035)
for y in [-.76,.76]:
 cyl('Headlight bezel',(-2.4,y,2.02),.26,.14,steel,'X'); cyl('Headlight lens',(-2.48,y,2.02),.21,.03,lamp,'X')
cube('Cabin',(.45,0,2.5),(2.9,1.84,1.2),coral,.08)
cube('Windshield',(-1.035,0,2.69),(.035,1.62,.7),glass,.03)
cube('Windshield divider',(-1.06,0,2.69),(.06,.045,.72),coral,.01)
for y in [-.935,.935]:
 for x in [-.24,1.13]:
  cube('Side window',(x,y,2.72),(1.05,.035,.67),glass,.06)
  cube('Door panel',(x,y,1.97),(1.18,.045,.65),coral,.035)
  cube('Door handle',(x+.33,y*1.03,2.29),(.22,.07,.065),steel,.02)
 cube('Running board',(.35,y*1.12,1.25),(2.65,.25,.14),dark)
 cube('Wing mirror',(-.9,y*1.23,2.58),(.28,.18,.25),dark)
 for x in [-1.55,1.5]:
  cube('Fender top',(x,y*1.15,1.85),(1.65,.5,.18),dark)
  for dx in [-.72,.72]:
   o=cube('Fender sloping end',(x+dx,y*1.15,1.57),(.18,.5,.55),dark); o.rotation_euler[1]=-.4 if dx<0 else .4
cube('Ivory roof',(.43,0,3.15),(3.1,1.98,.16),cream)
cube('Front bumper',(-2.56,0,1.21),(.32,2.5,.26),dark)
cube('Winch mounting plate',(-2.65,0,1.4),(.42,.95,.18),orange)
cyl('Winch drum',(-2.72,0,1.55),.16,.6,steel,'Y')
for y in [-.38,.38]: cube('Winch end',(-2.72,y,1.55),(.32,.12,.36),orange)
rod('Recovery hook',(-2.83,0,1.57),(-2.86,0,1.19),.05,orange)
cube('Rear bumper',(2.02,0,1.22),(.28,2.15,.25),dark)
cyl('Rear spare tire',(2.18,0,2.2),.7,.4,rubber,'X'); cyl('Spare rim',(2.41,0,2.2),.43,.06,orange,'X')
# Roof rack and expedition luggage.
for y in [-.84,.84]:
 rod('Rack rail',(-1.08,y,3.35),(1.95,y,3.35),.065,dark)
 for x in [-.8,1.65]: rod('Rack foot',(x,y,3.2),(x,y,3.4),.06,dark)
for x in [-1.08,-.4,.4,1.2,1.95]: rod('Rack crossbar',(x,-.84,3.35),(x,.84,3.35),.055,dark)
cube('Orange roof duffel',(-.45,0,3.63),(1.4,1.25,.5),orange,.22)
for x in [-.85,-.05]: cube('Duffel strap',(x,0,3.65),(.075,1.28,.52),strap,.025)
cube('Rear cargo case',(1.05,0,3.61),(1.15,1.3,.44),sand,.08)
for x in [.7,1.4]: cube('Cargo strap',(x,0,3.64),(.07,1.32,.46),strap,.02)
for y in [-.64,.64]: cyl('Roof spotlight',(-1.08,y,3.51),.15,.22,dark,'X'); cyl('Roof spotlight lens',(-1.2,y,3.51),.12,.025,lamp,'X')
rod('Antenna',(1.7,.8,3.3),(1.7,.8,4.25),.018,steel)
cube('Side expedition can',(1.55,-1.02,2.63),(.48,.18,.65),orange,.08)
# Studio floor, camera and lighting.
floor=mat('Warm studio',(.83,.80,.73)); cube('Ground',(0,0,-.07),(200,200,.12),floor,.0)
world=bpy.context.scene.world; world.color=(.65,.65,.65); world.use_nodes=True; world.node_tree.nodes['Background'].inputs[0].default_value=(.7,.75,.8,1); world.node_tree.nodes['Background'].inputs[1].default_value=.45
for n,loc,power,size in [('Key',(-5,-6,9),1800,7),('Fill',(2,-1,7),900,5),('Rim',(4,5,7),1600,5)]:
 bpy.ops.object.light_add(type='AREA',location=loc); o=bpy.context.object; o.name=n; o.data.energy=power; o.data.shape='DISK'; o.data.size=size; o.rotation_euler=(Vector((0,0,1.5))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-7.5,-8,5.1)); camera=bpy.context.object; camera.rotation_euler=(Vector((0,0,1.9))-camera.location).to_track_quat('-Z','Y').to_euler(); camera.data.type='ORTHO'; camera.data.ortho_scale=8.4
scene=bpy.context.scene; scene.camera=camera; scene.render.engine='CYCLES'; scene.cycles.samples=32; scene.render.resolution_x=1400; scene.render.resolution_y=1100; scene.render.resolution_percentage=100; scene.view_settings.view_transform='AgX'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Expedition_Rover.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:
 if o.type=='MESH' and o.name!='Ground': o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'Expedition_Rover.glb'),use_selection=True)
scene.render.filepath=os.path.join(ROOT,'Expedition_Rover.png'); bpy.ops.render.render(write_still=True)
