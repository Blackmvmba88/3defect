from __future__ import annotations

import bpy
from bpy.props import FloatProperty

from .brake_rig_math import BrakeRigSpec, simulate_braking_run
from .double_wishbone_math import DoubleWishboneSpec
from .wishbone_ui import spec_from_scene


class BM_OT_brake_dive_test(bpy.types.Operator):
    bl_idname = "blackmamba.brake_dive_test"
    bl_label = "Run BlackMamba Brake Dive Test"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        suspension: DoubleWishboneSpec = spec_from_scene(scene)
        rig = BrakeRigSpec(
            vehicle_mass_kg=scene.bm_brake_vehicle_mass_kg,
            wheelbase_m=scene.bm_brake_wheelbase_m,
            cg_height_m=scene.bm_brake_cg_height_m,
            initial_speed_mps=scene.bm_brake_initial_speed_mps,
            decel_mps2=scene.bm_brake_decel_mps2,
            front_corner_sprung_mass_kg=scene.bm_brake_corner_mass_kg,
            spring_rate_n_per_m=scene.bm_brake_spring_rate,
            damping_n_s_per_m=scene.bm_brake_damping,
            duration_s=scene.bm_brake_duration_s,
            sample_hz=scene.bm_brake_sample_hz,
            min_angle_deg=scene.bm_wishbone_travel_min_angle_deg,
            max_angle_deg=scene.bm_wishbone_travel_max_angle_deg,
        )

        try:
            samples = simulate_braking_run(suspension, rig)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        curve = bpy.data.curves.new("BM_BrakeDiveTrace", type="CURVE")
        curve.dimensions = "3D"
        curve.bevel_depth = max(suspension.tube_diameter * 0.10, 0.001)
        curve.bevel_resolution = 3

        spline = curve.splines.new("POLY")
        spline.points.add(len(samples) - 1)
        for point, sample in zip(spline.points, samples):
            point.co = (
                sample.pose.upright_midpoint[0],
                sample.time_s,
                sample.pose.upright_midpoint[1],
                1.0,
            )

        obj = bpy.data.objects.new("BM_BrakeDiveTrace", curve)
        context.collection.objects.link(obj)
        obj.location = scene.cursor.location
        obj["bm_module_id"] = "mechanics.suspension"
        obj["bm_component"] = "brake_dive_test"
        obj["bm_initial_speed_mps"] = rig.initial_speed_mps
        obj["bm_decel_mps2"] = rig.decel_mps2
        obj["bm_longitudinal_g"] = rig.decel_mps2 / 9.80665
        obj["bm_total_load_transfer_n"] = rig.total_load_transfer_n
        obj["bm_front_corner_load_step_n"] = rig.front_corner_load_step_n
        obj["bm_static_corner_compression_m"] = rig.static_corner_compression_m
        obj["bm_peak_compression_m"] = max(s.compression_m for s in samples)
        obj["bm_peak_upright_lean_deg"] = max(
            abs(s.pose.upright_lean_deg) for s in samples
        )
        obj["bm_maturity"] = "concept_validation"

        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        context.view_layer.objects.active = obj

        self.report(
            {"INFO"},
            (
                f"Brake dive peak {obj['bm_peak_compression_m']:.4f} m | "
                f"load transfer {rig.total_load_transfer_n:.0f} N"
            ),
        )
        return {"FINISHED"}


class BM_PT_brake_rig(bpy.types.Panel):
    bl_label = "Suspension > Brake Rig"
    bl_idname = "BM_PT_brake_rig"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BLACKMAMBA"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        vehicle = layout.box()
        vehicle.label(text="Vehicle", icon="AUTO")
        vehicle.prop(scene, "bm_brake_vehicle_mass_kg")
        vehicle.prop(scene, "bm_brake_wheelbase_m")
        vehicle.prop(scene, "bm_brake_cg_height_m")
        vehicle.prop(scene, "bm_brake_initial_speed_mps")
        vehicle.prop(scene, "bm_brake_decel_mps2")

        corner = layout.box()
        corner.label(text="Front Corner", icon="PHYSICS")
        corner.prop(scene, "bm_brake_corner_mass_kg")
        corner.prop(scene, "bm_brake_spring_rate")
        corner.prop(scene, "bm_brake_damping")
        corner.prop(scene, "bm_brake_duration_s")
        corner.prop(scene, "bm_brake_sample_hz")
        corner.operator(
            "blackmamba.brake_dive_test",
            text="Run Brake Dive Test",
            icon="PLAY",
        )


_CLASSES = (BM_OT_brake_dive_test, BM_PT_brake_rig)
_PROPERTIES = (
    "bm_brake_vehicle_mass_kg",
    "bm_brake_wheelbase_m",
    "bm_brake_cg_height_m",
    "bm_brake_initial_speed_mps",
    "bm_brake_decel_mps2",
    "bm_brake_corner_mass_kg",
    "bm_brake_spring_rate",
    "bm_brake_damping",
    "bm_brake_duration_s",
    "bm_brake_sample_hz",
)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bm_brake_vehicle_mass_kg = FloatProperty(
        name="Vehicle Mass (kg)", default=1500.0, min=100.0, max=10000.0
    )
    bpy.types.Scene.bm_brake_wheelbase_m = FloatProperty(
        name="Wheelbase (m)", default=2.70, min=0.5, max=10.0, precision=3
    )
    bpy.types.Scene.bm_brake_cg_height_m = FloatProperty(
        name="CG Height (m)", default=0.55, min=0.05, max=3.0, precision=3
    )
    bpy.types.Scene.bm_brake_initial_speed_mps = FloatProperty(
        name="Initial Speed (m/s)", default=27.78, min=0.1, max=150.0, precision=2
    )
    bpy.types.Scene.bm_brake_decel_mps2 = FloatProperty(
        name="Deceleration (m/s²)", default=8.0, min=0.1, max=30.0, precision=2
    )
    bpy.types.Scene.bm_brake_corner_mass_kg = FloatProperty(
        name="Corner Sprung Mass (kg)", default=375.0, min=20.0, max=3000.0
    )
    bpy.types.Scene.bm_brake_spring_rate = FloatProperty(
        name="Spring Rate (N/m)", default=35000.0, min=1000.0, max=500000.0
    )
    bpy.types.Scene.bm_brake_damping = FloatProperty(
        name="Damping (N·s/m)", default=3200.0, min=100.0, max=50000.0
    )
    bpy.types.Scene.bm_brake_duration_s = FloatProperty(
        name="Duration (s)", default=2.0, min=0.1, max=20.0, precision=2
    )
    bpy.types.Scene.bm_brake_sample_hz = FloatProperty(
        name="Sample Rate (Hz)", default=120.0, min=10.0, max=1000.0, precision=1
    )


def unregister():
    for attr in _PROPERTIES:
        if hasattr(bpy.types.Scene, attr):
            delattr(bpy.types.Scene, attr)
    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)
