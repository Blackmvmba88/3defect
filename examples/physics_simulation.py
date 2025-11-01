#!/usr/bin/env python3
"""
Example: Physics simulation with a car.

This script demonstrates how to use the physics simulator to simulate
a car with gravity and forces.
"""

import sys
import os

# Add parent directory to path to import defect3d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from defect3d import Car, Sphere
from defect3d.physics import PhysicsSimulator


def main():
    print("Physics Simulation Example")
    print("=" * 50)

    # Create a simple sphere for demonstration
    print("\n1. Dropping a sphere with gravity...")
    sphere = Sphere(radius=0.5, position=(0, 0, 10))

    # Create physics simulator
    sim = PhysicsSimulator(gravity=(0, 0, -9.81))
    sim.add_object(sphere, mass=1.0, velocity=(0, 0, 0))

    print(f"  Initial position: {sphere.position}")
    print(f"  Initial height: {sphere.position[2]:.2f}m")

    # Simulate for 1 second
    states = sim.simulate(duration=1.0, apply_gravity=True)

    print(f"  Final position: {sphere.position}")
    print(f"  Final height: {sphere.position[2]:.2f}m")
    print(f"  Distance fallen: {10 - sphere.position[2]:.2f}m")
    print(f"  Simulation steps: {len(states)}")

    # Energy calculations
    ke = sim.get_kinetic_energy(0)
    pe = sim.get_potential_energy(0)
    print(f"  Final kinetic energy: {ke:.2f} J")
    print(f"  Final potential energy: {pe:.2f} J")
    print(f"  Total energy: {ke + pe:.2f} J")

    # Reset and simulate projectile motion
    print("\n2. Projectile motion...")
    sim.reset()

    sphere2 = Sphere(radius=0.5, position=(0, 0, 1))
    sim.add_object(sphere2, mass=1.0, velocity=(5, 0, 5))  # Launch at angle

    print(f"  Initial position: {sphere2.position}")
    print(f"  Initial velocity: (5, 0, 5) m/s")

    states = sim.simulate(duration=1.5, apply_gravity=True)

    print(f"  Final position: {sphere2.position}")
    print(f"  Horizontal distance: {sphere2.position[0]:.2f}m")

    # Car simulation
    print("\n3. Car with applied force...")
    sim.reset()

    car = Car(car_type="sedan", position=(0, 0, 0))
    car_mass = 1500  # kg
    sim.add_object(car, mass=car_mass, velocity=(0, 0, 0))

    print(f"  Car mass: {car_mass} kg")
    print(f"  Initial position: {car.position}")

    # Apply driving force for 0.5 seconds
    for i in range(30):  # 30 steps = ~0.5 seconds at 60 FPS
        sim.apply_force(0, (5000, 0, 0))  # 5000 N forward force
        sim.step()

    velocity = sim.objects[0]['velocity']
    speed = (velocity[0]**2 + velocity[1]**2 + velocity[2]**2)**0.5

    print(f"  Final position: {car.position}")
    print(f"  Final velocity: {velocity}")
    print(f"  Final speed: {speed:.2f} m/s ({speed * 3.6:.2f} km/h)")

    print("\n" + "=" * 50)
    print("Simulation complete!")


if __name__ == "__main__":
    main()
