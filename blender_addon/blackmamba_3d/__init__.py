bl_info = {
    "name": "BlackMamba 3D",
    "author": "BlackMamba RECORDS / Iyari Gomez",
    "version": (0, 5, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > BLACKMAMBA",
    "description": "Modular BlackMamba 3D authoring layer",
    "category": "3D View",
}

import bpy
from bpy.props import EnumProperty, FloatProperty, IntProperty

from .control_arm_math import ControlArmSpec
from .damper_math import DamperSpec
from .materials import PRESETS, apply_preset
from .mechanics import create_control_arm, create_damper, create_spring
from .spring_math import SpringSpec
from .wishbone_ui import register as register_wishbone_ui
from .wishbone_ui import unregister as unregister_wishbone_ui


class BM_OT_add_primitive(bpy.types.Operator):
    bl_idname = "blackmamba.add_primitive"
    bl_label = "Add BlackMamba Primitive"
    bl_options = {"REGISTER", "UNDO"}

    primitive: EnumProperty(
        items=(
            ("CUBE", "Cube", ""),
            ("SPHERE", "Sphere", ""),
            ("CYLINDER", "Cylinder", ""),
        )
    )

    def execute(self, context):
        if self.primitive == "CUBE":
            bpy.ops.mesh.primitive_cube_add()
        elif self.primitive == "SPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24)
        elif self.primitive == "CYLINDER":
            bpy.ops.mesh.primitive_cylinder_add(vertices=64)
        else:
            return {"CANCELLED"}

        obj = context.active_object
        if obj is not None:
            obj.name = f"BM_{self.primitive.title()}"
        return {"FINISHED"}


class BM_OT_apply_material(bpy.types.Operator):
    bl_idname = "blackmamba.apply_material"
    bl_label = "Apply BlackMamba Material"
    bl_options = {"REGISTER", "UNDO"}

    preset: EnumProperty(items=PRESETS)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and getattr(obj, "data", None) is not None

    def execute(self, context):
        try:
            material = apply_preset(context.active_object, self.preset, context=context)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        self.report({"INFO"}, f"Applied {material.name}")
        return {"FINISHED"}


class BM_OT_form_action(bpy.types.Operator):
    bl_idname = "blackmamba.form_action"
    bl_label = "BlackMamba Form Action"
    bl_options = {"REGISTER", "UNDO"}

    action: EnumProperty(
        items=(
            ("BEVEL", "Bevel", ""),
            ("SUBDIVISION", "Subdivision", ""),
            ("SMOOTH", "Smooth", ""),
        )
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"

    def execute(self, context):
        obj = context.active_object
        scene = context.scene

        if self.action == "BEVEL":
            modifier = obj.modifiers.get("BM_Bevel") or obj.modifiers.new("BM_Bevel", "BEVEL")
            modifier.width = scene.bm_bevel_width
            modifier.segments = scene.bm_bevel_segments
            if hasattr(modifier, "limit_method"):
                modifier.limit_method = "ANGLE"
        elif self.action == "SUBDIVISION":
            modifier = obj.modifiers.get("BM_Subdivision") or obj.modifiers.new(
                "BM_Subdivision", "SUBSURF"
            )
            modifier.levels = scene.bm_subdivision_levels
            modifier.render_levels = max(scene.bm_subdivision_levels, 2)
        elif self.action == "SMOOTH":
            for polygon in obj.data.polygons:
                polygon.use_smooth = True
        else:
            return {"CANCELLED"}

        return {"FINISHED"}


class BM_OT_add_spring(bpy.types.Operator):
    bl_idname = "blackmamba.add_spring"
    bl_label = "Add BlackMamba Spring"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        spec = SpringSpec(
            wire_diameter=scene.bm_spring_wire_diameter,
            coil_diameter=scene.bm_spring_coil_diameter,
            free_length=scene.bm_spring_free_length,
            turns=scene.bm_spring_turns,
        )
        try:
            obj = create_spring(context, spec)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            f"Created {obj.name}: OD {spec.outer_diameter:.4f}, free length {spec.free_length:.4f}",
        )
        return {"FINISHED"}


class BM_OT_add_damper(bpy.types.Operator):
    bl_idname = "blackmamba.add_damper"
    bl_label = "Add BlackMamba Damper"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        spec = DamperSpec(
            body_diameter=scene.bm_damper_body_diameter,
            body_length=scene.bm_damper_body_length,
            rod_diameter=scene.bm_damper_rod_diameter,
            stroke=scene.bm_damper_stroke,
            mount_outer_diameter=scene.bm_damper_mount_outer_diameter,
            mount_bore_diameter=scene.bm_damper_mount_bore_diameter,
            mount_width=scene.bm_damper_mount_width,
            extension_fraction=scene.bm_damper_extension_fraction,
        )
        try:
            obj = create_damper(context, spec)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            (
                f"Created {obj.name}: {spec.current_center_distance:.4f} eye-to-eye, "
                f"{spec.extension_fraction:.0%} extension"
            ),
        )
        return {"FINISHED"}


