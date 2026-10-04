"""Inspect the P911_REF_001 parametric reference model."""

from pprint import pprint

from defect3d.vehicles.reference import P911Reference, P911ReferenceParams

params = P911ReferenceParams(reference_match=1.0, body_color=(0.86, 0.025, 0.055))
car = P911Reference(params)

print(car.model_id)
print("\nResolved dimensions:")
pprint(car.resolved())
print("\nWheel centers:")
pprint(car.wheel_centers())
print("\nPart graph:")
pprint(car.part_graph())
