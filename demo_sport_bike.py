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

# Compuesto / Composite: Motorcycle_sport
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6, location=(0.0, 0.0, 0.52))
obj_0_0_0 = bpy.context.object
obj_0_0_0.name = 'MainFrame_0_0_0'
obj_0_0_0.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_0_0 = create_material('Material_0_0_0', (0.2, 0.2, 0.2, 1.0))
obj_0_0_0.data.materials.append(mat_0_0_0)

bpy.ops.mesh.primitive_cube_add(size=0.05, location=(-0.4, 0.0, 0.72))
obj_0_0_1 = bpy.context.object
obj_0_0_1.name = 'Subframe_0_0_1'
obj_0_0_1.scale = (0.8, 0.35, 0.4)
mat_0_0_1 = create_material('Material_0_0_1', (0.2, 0.2, 0.2, 1.0))
obj_0_0_1.data.materials.append(mat_0_0_1)

# Compuesto anidado / Nested Composite: MotorcycleEngine
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0.0, 0.0, 0.52))
obj_0_2_1_0 = bpy.context.object
obj_0_2_1_0.name = 'EngineBlock_0_2_1_0'
obj_0_2_1_0.scale = (0.6, 0.6, 0.6)
mat_0_2_1_0 = create_material('Material_0_2_1_0', (0.3, 0.3, 0.3, 1.0))
obj_0_2_1_0.data.materials.append(mat_0_2_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(-0.3, 0.0, 0.92))
obj_0_2_1_1 = bpy.context.object
obj_0_2_1_1.name = 'Cylinder_1_0_2_1_1'
obj_0_2_1_1.scale = (0.6, 0.6, 0.6)
mat_0_2_1_1 = create_material('Material_0_2_1_1', (0.4, 0.4, 0.4, 1.0))
obj_0_2_1_1.data.materials.append(mat_0_2_1_1)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(-0.15, 0.0, 0.92))
obj_0_2_1_2 = bpy.context.object
obj_0_2_1_2.name = 'Cylinder_2_0_2_1_2'
obj_0_2_1_2.scale = (0.6, 0.6, 0.6)
mat_0_2_1_2 = create_material('Material_0_2_1_2', (0.4, 0.4, 0.4, 1.0))
obj_0_2_1_2.data.materials.append(mat_0_2_1_2)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(0.0, 0.0, 0.92))
obj_0_2_1_3 = bpy.context.object
obj_0_2_1_3.name = 'Cylinder_3_0_2_1_3'
obj_0_2_1_3.scale = (0.6, 0.6, 0.6)
mat_0_2_1_3 = create_material('Material_0_2_1_3', (0.4, 0.4, 0.4, 1.0))
obj_0_2_1_3.data.materials.append(mat_0_2_1_3)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=(0.15, 0.0, 0.92))
obj_0_2_1_4 = bpy.context.object
obj_0_2_1_4.name = 'Cylinder_4_0_2_1_4'
obj_0_2_1_4.scale = (0.6, 0.6, 0.6)
mat_0_2_1_4 = create_material('Material_0_2_1_4', (0.4, 0.4, 0.4, 1.0))
obj_0_2_1_4.data.materials.append(mat_0_2_1_4)

# Compuesto anidado / Nested Composite: Wheel_1
bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.12, location=(0.8, 0.0, 0.16))
obj_0_3_1_0 = bpy.context.object
obj_0_3_1_0.name = 'Tire_0_3_1_0'
obj_0_3_1_0.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_3_1_0 = create_material('Material_0_3_1_0', (0.1, 0.1, 0.1, 1.0))
obj_0_3_1_0.data.materials.append(mat_0_3_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.22399999999999998, depth=0.096, location=(0.8, 0.0, 0.16))
obj_0_3_1_1 = bpy.context.object
obj_0_3_1_1.name = 'Rim_0_3_1_1'
obj_0_3_1_1.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_3_1_1 = create_material('Material_0_3_1_1', (0.7, 0.7, 0.8, 1.0))
obj_0_3_1_1.data.materials.append(mat_0_3_1_1)

# Compuesto anidado / Nested Composite: Wheel_2
bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.12, location=(-0.8, 0.0, 0.16))
obj_0_4_1_0 = bpy.context.object
obj_0_4_1_0.name = 'Tire_0_4_1_0'
obj_0_4_1_0.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_4_1_0 = create_material('Material_0_4_1_0', (0.1, 0.1, 0.1, 1.0))
obj_0_4_1_0.data.materials.append(mat_0_4_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.22399999999999998, depth=0.096, location=(-0.8, 0.0, 0.16))
obj_0_4_1_1 = bpy.context.object
obj_0_4_1_1.name = 'Rim_0_4_1_1'
obj_0_4_1_1.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_4_1_1 = create_material('Material_0_4_1_1', (0.7, 0.7, 0.8, 1.0))
obj_0_4_1_1.data.materials.append(mat_0_4_1_1)

bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0.2, 0.0, 0.8200000000000001))
obj_0_0_5 = bpy.context.object
obj_0_0_5.name = 'FuelTank_0_0_5'
obj_0_0_5.scale = (0.8, 0.5, 0.4)
mat_0_0_5 = create_material('Material_0_0_5', (0.1, 0.3, 0.9, 1.0))
obj_0_0_5.data.materials.append(mat_0_0_5)

bpy.ops.mesh.primitive_cube_add(size=0.3, location=(-0.3, 0.0, 0.8200000000000001))
obj_0_0_6 = bpy.context.object
obj_0_0_6.name = 'Seat_0_0_6'
obj_0_0_6.scale = (0.6, 0.4, 0.2)
mat_0_0_6 = create_material('Material_0_0_6', (0.1, 0.1, 0.1, 1.0))
obj_0_0_6.data.materials.append(mat_0_0_6)

bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.6, location=(0.7, 0.0, 1.02))
obj_0_0_7 = bpy.context.object
obj_0_0_7.name = 'Handlebar_0_0_7'
obj_0_0_7.rotation_euler = (0.0, 1.5707963267948966, 0.0)
mat_0_0_7 = create_material('Material_0_0_7', (0.3, 0.3, 0.3, 1.0))
obj_0_0_7.data.materials.append(mat_0_0_7)


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
