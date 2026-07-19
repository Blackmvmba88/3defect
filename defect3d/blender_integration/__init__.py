"""Blender integration for 3defect."""

from ._blender_check import (
    is_blender_available,
    get_blender_error,
    require_blender,
    warn_blender_unavailable
)

# Import core classes, but handle graceful degradation
try:
    from .exporter import BlenderExporter, export_to_blender
except (ImportError, RuntimeError):
    # If bpy is unavailable, these won't work, but we still expose them
    # for compatibility. They'll warn/error when actually called.
    BlenderExporter = None
    export_to_blender = None

try:
    from .renderer import BlenderRenderer, render_to_image
except (ImportError, RuntimeError):
    BlenderRenderer = None
    render_to_image = None

__all__ = [
    'is_blender_available',
    'get_blender_error',
    'require_blender',
    'warn_blender_unavailable',
    'BlenderExporter',
    'export_to_blender',
    'BlenderRenderer',
    'render_to_image'
]
