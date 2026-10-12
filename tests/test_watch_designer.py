import ast
from collections import Counter
import math
import numpy as np
import pytest
from defect3d import Gear, Spring, GearTrain
from defect3d.blender_integration.exporter import BlenderExporter


def assert_closed(mesh):
    edges = Counter(tuple(sorted((face[i], face[(i+1)%len(face)])))
                    for face in mesh.faces for i in range(len(face)))
    assert set(edges.values()) == {2}
    assert np.isfinite(mesh.vertices).all()
    volume = sum(np.dot(mesh.vertices[f[0]], np.cross(mesh.vertices[f[i]], mesh.vertices[f[i+1]]))/6
                 for f in mesh.faces for i in range(1, len(f)-1))
    assert volume > 0
    return volume


def test_involute_mesh_and_pitch():
    gear = Gear(40, 0.2, 0.3)
    assert gear.pitch_radius == 4
    radii = np.linalg.norm(np.array(gear.mesh.vertices)[:-2, :2], axis=1)
    assert radii.min() == pytest.approx(gear.root_radius)
    assert radii.max() == pytest.approx(gear.addendum_radius)
    assert assert_closed(gear.mesh) == pytest.approx(gear.volume())
    assert Gear(12).undercut_risk
    assert not Gear(40).undercut_risk
    # Interpolate the actual first flank at the pitch circle.
    vertices = np.array(gear.mesh.vertices)
    flank = vertices[1:10, :2]
    r = np.linalg.norm(flank, axis=1)
    angle = np.interp(gear.pitch_radius, r, np.arctan2(flank[:, 1], flank[:, 0]))
    tooth_width = -2 * angle * gear.pitch_radius
    assert tooth_width == pytest.approx(math.pi * gear.module / 2, rel=.01)



@pytest.mark.parametrize('kwargs', [{'teeth':0}, {'teeth':2.5}, {'teeth':True},
    {'module':-1}, {'thickness':float('nan')}, {'pressure_angle':90}, {'position':(0,0,float('inf'))}])
def test_gear_validation(kwargs):
    with pytest.raises(ValueError): Gear(**kwargs)


def test_helix_continuity_and_hooke():
    spring = Spring(coils=3.5, free_length=2)
    assert len(spring.part.parts) == 1
    assert spring.centerline[0] == pytest.approx((.25,0,0))
    assert spring.centerline[-1] == pytest.approx((-.25,0,2))
    assert_closed(spring.mesh)
    assert spring.energy(.1) == pytest.approx(.5)
    assert spring.force(.1) == 10
    assert Spring(free_length=.1).coil_overlap_risk
    with pytest.raises(ValueError): Spring(coils=0)
    with pytest.raises(ValueError): Spring(wire_diameter=1)


def test_connections_direction_and_simulation():
    train = GearTrain()
    for teeth, parent in [(40,None), (20,0), (80,0), (40,1)]:
        train.add_gear(Gear(teeth), parent)
    assert train.speed_factors() == [1,-2,-.5,1]
    assert train.total_ratio() == 1
    assert train.output_speed(60) == 60
    states = train.simulate(.025, 2, .01)
    assert [s['time'] for s in states] == [0,.01,.02,.025]
    assert states[-1]['angles'] == pytest.approx([.05,-.1,-.025,.05])
    assert train.simulate(0)[0]['time'] == 0
    with pytest.raises(ValueError): train.add_gear(Gear(), 99)
    with pytest.raises(ValueError): train.add_gear(Gear(module=2),0)
    with pytest.raises(ValueError): train.simulate(1,dt=0)
    reduction = GearTrain()
    reduction.add_gear(Gear(20)); reduction.add_gear(Gear(40))
    assert reduction.total_ratio() == 2
    assert reduction.output_speed(60) == 30
    assert reduction.signed_output_speed(60) == -30


def test_mesh_export_and_transforms():
    exporter = BlenderExporter()
    for part in (Gear(position=(1,2,3)).part, Spring().part): exporter.add_object(part)
    script = exporter.generate_blender_script()
    ast.parse(script)
    assert script.count('.from_pydata(') == 2
    mesh = Gear().mesh
    low, high = mesh.get_bounds()
    mesh.translate(1,2,3)
    shifted_low, shifted_high = mesh.get_bounds()
    assert shifted_low == pytest.approx(low+[1,2,3])
    assert shifted_high == pytest.approx(high+[1,2,3])


def test_optimizer_rebuilds_derived_properties():
    import random
    from defect3d import Pendulum
    from defect3d.evolutionary import ClockOptimizer
    state = random.getstate()
    try:
        random.seed(42)
        best, fitness, history = ClockOptimizer.optimize_for_precision(Pendulum, generations=4)
    finally:
        random.setstate(state)
    assert best.period == pytest.approx(2*math.pi*math.sqrt(best.length/9.81))
    assert fitness == pytest.approx(1/(1+abs(best.period-1)))
    assert history == sorted(history)
    assert best.part.parts[0].height == best.length


def test_universal_serialization_keeps_mesh():
    import json
    from defect3d.core.serializer import to_json
    data = json.loads(to_json(Gear().part))
    assert len(data['parts'][0]['vertices']) > 100
