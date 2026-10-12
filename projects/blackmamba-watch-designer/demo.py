"""Run from repository root: python -m projects.blackmamba-watch-designer.demo."""
import argparse
import json
from pathlib import Path
from defect3d import Gear, Spring, GearTrain
from defect3d.blender_integration import BlenderExporter


def main():
    parser = argparse.ArgumentParser(description='BlackMamba Watch Designer: ideal mechanical design study')
    parser.add_argument('--output', type=Path, default=Path('watch-output'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    train = GearTrain('BlackMamba Watch Designer')
    train.add_gear(Gear(20, .001, .001))
    train.add_gear(Gear(40, .001, .001, (.03, 0, 0)))
    # Visual indexing: wheel tooth faces the pinion tooth gap at the pitch point.
    train.gears[1]['gear'].mesh.rotate(0, 0, 180/40)
    spring = Spring(coils=6, wire_diameter=.0004, coil_diameter=.004,
                    free_length=.006, position=(0, .025, 0))
    exporter = BlenderExporter()
    exporter.add_object(train.part)
    exporter.add_object(spring.part)
    exporter.save_script(str(args.output / 'watch_blender.py'))
    exporter.save_json(str(args.output / 'watch_geometry.json'))
    (args.output / 'simulation.json').write_text(json.dumps(train.simulate(1, 2, .1), indent=2))
    print('Ideal external gear reduction: 2:1; signed output speed: -1 rad/s')
    print('Geometry study only; accuracy, contacts and manufacturing are not validated.')


if __name__ == '__main__':
    main()
