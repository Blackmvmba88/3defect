# BlackMamba 3D — Road Input Rig

A suspension mechanism needs an input surface to demonstrate meaningful travel. The road rig is the next validation layer above the double-wishbone solver.

## Coordinate contract

- X: lateral / outboard
- Y: vehicle longitudinal / road direction
- Z: vertical

The double-wishbone kinematics remain solved in the X/Z front-view plane. Road input varies along Y and is sampled by distance traveled:

```text
distance = speed * time
road_z = profile(distance)
```

The rig then resolves the lower-arm angle that best matches the requested hub-height displacement while preserving all wishbone link lengths.

## First profiles

- `flat`: zero displacement, baseline high-speed run
- `sine`: repeating smooth waviness
- `bump`: localized smooth raised bump
- `dip`: localized smooth depression

## Validation chain

```text
ROAD PROFILE
→ vehicle speed
→ longitudinal position
→ road height input
→ target hub vertical displacement
→ inverse wishbone solve
→ arm pose
→ upright lean / camber proxy
→ travel trace
```

## Important boundary

This first rig is a deterministic kinematic road-input simulator. It does **not** yet model tire compliance, unsprung mass, spring force, damping force, inertia, grip, chassis pitch/roll, or transient dynamics. Those belong to the later dynamics layer.
