import pytest

from defect3d.blender_integration.module_registry import (
    ModuleRegistry,
    ModuleSpec,
    default_registry,
)


def test_default_registry_contains_canonical_root_modules():
    registry = default_registry()

    for module_id in (
        "create",
        "material",
        "form",
        "mechanics",
        "assembly",
        "animation",
        "physics",
        "world",
        "output",
    ):
        assert registry.get(module_id).module_id == module_id


def test_material_registry_contains_first_visual_presets():
    material = default_registry().get("material")

    assert "metallic" in material.actions
    assert "pearlescent" in material.actions
    assert "iridescent" in material.actions
    assert "transparent" in material.actions


def test_suspension_is_a_mechanics_child_with_generators_and_test():
    registry = default_registry()
    mechanics = registry.get("mechanics")
    suspension = registry.get("mechanics.suspension")

    assert "mechanics.suspension" in mechanics.children
    assert suspension.category == "mechanics"
    assert "double_wishbone" in suspension.actions
    assert "spring" in suspension.actions
    assert "damper" in suspension.actions
    assert "travel_test" in suspension.actions


def test_duplicate_module_ids_are_rejected():
    spec = ModuleSpec("material", "Material", "root")
    registry = ModuleRegistry([spec])

    with pytest.raises(ValueError, match="duplicate module_id"):
        registry.register(spec)


def test_unknown_module_is_explicit_failure():
    with pytest.raises(KeyError, match="unknown BlackMamba module"):
        default_registry().get("does.not.exist")
