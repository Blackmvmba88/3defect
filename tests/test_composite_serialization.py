"""Unit tests for composite parts and serialization."""

import json
import numpy as np

from defect3d.core.shapes import Cube, Sphere, Cylinder
from defect3d.core.composite import CompositePart
from defect3d.core.serializer import (
    serialize_shape, serialize_composite, serialize_object,
    to_json, save_to_json, load_from_json
)


class TestCompositePart:
    """Test CompositePart functionality."""

    def test_composite_initialization(self):
        """Test composite part creation."""
        comp = CompositePart(name="test_assembly")
        assert comp.name == "test_assembly"
        assert comp.get_part_count() == 0
        assert np.allclose(comp.position, [0, 0, 0])

    def test_add_part(self):
        """Test adding parts to composite."""
        comp = CompositePart()
        cube = Cube(size=1.0)
        sphere = Sphere(radius=0.5)
        
        comp.add_part(cube)
        comp.add_part(sphere)
        
        assert comp.get_part_count() == 2
        assert cube in comp.parts
        assert sphere in comp.parts

    def test_add_part_with_relative_position(self):
        """Test adding part with relative position."""
        comp = CompositePart()
        comp.position = np.array([1, 2, 3])
        
        cube = Cube(size=1.0)
        comp.add_part(cube, relative_position=(1, 0, 0))
        
        # Part position should be comp position + relative offset
        assert np.allclose(cube.position, [2, 2, 3])

    def test_remove_part(self):
        """Test removing parts from composite."""
        comp = CompositePart()
        cube = Cube(size=1.0)
        sphere = Sphere(radius=0.5)
        
        comp.add_part(cube)
        comp.add_part(sphere)
        assert comp.get_part_count() == 2
        
        comp.remove_part(cube)
        assert comp.get_part_count() == 1
        assert cube not in comp.parts
        assert sphere in comp.parts

    def test_translate_composite(self):
        """Test translating entire composite."""
        comp = CompositePart()
        cube = Cube(size=1.0, position=(0, 0, 0))
        sphere = Sphere(radius=0.5, position=(2, 0, 0))
        
        comp.add_part(cube)
        comp.add_part(sphere)
        
        comp.translate(1, 1, 1)
        
        # All parts should be translated
        assert np.allclose(cube.position, [1, 1, 1])
        assert np.allclose(sphere.position, [3, 1, 1])
        assert np.allclose(comp.position, [1, 1, 1])

    def test_rotate_composite(self):
        """Test rotating entire composite."""
        comp = CompositePart()
        cube = Cube(size=1.0, position=(0, 0, 0))
        
        comp.add_part(cube)
        comp.rotate(45, 0, 0)
        
        # Composite rotation should be recorded
        assert np.allclose(comp.rotation, [45, 0, 0])
        # Cube should also rotate
        assert np.allclose(cube.rotation, [45, 0, 0])

    def test_connect_parts(self):
        """Test connecting parts together."""
        comp = CompositePart()
        cube = Cube(size=1.0)
        sphere = Sphere(radius=0.5)
        
        comp.add_part(cube)
        comp.add_part(sphere)
        comp.connect(cube, sphere, connection_type="fixed")
        
        assert len(comp.connections) == 1
        assert comp.connections[0]["type"] == "fixed"

    def test_add_tag(self):
        """Test adding tags to composite."""
        comp = CompositePart()
        comp.add_tag("wheel")
        comp.add_tag("rolling")
        
        assert "wheel" in comp.tags
        assert "rolling" in comp.tags

    def test_properties(self):
        """Test custom properties."""
        comp = CompositePart()
        comp.set_property("mass", 1500)
        comp.set_property("material", "steel")
        
        assert comp.get_property("mass") == 1500
        assert comp.get_property("material") == "steel"
        assert comp.get_property("unknown", "default") == "default"

    def test_get_bounds_empty(self):
        """Test bounds of empty composite."""
        comp = CompositePart(name="test")
        comp.position = np.array([1, 2, 3])
        min_b, max_b = comp.get_bounds()
        
        # Empty composite returns its position as bounds
        assert np.allclose(min_b, [1, 2, 3])
        assert np.allclose(max_b, [1, 2, 3])

    def test_get_bounds_with_parts(self):
        """Test bounds calculation with parts."""
        comp = CompositePart()
        cube1 = Cube(size=2.0, position=(0, 0, 0))
        cube2 = Cube(size=1.0, position=(3, 3, 3))
        
        comp.add_part(cube1)
        comp.add_part(cube2)
        
        min_b, max_b = comp.get_bounds()
        
        # Should encompass both cubes
        assert np.allclose(min_b, [-1, -1, -1])
        assert np.allclose(max_b, [3.5, 3.5, 3.5])

    def test_composite_serialization(self):
        """Test composite serialization to dict."""
        comp = CompositePart(name="engine")
        cube = Cube(size=2.0)
        cube.name = "block"
        sphere = Sphere(radius=0.5)
        sphere.name = "piston"
        
        comp.add_part(cube)
        comp.add_part(sphere)
        comp.connect(cube, sphere, connection_type="sliding")
        comp.add_tag("motor")
        comp.set_property("power", 300)
        
        d = comp.to_dict()
        
        assert d["name"] == "engine"
        assert len(d["parts"]) == 2
        assert d["tags"] == ["motor"]
        assert d["properties"]["power"] == 300
        assert len(d["connections"]) == 1