class BM_OT_add_control_arm(bpy.types.Operator):
    bl_idname = "blackmamba.add_control_arm"
    bl_label = "Add BlackMamba Control Arm"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        spec = ControlArmSpec(
            arm_length=scene.bm_control_arm_length,
            pivot_spacing=scene.bm_control_arm_pivot_spacing,
            upright_z=scene.bm_control_arm_upright_z,
            tube_diameter=scene.bm_control_arm_tube_diameter,
            joint_diameter=scene.bm_control_arm_joint_diameter,
        )
        try:
            obj = create_control_arm(context, spec)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            (
                f"Created {obj.name}: pivots {spec.pivot_spacing:.4f}, "
                f"arm {spec.arm_length:.4f}"
            ),
        )
        return {"FINISHED"}


class BM_PT_main(bpy.types.Panel):
    bl_label = "BlackMamba 3D"
    bl_idname = "BM_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BLACKMAMBA"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        header = layout.box()
        header.label(text="BLACKMAMBA 3D", icon="MODIFIER")
        header.label(text=f"Active: {obj.name if obj else 'None'}")

        create = layout.box()
        create.label(text="Create", icon="MESH_CUBE")
        row = create.row(align=True)
        for primitive, label in (("CUBE", "Cube"), ("SPHERE", "Sphere"), ("CYLINDER", "Cylinder")):
            op = row.operator("blackmamba.add_primitive", text=label)
            op.primitive = primitive

        material = layout.box()
        material.label(text="Material", icon="MATERIAL")
        grid = material.grid_flow(columns=2, align=True)
        for preset, label, _description in PRESETS:
            op = grid.operator("blackmamba.apply_material", text=label)
            op.preset = preset

        form = layout.box()
        form.label(text="Form", icon="MOD_BEVEL")
        form.prop(context.scene, "bm_bevel_width")
        form.prop(context.scene, "bm_bevel_segments")
        row = form.row(align=True)
        op = row.operator("blackmamba.form_action", text="Bevel")
        op.action = "BEVEL"
        op = row.operator("blackmamba.form_action", text="Smooth")
        op.action = "SMOOTH"
        form.prop(context.scene, "bm_subdivision_levels")
        op = form.operator("blackmamba.form_action", text="Subdivision")
        op.action = "SUBDIVISION"

        mechanics = layout.box()
        mechanics.label(text="Mechanics", icon="PHYSICS")

        spring = mechanics.box()
        spring.label(text="Suspension > Spring", icon="CURVE_DATA")
        spring.prop(context.scene, "bm_spring_wire_diameter")
        spring.prop(context.scene, "bm_spring_coil_diameter")
        spring.prop(context.scene, "bm_spring_free_length")
        spring.prop(context.scene, "bm_spring_turns")
        spring.operator("blackmamba.add_spring", text="Add Spring", icon="ADD")

        damper = mechanics.box()
        damper.label(text="Suspension > Damper", icon="CONSTRAINT_BONE")
        damper.prop(context.scene, "bm_damper_body_diameter")
        damper.prop(context.scene, "bm_damper_body_length")
        damper.prop(context.scene, "bm_damper_rod_diameter")
        damper.prop(context.scene, "bm_damper_stroke")
        damper.prop(context.scene, "bm_damper_mount_outer_diameter")
        damper.prop(context.scene, "bm_damper_mount_bore_diameter")
        damper.prop(context.scene, "bm_damper_mount_width")
        damper.prop(context.scene, "bm_damper_extension_fraction", slider=True)
        damper.operator("blackmamba.add_damper", text="Add Damper", icon="ADD")

        arm = mechanics.box()
        arm.label(text="Suspension > Control Arm", icon="MOD_ARMATURE")
        arm.prop(context.scene, "bm_control_arm_length")
        arm.prop(context.scene, "bm_control_arm_pivot_spacing")
        arm.prop(context.scene, "bm_control_arm_upright_z")
        arm.prop(context.scene, "bm_control_arm_tube_diameter")
        arm.prop(context.scene, "bm_control_arm_joint_diameter")
        arm.operator("blackmamba.add_control_arm", text="Add Control Arm", icon="ADD")


