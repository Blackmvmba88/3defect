"""
Pytest fixtures for 3defect testing.

Provides reusable test fixtures for shapes, composites, and complete scenes.
这个模块提供了可重用的测试 fixtures，用于形状、合成体和完整场景。
"""

import pytest
import numpy as np
from defect3d.core.shapes import Cube, Sphere, Cylinder, Cone, Torus
from defect3d.core.composite import CompositePart


# ============================================================================
# Shape Fixtures
# ============================================================================

@pytest.fixture
def basic_cube():
    """Basic cube fixture: 2x2x2 at origin."""
    cube = Cube(size=2.0, position=(0, 0, 0))
    cube.name = "basic_cube"
    return cube


@pytest.fixture
def basic_sphere():
    """Basic sphere fixture: radius 1.0 at origin."""
    sphere = Sphere(radius=1.0, position=(0, 0, 0))
    sphere.name = "basic_sphere"
    return sphere


@pytest.fixture
def basic_cylinder():
    """Basic cylinder fixture: radius 0.5, height 2.0 at origin."""
    cylinder = Cylinder(radius=0.5, height=2.0, position=(0, 0, 0))
    cylinder.name = "basic_cylinder"
    return cylinder


@pytest.fixture
def basic_cone():
    """Basic cone fixture: radius 0.5, height 2.0 at origin."""
    cone = Cone(radius=0.5, height=2.0, position=(0, 0, 0))
    cone.name = "basic_cone"
    return cone


@pytest.fixture
def basic_torus():
    """Basic torus fixture: major=1.0, minor=0.3."""
    torus = Torus(major_radius=1.0, minor_radius=0.3, position=(0, 0, 0))
    torus.name = "basic_torus"
    return torus


@pytest.fixture
def all_shapes():
    """Fixture with all 5 primitive shapes."""
    shapes = {
        'cube': Cube(size=2.0, position=(0, 0, 0)),
        'sphere': Sphere(radius=1.0, position=(1, 0, 0)),
        'cylinder': Cylinder(radius=0.5, height=2.0, position=(2, 0, 0)),
        'cone': Cone(radius=0.5, height=2.0, position=(3, 0, 0)),
        'torus': Torus(major_radius=1.0, minor_radius=0.3, position=(4, 0, 0)),
    }
    shapes['cube'].name = "cube"
    shapes['sphere'].name = "sphere"
    shapes['cylinder'].name = "cylinder"
    shapes['cone'].name = "cone"
    shapes['torus'].name = "torus"
    return shapes


@pytest.fixture
def colored_shapes():
    """Fixture with colored shapes (red, green, blue, yellow, magenta)."""
    colors = {
        'red': (1.0, 0.0, 0.0, 1.0),
        'green': (0.0, 1.0, 0.0, 1.0),
        'blue': (0.0, 0.0, 1.0, 1.0),
        'yellow': (1.0, 1.0, 0.0, 1.0),
        'magenta': (1.0, 0.0, 1.0, 1.0),
    }
    
    shapes = {}
    for i, (color_name, color_value) in enumerate(colors.items()):
        shape = Cube(size=1.0, position=(i, 0, 0))
        shape.name = f"cube_{color_name}"
        r, g, b, a = color_value
        shape.set_color(r, g, b, a)
        shapes[color_name] = shape
    
    return shapes


@pytest.fixture
def transformed_cube():
    """Cube with transformations applied: translated, rotated, scaled."""
    cube = Cube(size=2.0, position=(1, 2, 3))
    cube.name = "transformed_cube"
    cube.translate(1, 1, 1)
    cube.rotate(45, 30, 60)
    cube.set_scale(1.5, 2.0, 0.8)
    return cube


# ============================================================================
# Composite/Assembly Fixtures
# ============================================================================

@pytest.fixture
def empty_composite():
    """Empty composite part with no children."""
    return CompositePart(name="empty_assembly")


