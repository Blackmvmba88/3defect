"""Validation helpers for the BlackMamba 3D asset contract.

The validator is intentionally independent from Blender so it can run in CI,
asset processors, web services, or command-line tooling before a scene is
opened in a DCC application.
"""

from typing import Any, List, Mapping


PASS = "pass"
CORE_CHECKS = ("dimensions", "interfaces", "assembly")
MANUFACTURING_STAGE = "manufacturing_ready"


def dimension_within_tolerance(
    target: float,
    measured: float,
    tolerance: float,
) -> bool:
    """Return True when a measured value is inside the declared tolerance."""
    if tolerance < 0:
        return False
    return abs(float(measured) - float(target)) <= float(tolerance)


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_dimension(
    part_id: str,
    name: str,
    spec: Mapping[str, Any],
    errors: List[str],
) -> None:
    target = spec.get("target")
    tolerance = spec.get("tolerance")
    measured = spec.get("measured")

    if not isinstance(target, (int, float)) or isinstance(target, bool):
        errors.append(f"{part_id}.{name}: target must be numeric")
        return
    if not isinstance(tolerance, (int, float)) or isinstance(tolerance, bool):
        errors.append(f"{part_id}.{name}: tolerance must be numeric")
        return
    if tolerance < 0:
        errors.append(f"{part_id}.{name}: tolerance must be >= 0")
        return
    if measured is None:
        if spec.get("status") == PASS:
            errors.append(
                f"{part_id}.{name}: status=pass requires measured value"
            )
        return
    if not isinstance(measured, (int, float)) or isinstance(measured, bool):
        errors.append(f"{part_id}.{name}: measured must be numeric or null")
        return

    in_tolerance = dimension_within_tolerance(target, measured, tolerance)
    status = spec.get("status")
    if in_tolerance and status == "fail":
        errors.append(
            f"{part_id}.{name}: measured value is in tolerance but status=fail"
        )
    if not in_tolerance:
        delta = abs(float(measured) - float(target))
        errors.append(
            f"{part_id}.{name}: out of tolerance "
            f"(delta={delta:g}, tolerance={float(tolerance):g})"
        )


def _validate_parts(data: Mapping[str, Any], errors: List[str]) -> None:
    parts = data.get("parts")
    if not isinstance(parts, list):
        errors.append("parts must be a list")
        return

    seen = set()
    for index, part in enumerate(parts):
        if not isinstance(part, Mapping):
            errors.append(f"parts[{index}] must be an object")
            continue

        part_id = part.get("part_id")
        if not _non_empty_string(part_id):
            errors.append(f"parts[{index}].part_id must be a non-empty string")
            part_id = f"parts[{index}]"
        elif part_id in seen:
            errors.append(f"duplicate part_id: {part_id}")
        else:
            seen.add(part_id)

        dimensions = part.get("dimensions", {})
        if not isinstance(dimensions, Mapping):
            errors.append(f"{part_id}.dimensions must be an object")
            continue

        for name, spec in dimensions.items():
            if not isinstance(spec, Mapping):
                errors.append(f"{part_id}.{name}: dimension must be an object")
                continue
            _validate_dimension(str(part_id), str(name), spec, errors)

        if part.get("status") == "validated" and not dimensions:
            errors.append(
                f"{part_id}: validated part must declare dimensions"
            )


def _validate_declared_summary(
    data: Mapping[str, Any], errors: List[str]
) -> None:
    validation = data.get("validation")
    if not isinstance(validation, Mapping):
        errors.append("validation must be an object")
        return

    if validation.get("dimensions") == PASS:
        parts = data.get("parts", [])
        for part in parts if isinstance(parts, list) else []:
            if not isinstance(part, Mapping):
                continue
            part_id = part.get("part_id", "unknown")
            dimensions = part.get("dimensions", {})
            if not isinstance(dimensions, Mapping):
                continue
            for name, spec in dimensions.items():
                if not isinstance(spec, Mapping):
                    continue
                if spec.get("measured") is None:
                    errors.append(
                        f"{part_id}.{name}: global dimensions=pass "
                        "requires measured value"
                    )
                elif not dimension_within_tolerance(
                    spec.get("target", 0),
                    spec.get("measured", 0),
                    spec.get("tolerance", -1),
                ):
                    errors.append(
                        f"{part_id}.{name}: global dimensions=pass "
                        "contradicts measured geometry"
                    )


def _validate_manufacturing_gate(
    data: Mapping[str, Any], errors: List[str]
) -> None:
    manufacturing = data.get("manufacturing")
    if not isinstance(manufacturing, Mapping):
        errors.append("manufacturing must be an object")
        return

    ready = manufacturing.get("ready") is True
    stage = data.get("stage")

    if stage == MANUFACTURING_STAGE and not ready:
        errors.append(
            "stage=manufacturing_ready requires manufacturing.ready=true"
        )

    if not ready:
        return

    if stage != MANUFACTURING_STAGE:
        errors.append(
            "manufacturing.ready=true requires stage=manufacturing_ready"
        )

    for field in ("process", "material_spec"):
        if not _non_empty_string(manufacturing.get(field)):
            errors.append(
                f"manufacturing.ready=true requires non-empty {field}"
            )

    evidence = manufacturing.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(
            "manufacturing.ready=true requires at least one evidence item"
        )

    validation = data.get("validation")
    if not isinstance(validation, Mapping):
        return

    for check in CORE_CHECKS:
        if validation.get(check) != PASS:
            errors.append(
                "manufacturing.ready=true requires "
                f"validation.{check}=pass"
            )

    if validation.get("closed_geometry") != PASS:
        errors.append(
            "manufacturing.ready=true requires "
            "validation.closed_geometry=pass"
        )


def validate_asset_contract(data: Mapping[str, Any]) -> List[str]:
    """Return deterministic validation errors for a Mamba3D asset manifest."""
    errors: List[str] = []

    if not isinstance(data, Mapping):
        return ["asset manifest must be an object"]

    for field in ("asset_id", "revision", "stage", "units"):
        if not _non_empty_string(data.get(field)):
            errors.append(f"{field} must be a non-empty string")

    blueprint = data.get("blueprint")
    if not isinstance(blueprint, Mapping):
        errors.append("blueprint must be an object")
    else:
        for field in ("id", "revision"):
            if not _non_empty_string(blueprint.get(field)):
                errors.append(
                    f"blueprint.{field} must be a non-empty string"
                )

    _validate_parts(data, errors)
    _validate_declared_summary(data, errors)
    _validate_manufacturing_gate(data, errors)
    return errors


def assert_valid_asset_contract(data: Mapping[str, Any]) -> None:
    """Raise ValueError when a Mamba3D asset manifest is invalid."""
    errors = validate_asset_contract(data)
    if errors:
        raise ValueError("; ".join(errors))
