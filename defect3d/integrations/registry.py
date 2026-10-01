"""Capability registry for the BlackMamba 3D ecosystem.

The registry deliberately avoids importing sibling repositories. It records what
those repositories can provide so integrations can be added through adapters
without coupling the 3defect core to their internal layout.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Tuple


@dataclass(frozen=True)
class Provider:
    """One repository/provider in the BlackMamba 3D ecosystem."""

    key: str
    repository: str
    role: str
    capabilities: Tuple[str, ...]
    integration_mode: str = "adapter"
    status: str = "declared"

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities


PROVIDERS: Tuple[Provider, ...] = (
    Provider(
        key="core",
        repository="Blackmvmba88/3defect",
        role="canonical orchestration, geometry, validation and export core",
        capabilities=(
            "geometry",
            "composites",
            "mechanics",
            "physics",
            "validation",
            "blender",
            "render",
            "export",
        ),
        integration_mode="native",
        status="active",
    ),
    Provider(
        key="assembly",
        repository="Blackmvmba88/weaponassambly",
        role="deterministic assembly, sockets and Bolt optimization patterns",
        capabilities=(
            "assembly",
            "sockets",
            "scene_manifest",
            "determinism",
            "parametric_descriptors",
            "performance",
        ),
    ),
    Provider(
        key="architecture",
        repository="Blackmvmba88/mamba-architecture",
        role="procedural, organic and architectural geometry provider",
        capabilities=(
            "procedural_geometry",
            "organic_geometry",
            "architecture",
            "mesh_export",
            "stl",
            "gltf",
        ),
    ),
    Provider(
        key="ocarina",
        repository="Blackmvmba88/ocarine",
        role="dimension-sensitive physical-object reference implementation",
        capabilities=(
            "dimensional_validation",
            "bmesh_validation",
            "physical_object",
            "acoustics",
            "glb",
            "threejs",
        ),
    ),
    Provider(
        key="circuit",
        repository="Blackmvmba88/circuit",
        role="engineering component and PCB visualization provider",
        capabilities=(
            "components",
            "pcb",
            "blender",
            "stl",
            "obj",
            "gltf",
            "fbx",
        ),
    ),
    Provider(
        key="xarvis_blender",
        repository="Blackmvmba88/XarvisCore",
        role="automated Blender assembly, render and export pipeline",
        capabilities=(
            "blender_automation",
            "procedural_assembly",
            "render_presets",
            "product_render",
            "gltf",
            "fbx",
        ),
    ),
    Provider(
        key="motion",
        repository="Blackmvmba88/blender-motion-capture",
        role="real-time motion transport and Blender bridge",
        capabilities=(
            "websocket",
            "motion_capture",
            "rig",
            "animation",
            "live_stream",
            "replay",
        ),
    ),
    Provider(
        key="wave3d",
        repository="Blackmvmba88/3dwave",
        role="real-time procedural WebGL geometry and GPU rendering research",
        capabilities=(
            "webgl",
            "procedural_mesh",
            "gpu_render",
            "audio_reactive",
            "realtime_render",
        ),
    ),
    Provider(
        key="avion",
        repository="Blackmvmba88/Avion",
        role="Three.js runtime, GLB scene integration and browser optimization",
        capabilities=(
            "threejs",
            "webgl",
            "glb",
            "runtime",
            "resource_optimization",
            "network_compression",
        ),
    ),
    Provider(
        key="patronaje",
        repository="Blackmvmba88/Patronaje",
        role="2D pattern to 3D surface and mesh conversion",
        capabilities=("surface_generation", "mesh", "obj", "stl", "gltf"),
    ),
    Provider(
        key="geo3d",
        repository="Blackmvmba88/js-3d-area-explorer",
        role="geospatial and photorealistic 3D environment visualization",
        capabilities=("geospatial", "cesium", "3d_tiles", "environment_viewer"),
    ),
    Provider(
        key="mastersong_migration",
        repository="Blackmvmba88/MasterSong",
        role="migration source for Blender/bmesh architecture generators",
        capabilities=("blender_scripts", "bmesh", "terrain", "landscape"),
        integration_mode="migration_source",
    ),
    Provider(
        key="rod_forge",
        repository="Blackmvmba88/BlackMamba-Rod-Forge",
        role="Blender blockout/modeling migration source",
        capabilities=("blender", "blockout", "modeling"),
        integration_mode="migration_source",
    ),
    Provider(
        key="circuits_d",
        repository="Blackmvmba88/circuits-D",
        role="circuit design with planned 3D export",
        capabilities=("circuit_design", "planned_glb_export"),
        status="planned",
    ),
    Provider(
        key="rainboe",
        repository="Blackmvmba88/rainboe",
        role="WebGL audiovisual runtime reference",
        capabilities=("webgl", "audio_reactive", "android_runtime"),
    ),
    Provider(
        key="rainbow_wave",
        repository="Blackmvmba88/rainbow-wave-visualizer",
        role="planned WebGL/Three.js and WebXR visualization provider",
        capabilities=("planned_threejs", "planned_webgl", "planned_webxr"),
        status="planned",
    ),
    Provider(
        key="rockhero",
        repository="Blackmvmba88/Rockhero",
        role="Three.js/WebGL audiovisual visualization reference",
        capabilities=("threejs", "webgl", "audio_reactive"),
    ),
)


_PROVIDER_BY_KEY: Dict[str, Provider] = {provider.key: provider for provider in PROVIDERS}


def get_provider(key: str) -> Optional[Provider]:
    """Return a provider by canonical key."""
    return _PROVIDER_BY_KEY.get(key)


def providers_for(capability: str) -> List[Provider]:
    """Return providers advertising one capability, preserving registry order."""
    return [provider for provider in PROVIDERS if provider.supports(capability)]


def all_capabilities() -> Tuple[str, ...]:
    """Return the sorted union of declared ecosystem capabilities."""
    capabilities = {
        capability
        for provider in PROVIDERS
        for capability in provider.capabilities
    }
    return tuple(sorted(capabilities))


def capability_matrix() -> Mapping[str, Tuple[str, ...]]:
    """Return capability -> provider keys mapping."""
    return {
        capability: tuple(provider.key for provider in providers_for(capability))
        for capability in all_capabilities()
    }


def ecosystem_summary() -> List[Mapping[str, object]]:
    """Return a JSON-serializable provider summary for CLI/API consumers."""
    return [
        {
            "key": provider.key,
            "repository": provider.repository,
            "role": provider.role,
            "capabilities": list(provider.capabilities),
            "integration_mode": provider.integration_mode,
            "status": provider.status,
        }
        for provider in PROVIDERS
    ]


def missing_capabilities(required: Iterable[str]) -> Tuple[str, ...]:
    """Return required capabilities with no declared provider."""
    available = set(all_capabilities())
    return tuple(cap for cap in required if cap not in available)