@pytest.fixture
def simple_composite():
    """Simple composite: cube + sphere."""
    comp = CompositePart(name="simple_assembly")
    cube = Cube(size=1.0, position=(0, 0, 0))
    cube.name = "chassis"
    comp.add_part(cube)
    sphere = Sphere(radius=0.3, position=(0.5, 0, 0))
    sphere.name = "wheel_1"
    comp.add_part(sphere)
    return comp


@pytest.fixture
def multi_part_composite():
    """Composite with many parts: 5 shapes in a line."""
    comp = CompositePart(name="multi_part_assembly")
    positions = [(i, 0, 0) for i in range(5)]
    
    body = Cube(size=1.0, position=positions[0])
    body.name = "body"
    comp.add_part(body)
    
    wheel_1 = Sphere(radius=0.3, position=positions[1])
    wheel_1.name = "wheel_1"
    comp.add_part(wheel_1)
    
    wheel_2 = Sphere(radius=0.3, position=positions[2])
    wheel_2.name = "wheel_2"
    comp.add_part(wheel_2)
    
    axle = Cylinder(radius=0.2, height=0.5, position=positions[3])
    axle.name = "axle"
    comp.add_part(axle)
    
    bearing = Torus(major_radius=0.4, minor_radius=0.1, position=positions[4])
    bearing.name = "bearing"
    comp.add_part(bearing)
    
    return comp


@pytest.fixture
def tagged_composite():
    """Composite with tags applied to parts."""
    comp = CompositePart(name="tagged_assembly")
    comp.add_tag("vehicle")
    comp.set_property("mass", 1500)
    comp.set_property("max_speed", 120)
    
    body = Cube(size=2.0, position=(0, 0, 0))
    body.name = "body"
    body.add_tag("structural")
    comp.add_part(body)
    
    wheel = Sphere(radius=0.5, position=(1, -1, 0))
    wheel.name = "wheel"
    wheel.add_tag("movable")
    comp.add_part(wheel)
    
    return comp


@pytest.fixture
def nested_composite():
    """Composite with nested composites (3 levels)."""
    # Level 0 (root)
    root = CompositePart(name="vehicle")
    
    # Level 1 (subsystems)
    chassis = CompositePart(name="chassis")
    frame = Cube(size=3.0, position=(0, 0, 0))
    frame.name = "frame"
    chassis.add_part(frame)
    root.add_part(chassis)
    
    # Level 2 (wheels)
    wheel_assembly = CompositePart(name="wheel_assembly")
    tire_1 = Sphere(radius=0.5, position=(0, 0, 0))
    tire_1.name = "tire_1"
    wheel_assembly.add_part(tire_1)
    
    tire_2 = Sphere(radius=0.5, position=(1, 0, 0))
    tire_2.name = "tire_2"
    wheel_assembly.add_part(tire_2)
    
    chassis.add_part(wheel_assembly)
    
    return root


# ============================================================================
# Vehicle Fixtures (common models)
# ============================================================================

@pytest.fixture
def car_model():
    """Simple car model: chassis + 4 wheels."""
    car = CompositePart(name="car")
    car.add_tag("vehicle")
    car.set_property("type", "sedan")
    car.set_property("wheels", 4)
    
    # Chassis (elongated cube)
    chassis = Cube(size=4.0, position=(0, 0, 0))
    chassis.name = "chassis"
    chassis.set_scale(2.0, 1.0, 1.0)  # Make it longer
    chassis.set_color(0.8, 0.2, 0.2, 1.0)  # Red
    car.add_part(chassis)
    
    # 4 wheels (spheres at corners)
    wheel_positions = [(-1, -1.2, 0), (1, -1.2, 0), (-1, 1.2, 0), (1, 1.2, 0)]
    for i, pos in enumerate(wheel_positions):
        wheel = Sphere(radius=0.4, position=pos)
        wheel.name = f"wheel_{i+1}"
        wheel.add_tag("wheel")
        wheel.set_color(0.1, 0.1, 0.1, 1.0)  # Black
        car.add_part(wheel)
    
    return car


