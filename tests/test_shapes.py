"""Unit tests for core 3D shapes."""

import math
import numpy as np
import pytest

from defect3d.core.shapes import Cube, Sphere, Cylinder, Cone, Torus, Shape3D


class TestShape3DBase:
    """Test Shape3D base class."""

    def test_default_initialization(self):
        """Test default Shape3D initialization."""
        shape = Shape3D()
        assert np.allclose(shape.position, [0, 0, 0])
        assert np.allclose(shape.rotation, [0, 0, 0])
        assert np.allclose(shape.scale, [1, 1, 1])
        assert shape.tags == []
        assert shape.material["color"] == (0.8, 0.8, 0.8, 1.0)

    def test_custom_initialization(self):
        """Test Shape3D with custom parameters."""
        pos = (1, 2, 3)
        rot = (45, 90, 180)
        scale = (2, 2, 2)
        shape = Shape3D(position=pos, rotation=rot, scale=scale)
        assert np.allclose(shape.position, pos)
        assert np.allclose(shape.rotation, rot)
        assert np.allclose(shape.scale, scale)

    def test_translate(self):
        """Test translation of shape."""
        shape = Shape3D(position=(1, 2, 3))
        shape.translate(2, 3, 4)
        assert np.allclose(shape.position, [3, 5, 7])

    def test_rotate(self):
        """Test rotation of shape."""
        shape = Shape3D(rotation=(45, 0, 0))
        shape.rotate(45, 90, 180)
        assert np.allclose(shape.rotation, [90, 90, 180])

    def test_set_scale(self):
        """Test scale modification."""
        shape = Shape3D()
        shape.set_scale(2, 3, 4)
        assert np.allclose(shape.scale, [2, 3, 4])

    def test_set_color(self):
        """Test color setting."""
        shape = Shape3D()
        shape.set_color(1.0, 0.5, 0.0, 0.8)
        assert shape.material["color"] == (1.0, 0.5, 0.0, 0.8)

    def test_add_tag(self):
        """Test adding tags."""
        shape = Shape3D()
        shape.add_tag("wheel")
        shape.add_tag("rolling")
        assert "wheel" in shape.tags
        assert "rolling" in shape.tags
        assert len(shape.tags) == 2

    def test_add_duplicate_tag(self):
        """Test that duplicate tags are not added."""
        shape = Shape3D()
        shape.add_tag("wheel")
        shape.add_tag("wheel")
        assert shape.tags.count("wheel") == 1

    def test_to_dict(self):
        """Test serialization to dictionary."""
        shape = Shape3D(position=(1, 2, 3))
        shape.add_tag("test")
        shape.set_color(1, 0, 0)
        d = shape.to_dict()
        assert d["type"] == "Shape3D"
        assert d["position"] == [1, 2, 3]
        assert d["tags"] == ["test"]


class TestCube:
    """Test Cube primitive."""

    def test_cube_initialization(self):
        """Test cube creation."""
        cube = Cube(size=2.0)
        assert cube.size == 2.0
        assert cube.name == "Cube"

    def test_cube_volume(self):
        """Test cube volume calculation."""
        cube = Cube(size=2.0)
        assert cube.volume() == 8.0

    def test_cube_volume_scaled(self):
        """Test cube volume with scale (size is base, volume not affected by scale)."""
        cube = Cube(size=2.0)
        cube.set_scale(2, 2, 2)
        # Volume should remain 8.0 (scale affects rendering, not geometry)
        assert cube.volume() == 8.0

    def test_cube_bounds(self):
        """Test cube bounding box."""
        cube = Cube(size=2.0, position=(1, 1, 1))
        min_b, max_b = cube.get_bounds()
        expected_min = np.array([0, 0, 0])
        expected_max = np.array([2, 2, 2])
        assert np.allclose(min_b, expected_min)
        assert np.allclose(max_b, expected_max)

    def test_cube_bounds_scaled(self):
        """Test cube bounding box with scale."""
        cube = Cube(size=2.0, position=(0, 0, 0))
        cube.set_scale(2, 2, 2)
        min_b, max_b = cube.get_bounds()
        # Scale doubles the half-size
        expected_min = np.array([-2, -2, -2])
        expected_max = np.array([2, 2, 2])
        assert np.allclose(min_b, expected_min)
        assert np.allclose(max_b, expected_max)

    def test_cube_serialization(self):
        """Test cube serialization."""
        cube = Cube(size=1.5, position=(1, 2, 3))
        d = cube.to_dict()
        assert d["type"] == "Cube"
        assert d["position"] == [1, 2, 3]
        assert d["name"] == "Cube"


