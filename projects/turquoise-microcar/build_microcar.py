"""Detailed stylized microcar, built from curved shells and separate trim."""
import bpy, math, json, struct
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
CAR=bpy.data.collections.new('MICROCAR • editable components'); bpy.context.scene.collection.children.link(CAR)
def car(o):
 for c in list(o.users_collection): c.objects.unlink(o)
 CAR.objects.link(o); return o
def material(name,c,metal=0,rough=.3):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough; return m
paint=material('Turquoise clearcoat',(.012,.48,.58),.25,.3); paint.node_tree.nodes['Principled BSDF'].inputs['Coat Weight'].default_value=.5
blue=material('Deep turquoise trim',(.008,.22,.30),.4,.26); chrome=material('Polished silver',(.63,.72,.78),.9,.2); seal=material('Rubber window seals',(.008,.013,.025),0,.48); tire=material('Soft black tires',(.022,.026,.045),0,.66); seat=material('Indigo upholstery',(.022,.045,.23),0,.6); stitch=material('Seat piping',(.05,.17,.43),0,.5); dash=material('Dashboard',(.014,.037,.075),0,.5); amber=material('Amber indicator',(.95,.28,.016),.15,.2); ivory=material('License ivory',(.93,.85,.74)); black=material('Lettering',(.008,.014,.026))
glass=material('Tinted optical glass',(.72,.82,.94),0,.025); g=glass.node_tree.nodes['Principled BSDF']; g.inputs['Transmission Weight'].default_value=1; g.inputs['IOR'].default_value=1.45
head=material('Warm luminous headlights',(1,.88,.57),0,.2); h=head.node_tree.nodes['Principled BSDF']; h.inputs['Emission Color'].default_value=(1,.83,.43,1); h.inputs['Emission Strength'].default_value=2
red=material('Rear red lens',(.6,.01,.055),.15,.22)
def smooth(o):
 if o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
 return o
def box(n,p,d,m,r=.08):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p); o=car(bpy.context.object); o.name=n; o.dimensions=d; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if r:
  b=o.modifiers.new('Rounded corners','BEVEL'); b.width=r;b.segments=5; o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def sphere(n,p,d,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=p); o=car(bpy.context.object);o.name=n;o.scale=d;o.data.materials.append(m);return smooth(o)
def cylinder(n,p,r,depth,m,axis='Z'):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=p);o=car(bpy.context.object);o.name=n;o.data.materials.append(m)
 if axis=='Y':o.rotation_euler[0]=math.pi/2
 if axis=='X':o.rotation_euler[1]=math.pi/2
 b=o.modifiers.new('Machined edge','BEVEL');b.width=.012;b.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return smooth(o)
def tube(n,points,r,m,closed=False):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.resolution_u=20;c.bevel_depth=r;c.bevel_resolution=4;s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,v in zip(s.points,points):p.co=(*v,1)
 s.use_cyclic_u=closed;o=bpy.data.objects.new(n,c);CAR.objects.link(o);o.data.materials.append(m);return o
def rounded(points,amount=.16,steps=10):
 pts=[Vector(p) for p in points];out=[]
 for i,p in enumerate(pts):
  a=p.lerp(pts[i-1],amount);b=p.lerp(pts[(i+1)%len(pts)],amount)
  for j in range(steps):
   t=j/steps;out.append(tuple((1-t)**2*a+2*(1-t)*t*p+t*t*b))
 return out
def pane(n,points):
 me=bpy.data.meshes.new(n);me.from_pydata(points,[],[list(range(len(points)))]);me.update();o=bpy.data.objects.new(n,me);CAR.objects.link(o);o.data.materials.append(glass);s=o.modifiers.new('Real glass thickness','SOLIDIFY');s.thickness=.012;return o
