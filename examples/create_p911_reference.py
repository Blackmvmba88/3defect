"""Create and export the P911_REF_001 parametric reference model."""

from pathlib import Path
from pprint import pprint

from defect3d.blender_integration.reference_vehicle import (
    generate_p911_reference_script,
)
from defect3d.vehicles.reference import P911Reference, P911ReferenceParams


params = P911ReferenceParams(
    reference_match=1.0,
    body_color=(0.86, 0.025, 0.055),
)
car = P911Reference(params)

print(car.model_id)
print("\nResolved dimensions:")
pprint(car.resolved())

print("\nWheel centers:")
pprint(car.wheel_centers())

print("\nPart graph:")
pprint(car.part_graph())

output = Path("p911_ref_001_blender.py")
output.write_text(generate_p911_reference_script(car), encoding="utf-8")
print(f"\nBlender script written to: {output}")
