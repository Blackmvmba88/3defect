import bpy
import math

# Limpiar objetos existentes / Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Función auxiliar para crear materiales / Helper function to create materials
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = color
    return mat

# Compuesto / Composite: Car_sports
# Compuesto anidado / Nested Composite: Chassis
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.23936000000000054, 0.0, -43.76468608000007))
obj_0_0_1_0 = bpy.context.object
obj_0_0_1_0.name = 'ChassisBody_0_0_1_0'
obj_0_0_1_0.scale = (4.2, 1.9, 0.3)
mat_0_0_1_0 = create_material('Material_0_0_1_0', (0.5, 0.5, 0.6, 1.0))
obj_0_0_1_0.data.materials.append(mat_0_0_1_0)

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.23936000000000054, -0.76, -43.76468608000007))
obj_0_0_1_1 = bpy.context.object
obj_0_0_1_1.name = 'Rail_-1_0_0_1_1'
obj_0_0_1_1.scale = (3.7800000000000002, 0.1, 0.6)
mat_0_0_1_1 = create_material('Material_0_0_1_1', (0.3, 0.3, 0.3, 1.0))
obj_0_0_1_1.data.materials.append(mat_0_0_1_1)

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.23936000000000054, 0.76, -43.76468608000007))
obj_0_0_1_2 = bpy.context.object
obj_0_0_1_2.name = 'Rail_1_0_0_1_2'
obj_0_0_1_2.scale = (3.7800000000000002, 0.1, 0.6)
mat_0_0_1_2 = create_material('Material_0_0_1_2', (0.3, 0.3, 0.3, 1.0))
obj_0_0_1_2.data.materials.append(mat_0_0_1_2)

# Compuesto anidado / Nested Composite: Engine
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(1.4993599999999903, 0.0, -43.46468608000007))
obj_0_1_1_0 = bpy.context.object
obj_0_1_1_0.name = 'EngineBlock_0_1_1_0'
obj_0_1_1_0.scale = (1.2, 0.8, 0.6)
mat_0_1_1_0 = create_material('Material_0_1_1_0', (0.3, 0.3, 0.3, 1.0))
obj_0_1_1_0.data.materials.append(mat_0_1_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(1.0493599999999903, 0.0, -43.064686080000065))
obj_0_1_1_1 = bpy.context.object
obj_0_1_1_1.name = 'Cylinder_1_0_1_1_1'
mat_0_1_1_1 = create_material('Material_0_1_1_1', (0.4, 0.4, 0.4, 1.0))
obj_0_1_1_1.data.materials.append(mat_0_1_1_1)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(1.1993599999999902, 0.0, -43.064686080000065))
obj_0_1_1_2 = bpy.context.object
obj_0_1_1_2.name = 'Cylinder_2_0_1_1_2'
mat_0_1_1_2 = create_material('Material_0_1_1_2', (0.4, 0.4, 0.4, 1.0))
obj_0_1_1_2.data.materials.append(mat_0_1_1_2)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(1.3493599999999903, 0.0, -43.064686080000065))
obj_0_1_1_3 = bpy.context.object
obj_0_1_1_3.name = 'Cylinder_3_0_1_1_3'
mat_0_1_1_3 = create_material('Material_0_1_1_3', (0.4, 0.4, 0.4, 1.0))
obj_0_1_1_3.data.materials.append(mat_0_1_1_3)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(1.4993599999999903, 0.0, -43.064686080000065))
obj_0_1_1_4 = bpy.context.object
obj_0_1_1_4.name = 'Cylinder_4_0_1_1_4'
mat_0_1_1_4 = create_material('Material_0_1_1_4', (0.4, 0.4, 0.4, 1.0))
obj_0_1_1_4.data.materials.append(mat_0_1_1_4)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(1.6493599999999902, 0.0, -43.064686080000065))
obj_0_1_1_5 = bpy.context.object
obj_0_1_1_5.name = 'Cylinder_5_0_1_1_5'
mat_0_1_1_5 = create_material('Material_0_1_1_5', (0.4, 0.4, 0.4, 1.0))
obj_0_1_1_5.data.materials.append(mat_0_1_1_5)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(1.7993599999999903, 0.0, -43.064686080000065))
obj_0_1_1_6 = bpy.context.object
obj_0_1_1_6.name = 'Cylinder_6_0_1_1_6'
mat_0_1_1_6 = create_material('Material_0_1_1_6', (0.4, 0.4, 0.4, 1.0))
obj_0_1_1_6.data.materials.append(mat_0_1_1_6)

