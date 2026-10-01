from __future__ import annotations

from math import pi

import bpy
from mathutils import Vector

from .control_arm_math import ControlArmSpec
from .damper_math import DamperSpec
from .double_wishbone_math import DoubleWishboneSpec
from .spring_math import SpringSpec


SPRING_OBJECT_NAME = "BM_Spring"
SPRING_CURVE_NAME = "BM_SpringCurve"
DAMPER_ROOT_NAME = "BM_Damper"
CONTROL_ARM_ROOT_NAME = "BM_ControlArm"
DOUBLE_WISHBONE_ROOT_NAME = "BM_DoubleWishbone"
TRAVEL_PATH_NAME = "BM_WishboneTravelPath"


def _activate(context, obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    context.view_layer.objects.active = obj


def create_spring(context, spec: SpringSpec):
    """Create one parametric spring curve and make it the active object."""

    points = spec.helix_points()

    curve = bpy.data.curves.new(SPRING_CURVE_NAME, type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = spec.wire_diameter / 2.0
    curve.bevel_resolution = 4

    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for spline_point, point in zip(spline.points, points):
        spline_point.co = (*point, 1.0)

    obj = bpy.data.objects.new(SPRING_OBJECT_NAME, curve)
    context.collection.objects.link(obj)

    obj["bm_module_id"] = "mechanics.suspension"
    obj["bm_component"] = "spring"
    obj["bm_wire_diameter"] = spec.wire_diameter
    obj["bm_coil_diameter"] = spec.coil_diameter
    obj["bm_free_length"] = spec.free_length
    obj["bm_turns"] = spec.turns
    obj["bm_pitch"] = spec.pitch
    obj["bm_outer_diameter"] = spec.outer_diameter
    obj["bm_inner_diameter"] = spec.inner_diameter
    obj["bm_maturity"] = "concept"

    _activate(context, obj)
    return obj


def _add_cylinder(name: str, radius: float, depth: float, location):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,
        radius=radius,
        depth=depth,
        location=location,
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


def _add_mount_eye(name: str, spec: DamperSpec, location):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=spec.mount_major_radius,
        minor_radius=spec.mount_minor_radius,
        major_segments=64,
        minor_segments=16,
        location=location,
        rotation=(pi / 2.0, 0.0, 0.0),
    )
    obj = bpy.context.active_object
    obj.name = name

    natural_width = 2.0 * spec.mount_minor_radius
    if natural_width > 0:
        obj.scale.y = spec.mount_width / natural_width
    return obj


def create_damper(context, spec: DamperSpec):
    """Create a grouped telescopic damper concept at the 3D cursor."""

    geometry = spec.geometry()

    root = bpy.data.objects.new(DAMPER_ROOT_NAME, None)
    context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"

    body = _add_cylinder(
        "BM_Damper_Body",
        geometry["body_radius"],
        geometry["body_depth"],
        geometry["body_center"],
    )
    rod = _add_cylinder(
        "BM_Damper_Rod",
        geometry["rod_radius"],
        geometry["rod_depth"],
        geometry["rod_center"],
    )
    bottom_eye = _add_mount_eye(
        "BM_Damper_BottomEye",
        spec,
        geometry["bottom_mount_center"],
    )
    top_eye = _add_mount_eye(
        "BM_Damper_TopEye",
        spec,
        geometry["top_mount_center"],
    )

    for child in (body, rod, bottom_eye, top_eye):
        child.parent = root
        child["bm_component_parent"] = "damper"

    root.location = context.scene.cursor.location
    root["bm_module_id"] = "mechanics.suspension"
    root["bm_component"] = "damper"
    root["bm_body_diameter"] = spec.body_diameter
    root["bm_body_length"] = spec.body_length
    root["bm_rod_diameter"] = spec.rod_diameter
    root["bm_stroke"] = spec.stroke
    root["bm_extension_fraction"] = spec.extension_fraction
    root["bm_current_center_distance"] = spec.current_center_distance
    root["bm_collapsed_center_distance"] = spec.collapsed_center_distance
    root["bm_extended_center_distance"] = spec.extended_center_distance
    root["bm_mount_outer_diameter"] = spec.mount_outer_diameter
    root["bm_mount_bore_diameter"] = spec.mount_bore_diameter
    root["bm_mount_width"] = spec.mount_width
    root["bm_maturity"] = "concept"

    _activate(context, root)
    return root


def _add_strut(name: str, start, end, radius: float):
    start_v = Vector(start)
    end_v = Vector(end)
    direction = end_v - start_v
    length = direction.length
    if length <= 0:
        raise ValueError("strut endpoints must be distinct")

    midpoint = (start_v + end_v) / 2.0
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=48,
        radius=radius,
        depth=length,
        location=midpoint,
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    return obj


def _add_joint(name: str, location, radius: float):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=48,
        ring_count=24,
        radius=radius,
        location=location,
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


def create_control_arm(context, spec: ControlArmSpec):
    """Create a dimensioned A-arm from two chassis pivots and one upright joint."""

    geometry = spec.geometry()
    front = geometry["front_pivot"]
    rear = geometry["rear_pivot"]
    upright = geometry["upright_joint"]

    root = bpy.data.objects.new(CONTROL_ARM_ROOT_NAME, None)
    context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"

    front_leg = _add_strut(
        "BM_ControlArm_FrontLeg", front, upright, geometry["tube_radius"]
    )
    rear_leg = _add_strut(
        "BM_ControlArm_RearLeg", rear, upright, geometry["tube_radius"]
    )
    front_joint = _add_joint(
        "BM_ControlArm_FrontPivot", front, geometry["joint_radius"]
    )
    rear_joint = _add_joint(
        "BM_ControlArm_RearPivot", rear, geometry["joint_radius"]
    )
    upright_joint = _add_joint(
        "BM_ControlArm_UprightJoint", upright, geometry["joint_radius"]
    )

    for child in (front_leg, rear_leg, front_joint, rear_joint, upright_joint):
        child.parent = root
        child["bm_component_parent"] = "control_arm"

    root.location = context.scene.cursor.location
    root["bm_module_id"] = "mechanics.suspension"
    root["bm_component"] = "control_arm"
    root["bm_arm_length"] = spec.arm_length
    root["bm_pivot_spacing"] = spec.pivot_spacing
    root["bm_upright_z"] = spec.upright_z
    root["bm_tube_diameter"] = spec.tube_diameter
    root["bm_joint_diameter"] = spec.joint_diameter
    root["bm_front_leg_length"] = spec.front_leg_length
    root["bm_rear_leg_length"] = spec.rear_leg_length
    root["bm_interface_front_pivot"] = list(spec.front_pivot)
    root["bm_interface_rear_pivot"] = list(spec.rear_pivot)
    root["bm_interface_upright_joint"] = list(spec.upright_joint)
    root["bm_maturity"] = "concept"

    _activate(context, root)
    return root


def _wishbone_points(spec: DoubleWishboneSpec, pose):
    return {
        "lower_front": (0.0, spec.lower_pivot_spacing / 2.0, 0.0),
        "lower_rear": (0.0, -spec.lower_pivot_spacing / 2.0, 0.0),
        "upper_front": (
            0.0,
            spec.upper_pivot_spacing / 2.0,
            spec.chassis_vertical_separation,
        ),
        "upper_rear": (
            0.0,
            -spec.upper_pivot_spacing / 2.0,
            spec.chassis_vertical_separation,
        ),
        "lower_joint": (pose.lower_joint[0], 0.0, pose.lower_joint[1]),
        "upper_joint": (pose.upper_joint[0], 0.0, pose.upper_joint[1]),
        "hub": (pose.upright_midpoint[0], 0.0, pose.upright_midpoint[1]),
    }


def create_double_wishbone(
    context,
    spec: DoubleWishboneSpec,
    *,
    lower_angle_deg: float = 0.0,
):
    """Build a solved four-link double-wishbone pose at the 3D cursor."""

    pose = spec.solve(lower_angle_deg)
    points = _wishbone_points(spec, pose)
    tube_radius = spec.tube_diameter / 2.0
    joint_radius = spec.joint_diameter / 2.0

    root = bpy.data.objects.new(DOUBLE_WISHBONE_ROOT_NAME, None)
    context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"

    children = [
        _add_strut("BM_DW_LowerFrontLeg", points["lower_front"], points["lower_joint"], tube_radius),
        _add_strut("BM_DW_LowerRearLeg", points["lower_rear"], points["lower_joint"], tube_radius),
        _add_strut("BM_DW_UpperFrontLeg", points["upper_front"], points["upper_joint"], tube_radius),
        _add_strut("BM_DW_UpperRearLeg", points["upper_rear"], points["upper_joint"], tube_radius),
        _add_strut("BM_DW_Upright", points["lower_joint"], points["upper_joint"], tube_radius),
    ]

    for name, point in (
        ("BM_DW_LowerFrontPivot", points["lower_front"]),
        ("BM_DW_LowerRearPivot", points["lower_rear"]),
        ("BM_DW_UpperFrontPivot", points["upper_front"]),
        ("BM_DW_UpperRearPivot", points["upper_rear"]),
        ("BM_DW_LowerJoint", points["lower_joint"]),
        ("BM_DW_UpperJoint", points["upper_joint"]),
        ("BM_DW_Hub", points["hub"]),
    ):
        children.append(_add_joint(name, point, joint_radius))

    for child in children:
        child.parent = root
        child["bm_component_parent"] = "double_wishbone"

    root.location = context.scene.cursor.location
    root["bm_module_id"] = "mechanics.suspension"
    root["bm_component"] = "double_wishbone"
    root["bm_lower_arm_length"] = spec.lower_arm_length
    root["bm_upper_arm_length"] = spec.upper_arm_length
    root["bm_chassis_vertical_separation"] = spec.chassis_vertical_separation
    root["bm_upright_length"] = spec.upright_length
    root["bm_lower_angle_deg"] = pose.lower_angle_deg
    root["bm_upright_lean_deg"] = pose.upright_lean_deg
    root["bm_travel_z"] = pose.travel_z
    root["bm_hub_point"] = list(points["hub"])
    root["bm_maturity"] = "concept"

    _activate(context, root)
    return root


def create_wishbone_travel_path(
    context,
    spec: DoubleWishboneSpec,
    *,
    min_angle_deg: float,
    max_angle_deg: float,
    steps: int,
):
    """Create a hub-center path for a deterministic suspension travel sweep."""

    poses = spec.travel_sweep(min_angle_deg, max_angle_deg, steps)
    curve = bpy.data.curves.new(TRAVEL_PATH_NAME, type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = max(spec.tube_diameter * 0.12, 0.001)
    curve.bevel_resolution = 3

    spline = curve.splines.new("POLY")
    spline.points.add(len(poses) - 1)
    for point, pose in zip(spline.points, poses):
        point.co = (pose.upright_midpoint[0], 0.0, pose.upright_midpoint[1], 1.0)

    obj = bpy.data.objects.new(TRAVEL_PATH_NAME, curve)
    context.collection.objects.link(obj)
    obj.location = context.scene.cursor.location
    obj["bm_module_id"] = "mechanics.suspension"
    obj["bm_component"] = "travel_test"
    obj["bm_parent_component"] = "double_wishbone"
    obj["bm_min_angle_deg"] = min_angle_deg
    obj["bm_max_angle_deg"] = max_angle_deg
    obj["bm_steps"] = steps
    obj["bm_min_travel_z"] = min(pose.travel_z for pose in poses)
    obj["bm_max_travel_z"] = max(pose.travel_z for pose in poses)
    obj["bm_min_upright_lean_deg"] = min(pose.upright_lean_deg for pose in poses)
    obj["bm_max_upright_lean_deg"] = max(pose.upright_lean_deg for pose in poses)
    obj["bm_maturity"] = "concept_validation"

    _activate(context, obj)
    return obj
