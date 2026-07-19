"""
Example tests demonstrating fixture usage.

These tests show how to use the reusable fixtures from conftest.py
to write simpler, more maintainable tests.
"""

import pytest
import numpy as np
from defect3d.core.serializer import save_to_json, load_from_json
import tempfile
import os


class TestFixtureUsage:
    """Tests demonstrating fixture usage."""
    
    def test_basic_cube_fixture(self, basic_cube):
        """Test using basic_cube fixture."""
        assert basic_cube.name == "basic_cube"
        assert basic_cube.size == 2.0
        assert np.allclose(basic_cube.position, [0, 0, 0])
    
    def test_simple_composite_fixture(self, simple_composite):
        """Test using simple_composite fixture."""
        assert simple_composite.name == "simple_assembly"
        assert len(simple_composite.parts) == 2
    
    def test_car_model_fixture(self, car_model):
        """Test using car_model fixture with tags and properties."""
        assert car_model.name == "car"
        assert "vehicle" in car_model.tags
        assert car_model.properties.get("type") == "sedan"
        assert car_model.properties.get("wheels") == 4
        assert len(car_model.parts) == 5  # chassis + 4 wheels
    
    def test_motorcycle_fixture(self, motorcycle_model):
        """Test using motorcycle_model fixture."""
        assert motorcycle_model.name == "motorcycle"
        assert "vehicle" in motorcycle_model.tags
        assert motorcycle_model.properties.get("type") == "sport"
        assert motorcycle_model.properties.get("wheels") == 2
    
    def test_nested_composite_fixture(self, nested_composite):
        """Test using nested_composite fixture with hierarchy."""
        assert nested_composite.name == "vehicle"
        assert len(nested_composite.parts) == 1  # chassis
        
        chassis = nested_composite.parts[0]
        assert chassis.name == "chassis"
        assert len(chassis.parts) == 2  # frame + wheel_assembly
    
    def test_all_shapes_fixture(self, all_shapes):
        """Test using all_shapes fixture."""
        assert len(all_shapes) == 5
        assert "cube" in all_shapes
        assert "sphere" in all_shapes
        assert "cylinder" in all_shapes
        assert "cone" in all_shapes
        assert "torus" in all_shapes
    
    def test_colored_shapes_fixture(self, colored_shapes):
        """Test using colored_shapes fixture."""
        assert len(colored_shapes) == 5
        for color_name, shape in colored_shapes.items():
            assert shape.name == f"cube_{color_name}"
            # Verify material was set (colors are in material)
            assert shape.material is not None
    
    def test_cube_sizes_parametrized(self, cube_sizes):
        """Test using parametrized cube_sizes fixture."""
        # This test runs 3 times with different sizes
        assert cube_sizes.size in [1.0, 2.0, 5.0]
    
    def test_cylinder_variants_parametrized(self, cylinder_variants):
        """Test using parametrized cylinder_variants fixture."""
        # This test runs 3 times with different dimensions
        assert cylinder_variants.radius in [0.5, 1.0, 2.0]
        assert cylinder_variants.height in [1.0, 2.0, 4.0]
    
    def test_color_values_parametrized(self, color_values):
        """Test using parametrized color_values fixture."""
        # This test runs 5 times with different colors
        assert len(color_values) == 4  # RGBA
        assert all(0 <= c <= 1 for c in color_values)
    
    def test_scene_with_car_and_motorcycle(self, simple_scene):
        """Test using simple_scene fixture."""
        assert simple_scene.name == "scene"
        assert len(simple_scene.parts) == 2
        
        # Verify positions were updated
        car, bike = simple_scene.parts
        assert np.allclose(car.position, [0, 0, 0])
        assert np.allclose(bike.position, [5, 0, 0])
    
    def test_complex_scene_all_shapes(self, complex_scene):
        """Test using complex_scene fixture."""
        assert complex_scene.name == "shapes_showcase"
        assert len(complex_scene.parts) == 5
    
    def test_tagged_composite_fixture(self, tagged_composite):
        """Test using tagged_composite fixture with tags and properties."""
        assert "vehicle" in tagged_composite.tags
        assert tagged_composite.properties.get("mass") == 1500
        assert tagged_composite.properties.get("max_speed") == 120
        
        # Verify parts have tags too
        for part in tagged_composite.parts:
            assert len(part.tags) > 0


class TestFixtureReusability:
    """Tests demonstrating fixture reusability across multiple tests."""
    
    def test_empty_composite_is_really_empty(self, empty_composite):
        """Empty composite should have no parts."""
        assert len(empty_composite.parts) == 0
        assert empty_composite.name == "empty_assembly"
    
    def test_empty_composite_can_add_parts(self, empty_composite):
        """Empty composite should be able to add parts."""
        from defect3d.core.shapes import Cube
        original_count = len(empty_composite.parts)
        empty_composite.add_part(Cube(size=2.0, position=(0, 0, 0)))  # Add a cube
        assert len(empty_composite.parts) == original_count + 1
    
    def test_multi_part_composite_iteration(self, multi_part_composite):
        """Test iterating over multi-part composite."""
        part_count = 0
        for part in multi_part_composite.parts:
            part_count += 1
            assert part is not None
        assert part_count == 5
    
    def test_multi_part_serialization(self, multi_part_composite):
        """Test serializing multi-part composite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'multi.json')
            save_to_json(multi_part_composite, filepath)
            
            # Verify file was created
            assert os.path.exists(filepath)
            
            # Load and verify structure
            loaded = load_from_json(filepath)
            assert loaded['name'] == 'multi_part_assembly'
            assert len(loaded['parts']) == 5


class TestFixtureIntegration:
    """Integration tests using multiple fixtures."""
    
    def test_car_and_motorcycle_comparison(self, car_model, motorcycle_model):
        """Compare two vehicle models."""
        assert car_model.properties.get("type") != motorcycle_model.properties.get("type")
        assert car_model.properties.get("wheels") == 4
        assert motorcycle_model.properties.get("wheels") == 2
    
    def test_add_motorcycle_to_scene(self, simple_scene, motorcycle_model):
        """Add motorcycle to existing scene."""
        initial_count = len(simple_scene.parts)
        # Create a new motorcycle (don't reuse fixture to avoid mutation)
        new_bike = motorcycle_model
        new_bike.position = np.array([10, 0, 0])
        simple_scene.add_part(new_bike)
        
        assert len(simple_scene.parts) == initial_count + 1
    
    def test_composite_bounds_with_shapes(self, simple_composite, all_shapes):
        """Test bounds calculation with various shapes."""
        bounds = simple_composite.get_bounds()
        assert bounds is not None
        assert len(bounds) == 2  # min and max
    
    def test_vehicle_serialization_roundtrip(self, car_model):
        """Test serializing and deserializing a vehicle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'car.json')
            save_to_json(car_model, filepath)
            
            # Load and verify data
            loaded_data = load_from_json(filepath)
            
            assert loaded_data['name'] == 'car'
            assert 'parts' in loaded_data
            assert len(loaded_data['parts']) > 0