# Compuesto anidado / Nested Composite: Wheel_1
bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.25, location=(1.4993599999999903, 0.855, -43.954686080000066))
obj_0_2_1_0 = bpy.context.object
obj_0_2_1_0.name = 'Tire_0_2_1_0'
obj_0_2_1_0.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_2_1_0 = create_material('Material_0_2_1_0', (0.1, 0.1, 0.1, 1.0))
obj_0_2_1_0.data.materials.append(mat_0_2_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.26599999999999996, depth=0.2, location=(1.4993599999999903, 0.855, -43.954686080000066))
obj_0_2_1_1 = bpy.context.object
obj_0_2_1_1.name = 'Rim_0_2_1_1'
obj_0_2_1_1.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_2_1_1 = create_material('Material_0_2_1_1', (0.7, 0.7, 0.8, 1.0))
obj_0_2_1_1.data.materials.append(mat_0_2_1_1)

# Compuesto anidado / Nested Composite: Wheel_2
bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.25, location=(1.4993599999999903, -0.855, -43.954686080000066))
obj_0_3_1_0 = bpy.context.object
obj_0_3_1_0.name = 'Tire_0_3_1_0'
obj_0_3_1_0.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_3_1_0 = create_material('Material_0_3_1_0', (0.1, 0.1, 0.1, 1.0))
obj_0_3_1_0.data.materials.append(mat_0_3_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.26599999999999996, depth=0.2, location=(1.4993599999999903, -0.855, -43.954686080000066))
obj_0_3_1_1 = bpy.context.object
obj_0_3_1_1.name = 'Rim_0_3_1_1'
obj_0_3_1_1.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_3_1_1 = create_material('Material_0_3_1_1', (0.7, 0.7, 0.8, 1.0))
obj_0_3_1_1.data.materials.append(mat_0_3_1_1)

# Compuesto anidado / Nested Composite: Wheel_3
bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.25, location=(-1.0206400000000098, 0.855, -43.954686080000066))
obj_0_4_1_0 = bpy.context.object
obj_0_4_1_0.name = 'Tire_0_4_1_0'
obj_0_4_1_0.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_4_1_0 = create_material('Material_0_4_1_0', (0.1, 0.1, 0.1, 1.0))
obj_0_4_1_0.data.materials.append(mat_0_4_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.26599999999999996, depth=0.2, location=(-1.0206400000000098, 0.855, -43.954686080000066))
obj_0_4_1_1 = bpy.context.object
obj_0_4_1_1.name = 'Rim_0_4_1_1'
obj_0_4_1_1.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_4_1_1 = create_material('Material_0_4_1_1', (0.7, 0.7, 0.8, 1.0))
obj_0_4_1_1.data.materials.append(mat_0_4_1_1)

# Compuesto anidado / Nested Composite: Wheel_4
bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.25, location=(-1.0206400000000098, -0.855, -43.954686080000066))
obj_0_5_1_0 = bpy.context.object
obj_0_5_1_0.name = 'Tire_0_5_1_0'
obj_0_5_1_0.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_5_1_0 = create_material('Material_0_5_1_0', (0.1, 0.1, 0.1, 1.0))
obj_0_5_1_0.data.materials.append(mat_0_5_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.26599999999999996, depth=0.2, location=(-1.0206400000000098, -0.855, -43.954686080000066))
obj_0_5_1_1 = bpy.context.object
obj_0_5_1_1.name = 'Rim_0_5_1_1'
obj_0_5_1_1.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_5_1_1 = create_material('Material_0_5_1_1', (0.7, 0.7, 0.8, 1.0))
obj_0_5_1_1.data.materials.append(mat_0_5_1_1)

# Compuesto anidado / Nested Composite: Body_sports
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.23936000000000054, 0.0, -43.26468608000007))
obj_0_6_1_0 = bpy.context.object
obj_0_6_1_0.name = 'LowerBody_0_6_1_0'
obj_0_6_1_0.scale = (2.2, 1.3, 0.4)
mat_0_6_1_0 = create_material('Material_0_6_1_0', (0.9, 0.1, 0.1, 1.0))
obj_0_6_1_0.data.materials.append(mat_0_6_1_0)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.23936000000000054, 0.0, -42.86468608000008))
obj_0_6_1_1 = bpy.context.object
obj_0_6_1_1.name = 'Cabin_0_6_1_1'
obj_0_6_1_1.scale = (1.0, 1.1, 0.4)
mat_0_6_1_1 = create_material('Material_0_6_1_1', (0.2, 0.2, 0.2, 1.0))
obj_0_6_1_1.data.materials.append(mat_0_6_1_1)


# Añadir cámara / Add camera
bpy.ops.object.camera_add(location=(10, -10, 8))
camera = bpy.context.object
camera.rotation_euler = (1.1, 0, 0.8)

# Establecer cámara como activa / Set camera as active
bpy.context.scene.camera = camera

# Añadir luz solar / Add sun light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
light = bpy.context.object
light.data.energy = 2.0

# Establecer sombreado del viewport en sólido / Set viewport shading to solid
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'SOLID'
