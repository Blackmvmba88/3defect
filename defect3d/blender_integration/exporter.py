"""
Blender integration and export functionality.

This module provides functions to export 3defect models to Blender
for visualization and rendering.
"""

from typing import List, Union
import json


class BlenderExporter:
    """
    Export 3defect models to Blender.

    This class handles the conversion of 3defect shapes and composite parts
    into Blender-compatible Python scripts.
    """

    def __init__(self):
        """Initialize the Blender exporter."""
        self.objects = []

    def add_object(self, obj):
        """Add an object to export."""
        self.objects.append(obj)

    def generate_blender_script(self) -> str:
        """
        Generate a Blender Python script to create the objects.

        Returns:
            A string containing the Blender Python script
        """
        script_lines = [
            "import bpy",
            "import math",
            "",
            "# Clear existing objects",
            "bpy.ops.object.select_all(action='SELECT')",
            "bpy.ops.object.delete()",
            "",
            "# Helper function to create materials",
            "def create_material(name, color):",
            "    mat = bpy.data.materials.new(name=name)",
            "    mat.use_nodes = True",
            "    bsdf = mat.node_tree.nodes['Principled BSDF']",
            "    bsdf.inputs['Base Color'].default_value = color",
            "    return mat",
            "",
        ]

        obj_counter = 0

        for obj in self.objects:
            script_lines.extend(self._convert_object(obj, obj_counter))
            obj_counter += 1

        # Add camera and lighting
        script_lines.extend([
            "",
            "# Add camera",
            "bpy.ops.object.camera_add(location=(10, -10, 8))",
            "camera = bpy.context.object",
            "camera.rotation_euler = (1.1, 0, 0.8)",
            "",
            "# Set camera as active",
            "bpy.context.scene.camera = camera",
            "",
            "# Add sun light",
            "bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))",
            "light = bpy.context.object",
            "light.data.energy = 2.0",
            "",
            "# Set viewport shading to solid",
            "for area in bpy.context.screen.areas:",
            "    if area.type == 'VIEW_3D':",
            "        for space in area.spaces:",
            "            if space.type == 'VIEW_3D':",
            "                space.shading.type = 'SOLID'",
            "",
        ])

        return "\n".join(script_lines)

    def _convert_object(self, obj, counter: int) -> List[str]:
        """Convert a single object to Blender script lines."""
        from ..core.shapes import Shape3D
        from ..core.composite import CompositePart

        lines = []

        if isinstance(obj, CompositePart):
            lines.append(f"# Composite: {obj.name}")
            # Recursively process all parts, including nested composites
            self._process_composite(obj, lines, counter)
        elif isinstance(obj, Shape3D):
            lines.extend(self._convert_shape(obj, str(counter)))

        return lines

    def _process_composite(
            self,
            composite,
            lines: List[str],
            counter: int,
            level: int = 0):
        """Process a composite part recursively."""
        from ..core.shapes import Shape3D
        from ..core.composite import CompositePart

        for i, part in enumerate(composite.parts):
            if isinstance(part, CompositePart):
                lines.append(f"# Nested Composite: {part.name}")
                self._process_composite(
                    part, lines, f"{counter}_{i}", level + 1)
            elif isinstance(part, Shape3D):
                lines.extend(
                    self._convert_shape(
                        part, f"{counter}_{level}_{i}"))

    def _convert_shape(self, shape, obj_id: str) -> List[str]:
        """Convert a shape to Blender creation code."""
        lines = []
        shape_type = type(shape).__name__

        # Helper to convert numpy values to Python floats
        def to_tuple(arr):
            return tuple(float(x) for x in arr)

        # Create the primitive
        if shape_type == "Cube":
            lines.append(
                f"bpy.ops.mesh.primitive_cube_add(size={
                    float(
                        shape.size)}, " f"location={
                    to_tuple(
                        shape.position)})")
        elif shape_type == "Sphere":
            lines.append(
                f"bpy.ops.mesh.primitive_uv_sphere_add(radius={
                    float(
                        shape.radius)}, " f"location={
                    to_tuple(
                        shape.position)})")
        elif shape_type == "Cylinder":
            lines.append(
                f"bpy.ops.mesh.primitive_cylinder_add(radius={
                    float(
                        shape.radius)}, " f"depth={
                    float(
                        shape.height)}, location={
                    to_tuple(
                        shape.position)})")
        elif shape_type == "Cone":
            lines.append(
                f"bpy.ops.mesh.primitive_cone_add(radius1={
                    float(
                        shape.radius)}, " f"depth={
                    float(
                        shape.height)}, location={
                    to_tuple(
                        shape.position)})")
        elif shape_type == "Torus":
            lines.append(
                f"bpy.ops.mesh.primitive_torus_add(major_radius={
                    float(
                        shape.major_radius)}, " f"minor_radius={
                    float(
                        shape.minor_radius)}, location={
                    to_tuple(
                        shape.position)})")
        else:
            # Default to cube
            lines.append(
                f"bpy.ops.mesh.primitive_cube_add(location={
                    to_tuple(
                        shape.position)})")

        lines.append(f"obj_{obj_id} = bpy.context.object")
        lines.append(f"obj_{obj_id}.name = '{shape.name}_{obj_id}'")

        # Apply rotation (convert degrees to radians)
        if any(shape.rotation != 0):
            import math
            rot_rad = tuple(float(r) * math.pi / 180.0 for r in shape.rotation)
            lines.append(f"obj_{obj_id}.rotation_euler = {rot_rad}")

        # Apply scale
        if any(shape.scale != 1):
            lines.append(f"obj_{obj_id}.scale = {to_tuple(shape.scale)}")

        # Apply material/color
        color = shape.material.get("color", (0.8, 0.8, 0.8, 1.0))
        lines.append(
            f"mat_{obj_id} = create_material('Material_{obj_id}', {color})")
        lines.append(f"obj_{obj_id}.data.materials.append(mat_{obj_id})")
        lines.append("")

        return lines

    def save_script(self, filename: str):
        """
        Save the Blender script to a file.

        Args:
            filename: Path to save the script
        """
        script = self.generate_blender_script()
        with open(filename, 'w') as f:
            f.write(script)
        print(f"Blender script saved to: {filename}")

    def save_json(self, filename: str):
        """
        Save objects as JSON for alternative processing.

        Args:
            filename: Path to save the JSON file
        """
        data = {
            "objects": [obj.to_dict() for obj in self.objects]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"JSON data saved to: {filename}")


def export_to_blender(objects: Union[object, List[object]],
                      output_file: str = "blender_export.py",
                      also_json: bool = False) -> BlenderExporter:
    """
    Quick export function for objects to Blender.

    Args:
        objects: Single object or list of objects to export
        output_file: Output filename for the Blender script
        also_json: Also save as JSON format

    Returns:
        The BlenderExporter instance used
    """
    exporter = BlenderExporter()

    if isinstance(objects, list):
        for obj in objects:
            exporter.add_object(obj)
    else:
        exporter.add_object(objects)

    exporter.save_script(output_file)

    if also_json:
        json_file = output_file.replace('.py', '.json')
        exporter.save_json(json_file)

    return exporter
