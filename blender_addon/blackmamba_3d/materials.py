"""Fast material presets for the BlackMamba Blender add-on."""

import bpy


PRESETS = (
    ("METALLIC", "Metallic", "Dark polished metal"),
    ("PEARLESCENT", "Pearlescent", "Soft pearl with view-dependent tint"),
    ("IRIDESCENT", "Iridescent", "Angle-dependent rainbow material"),
    ("TRANSPARENT", "Transparent", "Clean transparent/glass-like surface"),
)


def _socket(node, *names):
    for name in names:
        socket = node.inputs.get(name)
        if socket is not None:
            return socket
    return None


def _set(node, value, *names):
    socket = _socket(node, *names)
    if socket is not None:
        socket.default_value = value


def _base_material(name):
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (420, 0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (80, 0)
    material.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return material, bsdf


def _facing_ramp(material, bsdf, colors):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    layer = nodes.new("ShaderNodeLayerWeight")
    layer.location = (-520, 40)
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-260, 40)

    elements = ramp.color_ramp.elements
    elements[0].position = 0.0
    elements[0].color = colors[0]
    elements[1].position = 1.0
    elements[1].color = colors[-1]

    if len(colors) > 2:
        step = 1.0 / (len(colors) - 1)
        for index, color in enumerate(colors[1:-1], start=1):
            element = elements.new(index * step)
            element.color = color

    links.new(layer.outputs["Facing"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], _socket(bsdf, "Base Color"))


def _configure_transparency(material):
    if hasattr(material, "surface_render_method"):
        try:
            material.surface_render_method = "DITHERED"
            return
        except (TypeError, ValueError):
            pass
    if hasattr(material, "blend_method"):
        try:
            material.blend_method = "BLEND"
        except (TypeError, ValueError):
            pass


def build_preset(preset):
    preset = preset.upper()

    if preset == "METALLIC":
        material, bsdf = _base_material("BM_Metallic")
        _set(bsdf, (0.028, 0.032, 0.04, 1.0), "Base Color")
        _set(bsdf, 1.0, "Metallic")
        _set(bsdf, 0.16, "Roughness")
        _set(bsdf, 0.35, "Coat Weight", "Clearcoat")
        return material

    if preset == "PEARLESCENT":
        material, bsdf = _base_material("BM_Pearlescent")
        _facing_ramp(
            material,
            bsdf,
            (
                (0.55, 0.24, 0.68, 1.0),
                (0.95, 0.72, 0.95, 1.0),
                (0.92, 0.96, 1.0, 1.0),
                (0.55, 0.78, 1.0, 1.0),
            ),
        )
        _set(bsdf, 0.22, "Metallic")
        _set(bsdf, 0.2, "Roughness")
        _set(bsdf, 0.65, "Coat Weight", "Clearcoat")
        _set(bsdf, 0.08, "Coat Roughness", "Clearcoat Roughness")
        return material

    if preset == "IRIDESCENT":
        material, bsdf = _base_material("BM_Iridescent")
        _facing_ramp(
            material,
            bsdf,
            (
                (0.05, 0.22, 0.95, 1.0),
                (0.1, 0.95, 0.75, 1.0),
                (0.95, 0.92, 0.08, 1.0),
                (0.95, 0.12, 0.55, 1.0),
                (0.4, 0.08, 0.95, 1.0),
            ),
        )
        _set(bsdf, 0.68, "Metallic")
        _set(bsdf, 0.17, "Roughness")
        _set(bsdf, 0.45, "Coat Weight", "Clearcoat")
        return material

    if preset == "TRANSPARENT":
        material, bsdf = _base_material("BM_Transparent")
        _set(bsdf, (0.72, 0.9, 1.0, 1.0), "Base Color")
        _set(bsdf, 0.05, "Roughness")
        _set(bsdf, 1.0, "Transmission Weight", "Transmission")
        _set(bsdf, 1.45, "IOR")
        _set(bsdf, 0.28, "Alpha")
        _configure_transparency(material)
        return material

    raise ValueError(f"Unknown BlackMamba material preset: {preset}")


def apply_preset(obj, preset, context=None):
    """Apply a preset to the selected object's first material slot."""

    if obj is None or not getattr(obj, "data", None):
        raise ValueError("Select an object with material data first")
    if not hasattr(obj.data, "materials"):
        raise ValueError(f"Object type {obj.type!r} does not support materials")

    material = build_preset(preset)
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

    if context is not None and context.screen is not None:
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.shading.type = "MATERIAL"
                        break

    return material
