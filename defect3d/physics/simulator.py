"""
Physics simulation for mechanical systems.

This module provides basic physics simulation capabilities including:
- Gravity
- Velocity and acceleration
- Simple collision detection
- Force application
"""

import numpy as np
from typing import Tuple, List, Optional


class PhysicsSimulator:
    """
    Simple physics simulator for 3D objects.

    This simulator handles basic Newtonian physics including gravity,
    velocity, acceleration, and forces.
    """

    def __init__(self, gravity: Tuple[float, float, float] = (0, 0, -9.81)):
        """
        Initialize the physics simulator.

        Args:
            gravity: Gravity vector (default is Earth gravity in -Z direction)
        """
        self.gravity = np.array(gravity)
        self.objects = []
        self.time = 0.0
        self.dt = 0.016  # ~60 FPS / frames por segundo

    def add_object(self, obj, mass: float = 1.0,
                   velocity: Tuple[float, float, float] = (0, 0, 0)):
        """
        Add an object to the simulation.

        Args:
            obj: The object to simulate
            mass: Mass of the object in kg
            velocity: Initial velocity vector
        """
        self.objects.append({
            'object': obj,
            'mass': mass,
            'velocity': np.array(velocity, dtype=float),
            'acceleration': np.array([0.0, 0.0, 0.0]),
            'forces': []
        })

    def apply_force(self, obj_index: int, force: Tuple[float, float, float]):
        """
        Apply a force to an object.

        Args:
            obj_index: Index of the object
            force: Force vector to apply
        """
        if 0 <= obj_index < len(self.objects):
            self.objects[obj_index]['forces'].append(np.array(force))

    def apply_gravity(self, obj_index: int):
        """Apply gravitational force to an object."""
        if 0 <= obj_index < len(self.objects):
            obj_data = self.objects[obj_index]
            gravity_force = obj_data['mass'] * self.gravity
            obj_data['forces'].append(gravity_force)

    def step(self, dt: Optional[float] = None):
        """
        Advance the simulation by one time step.

        Args:
            dt: Time step in seconds (uses default if not provided)
        """
        if dt is None:
            dt = self.dt

        for obj_data in self.objects:
            # Calcular fuerza neta / Calculate net force
            net_force = np.sum(
                obj_data['forces'], axis=0) if obj_data['forces'] else np.array([0.0, 0.0, 0.0])

            # F = ma, entonces a = F/m / F = ma, so a = F/m
            obj_data['acceleration'] = net_force / obj_data['mass']

            # Actualizar velocidad: v = v0 + a*dt / Update velocity: v = v0 + a*dt
            obj_data['velocity'] += obj_data['acceleration'] * dt

            # Actualizar posición: p = p0 + v*dt / Update position: p = p0 + v*dt
            displacement = obj_data['velocity'] * dt
            obj_data['object'].translate(
                displacement[0], displacement[1], displacement[2])

            # Limpiar fuerzas para el siguiente paso / Clear forces for next step
            obj_data['forces'] = []

        self.time += dt

    def simulate(
            self,
            duration: float,
            apply_gravity: bool = True) -> List[dict]:
        """
        Run the simulation for a given duration.

        Args:
            duration: Duration to simulate in seconds
            apply_gravity: Whether to apply gravity to all objects

        Returns:
            List of state snapshots for each time step
        """
        states = []
        num_steps = int(duration / self.dt)

        for _ in range(num_steps):
            # Aplicar gravedad si está habilitada / Apply gravity if enabled
            if apply_gravity:
                for i in range(len(self.objects)):
                    self.apply_gravity(i)

            # Avanzar la simulación / Step the simulation
            self.step()

            # Registrar estado / Record state
            state = {
                'time': self.time,
                'objects': [
                    {
                        'position': obj_data['object'].position.copy(),
                        'velocity': obj_data['velocity'].copy(),
                        'acceleration': obj_data['acceleration'].copy()
                    }
                    for obj_data in self.objects
                ]
            }
            states.append(state)

        return states

    def get_kinetic_energy(self, obj_index: int) -> float:
        """
        Calculate kinetic energy of an object.

        Args:
            obj_index: Index of the object

        Returns:
            Kinetic energy in Joules
        """
        if 0 <= obj_index < len(self.objects):
            obj_data = self.objects[obj_index]
            v = obj_data['velocity']
            speed_squared = np.dot(v, v)
            return 0.5 * obj_data['mass'] * speed_squared
        return 0.0

    def get_potential_energy(
            self,
            obj_index: int,
            reference_height: float = 0.0) -> float:
        """
        Calculate gravitational potential energy.

        Args:
            obj_index: Index of the object
            reference_height: Reference height (z=0 by default)

        Returns:
            Potential energy in Joules
        """
        if 0 <= obj_index < len(self.objects):
            obj_data = self.objects[obj_index]
            height = obj_data['object'].position[2] - reference_height
            # EP = mgh (usando magnitud de gravedad) / PE = mgh (using magnitude of gravity)
            g = np.linalg.norm(self.gravity)
            return obj_data['mass'] * g * height
        return 0.0

    def reset(self):
        """Reset the simulation."""
        self.objects = []
        self.time = 0.0


def simulate_motion(obj, initial_velocity: Tuple[float, float, float],
                    duration: float = 2.0, mass: float = 1.0,
                    apply_gravity: bool = True) -> List[dict]:
    """
    Convenience function to simulate an object's motion.

    Args:
        obj: Object to simulate
        initial_velocity: Initial velocity vector
        duration: Duration of simulation in seconds
        mass: Mass of the object
        apply_gravity: Whether to apply gravity

    Returns:
        List of state snapshots
    """
    sim = PhysicsSimulator()
    sim.add_object(obj, mass=mass, velocity=initial_velocity)
    return sim.simulate(duration, apply_gravity=apply_gravity)
