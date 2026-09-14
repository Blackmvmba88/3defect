"""Canonical BlackMamba 3D orchestration pipeline.

This module plans work across the ecosystem without importing sibling
repositories. Execution adapters can be attached later while the plan and
contract remain stable.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from .asset_contract import validate_asset_contract
from .integrations import Provider, providers_for


@dataclass(frozen=True)
class PipelineStep:
    """One stable stage in the BlackMamba 3D production pipeline."""

    key: str
    description: str
    capabilities: Tuple[str, ...]
    required: bool = True


PIPELINE_STEPS: Tuple[PipelineStep, ...] = (
    PipelineStep(
        "contract",
        "Validate blueprint, BOM, dimensions, tolerances and maturity state",
        ("validation",),
    ),
    PipelineStep(
        "geometry",
        "Generate or ingest the canonical geometry",
        ("geometry", "procedural_geometry", "surface_generation"),
    ),
    PipelineStep(
        "measure",
        "Measure generated geometry against declared dimensions/tolerances",
        ("dimensional_validation", "validation"),
    ),
    PipelineStep(
        "assemble",
        "Resolve part interfaces, sockets and deterministic assembly",
        ("assembly", "sockets"),
    ),
    PipelineStep(
        "dcc",
        "Build/inspect the production scene in Blender or a compatible DCC",
        ("blender_automation", "blender"),
    ),
    PipelineStep(
        "render",
        "Produce deterministic preview/product renders",
        ("render", "product_render", "gpu_render"),
    ),
    PipelineStep(
        "export",
        "Export delivery/runtime geometry",
        ("export", "gltf", "glb", "stl", "obj", "fbx"),
    ),
    PipelineStep(
        "runtime",
        "Preview or stream the asset in web/realtime runtimes when requested",
        ("threejs", "webgl", "websocket", "runtime"),
        required=False,
    ),
    PipelineStep(
        "manufacturing_gate",
        "Allow manufacturing status only after engineering evidence passes",
        ("validation", "dimensional_validation"),
        required=False,
    ),
)


def _providers_for_any(capabilities: Sequence[str]) -> List[Provider]:
    seen = set()
    matches: List[Provider] = []
    for capability in capabilities:
        for provider in providers_for(capability):
            if provider.key in seen:
                continue
            seen.add(provider.key)
            matches.append(provider)
    return matches


def _requested_runtime(data: Mapping[str, Any]) -> bool:
    exports = data.get("exports", [])
    if not isinstance(exports, list):
        return False
    runtime_formats = {"glb", "gltf", "webgl", "threejs", "websocket"}
    return any(str(item).lower() in runtime_formats for item in exports)


def _manufacturing_requested(data: Mapping[str, Any]) -> bool:
    manufacturing = data.get("manufacturing")
    if not isinstance(manufacturing, Mapping):
        return False
    return data.get("stage") == "manufacturing_ready" or manufacturing.get("ready") is True


def plan_asset_pipeline(data: Mapping[str, Any]) -> Dict[str, Any]:
    """Return a deterministic, JSON-serializable integration plan for an asset.

    Planning never claims that an external provider was executed. It only
    selects declared providers capable of each step and reports contract
    blockers before any DCC/manufacturing work is attempted.
    """
    contract_errors = validate_asset_contract(data)
    planned_steps: List[Dict[str, Any]] = []

    for step in PIPELINE_STEPS:
        enabled = step.required
        if step.key == "runtime":
            enabled = _requested_runtime(data)
        elif step.key == "manufacturing_gate":
            enabled = _manufacturing_requested(data)

        if not enabled:
            continue

        providers = _providers_for_any(step.capabilities)
        planned_steps.append(
            {
                "key": step.key,
                "description": step.description,
                "capabilities": list(step.capabilities),
                "providers": [provider.key for provider in providers],
                "repositories": [provider.repository for provider in providers],
                "status": "blocked" if contract_errors and step.key != "contract" else "planned",
            }
        )

    return {
        "asset_id": data.get("asset_id"),
        "revision": data.get("revision"),
        "stage": data.get("stage"),
        "contract_valid": not contract_errors,
        "contract_errors": contract_errors,
        "steps": planned_steps,
    }


def pipeline_provider_keys() -> Tuple[str, ...]:
    """Return every provider key referenced by the canonical pipeline."""
    seen = []
    for step in PIPELINE_STEPS:
        for provider in _providers_for_any(step.capabilities):
            if provider.key not in seen:
                seen.append(provider.key)
    return tuple(seen)