# Lower body: curved shell with four genuine wheel openings.
body=box('Rounded lower body',(0,0,.99),(2.95,1.7,.92),paint,.25)
bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier='Rounded corners')
for x in [-.94,.94]:
 for y in [-.81,.81]:
  cut=cylinder('Temporary wheel opening',(x,y,.48),.56,.65,tire,'Y')
  bpy.context.view_layer.objects.active=cut;bpy.ops.object.modifier_apply(modifier='Machined edge')
  mod=body.modifiers.new('Wheel opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# Hollow the passenger compartment so the seats remain visible through glass.
cut=box('Temporary cabin cavity',(.25,0,1.48),(1.96,1.31,1.25),dash,.12)
bpy.context.view_layer.objects.active=cut;bpy.ops.object.modifier_apply(modifier='Rounded corners')
mod=body.modifiers.new('Hollow passenger compartment','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut
bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
be=body.modifiers.new('Wheel opening edge radius','BEVEL');be.width=.018;be.segments=3
box('Floor pan',(0,0,.56),(2.3,1.35,.12),dash,.05)
# Roof has a smooth dome; cabin pillars are curves, not a solid window-blocking box.
# A domed superellipse roof joins the upper pillars without a flat box silhouette.
verts=[]; faces=[]; segments=80; rings=16
for j in range(rings+1):
 t=.001+(math.pi/2-.001)*j/rings; radial=math.sin(t)
 for i in range(segments):
  a=i*math.tau/segments; co=math.cos(a); si=math.sin(a)
  verts.append((.16+1.02*radial*math.copysign(abs(co)**.55,co),.78*radial*math.copysign(abs(si)**.55,si),2.56+.28*math.cos(t)))
for j in range(rings):
 for i in range(segments):
  a=j*segments+i;b=j*segments+(i+1)%segments;faces.append((a,a+segments,b+segments,b))
faces.append(tuple(range(segments)));faces.append(tuple(rings*segments+i for i in reversed(range(segments))))
me=bpy.data.meshes.new('Domed roof shell');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Integrated domed roof',me);CAR.objects.link(o);o.data.materials.append(paint);smooth(o)
def side_y(z,s):return s*(.87-.14*((z-1.4)/1.25))
for sign in [-1,1]:
 front=rounded([(-1.02,side_y(1.46,sign),1.46),(-.66,side_y(2.59,sign),2.59),(.27,side_y(2.61,sign),2.61),(.35,side_y(1.54,sign),1.54)],.15)
 rear=rounded([(.49,side_y(1.55,sign),1.55),(.43,side_y(2.60,sign),2.60),(.86,side_y(2.57,sign),2.57),(1.25,side_y(1.59,sign),1.59)],.2)
 for label,pts in [('Door',front),('Quarter',rear)]:
  pane(label+' glass '+str(sign),pts);tube(label+' painted frame '+str(sign),pts,.063,paint,True);tube(label+' weather seal '+str(sign),[(x,y+sign*.017,z) for x,y,z in pts],.026,seal,True);tube(label+' chrome reveal '+str(sign),[(x,y+sign*.031,z) for x,y,z in pts],.010,chrome,True)
 # Door shut line follows the lower sill and meets the window frame.
 pts=rounded([(-1.03,sign*.864,1.48),(-.86,sign*.862,.66),(.37,sign*.868,.66),(.38,sign*.864,1.54)],.12)
 tube('Door panel seam '+str(sign),pts,.009,blue,True)
 tube('Lower sill chrome '+str(sign),[(-.5,sign*.874,.59),(.5,sign*.874,.59)],.015,chrome)
 box('Door handle pocket '+str(sign),(.17,sign*.876,1.36),(.19,.012,.06),blue,.025)
 tube('Chrome door handle '+str(sign),[(.10,sign*.9,1.37),(.24,sign*.9,1.39)],.015,chrome)
 tube('Mirror stalk '+str(sign),[(-.82,sign*.85,1.5),(-.9,sign*1.04,1.58)],.018,chrome)
 sphere('Mirror housing '+str(sign),(-.9,sign*1.07,1.61),(.035,.10,.10),chrome)
 sphere('Mirror reflecting face '+str(sign),(-.872,sign*1.07,1.61),(.009,.085,.085),chrome)
# Front windshield and rear hatch glass.
wind=rounded([(-1.05,-.78,1.44),(-.69,-.65,2.58),(-.69,.65,2.58),(-1.05,.78,1.44)],.13,14)
pane('Panoramic windshield',wind);tube('Windshield painted surround',wind,.06,paint,True);tube('Windshield gasket',[(x-.024,y,z) for x,y,z in wind],.025,seal,True);tube('Windshield brightwork',[(x-.042,y,z) for x,y,z in wind],.009,chrome,True)
back=rounded([(1.29,-.72,1.49),(.97,-.62,2.51),(.97,.62,2.51),(1.29,.72,1.49)],.18)
pane('Rear hatch glass',back);tube('Rear hatch frame',back,.07,paint,True);tube('Rear hatch seal',back,.024,seal,True)
# Dashboard, two front seats, rear bench, foot controls, instruments.
box('Dashboard',(-.81,0,1.37),(.4,1.40,.16),dash,.07)
for y in [-.37,.37]:
 box('Seat cushion',(.0,y,.85),(.66,.56,.17),seat,.08)
 o=box('Seat back',(.31,y,1.17),(.18,.58,.73),seat,.09);o.rotation_euler[1]=-.13
 box('Integrated headrest',(.36,y,1.55),(.17,.35,.2),seat,.08)
 for off in [-.17,0,.17]:tube('Seat stitched channel',[(.205,y+off,.92),(.25,y+off,1.39)],.007,stitch)
 tube('Seat outer piping',rounded([(-.28,y-.25,.94),(-.28,y+.25,.94),(.26,y+.25,.94),(.26,y-.25,.94)],.25),.009,stitch,True)
 tube('Seatbelt',[(.25,y+.23,.84),(.21,y-.19,1.43)],.018,seal)
box('Rear bench',(.92,0,.94),(.43,1.25,.22),seat,.08);box('Rear bench back',(1.11,0,1.23),(.14,1.25,.48),seat,.07)
# Steering wheel in the YZ plane and two readable gauges.
ring=[(-.49,-.37+.18*math.cos(t),1.48+.18*math.sin(t)) for t in [j*math.tau/64 for j in range(64)]]
tube('Steering wheel rim',ring,.025,seal,True);cylinder('Steering hub',(-.49,-.37,1.48),.055,.06,chrome,'X')
for t in [0,2.1,4.2]:tube('Steering spoke',[(-.49,-.37,1.48),(-.49,-.37+.17*math.cos(t),1.48+.17*math.sin(t))],.012,chrome)
for y in [-.40,-.15]:
 cylinder('Gauge bezel',(-.595,y,1.44),.083,.015,chrome,'X');cylinder('Gauge face',(-.58,y,1.44),.07,.016,black,'X');tube('Gauge needle',[(-.568,y,1.44),(-.568,y+.03,1.48)],.004,ivory)
tube('Gear lever',[(.04,.04,.68),(-.03,.04,.97)],.018,chrome);sphere('Gear knob',(-.03,.04,.97),(.05,.05,.05),black)
for y in [-.38,-.19]:box('Pedal',(-.65,y,.71),(.1,.08,.04),seal,.012)
# Thin rounded hood panel, panel gap, decorative center crease and wipers.
hood=box('Hood lid',(-1.10,0,1.38),(.7,1.30,.09),paint,.045)
tube('Hood seam',rounded([(-1.43,-.58,1.38),(-.80,-.62,1.43),(-.80,.62,1.43),(-1.43,.58,1.38)],.22),.008,blue,True)
tube('Hood center rib',[(-1.44,0,1.41),(-1.2,0,1.45),(-.82,0,1.48)],.014,chrome)
for y in [-.4,.38]:
 tube('Wiper arm',[(-1.076,y,1.49),(-1.038,y+.23,1.61)],.01,chrome);tube('Wiper blade',[(-1.052,y+.13,1.56),(-1.004,y+.39,1.72)],.014,seal)
# Wheels: rounded tires, concentric polished hubcaps, valve stems and tread grooves.
for x in [-.94,.94]:
 for sign in [-1,1]:
  y=sign*.84
  bpy.ops.mesh.primitive_torus_add(major_radius=.36,minor_radius=.12,major_segments=80,minor_segments=20,location=(x,y,.49),rotation=(math.pi/2,0,0));o=car(bpy.context.object);o.name='Rounded tire';o.data.materials.append(tire);smooth(o)
  cylinder('Wheel barrel',(x,y,.49),.32,.20,blue,'Y')
  outside=y+sign*.125
  cylinder('Wheel silver outer lip',(x,outside,.49),.325,.025,chrome,'Y');cylinder('Inset painted wheel',(x,outside+sign*.017,.49),.292,.025,blue,'Y');sphere('Domed hubcap',(x,outside+sign*.035,.49),(.24,.065,.24),paint)
  for j in range(48):
   t=j*math.tau/48
   pts=[]
   for k in range(5):
    a=-.65+k*.325;r=.36+.12*math.cos(a);pts.append((x+r*math.sin(t),y+.12*math.sin(a),.49+r*math.cos(t)))
   tube('Tire tread siping',pts,.003,seal)
  cylinder('Valve stem',(x+.23,outside+sign*.04,.59),.012,.035,seal,'Y')
  pts=[(x+.555*math.cos(t),sign*.871,.49+.555*math.sin(t)) for t in [j*math.pi/48 for j in range(49)]]
  tube('Sculpted wheel arch',pts,.045,paint);tube('Wheel arch edge',[(a,b+sign*.023,c) for a,b,c in pts],.009,blue)
# Round lighting, indicator lenses, bumpers, nose badge and rear fittings.
for y in [-.56,.56]:
 cylinder('Headlamp rubber seat',(-1.475,y,1.07),.213,.05,seal,'X');cylinder('Headlamp chrome bezel',(-1.51,y,1.07),.2,.06,chrome,'X');sphere('Convex headlamp lens',(-1.551,y,1.07),(.04,.171,.171),head)
 for off in [-.09,-.045,0,.045,.09]:tube('Headlamp lens fluting',[(-1.59,y+off,.95),(-1.594,y+off,1.19)],.0025,ivory)
 cylinder('Indicator bezel',(-1.49,y,.78),.09,.035,chrome,'X');sphere('Amber front indicator',(-1.52,y,.78),(.025,.071,.071),amber)
for sign in [-1,1]:
 sphere('Side marker',(-1.13,sign*.851,1.23),(.09,.014,.027),amber)
 cylinder('Rear lamp bezel',(1.46,sign*.53,.99),.12,.03,chrome,'X');sphere('Rear red lamp',(1.48,sign*.53,.99),(.03,.096,.096),red)
 sphere('Fuel cap',(1.08,sign*.854,1.36),(.07,.014,.07),chrome)
for x in [-1.49,1.47]:
 tube('Wraparound polished bumper',[(x*.9,-.82,.68),(x,-.7,.66),(x,0,.65),(x,.7,.66),(x*.9,.82,.68)],.039,chrome)
 tube('Bumper rubber insert',[(x-.012 if x<0 else x+.012,-.71,.65),(x-.012 if x<0 else x+.012,.71,.65)],.013,blue)
cylinder('Nose badge bezel',(-1.496,0,1.09),.073,.02,chrome,'X');cylinder('Nose badge enamel',(-1.509,0,1.09),.056,.02,blue,'X');tube('Badge slash',[(-1.526,-.043,1.12),(-1.526,.043,1.065)],.007,chrome)
box('License plate',(-1.55,0,.59),(.027,.44,.18),ivory,.016)
bpy.ops.object.text_add(location=(-1.569,.18,.54));o=car(bpy.context.object);o.name='License TO64';o.data.body='TO64';o.data.size=.105;o.data.extrude=.001;o.data.materials.append(black);o.rotation_euler=(math.pi/2,0,-math.pi/2)
for y in [-.19,.19]:cylinder('License screw',(-1.573,y,.65),.007,.008,chrome,'X')
# Studio with a lavender floor, warm key and blue rim.
floor=material('Lavender studio',(.29,.17,.61),0,.63)
bpy.ops.mesh.primitive_plane_add(size=200);o=bpy.context.object;o.name='Studio floor';o.data.materials.append(floor)
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.19,.38,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35
for name,loc,energy,size,color in [('Warm key',(-4,-4,7),650,5,(1,.81,.74)),('Cyan rim',(3,3,5),900,4,(.30,.62,1)),('Pink fill',(-1,4,3),400,4,(1,.36,.69))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((0,0,1.3))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-5.2,-6.4,3.65));camera=bpy.context.object;camera.name='Reference three-quarter camera';camera.rotation_euler=(Vector((0,0,1.4))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=4.8
scene=bpy.context.scene;scene.camera=camera;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True;scene.render.resolution_x=1200;scene.render.resolution_y=1200;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX'
# Optical bloom lives in the Blender compositor and remains fully editable.
comp=bpy.data.node_groups.new('Microcar optical bloom','CompositorNodeTree')
comp.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
scene.compositing_node_group=comp
render=comp.nodes.new('CompositorNodeRLayers'); render.location=(-320,0)
glow=comp.nodes.new('CompositorNodeGlare'); glow.name='Headlight bloom'; glow.inputs['Type'].default_value='Fog Glow'; glow.inputs['Quality'].default_value='High'; glow.location=(-80,0)
if 'Threshold' in glow.inputs: glow.inputs['Threshold'].default_value=2.0
if 'Strength' in glow.inputs: glow.inputs['Strength'].default_value=.35
output=comp.nodes.new('NodeGroupOutput'); output.location=(180,0)
comp.links.new(render.outputs['Image'],glow.inputs['Image']);comp.links.new(glow.outputs['Image'],output.inputs['Image'])
# Pack the source reference when available; it never becomes vehicle geometry.
ref=Path('/Users/blackmamba/Downloads/0967272d218cf4c725ec25e4d061dee0.jpg')
if ref.exists(): im=bpy.data.images.load(str(ref));im.name='Design reference';im.pack()
import sys
sys.path.insert(0,str(ROOT))
from integrate_body import integrate_shell
shell_report=integrate_shell()
report={'components':len(CAR.objects),'mesh_objects':sum(o.type=='MESH' for o in CAR.objects),'curve_objects':sum(o.type=='CURVE' for o in CAR.objects),'finite_geometry':all(math.isfinite(c) for o in CAR.objects if o.type=='MESH' for v in o.data.vertices for c in v.co),'reference_packed':any(i.packed_file for i in bpy.data.images),'features':['curved body with boolean wheel openings','glass thickness and transmission','window seals and chrome trim','front seats and rear bench','dashboard gauges and steering wheel','tread siping and valve stems','headlight lens fluting','door seams and handles','wipers and license plate']}
report.update(shell_report)
assert report['finite_geometry'];(ROOT/'validation.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Turquoise_Microcar.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in CAR.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'Turquoise_Microcar.glb'),use_selection=True,export_apply=True)
scene.render.filepath=str(ROOT/'Turquoise_Microcar.png');bpy.ops.render.render(write_still=True)
print('MICROCAR_VALIDATED',json.dumps(report))
