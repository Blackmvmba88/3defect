# BlackMamba 3D — Double Wishbone Validation Stack

This slice joins the first suspension components into a mechanism and then gives that mechanism two physical inputs: road profile and braking load transfer.

## Layer 1 — Kinematics

The double-wishbone is solved as a front-view four-bar mechanism. Lower arm, upper arm and upright lengths remain invariant while the lower-arm input angle changes.

Outputs include:

- hub vertical travel
- upright lean / camber proxy
- deterministic travel sweep

## Layer 2 — Road Rig

Longitudinal road distance is derived from speed and time. A road-height profile is sampled under the tire/contact point and inverted through the wishbone travel curve.

Supported first profiles:

- flat
- sine / micro-undulation
- localized bump
- localized dip

A perfectly flat road remains a zero-input baseline regardless of speed.

## Layer 3 — Brake Rig

Longitudinal braking load transfer is computed from vehicle mass, deceleration, CG height and wheelbase. One front corner receives half the transferred load and responds through a linear spring-damper model.

That compression is then mapped into the same wishbone solver used by the road rig.

## Why the layers stay separate

```text
geometry -> kinematics -> road/braking input -> dynamics -> validation
```

The mechanism never invents its own forces, and the force model never changes geometry silently. This keeps every later upgrade replaceable and testable.
