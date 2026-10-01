from __future__ import annotations

import bpy

from .spring_math import SpringSpec


SPRING_OBJECT_NAME = "BM_Spring"
SPRING_CURVE_NAME = "BM_SpringCurve"


def create_spring(context, spec: SpringSpec):
    """Create one parametric spring curve and make it the active object."""

    points = spec.helix_points()

    curve = bpy.data.curves.new(SPRING_CURVE_NAME, type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = spec.wire_diameter / 2.0
    curve.bevel_resolution = 4
    curve.resolution_u = 2

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

    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    context.view_layer.objects.active = obj
    return obj