class TestSphere:
    """Test Sphere primitive."""

    def test_sphere_initialization(self):
        """Test sphere creation."""
        sphere = Sphere(radius=2.0)
        assert sphere.radius == 2.0
        assert sphere.name == "Sphere"

    def test_sphere_volume(self):
        """Test sphere volume calculation."""
        sphere = Sphere(radius=1.0)
        expected = (4 / 3) * math.pi
        assert math.isclose(sphere.volume(), expected, rel_tol=1e-9)

    def test_sphere_volume_radius_2(self):
        """Test sphere volume with radius=2."""
        sphere = Sphere(radius=2.0)
        expected = (4 / 3) * math.pi * 8
        assert math.isclose(sphere.volume(), expected, rel_tol=1e-9)

    def test_sphere_bounds(self):
        """Test sphere bounding box."""
        sphere = Sphere(radius=1.0, position=(1, 1, 1))
        min_b, max_b = sphere.get_bounds()
        expected_min = np.array([0, 0, 0])
        expected_max = np.array([2, 2, 2])
        assert np.allclose(min_b, expected_min)
        assert np.allclose(max_b, expected_max)

    def test_sphere_bounds_scaled(self):
        """Test sphere bounding box with scale."""
        sphere = Sphere(radius=1.0, position=(0, 0, 0))
        sphere.set_scale(2, 2, 2)
        min_b, max_b = sphere.get_bounds()
        expected_min = np.array([-2, -2, -2])
        expected_max = np.array([2, 2, 2])
        assert np.allclose(min_b, expected_min)
        assert np.allclose(max_b, expected_max)


class TestCylinder:
    """Test Cylinder primitive."""

    def test_cylinder_initialization(self):
        """Test cylinder creation."""
        cyl = Cylinder(radius=1.0, height=2.0)
        assert cyl.radius == 1.0
        assert cyl.height == 2.0
        assert cyl.name == "Cylinder"

    def test_cylinder_volume(self):
        """Test cylinder volume calculation."""
        cyl = Cylinder(radius=2.0, height=5.0)
        expected = math.pi * 4 * 5
        assert math.isclose(cyl.volume(), expected, rel_tol=1e-9)

    def test_cylinder_bounds(self):
        """Test cylinder bounding box."""
        cyl = Cylinder(radius=1.0, height=2.0, position=(0, 0, 0))
        min_b, max_b = cyl.get_bounds()
        # Cylinder is centered at position
        expected_min = np.array([-1, -1, -1])
        expected_max = np.array([1, 1, 1])
        assert np.allclose(min_b, expected_min)
        assert np.allclose(max_b, expected_max)


class TestCone:
    """Test Cone primitive."""

    def test_cone_initialization(self):
        """Test cone creation."""
        cone = Cone(radius=1.0, height=3.0)
        assert cone.radius == 1.0
        assert cone.height == 3.0
        assert cone.name == "Cone"

    def test_cone_volume(self):
        """Test cone volume calculation."""
        cone = Cone(radius=2.0, height=6.0)
        expected = (1 / 3) * math.pi * 4 * 6
        assert math.isclose(cone.volume(), expected, rel_tol=1e-9)

    def test_cone_bounds(self):
        """Test cone bounding box."""
        cone = Cone(radius=1.0, height=2.0, position=(0, 0, 0))
        min_b, max_b = cone.get_bounds()
        expected_min = np.array([-1, -1, 0])
        expected_max = np.array([1, 1, 2])
        assert np.allclose(min_b, expected_min)
        assert np.allclose(max_b, expected_max)