_CLASSES = (
    BM_OT_add_primitive,
    BM_OT_apply_material,
    BM_OT_form_action,
    BM_OT_add_spring,
    BM_OT_add_damper,
    BM_OT_add_control_arm,
    BM_PT_main,
)


def _length_property(name, default, minimum, soft_max):
    return FloatProperty(
        name=name,
        default=default,
        min=minimum,
        soft_max=soft_max,
        precision=4,
        subtype="DISTANCE",
        unit="LENGTH",
    )


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bm_bevel_width = FloatProperty(
        name="Bevel Width", default=0.08, min=0.0, soft_max=1.0, precision=3
    )
    bpy.types.Scene.bm_bevel_segments = IntProperty(
        name="Bevel Segments", default=4, min=1, max=16
    )
    bpy.types.Scene.bm_subdivision_levels = IntProperty(
        name="Subdivision", default=2, min=0, max=4
    )

    bpy.types.Scene.bm_spring_wire_diameter = _length_property("Wire Diameter", 0.012, 0.0005, 0.05)
    bpy.types.Scene.bm_spring_coil_diameter = _length_property("Coil Diameter", 0.080, 0.002, 0.50)
    bpy.types.Scene.bm_spring_free_length = _length_property("Free Length", 0.180, 0.002, 1.0)
    bpy.types.Scene.bm_spring_turns = IntProperty(name="Turns", default=8, min=1, max=64)

    bpy.types.Scene.bm_damper_body_diameter = _length_property("Body Diameter", 0.045, 0.002, 0.30)
    bpy.types.Scene.bm_damper_body_length = _length_property("Body Length", 0.120, 0.005, 1.0)
    bpy.types.Scene.bm_damper_rod_diameter = _length_property("Rod Diameter", 0.012, 0.001, 0.10)
    bpy.types.Scene.bm_damper_stroke = _length_property("Stroke", 0.080, 0.001, 0.50)
    bpy.types.Scene.bm_damper_mount_outer_diameter = _length_property("Mount OD", 0.030, 0.002, 0.20)
    bpy.types.Scene.bm_damper_mount_bore_diameter = _length_property("Mount Bore", 0.014, 0.001, 0.10)
    bpy.types.Scene.bm_damper_mount_width = _length_property("Mount Width", 0.018, 0.001, 0.10)
    bpy.types.Scene.bm_damper_extension_fraction = FloatProperty(
        name="Extension", default=0.50, min=0.0, max=1.0, precision=3, subtype="FACTOR"
    )

    bpy.types.Scene.bm_control_arm_length = _length_property("Arm Length", 0.320, 0.01, 1.0)
    bpy.types.Scene.bm_control_arm_pivot_spacing = _length_property("Pivot Spacing", 0.180, 0.01, 0.60)
    bpy.types.Scene.bm_control_arm_upright_z = FloatProperty(
        name="Upright Z",
        default=0.0,
        min=-0.50,
        max=0.50,
        precision=4,
        subtype="DISTANCE",
        unit="LENGTH",
    )
    bpy.types.Scene.bm_control_arm_tube_diameter = _length_property("Tube Diameter", 0.025, 0.002, 0.10)
    bpy.types.Scene.bm_control_arm_joint_diameter = _length_property("Joint Diameter", 0.038, 0.003, 0.15)

    register_wishbone_ui()


def unregister():
    unregister_wishbone_ui()

    for attr in (
        "bm_bevel_width",
        "bm_bevel_segments",
        "bm_subdivision_levels",
        "bm_spring_wire_diameter",
        "bm_spring_coil_diameter",
        "bm_spring_free_length",
        "bm_spring_turns",
        "bm_damper_body_diameter",
        "bm_damper_body_length",
        "bm_damper_rod_diameter",
        "bm_damper_stroke",
        "bm_damper_mount_outer_diameter",
        "bm_damper_mount_bore_diameter",
        "bm_damper_mount_width",
        "bm_damper_extension_fraction",
        "bm_control_arm_length",
        "bm_control_arm_pivot_spacing",
        "bm_control_arm_upright_z",
        "bm_control_arm_tube_diameter",
        "bm_control_arm_joint_diameter",
    ):
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)

    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
