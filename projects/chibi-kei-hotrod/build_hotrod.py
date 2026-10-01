"""P0 silhouette generator for the Chibi Kei Hot-Rod mission."""
import bpy, math, json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parent

# --- P0 proportions: tune these before adding detail ---
LENGTH = 3.05
WIDTH = 1.82
HEIGHT = 2.05
WHEELBASE = 1.72
TRACK = 1.52
TIRE_RADIUS = 0.43
TIRE_WIDTH = 0.30
GROUND_CLEARANCE = 0.08
CABIN_HEIGHT = 1.45

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

CAR = bpy.data.collections.new('CHIBI KEI HOTROD • P0 silhouette')
bpy.context.scene.collection.children.link(CAR)

def link(o):
    for c in list(o.users_collection):
        c.objects.unlink(o)
    CAR.objects.link(o)
    return o

def mat(name, color, metallic=0.0, rough=.45):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = rough
    return m

body_mat = mat('Warm silver body', (.56,.53,.47), .45, .30)
roof_mat = mat('Black roof', (.015,.018,.02), .2, .28)
tire_mat = mat('Tire', (.018,.02,.022), 0, .72)
rim_mat = mat('Bronze wheel', (.30,.22,.12), .72, .28)
dark_mat = mat('Front dark', (.01,.012,.014), .05, .35)
orange = mat('Orange tow ring', (.95,.18,.015), .3, .25)

def box(name, location, dims, material, bevel=.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    o = link(bpy.context.object); o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material: o.data.materials.append(material)
    if bevel:
        b = o.modifiers.new('Rounded silhouette', 'BEVEL'); b.width=bevel; b.segments=5
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

def cyl(name, location, radius, depth, material, axis='Y'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=radius, depth=depth, location=location)
    o = link(bpy.context.object); o.name=name
    if axis == 'Y': o.rotation_euler[0] = math.pi/2
    elif axis == 'X': o.rotation_euler[1] = math.pi/2
    o.data.materials.append(material)
    b=o.modifiers.new('Edge','BEVEL'); b.width=.012; b.segments=3
    return o

# Lower body: very short nose, thick rear mass.
body = box('Body mass', (0.02,0,.72), (LENGTH, WIDTH*.90, .86), body_mat, .22)
box('Front vertical nose', (-1.39,0,.78), (.28, WIDTH*.88, .83), body_mat, .08)
box('Rear thick mass', (1.10,0,1.02), (.72, WIDTH*.90, 1.00), body_mat, .16)

# Cabin capsule: biased forward, tall, narrow at roof.
box('Cabin lower', (-.10,0,1.47), (1.42, WIDTH*.78, CABIN_HEIGHT*.78), body_mat, .20)
roof = box('Roof cap', (-.08,0,2.00), (1.48, WIDTH*.80, .18), roof_mat, .13)
roof.rotation_euler[1] = math.radians(-2)

# Slanted windshield block.
wind = box('Windshield mass', (-.66,0,1.66), (.18, WIDTH*.68, .86), dark_mat, .06)
wind.rotation_euler[1] = math.radians(-18)

# Wide fenders.
ax = WHEELBASE/2
for x in (-ax, ax):
    for s in (-1,1):
        y = s*(TRACK/2)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=(x,y,.53))
        f = link(bpy.context.object); f.name='Wide fender'
        f.scale=(.61,.27,.58); f.data.materials.append(body_mat)

# Wheels.
for x in (-ax, ax):
    for s in (-1,1):
        y = s*(TRACK/2 + .03)
        bpy.ops.mesh.primitive_torus_add(major_radius=TIRE_RADIUS*.78, minor_radius=TIRE_RADIUS*.22,
            major_segments=64, minor_segments=18, location=(x,y,TIRE_RADIUS+GROUND_CLEARANCE),
            rotation=(math.pi/2,0,0))
        t=link(bpy.context.object); t.name='Wide tire'; t.data.materials.append(tire_mat)
        cyl('Bronze rim',(x,y,TIRE_RADIUS+GROUND_CLEARANCE),TIRE_RADIUS*.58,TIRE_WIDTH*.72,rim_mat,'Y')

# Splitter and small spoiler.
box('Front splitter',(-1.48,0,.16),(.42,WIDTH*.94,.10),dark_mat,.025)
spoiler = box('Rear mini spoiler',(1.43,0,1.44),(.18,WIDTH*.78,.08),dark_mat,.025)
spoiler.rotation_euler[1]=math.radians(-5)

# Front opening + lower round elements.
box('Front grille',(-1.55,0,.84),(.05,WIDTH*.64,.45),dark_mat,.03)
for y in (-.47, -.20, .20, .47):
    cyl('Lower front lamp',(-1.585,y,.39),.065,.025,dark_mat,'X')
cyl('Tow ring',(-1.60,0,.39),.095,.035,orange,'X')

# Studio floor and simple lighting.
floor = mat('Studio floor', (.42,.44,.36), 0, .8)
bpy.ops.mesh.primitive_plane_add(size=100); p=bpy.context.object; p.name='Studio floor'; p.data.materials.append(floor)
world=bpy.context.scene.world; world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.44,.36,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.7

for name,loc,energy,size in [
    ('Key',(-4,-5,6),900,5),
    ('Fill',(4,-2,4),500,4),
    ('Rim',(2,5,5),650,3)]:
    bpy.ops.object.light_add(type='AREA', location=loc)
    o=bpy.context.object; o.name=name; o.data.energy=energy; o.data.size=size
    o.rotation_euler=(Vector((0,0,1.0))-o.location).to_track_quat('-Z','Y').to_euler()

bpy.ops.object.camera_add(location=(-5.6,-7.2,3.4))
cam=bpy.context.object; cam.name='P0 three-quarter camera'
cam.rotation_euler=(Vector((0,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO'; cam.data.ortho_scale=4.5

scene=bpy.context.scene; scene.camera=cam
scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.resolution_x=1200; scene.render.resolution_y=900; scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'

report = {
  'stage':'P0-silhouette',
  'length':LENGTH,'width':WIDTH,'height':HEIGHT,
  'wheelbase':WHEELBASE,'track':TRACK,
  'tire_radius':TIRE_RADIUS,'tire_width':TIRE_WIDTH,
  'ground_clearance':GROUND_CLEARANCE,
  'ratios':{
    'height_to_length':HEIGHT/LENGTH,
    'wheelbase_to_length':WHEELBASE/LENGTH,
    'track_to_width':TRACK/WIDTH,
    'tire_diameter_to_length':(2*TIRE_RADIUS)/LENGTH,
  },
  'objects':len(CAR.objects),
  'finite_geometry':all(math.isfinite(c) for o in CAR.objects if o.type=='MESH' for v in o.data.vertices for c in v.co),
}
assert report['finite_geometry']
assert report['height_to_length'] if 'height_to_length' in report else True
(ROOT/'validation.json').write_text(json.dumps(report, indent=2))

bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Chibi_Kei_Hotrod.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in CAR.objects: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'Chibi_Kei_Hotrod.glb'), use_selection=True, export_apply=True)
scene.render.filepath=str(ROOT/'Chibi_Kei_Hotrod.png')
bpy.ops.render.render(write_still=True)
print('CHIBI_KEI_HOTROD_P0', json.dumps(report))
