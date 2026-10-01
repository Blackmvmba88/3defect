"""Canonical module registry for the BlackMamba Blender layer.

This module intentionally has no ``bpy`` dependency.  It defines the stable
vocabulary that UI adapters, Blender operators and external tools can share.
Runtime implementations can be added behind these identifiers without making
the user-facing module tree depend on Blender internals.
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class ModuleSpec:
    """Describe one user-facing BlackMamba 3D module."""

    module_id: str
    label: str
    category: str
    actions: Tuple[str, ...] = field(default_factory=tuple)
    children: Tuple[str, ...] = field(default_factory=tuple)
    parametric: bool = True
    previewable: bool = True
    preset_capable: bool = True


class ModuleRegistry:
    """In-memory registry used by UI and adapter layers."""

    def __init__(self, specs: Iterable[ModuleSpec] = ()) -> None:
        self._specs: Dict[str, ModuleSpec] = {}
        for spec in specs:
            self.register(spec)

    def register(self, spec: ModuleSpec) -> None:
        if spec.module_id in self._specs:
            raise ValueError(f"duplicate module_id: {spec.module_id}")
        self._specs[spec.module_id] = spec

    def get(self, module_id: str) -> ModuleSpec:
        try:
            return self._specs[module_id]
        except KeyError as exc:
            raise KeyError(f"unknown BlackMamba module: {module_id}") from exc

    def list_category(self, category: str) -> Tuple[ModuleSpec, ...]:
        return tuple(
            spec for spec in self._specs.values() if spec.category == category
        )

    def as_dict(self) -> Dict[str, ModuleSpec]:
        return dict(self._specs)


def default_registry() -> ModuleRegistry:
    """Return the canonical first-pass BlackMamba Blender module tree."""

    return ModuleRegistry(
        [
            ModuleSpec(
                "create",
                "Create",
                "root",
                actions=(
                    "cube",
                    "sphere",
                    "cylinder",
                    "plane",
                    "tube",
                    "spring",
                    "bolt",
                    "gear",
                ),
            ),
            ModuleSpec(
                "material",
                "Material",
                "root",
                actions=(
                    "metallic",
                    "brushed_metal",
                    "chrome",
                    "pearlescent",
                    "iridescent",
                    "holographic",
                    "transparent",
                    "glass",
                    "plastic",
                    "rubber",
                    "carbon_fiber",
                    "wood",
                    "stone",
                    "water",
                    "emissive",
                ),
            ),
            ModuleSpec(
                "form",
                "Form",
                "root",
                actions=(
                    "bevel",
                    "smooth",
                    "subdivision",
                    "solidify",
                    "mirror",
                    "array",
                    "boolean",
                    "twist",
                    "bend",
                    "taper",
                ),
            ),
            ModuleSpec(
                "mechanics",
                "Mechanics",
                "root",
                children=(
                    "mechanics.suspension",
                    "mechanics.drivetrain",
                    "mechanics.motion",
                    "mechanics.structure",
                ),
            ),
            ModuleSpec(
                "mechanics.suspension",
                "Suspension",
                "mechanics",
                actions=(
                    "macpherson",
                    "double_wishbone",
                    "multilink",
                    "trailing_arm",
                    "pushrod",
                    "hydraulic",
                    "pneumatic",
                    "spring",
                    "damper",
                    "control_arm",
                    "wheel_hub",
                    "steering_link",
                    "travel_test",
                ),
            ),
            ModuleSpec(
                "mechanics.drivetrain",
                "Drivetrain",
                "mechanics",
                actions=("axle", "gear", "pulley", "belt", "chain", "differential"),
            ),
            ModuleSpec(
                "mechanics.motion",
                "Motion",
                "mechanics",
                actions=("hinge", "piston", "rack", "cam", "slider", "universal_joint"),
            ),
            ModuleSpec(
                "mechanics.structure",
                "Structure",
                "mechanics",
                actions=("chassis", "mount", "anchor", "brace", "frame"),
            ),
            ModuleSpec(
                "assembly",
                "Assembly",
                "root",
                actions=(
                    "parent",
                    "constraint",
                    "align",
                    "snap",
                    "bolt_join",
                    "interface_match",
                    "verify_tolerances",
                ),
            ),
            ModuleSpec(
                "animation",
                "Animation",
                "root",
                actions=(
                    "rotate",
                    "translate",
                    "oscillate",
                    "bounce",
                    "compression",
                    "loop",
                    "keyframe",
                    "driver",
                    "camera_orbit",
                ),
            ),
            ModuleSpec(
                "physics",
                "Physics",
                "root",
                actions=(
                    "gravity",
                    "collision",
                    "rigid_body",
                    "soft_body",
                    "cloth",
                    "fluid",
                    "particles",
                    "spring_damper",
                ),
            ),
            ModuleSpec(
                "world",
                "World",
                "root",
                actions=(
                    "technical_floor",
                    "studio",
                    "industrial_room",
                    "garage",
                    "track",
                    "castle",
                    "scifi_lab",
                    "anime_scene",
                ),
            ),
            ModuleSpec(
                "output",
                "Output",
                "root",
                actions=(
                    "preview_render",
                    "turntable",
                    "final_render",
                    "wireframe",
                    "exploded_view",
                    "blueprint_view",
                    "export_glb",
                    "export_fbx",
                    "export_obj",
                    "export_stl",
                ),
            ),
        ]
    )