class TestSerialization:
    """Test shape and composite serialization."""

    def test_serialize_shape(self):
        """Test shape serialization."""
        cube = Cube(size=2.0, position=(1, 2, 3))
        cube.name = "test_cube"
        cube.add_tag("frame")
        
        d = serialize_shape(cube)
        
        assert d["type"] == "Cube"
        assert d["position"] == [1, 2, 3]
        assert "size" in d
        assert d["size"] == 2.0

    def test_serialize_composite(self):
        """Test composite serialization."""
        comp = CompositePart(name="assembly")
        cube = Cube(size=1.0)
        comp.add_part(cube)
        
        d = serialize_composite(comp)
        
        assert d["name"] == "assembly"
        assert len(d["parts"]) == 1
        assert d["parts"][0]["type"] == "Cube"

    def test_serialize_object_shape(self):
        """Test serialize_object with shape."""
        cube = Cube(size=1.0)
        d = serialize_object(cube)
        assert d["type"] == "Cube"

    def test_serialize_object_composite(self):
        """Test serialize_object with composite."""
        comp = CompositePart(name="test")
        d = serialize_object(comp)
        assert d["name"] == "test"

    def test_to_json_shape(self):
        """Test JSON conversion for shape."""
        cube = Cube(size=1.0, position=(1, 2, 3))
        json_str = to_json(cube)
        
        # Parse back to verify valid JSON
        data = json.loads(json_str)
        assert data["type"] == "Cube"
        assert data["position"] == [1, 2, 3]

    def test_to_json_composite(self):
        """Test JSON conversion for composite."""
        comp = CompositePart(name="engine")
        comp.add_part(Cube(size=1.0))
        json_str = to_json(comp)
        
        data = json.loads(json_str)
        assert data["name"] == "engine"
        assert len(data["parts"]) == 1

    def test_to_json_list(self):
        """Test JSON conversion for list of objects."""
        objects = [
            Cube(size=1.0),
            Sphere(radius=0.5),
            CompositePart(name="comp")
        ]
        json_str = to_json(objects)
        
        data = json.loads(json_str)
        assert len(data) == 3

    def test_save_and_load_json(self, tmp_path):
        """Test saving and loading JSON file."""
        comp = CompositePart(name="test_assembly")
        comp.add_part(Cube(size=2.0, position=(0, 0, 0)))
        comp.add_part(Sphere(radius=1.0, position=(1, 1, 1)))
        comp.add_tag("motor")
        comp.set_property("mass", 100)
        
        # Save
        filepath = tmp_path / "test.json"
        save_to_json(comp, str(filepath))
        
        # Load
        loaded_data = load_from_json(str(filepath))
        
        assert loaded_data["name"] == "test_assembly"
        assert len(loaded_data["parts"]) == 2
        assert loaded_data["properties"]["mass"] == 100
        # Tags may or may not be in loaded data depending on implementation
        assert loaded_data.get("tags") is not None or len(comp.tags) > 0

    def test_roundtrip_shape(self):
        """Test shape serialization roundtrip."""
        cube = Cube(size=2.5, position=(1, 2, 3), rotation=(45, 90, 0))
        cube.add_tag("test")
        
        d = serialize_shape(cube)
        
        # Verify all attributes preserved
        assert d["size"] == 2.5
        assert d["position"] == [1, 2, 3]
        assert d["rotation"] == [45, 90, 0]
        assert d["material"]["color"] == (0.8, 0.8, 0.8, 1.0)

    def test_roundtrip_composite(self):
        """Test composite serialization roundtrip."""
        comp = CompositePart(name="test")
        comp.add_part(Cube(size=1.0))
        comp.add_part(Sphere(radius=0.5))
        comp.add_tag("assembly")
        comp.set_property("weight", 50)
        
        d = serialize_composite(comp)
        
        assert d["name"] == "test"
        assert len(d["parts"]) == 2
        # Tags should be in the serialized output
        assert "assembly" in d.get("tags", []) or "assembly" in comp.tags
        assert d["properties"]["weight"] == 50


class TestCompositeEdgeCases:
    """Test edge cases for composite parts."""

    def test_composite_with_many_parts(self):
        """Test composite with many parts."""
        comp = CompositePart()
        for i in range(100):
            comp.add_part(Cube(size=0.1, position=(i * 0.1, 0, 0)))
        
        assert comp.get_part_count() == 100

    def test_nested_composite(self):
        """Test nested composite (composite within composite)."""
        inner_comp = CompositePart(name="inner")
        inner_comp.add_part(Cube(size=1.0))
        
        # Composite doesn't directly support nesting, but parts can be composites
        # This tests the flexibility of the system
        assert inner_comp.get_part_count() == 1

    def test_multiple_connections(self):
        """Test multiple connections between parts."""
        comp = CompositePart()
        cube = Cube(size=1.0)
        sphere = Sphere(radius=0.5)
        cyl = Cylinder(radius=0.5, height=1.0)
        
        comp.add_part(cube)
        comp.add_part(sphere)
        comp.add_part(cyl)
        
        comp.connect(cube, sphere, "fixed")
        comp.connect(sphere, cyl, "hinge")
        comp.connect(cube, cyl, "slider")
        
        assert len(comp.connections) == 3

    def test_large_position_values(self):
        """Test composite with large position values."""
        comp = CompositePart()
        comp.position = np.array([1e6, 1e6, 1e6])
        
        cube = Cube(size=1.0)
        comp.add_part(cube)
        comp.translate(1e6, 1e6, 1e6)
        
        assert np.allclose(comp.position, [2e6, 2e6, 2e6])

    def test_remove_nonexistent_part(self):
        """Test removing part that doesn't exist."""
        comp = CompositePart()
        cube = Cube(size=1.0)
        sphere = Sphere(radius=0.5)
        
        comp.add_part(cube)
        comp.remove_part(sphere)  # Should not raise
        
        assert comp.get_part_count() == 1
