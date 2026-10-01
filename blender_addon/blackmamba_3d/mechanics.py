from __future__ import annotations

from math import pi

import bpy

from .damper_math import DamperSpec
from .spring_math import SpringSpec


SPRING_OBJECT_NAME = "BM_Spring"
SPRING_CURVE_NAME = "BM_SpringCurve"
DAMPER_ROOT_NAME = "BM_Damper"


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

    # The torus hole axis is local Y after rotation.  Scale only that axis so
    # the visible concept mount respects the requested axial mount width.
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