@pytest.fixture
def motorcycle_model():
    """Simple motorcycle model: frame + 2 wheels."""
    bike = CompositePart(name="motorcycle")
    bike.add_tag("vehicle")
    bike.set_property("type", "sport")
    bike.set_property("wheels", 2)
    
    # Frame (cylinder)
    frame = Cylinder(radius=0.1, height=1.5, position=(0, 0, 0))
    frame.name = "frame"
    frame.set_color(0.2, 0.2, 0.8, 1.0)  # Blue
    bike.add_part(frame)
    
    # 2 wheels (spheres)
    wheel_positions = [(-0.75, 0, 0), (0.75, 0, 0)]
    for i, pos in enumerate(wheel_positions):
        wheel = Sphere(radius=0.3, position=pos)
        wheel.name = f"wheel_{i+1}"
        wheel.add_tag("wheel")
        wheel.set_color(0.1, 0.1, 0.1, 1.0)  # Black
        bike.add_part(wheel)
    
    return bike


# ============================================================================
# Scene Fixtures
# ============================================================================

@pytest.fixture
def simple_scene(car_model, motorcycle_model):
    """Scene with car and motorcycle."""
    scene = CompositePart(name="scene")
    car_model.position = np.array([0, 0, 0])
    motorcycle_model.position = np.array([5, 0, 0])
    scene.add_part(car_model)
    scene.add_part(motorcycle_model)
    return scene


@pytest.fixture
def complex_scene(all_shapes):
    """Scene with all 5 primitive shapes arranged in 3D space."""
    scene = CompositePart(name="shapes_showcase")
    
    # Arrange shapes in a line with different heights
    z_positions = [0, 0.5, 1.0, 1.5, 2.0]
    for (shape_name, shape), z_pos in zip(all_shapes.items(), z_positions):
        shape.position = np.array([shape.position[0], shape.position[1], z_pos])
        scene.add_part(shape)
    
    return scene


# ============================================================================
# Data Fixtures (for serialization tests)
# ============================================================================

@pytest.fixture
def shape_dict_data():
    """Sample shape dictionary data for deserialization tests."""
    return {
        'type': 'Cube',
        'name': 'test_cube',
        'size': 2.0,
        'position': [0, 0, 0],
        'rotation': [0, 0, 0],
        'scale': [1, 1, 1],
        'color': [0.8, 0.8, 0.8, 1.0],
        'tags': ['test', 'fixture']
    }


@pytest.fixture
def composite_dict_data():
    """Sample composite dictionary data for deserialization tests."""
    return {
        'type': 'CompositePart',
        'name': 'test_assembly',
        'position': [0, 0, 0],
        'rotation': [0, 0, 0],
        'parts': [],
        'tags': ['assembly'],
        'properties': {'mass': 100}
    }


# ============================================================================
# Parametrize Fixtures (for table-driven tests)
# ============================================================================

@pytest.fixture(
    params=[
        {'size': 1.0},
        {'size': 2.0},
        {'size': 5.0},
    ]
)
def cube_sizes(request):
    """Parametrized cube fixture with multiple sizes."""
    cube = Cube(position=(0, 0, 0), **request.param)
    cube.name = f"cube_{request.param['size']}"
    return cube


@pytest.fixture(
    params=[
        {'radius': 0.5, 'height': 1.0},
        {'radius': 1.0, 'height': 2.0},
        {'radius': 2.0, 'height': 4.0},
    ]
)
def cylinder_variants(request):
    """Parametrized cylinder fixture with multiple dimensions."""
    cylinder = Cylinder(position=(0, 0, 0), **request.param)
    cylinder.name = f"cylinder_{request.param['radius']}"
    return cylinder


@pytest.fixture(
    params=[
        (1.0, 0.0, 0.0, 1.0),  # Red
        (0.0, 1.0, 0.0, 1.0),  # Green
        (0.0, 0.0, 1.0, 1.0),  # Blue
        (1.0, 1.0, 1.0, 1.0),  # White
        (0.0, 0.0, 0.0, 1.0),  # Black
    ]
)
def color_values(request):
    """Parametrized color fixture."""
    return request.param
