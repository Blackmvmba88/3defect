# BlackMamba 3D — Brake Rig

Braking is one of the clearest suspension demonstrations because a flat road can still create visible front compression through longitudinal load transfer.

## First-order physical model

The brake rig uses the standard longitudinal load-transfer relation:

```text
Delta F = m * a * h / L
```

Where:

- `m` = vehicle mass
- `a` = braking deceleration
- `h` = center-of-gravity height
- `L` = wheelbase

Half of the transferred load is assigned to one front corner for the first single-corner visualization.

That corner is then simulated as a linear spring-damper response:

```text
m_corner * x_ddot + c * x_dot + k * x = F_corner(t)
```

The solved compression is mapped back into the double-wishbone kinematic solver so every visible arm/upright pose still preserves the mechanism's rigid link lengths.

## What the test can show

- initial speed
- deceleration in m/s² and g
- front load transfer
- front-corner force step
- compression over time
- compression velocity
- lower-arm angle
- hub vertical travel
- upright lean / camber proxy

## What it does not claim yet

This is a first longitudinal dynamics layer, not a complete vehicle model. It does not yet include tire compliance, anti-dive geometry, brake torque reaction at the upright, aerodynamic load, rear suspension, chassis pitch inertia, nonlinear spring rate, bump stops, damper force curves, or tire-force limits.

Those become later BlackMamba dynamics modules rather than hidden assumptions inside this test.