class TestTorus:
    """Test Torus primitive."""

    def test_torus_initialization(self):
        """Test torus creation."""
        torus = Torus(major_radius=2.0, minor_radius=0.5)
        assert torus.major_radius == 2.0
        assert torus.minor_radius == 0.5
        assert torus.name == "Torus"

    def test_torus_volume(self):
        """Test torus volume calculation."""
        torus = Torus(major_radius=2.0, minor_radius=0.5)
        expected = 2 * (math.pi ** 2) * 2.0 * (0.5 ** 2)
        assert math.isclose(torus.volume(), expected, rel_tol=1e-9)

    def test_torus_volume_formula(self):
        """Test torus volume with known values."""
        # V = 2π²Rr² where R is major radius, r is minor radius
        R, r = 3.0, 1.0
        torus = Torus(major_radius=R, minor_radius=r)
        expected = 2 * (math.pi ** 2) * R * (r ** 2)
        assert math.isclose(torus.volume(), expected, rel_tol=1e-9)

    def test_torus_default_values(self):
        """Test torus with default values."""
        torus = Torus()
        assert torus.major_radius == 1.0
        assert torus.minor_radius == 0.25


class TestShapeTransformations:
    """Test transformations across different shapes."""

    @pytest.mark.parametrize("ShapeClass,kwargs", [
        (Cube, {"size": 2.0}),
        (Sphere, {"radius": 1.5}),
        (Cylinder, {"radius": 1.0, "height": 2.0}),
        (Cone, {"radius": 1.0, "height": 2.0}),
        (Torus, {"major_radius": 2.0, "minor_radius": 0.5}),
    ])
    def test_shape_translate_and_rotate(self, ShapeClass, kwargs):
        """Test that all shapes support translate and rotate."""
        shape = ShapeClass(**kwargs)
        initial_pos = shape.position.copy()
        shape.translate(1, 2, 3)
        assert np.allclose(shape.position, initial_pos + [1, 2, 3])
        shape.rotate(45, 90, 180)
        assert np.allclose(shape.rotation, [45, 90, 180])

    @pytest.mark.parametrize("ShapeClass,kwargs", [
        (Cube, {"size": 2.0}),
        (Sphere, {"radius": 1.5}),
        (Cylinder, {"radius": 1.0, "height": 2.0}),
        (Cone, {"radius": 1.0, "height": 2.0}),
        (Torus, {"major_radius": 2.0, "minor_radius": 0.5}),
    ])
    def test_shape_color_and_tags(self, ShapeClass, kwargs):
        """Test that all shapes support color and tags."""
        shape = ShapeClass(**kwargs)
        shape.set_color(1, 0, 0, 0.5)
        assert shape.material["color"] == (1, 0, 0, 0.5)
        shape.add_tag("test_tag")
        assert "test_tag" in shape.tags


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_cube_zero_size(self):
        """Test cube with zero size."""
        cube = Cube(size=0)
        assert cube.volume() == 0

    def test_sphere_zero_radius(self):
        """Test sphere with zero radius."""
        sphere = Sphere(radius=0)
        assert sphere.volume() == 0

    def test_cylinder_zero_values(self):
        """Test cylinder with zero values."""
        cyl = Cylinder(radius=0, height=2)
        assert cyl.volume() == 0
        cyl2 = Cylinder(radius=1, height=0)
        assert cyl2.volume() == 0

    def test_large_values(self):
        """Test shapes with large values."""
        cube = Cube(size=1e6)
        assert cube.volume() == 1e18
        sphere = Sphere(radius=1e6)
        expected_vol = (4 / 3) * math.pi * (1e6 ** 3)
        assert math.isclose(sphere.volume(), expected_vol, rel_tol=1e-6)

    def test_negative_translate(self):
        """Test negative translation."""
        shape = Shape3D(position=(5, 5, 5))
        shape.translate(-3, -2, -1)
        assert np.allclose(shape.position, [2, 3, 4])

    def test_non_uniform_scale(self):
        """Test non-uniform scaling."""
        cube = Cube(size=2.0, position=(0, 0, 0))
        cube.set_scale(1, 2, 4)
        min_b, max_b = cube.get_bounds()
        # Half-size (1, 1, 1) scaled by (1, 2, 4) = (1, 2, 4)
        expected_min = np.array([-1, -2, -4])
        expected_max = np.array([1, 2, 4])
        assert np.allclose(min_b, expected_min)
        assert np.allclose(max_b, expected_max)
