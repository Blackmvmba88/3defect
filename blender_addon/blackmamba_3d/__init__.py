bl_info = {
    "name": "BlackMamba 3D",
    "author": "BlackMamba RECORDS / Iyari Gomez",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > BLACKMAMBA",
    "description": "Modular BlackMamba 3D authoring layer",
    "category": "3D View",
}

import bpy
from bpy.props import EnumProperty, FloatProperty, IntProperty

from .materials import PRESETS, apply_preset


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
        mechanics.label(text="Suspension contract ready")
        mechanics.label(text="Spring + damper runtime: next slice")


_CLASSES = (
    BM_OT_add_primitive,
    BM_OT_apply_material,
    BM_OT_form_action,
    BM_PT_main,
)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bm_bevel_width = FloatProperty(
        name="Bevel Width",
        default=0.08,
        min=0.0,
        soft_max=1.0,
        precision=3,
    )
    bpy.types.Scene.bm_bevel_segments = IntProperty(
        name="Bevel Segments",
        default=4,
        min=1,
        max=16,
    )
    bpy.types.Scene.bm_subdivision_levels = IntProperty(
        name="Subdivision",
        default=2,
        min=0,
        max=4,
    )


def unregister():
    for attr in ("bm_bevel_width", "bm_bevel_segments", "bm_subdivision_levels"):
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)

    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
