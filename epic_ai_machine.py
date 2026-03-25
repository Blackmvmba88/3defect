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

# Compuesto / Composite: AI_Generated_System
# Compuesto anidado / Nested Composite: Mechanical_Clock
# Compuesto anidado / Nested Composite: pendulum
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.248, location=(0.0, 0.0, -0.124))
obj_0_0_0_2_0 = bpy.context.object
obj_0_0_0_2_0.name = 'Cylinder_0_0_0_2_0'
mat_0_0_0_2_0 = create_material('Material_0_0_0_2_0', (0.5, 0.5, 0.5, 1.0))
obj_0_0_0_2_0.data.materials.append(mat_0_0_0_2_0)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5313292845913056, location=(0.0, 0.0, -0.248))
obj_0_0_0_2_1 = bpy.context.object
obj_0_0_0_2_1.name = 'Sphere_0_0_0_2_1'
mat_0_0_0_2_1 = create_material('Material_0_0_0_2_1', (0.8, 0.6, 0.2, 1.0))
obj_0_0_0_2_1.data.materials.append(mat_0_0_0_2_1)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0.0, 0.0, 0.0))
obj_0_0_0_2_2 = bpy.context.object
obj_0_0_0_2_2.name = 'Sphere_0_0_0_2_2'
mat_0_0_0_2_2 = create_material('Material_0_0_0_2_2', (0.3, 0.3, 0.3, 1.0))
obj_0_0_0_2_2.data.materials.append(mat_0_0_0_2_2)

# Compuesto anidado / Nested Composite: escapement
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.1, location=(0.5, 0.0, 0.0))
obj_0_0_1_2_0 = bpy.context.object
obj_0_0_1_2_0.name = 'Cylinder_0_0_1_2_0'
mat_0_0_1_2_0 = create_material('Material_0_0_1_2_0', (0.8, 0.6, 0.3, 1.0))
obj_0_0_1_2_0.data.materials.append(mat_0_0_1_2_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.15, location=(0.85, 0.0, 0.0))
obj_0_0_1_2_1 = bpy.context.object
obj_0_0_1_2_1.name = 'Cylinder_0_0_1_2_1'
mat_0_0_1_2_1 = create_material('Material_0_0_1_2_1', (0.7, 0.4, 0.3, 1.0))
obj_0_0_1_2_1.data.materials.append(mat_0_0_1_2_1)

# Compuesto anidado / Nested Composite: spring
bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, -0.4375))
obj_0_0_2_2_0 = bpy.context.object
obj_0_0_2_2_0.name = 'Torus_0_0_2_2_0'
mat_0_0_2_2_0 = create_material('Material_0_0_2_2_0', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_0.data.materials.append(mat_0_0_2_2_0)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, -0.375))
obj_0_0_2_2_1 = bpy.context.object
obj_0_0_2_2_1.name = 'Torus_0_0_2_2_1'
mat_0_0_2_2_1 = create_material('Material_0_0_2_2_1', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_1.data.materials.append(mat_0_0_2_2_1)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, -0.3125))
obj_0_0_2_2_2 = bpy.context.object
obj_0_0_2_2_2.name = 'Torus_0_0_2_2_2'
mat_0_0_2_2_2 = create_material('Material_0_0_2_2_2', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_2.data.materials.append(mat_0_0_2_2_2)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, -0.25))
obj_0_0_2_2_3 = bpy.context.object
obj_0_0_2_2_3.name = 'Torus_0_0_2_2_3'
mat_0_0_2_2_3 = create_material('Material_0_0_2_2_3', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_3.data.materials.append(mat_0_0_2_2_3)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, -0.1875))
obj_0_0_2_2_4 = bpy.context.object
obj_0_0_2_2_4.name = 'Torus_0_0_2_2_4'
mat_0_0_2_2_4 = create_material('Material_0_0_2_2_4', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_4.data.materials.append(mat_0_0_2_2_4)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, -0.125))
obj_0_0_2_2_5 = bpy.context.object
obj_0_0_2_2_5.name = 'Torus_0_0_2_2_5'
mat_0_0_2_2_5 = create_material('Material_0_0_2_2_5', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_5.data.materials.append(mat_0_0_2_2_5)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, -0.0625))
obj_0_0_2_2_6 = bpy.context.object
obj_0_0_2_2_6.name = 'Torus_0_0_2_2_6'
mat_0_0_2_2_6 = create_material('Material_0_0_2_2_6', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_6.data.materials.append(mat_0_0_2_2_6)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.0))
obj_0_0_2_2_7 = bpy.context.object
obj_0_0_2_2_7.name = 'Torus_0_0_2_2_7'
mat_0_0_2_2_7 = create_material('Material_0_0_2_2_7', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_7.data.materials.append(mat_0_0_2_2_7)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.0625))
obj_0_0_2_2_8 = bpy.context.object
obj_0_0_2_2_8.name = 'Torus_0_0_2_2_8'
mat_0_0_2_2_8 = create_material('Material_0_0_2_2_8', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_8.data.materials.append(mat_0_0_2_2_8)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.125))
obj_0_0_2_2_9 = bpy.context.object
obj_0_0_2_2_9.name = 'Torus_0_0_2_2_9'
mat_0_0_2_2_9 = create_material('Material_0_0_2_2_9', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_9.data.materials.append(mat_0_0_2_2_9)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.1875))
obj_0_0_2_2_10 = bpy.context.object
obj_0_0_2_2_10.name = 'Torus_0_0_2_2_10'
mat_0_0_2_2_10 = create_material('Material_0_0_2_2_10', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_10.data.materials.append(mat_0_0_2_2_10)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.25))
obj_0_0_2_2_11 = bpy.context.object
obj_0_0_2_2_11.name = 'Torus_0_0_2_2_11'
mat_0_0_2_2_11 = create_material('Material_0_0_2_2_11', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_11.data.materials.append(mat_0_0_2_2_11)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.3125))
obj_0_0_2_2_12 = bpy.context.object
obj_0_0_2_2_12.name = 'Torus_0_0_2_2_12'
mat_0_0_2_2_12 = create_material('Material_0_0_2_2_12', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_12.data.materials.append(mat_0_0_2_2_12)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.375))
obj_0_0_2_2_13 = bpy.context.object
obj_0_0_2_2_13.name = 'Torus_0_0_2_2_13'
mat_0_0_2_2_13 = create_material('Material_0_0_2_2_13', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_13.data.materials.append(mat_0_0_2_2_13)

bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.025, location=(1.0, 0.0, 0.4375))
obj_0_0_2_2_14 = bpy.context.object
obj_0_0_2_2_14.name = 'Torus_0_0_2_2_14'
mat_0_0_2_2_14 = create_material('Material_0_0_2_2_14', (0.6, 0.6, 0.7, 1.0))
obj_0_0_2_2_14.data.materials.append(mat_0_0_2_2_14)

