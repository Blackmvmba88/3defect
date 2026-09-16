from __future__ import annotations

import bpy
from bpy.props import FloatProperty, IntProperty

from .brake_ui import register as register_brake_ui
from .brake_ui import unregister as unregister_brake_ui
from .double_wishbone_math import DoubleWishboneSpec
from .mechanics import create_double_wishbone, create_wishbone_travel_path


class BM_OT_add_double_wishbone(bpy.types.Operator):
    bl_idname = "blackmamba.add_double_wishbone"
    bl_label = "Add BlackMamba Double Wishbone"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        spec = spec_from_scene(context.scene)
        try:
            obj = create_double_wishbone(
                context,
                spec,
                lower_angle_deg=context.scene.bm_wishbone_lower_angle_deg,
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            (
                f"Created {obj.name}: travel {obj['bm_travel_z']:.4f}, "
                f"upright lean {obj['bm_upright_lean_deg']:.2f} deg"
            ),
        )
        return {"FINISHED"}


class BM_OT_wishbone_travel_test(bpy.types.Operator):
    bl_idname = "blackmamba.wishbone_travel_test"
    bl_label = "Run BlackMamba Wishbone Travel Test"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        spec = spec_from_scene(scene)
        try:
            obj = create_wishbone_travel_path(
                context,
                spec,
                min_angle_deg=scene.bm_wishbone_travel_min_angle_deg,
                max_angle_deg=scene.bm_wishbone_travel_max_angle_deg,
                steps=scene.bm_wishbone_travel_steps,
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            (
                f"Travel path: {obj['bm_min_travel_z']:.4f} to "
                f"{obj['bm_max_travel_z']:.4f}"
            ),
        )
        return {"FINISHED"}


class BM_PT_wishbone(bpy.types.Panel):
    bl_label = "Suspension > Double Wishbone"
    bl_idname = "BM_PT_wishbone"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BLACKMAMBA"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        geometry = layout.box()
        geometry.label(text="Geometry", icon="MOD_ARMATURE")
        geometry.prop(scene, "bm_wishbone_lower_arm_length")
        geometry.prop(scene, "bm_wishbone_upper_arm_length")
        geometry.prop(scene, "bm_wishbone_chassis_vertical_separation")
        geometry.prop(scene, "bm_wishbone_lower_pivot_spacing")
        geometry.prop(scene, "bm_wishbone_upper_pivot_spacing")
        geometry.prop(scene, "bm_wishbone_tube_diameter")
        geometry.prop(scene, "bm_wishbone_joint_diameter")
        geometry.prop(scene, "bm_wishbone_lower_angle_deg")
        geometry.operator(
            "blackmamba.add_double_wishbone",
            text="Add Double Wishbone",
            icon="ADD",
        )

        travel = layout.box()
        travel.label(text="Travel Test", icon="FCURVE")
        travel.prop(scene, "bm_wishbone_travel_min_angle_deg")
        travel.prop(scene, "bm_wishbone_travel_max_angle_deg")
        travel.prop(scene, "bm_wishbone_travel_steps")
        travel.operator(
            "blackmamba.wishbone_travel_test",
            text="Generate Travel Path",
            icon="PLAY",
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


def spec_from_scene(scene) -> DoubleWishboneSpec:
    return DoubleWishboneSpec(
        lower_arm_length=scene.bm_wishbone_lower_arm_length,
        upper_arm_length=scene.bm_wishbone_upper_arm_length,
        chassis_vertical_separation=scene.bm_wishbone_chassis_vertical_separation,
        lower_pivot_spacing=scene.bm_wishbone_lower_pivot_spacing,
        upper_pivot_spacing=scene.bm_wishbone_upper_pivot_spacing,
        tube_diameter=scene.bm_wishbone_tube_diameter,
        joint_diameter=scene.bm_wishbone_joint_diameter,
    )


_CLASSES = (
    BM_OT_add_double_wishbone,
    BM_OT_wishbone_travel_test,
    BM_PT_wishbone,
)

_PROPERTIES = (
    "bm_wishbone_lower_arm_length",
    "bm_wishbone_upper_arm_length",
    "bm_wishbone_chassis_vertical_separation",
    "bm_wishbone_lower_pivot_spacing",
    "bm_wishbone_upper_pivot_spacing",
    "bm_wishbone_tube_diameter",
    "bm_wishbone_joint_diameter",
    "bm_wishbone_lower_angle_deg",
    "bm_wishbone_travel_min_angle_deg",
    "bm_wishbone_travel_max_angle_deg",
    "bm_wishbone_travel_steps",
)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bm_wishbone_lower_arm_length = _length_property(
        "Lower Arm Length", 0.340, 0.01, 1.0
    )
    bpy.types.Scene.bm_wishbone_upper_arm_length = _length_property(
        "Upper Arm Length", 0.300, 0.01, 1.0
    )
    bpy.types.Scene.bm_wishbone_chassis_vertical_separation = _length_property(
        "Chassis Vertical Sep", 0.180, 0.01, 0.80
    )
    bpy.types.Scene.bm_wishbone_lower_pivot_spacing = _length_property(
        "Lower Pivot Spacing", 0.200, 0.01, 0.80
    )
    bpy.types.Scene.bm_wishbone_upper_pivot_spacing = _length_property(
        "Upper Pivot Spacing", 0.160, 0.01, 0.80
    )
    bpy.types.Scene.bm_wishbone_tube_diameter = _length_property(
        "Tube Diameter", 0.025, 0.002, 0.10
    )
    bpy.types.Scene.bm_wishbone_joint_diameter = _length_property(
        "Joint Diameter", 0.038, 0.003, 0.15
    )
    bpy.types.Scene.bm_wishbone_lower_angle_deg = FloatProperty(
        name="Lower Arm Angle",
        default=0.0,
        min=-45.0,
        max=45.0,
        precision=2,
        subtype="ANGLE",
    )
    bpy.types.Scene.bm_wishbone_travel_min_angle_deg = FloatProperty(
        name="Travel Min Angle",
        default=-15.0,
        min=-45.0,
        max=44.0,
        precision=2,
    )
    bpy.types.Scene.bm_wishbone_travel_max_angle_deg = FloatProperty(
        name="Travel Max Angle",
        default=15.0,
        min=-44.0,
        max=45.0,
        precision=2,
    )
    bpy.types.Scene.bm_wishbone_travel_steps = IntProperty(
        name="Travel Samples",
        default=13,
        min=2,
        max=101,
    )

    register_brake_ui()


def unregister():
    unregister_brake_ui()

    for attr in _PROPERTIES:
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)

    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)
