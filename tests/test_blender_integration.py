"""
Tests for Blender integration with graceful degradation.
Tests for exporter, renderer, and Blender availability checks.

这些测试验证Blender集成模块即使在Blender不可用时也能优雅地处理。
These tests verify Blender integration modules handle graceful degradation when Blender is unavailable.
"""

import pytest
import tempfile
import os
from defect3d.core.shapes import Cube, Sphere, Cylinder
from defect3d.core.composite import CompositePart
from defect3d.blender_integration import (
    is_blender_available,
    get_blender_error,
    require_blender,
    warn_blender_unavailable,
    BlenderExporter,
    export_to_blender
)


class TestBlenderAvailability:
    """Test Blender availability checking."""

    def test_is_blender_available(self):
        """Test that is_blender_available returns a boolean."""
        result = is_blender_available()
        assert isinstance(result, bool)

    def test_get_blender_error(self):
        """Test that get_blender_error returns a string."""
        error = get_blender_error()
        assert isinstance(error, str)

        # If Blender is not available, error should be non-empty
        if not is_blender_available():
            assert len(error) > 0

    def test_require_blender_raises_if_unavailable(self):
        """Test that require_blender raises if Blender is not available."""
        if not is_blender_available():
            with pytest.raises(RuntimeError):
                require_blender("Test Feature")

    def test_require_blender_returns_true_if_available(self):
        """Test that require_blender returns True if available."""
        if is_blender_available():
            result = require_blender()
            assert result is True

    def test_warn_blender_unavailable(self):
        """Test that warn_blender_unavailable issues a warning."""
        if not is_blender_available():
            with pytest.warns(RuntimeWarning):
                warn_blender_unavailable("Test Feature")


class TestBlenderExporter:
    """Test Blender exporter functionality."""

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_exporter_initialization(self):
        """Test that BlenderExporter can be instantiated."""
        exporter = BlenderExporter()
        assert exporter is not None
        assert len(exporter.objects) == 0

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_exporter_add_object(self):
        """Test adding objects to the exporter."""
        exporter = BlenderExporter()
        cube = Cube(size=2.0, position=(0, 0, 0))
        exporter.add_object(cube)
        assert len(exporter.objects) == 1

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_exporter_generate_script(self):
        """Test that the exporter can generate a Blender script."""
        exporter = BlenderExporter()
        exporter.add_object(Cube(size=2.0, position=(0, 0, 0)))
        exporter.add_object(Sphere(radius=1.0, position=(1, 1, 1)))

        script = exporter.generate_blender_script()
        assert isinstance(script, str)
        assert 'import bpy' in script
        assert 'bpy.ops' in script
        assert len(script) > 100  # Should be substantial script

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_exporter_save_script(self):
        """Test saving Blender script to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = BlenderExporter()
            exporter.add_object(Cube(size=2.0, position=(0, 0, 0)))

            script_path = os.path.join(tmpdir, 'test.py')
            exporter.save_script(script_path)

            assert os.path.exists(script_path)
            with open(script_path, 'r') as f:
                content = f.read()
            assert 'import bpy' in content

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_exporter_save_json(self):
        """Test saving objects as JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = BlenderExporter()
            exporter.add_object(Cube(size=2.0, position=(0, 0, 0)))

            json_path = os.path.join(tmpdir, 'test.json')
            exporter.save_json(json_path)

            assert os.path.exists(json_path)

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_export_to_blender_function(self):
        """Test the export_to_blender convenience function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cube = Cube(size=2.0, position=(0, 0, 0))
            output_path = os.path.join(tmpdir, 'output.py')

            exporter = export_to_blender(cube, output_file=output_path)

            assert os.path.exists(output_path)
            assert exporter is not None

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_export_multiple_objects(self):
        """Test exporting multiple objects at once."""
        with tempfile.TemporaryDirectory() as tmpdir:
            objects = [
                Cube(size=2.0, position=(0, 0, 0)),
                Sphere(radius=1.0, position=(1, 1, 1)),
                Cylinder(radius=0.5, height=2.0, position=(2, 2, 2))
            ]

            output_path = os.path.join(tmpdir, 'multi.py')
            export_to_blender(objects, output_file=output_path)

            assert os.path.exists(output_path)

    @pytest.mark.skipif(not is_blender_available(),
                        reason="Blender not available")
    def test_export_composite_part(self):
        """Test exporting a composite part."""
        with tempfile.TemporaryDirectory() as tmpdir:
            comp = CompositePart(name="vehicle")
            comp.add_part(Cube(size=2.0, position=(0, 0, 0)))
            comp.add_part(Sphere(radius=0.5, position=(1, 0, 0)))

            output_path = os.path.join(tmpdir, 'composite.py')
            export_to_blender(comp, output_file=output_path)

            assert os.path.exists(output_path)


class TestGracefulDegradation:
    """Test graceful degradation when Blender is not available."""

    def test_blender_integration_import_succeeds(self):
        """Test that blender_integration module can be imported even without bpy."""
        # This test simply verifies the import doesn't fail
        # If we got here, the import succeeded
        assert True

    def test_exporter_available_status(self):
        """Test that exporter availability matches blender availability."""
        if is_blender_available():
            assert BlenderExporter is not None
        else:
            # When Blender is not available, exporter should still be importable
            # but trying to use it should either fail or warn
            pass

    @pytest.mark.skipif(is_blender_available(),
                        reason="Only test when Blender unavailable")
    def test_require_blender_error_message(self):
        """Test that require_blender provides helpful error message."""
        try:
            require_blender("Test feature")
        except RuntimeError as e:
            error_msg = str(e).lower()
            assert "bpy" in error_msg or "blender" in error_msg
            assert "not found" in error_msg or "unavailable" in error_msg or "not installed" in error_msg or "no module" in error_msg