# Compuesto anidado / Nested Composite: Transmission_System
# Compuesto anidado / Nested Composite: gear_box
# Compuesto anidado / Nested Composite: gear_40t
bpy.ops.mesh.primitive_cylinder_add(radius=10.0, depth=0.5, location=(3.5313292845913056, 0.0, 0.0))
obj_0_1_0_0_3_0 = bpy.context.object
obj_0_1_0_0_3_0.name = 'Cylinder_0_1_0_0_3_0'
mat_0_1_0_0_3_0 = create_material('Material_0_1_0_0_3_0', (0.7, 0.7, 0.8, 1.0))
obj_0_1_0_0_3_0.data.materials.append(mat_0_1_0_0_3_0)

bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=0.6, location=(3.5313292845913056, 0.0, 0.0))
obj_0_1_0_0_3_1 = bpy.context.object
obj_0_1_0_0_3_1.name = 'Cylinder_0_1_0_0_3_1'
mat_0_1_0_0_3_1 = create_material('Material_0_1_0_0_3_1', (0.5, 0.5, 0.6, 1.0))
obj_0_1_0_0_3_1.data.materials.append(mat_0_1_0_0_3_1)

# Compuesto anidado / Nested Composite: gear_20t
bpy.ops.mesh.primitive_cylinder_add(radius=5.0, depth=0.5, location=(5.031329284591306, 0.0, 0.0))
obj_0_1_0_1_3_0 = bpy.context.object
obj_0_1_0_1_3_0.name = 'Cylinder_0_1_0_1_3_0'
mat_0_1_0_1_3_0 = create_material('Material_0_1_0_1_3_0', (0.7, 0.7, 0.8, 1.0))
obj_0_1_0_1_3_0.data.materials.append(mat_0_1_0_1_3_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=0.6, location=(5.031329284591306, 0.0, 0.0))
obj_0_1_0_1_3_1 = bpy.context.object
obj_0_1_0_1_3_1.name = 'Cylinder_0_1_0_1_3_1'
mat_0_1_0_1_3_1 = create_material('Material_0_1_0_1_3_1', (0.5, 0.5, 0.6, 1.0))
obj_0_1_0_1_3_1.data.materials.append(mat_0_1_0_1_3_1)

# Compuesto anidado / Nested Composite: Mechanical_Arm
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.4, location=(24.531329284591305, 0.0, 0.0))
obj_0_2_1_0 = bpy.context.object
obj_0_2_1_0.name = 'Cylinder_0_2_1_0'
mat_0_2_1_0 = create_material('Material_0_2_1_0', (0.8, 0.8, 0.8, 1.0))
obj_0_2_1_0.data.materials.append(mat_0_2_1_0)

bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2.0, location=(24.531329284591305, 0.0, 1.2))
obj_0_2_1_1 = bpy.context.object
obj_0_2_1_1.name = 'Cylinder_0_2_1_1'
mat_0_2_1_1 = create_material('Material_0_2_1_1', (0.8, 0.8, 0.8, 1.0))
obj_0_2_1_1.data.materials.append(mat_0_2_1_1)

bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.4, location=(24.531329284591305, 0.0, 2.4))
obj_0_2_1_2 = bpy.context.object
obj_0_2_1_2.name = 'Cylinder_0_2_1_2'
mat_0_2_1_2 = create_material('Material_0_2_1_2', (0.8, 0.8, 0.8, 1.0))
obj_0_2_1_2.data.materials.append(mat_0_2_1_2)

bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.0, location=(24.531329284591305, 0.0, 3.1))
obj_0_2_1_3 = bpy.context.object
obj_0_2_1_3.name = 'Cylinder_0_2_1_3'
mat_0_2_1_3 = create_material('Material_0_2_1_3', (0.8, 0.8, 0.8, 1.0))
obj_0_2_1_3.data.materials.append(mat_0_2_1_3)

bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.4, location=(24.531329284591305, 0.0, 3.8))
obj_0_2_1_4 = bpy.context.object
obj_0_2_1_4.name = 'Cylinder_0_2_1_4'
mat_0_2_1_4 = create_material('Material_0_2_1_4', (0.8, 0.8, 0.8, 1.0))
obj_0_2_1_4.data.materials.append(mat_0_2_1_4)

bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.6666666666666666, location=(24.531329284591305, 0.0, 4.333333333333333))
obj_0_2_1_5 = bpy.context.object
obj_0_2_1_5.name = 'Cylinder_0_2_1_5'
mat_0_2_1_5 = create_material('Material_0_2_1_5', (0.8, 0.8, 0.8, 1.0))
obj_0_2_1_5.data.materials.append(mat_0_2_1_5)


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
