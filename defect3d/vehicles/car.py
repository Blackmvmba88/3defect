"""
Car vehicle implementation.

This module provides a complete car model with wheels, engine, chassis, and body.
"""

import math
from typing import Tuple, Optional
from ..core.composite import CompositePart
from .components import Wheel, Engine, Chassis, Body


class Car(CompositePart):
    """
    A complete car model.
    
    This class creates a full car with all necessary components:
    - 4 wheels
    - Engine
    - Chassis
    - Body
    """
    
    def __init__(self, 
                 car_type: str = "sedan",
                 position: Tuple[float, float, float] = (0, 0, 0),
                 color: Optional[Tuple[float, float, float]] = None):
        """
        Create a car.
        
        Args:
            car_type: Type of car (sedan, sports, suv)
            position: Position in 3D space
            color: RGB color tuple (0-1 range)
        """
        super().__init__(name=f"Car_{car_type}")
        self.car_type = car_type
        # Use parent class position
        self.position[:] = position
        
        # Set dimensions based on car type
        if car_type == "sedan":
            length, width, height = 4.5, 1.8, 1.5
            wheel_radius = 0.35
        elif car_type == "sports":
            length, width, height = 4.2, 1.9, 1.2
            wheel_radius = 0.38
        elif car_type == "suv":
            length, width, height = 5.0, 2.0, 1.9
            wheel_radius = 0.42
        else:
            length, width, height = 4.5, 1.8, 1.5
            wheel_radius = 0.35
        
        # Create chassis
        chassis_pos = (position[0], position[1], position[2] + wheel_radius)
        self.chassis = Chassis(length=length, width=width, height=0.3,
                              position=chassis_pos)
        self.add_part(self.chassis)
        
        # Create engine
        engine_pos = (position[0] + length * 0.3, position[1], chassis_pos[2] + 0.3)
        cylinders = 4 if car_type == "sedan" else 6 if car_type == "sports" else 6
        self.engine = Engine(cylinders=cylinders, position=engine_pos)
        self.add_part(self.engine)
        
        # Create wheels
        self.wheels = []
        wheel_positions = [
            (position[0] + length * 0.3, position[1] + width * 0.45, position[2] + wheel_radius * 0.5),   # Front right
            (position[0] + length * 0.3, position[1] - width * 0.45, position[2] + wheel_radius * 0.5),   # Front left
            (position[0] - length * 0.3, position[1] + width * 0.45, position[2] + wheel_radius * 0.5),   # Rear right
            (position[0] - length * 0.3, position[1] - width * 0.45, position[2] + wheel_radius * 0.5),   # Rear left
        ]
        
        for i, wheel_pos in enumerate(wheel_positions):
            wheel = Wheel(radius=wheel_radius, width=0.25, position=wheel_pos)
            wheel.name = f"Wheel_{i+1}"
            self.wheels.append(wheel)
            self.add_part(wheel)
        
        # Create body
        body_pos = (position[0], position[1], chassis_pos[2] + 0.5)
        body_style = car_type if car_type in ["sedan", "sports"] else "sedan"
        self.body = Body(style=body_style, position=body_pos)
        
        # Apply custom color if provided
        if color:
            for part in self.body.parts:
                if "Body" in part.name:
                    part.set_color(color[0], color[1], color[2])
        
        self.add_part(self.body)
        
        # Set properties
        self.set_property("type", car_type)
        self.set_property("length", length)
        self.set_property("width", width)
        self.set_property("height", height)
        self.set_property("wheel_count", 4)
        self.set_property("engine_power", self.engine.get_property("power", 200))
        
    def get_specifications(self) -> dict:
        """Get car specifications."""
        return {
            "type": self.car_type,
            "dimensions": {
                "length": self.get_property("length"),
                "width": self.get_property("width"),
                "height": self.get_property("height"),
            },
            "wheels": self.get_property("wheel_count"),
            "engine": {
                "cylinders": self.engine.get_property("cylinders"),
                "power": self.engine.get_property("power"),
            },
            "parts_count": self.get_part_count(),
        }
    
    def simulate_movement(self, distance: float, direction: Tuple[float, float, float] = (1, 0, 0)):
        """
        Simulate car movement.
        
        Args:
            distance: Distance to move
            direction: Direction vector (normalized)
        """
        import numpy as np
        dir_vector = np.array(direction)
        dir_vector = dir_vector / np.linalg.norm(dir_vector)  # Normalize
        
        movement = dir_vector * distance
        self.translate(movement[0], movement[1], movement[2])
        
        # Simulate wheel rotation (simple)
        if self.wheels:
            wheel_rotation = (distance / (2 * math.pi * self.wheels[0].radius)) * 360
            for wheel in self.wheels:
                wheel.rotate(0, wheel_rotation, 0)
