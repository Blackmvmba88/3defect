"""
Motorcycle vehicle implementation.

This module provides a complete motorcycle model with wheels, engine, frame, and body.
"""

from typing import Tuple, Optional
from ..core.composite import CompositePart
from ..core.shapes import Cylinder, Cube
from .components import Wheel, Engine


class Motorcycle(CompositePart):
    """
    A complete motorcycle model.
    
    This class creates a full motorcycle with all necessary components:
    - 2 wheels
    - Engine
    - Frame
    - Body/fuel tank
    """
    
    def __init__(self, 
                 bike_type: str = "sport",
                 position: Tuple[float, float, float] = (0, 0, 0),
                 color: Optional[Tuple[float, float, float]] = None):
        """
        Create a motorcycle.
        
        Args:
            bike_type: Type of motorcycle (sport, cruiser, touring)
            position: Position in 3D space
            color: RGB color tuple (0-1 range)
        """
        super().__init__(name=f"Motorcycle_{bike_type}")
        self.bike_type = bike_type
        self.position = position
        
        # Set dimensions based on bike type
        if bike_type == "sport":
            length, width, seat_height = 2.0, 0.7, 0.8
            wheel_radius = 0.32
        elif bike_type == "cruiser":
            length, width, seat_height = 2.3, 0.8, 0.7
            wheel_radius = 0.35
        elif bike_type == "touring":
            length, width, seat_height = 2.4, 0.9, 0.85
            wheel_radius = 0.34
        else:
            length, width, seat_height = 2.0, 0.7, 0.8
            wheel_radius = 0.32
        
        # Create frame
        frame_pos = (position[0], position[1], position[2] + wheel_radius + 0.2)
        self._create_frame(frame_pos, length, width)
        
        # Create engine
        engine_pos = (position[0], position[1], frame_pos[2])
        cylinders = 2 if bike_type == "cruiser" else 4
        self.engine = Engine(cylinders=cylinders, position=engine_pos)
        self.engine.name = "MotorcycleEngine"
        # Scale down engine for motorcycle
        for part in self.engine.parts:
            part.set_scale(0.6, 0.6, 0.6)
        self.add_part(self.engine)
        
        # Create wheels
        self.wheels = []
        wheel_positions = [
            (position[0] + length * 0.4, position[1], position[2] + wheel_radius * 0.5),   # Front wheel
            (position[0] - length * 0.4, position[1], position[2] + wheel_radius * 0.5),   # Rear wheel
        ]
        
        for i, wheel_pos in enumerate(wheel_positions):
            wheel = Wheel(radius=wheel_radius, width=0.12, position=wheel_pos)
            wheel.name = f"Wheel_{i+1}"
            self.wheels.append(wheel)
            self.add_part(wheel)
        
        # Create fuel tank and body
        self._create_body(frame_pos, length, width, seat_height, color)
        
        # Set properties
        self.set_property("type", bike_type)
        self.set_property("length", length)
        self.set_property("width", width)
        self.set_property("seat_height", seat_height)
        self.set_property("wheel_count", 2)
        self.set_property("engine_power", self.engine.get_property("power", 150))
        
    def _create_frame(self, position: Tuple[float, float, float], 
                     length: float, width: float):
        """Create the motorcycle frame."""
        # Main frame tube
        main_frame = Cylinder(radius=0.03, height=length * 0.8,
                             position=position, rotation=(0, 90, 0))
        main_frame.name = "MainFrame"
        main_frame.set_color(0.2, 0.2, 0.2)  # Dark gray
        self.add_part(main_frame)
        
        # Subframe
        subframe = Cube(size=0.05, position=(position[0] - length * 0.2, 
                                             position[1], 
                                             position[2] + 0.2))
        subframe.set_scale(length * 0.4, width * 0.5, 0.4)
        subframe.name = "Subframe"
        subframe.set_color(0.2, 0.2, 0.2)
        self.add_part(subframe)
        
    def _create_body(self, position: Tuple[float, float, float],
                    length: float, width: float, seat_height: float,
                    color: Optional[Tuple[float, float, float]]):
        """Create the motorcycle body and fuel tank."""
        # Fuel tank
        tank = Cube(size=0.4, position=(position[0] + length * 0.1,
                                        position[1],
                                        position[2] + 0.3))
        tank.set_scale(0.8, 0.5, 0.4)
        tank.name = "FuelTank"
        if color:
            tank.set_color(color[0], color[1], color[2])
        else:
            tank.set_color(0.1, 0.3, 0.8)  # Blue
        self.add_part(tank)
        
        # Seat
        seat = Cube(size=0.3, position=(position[0] - length * 0.15,
                                        position[1],
                                        position[2] + 0.3))
        seat.set_scale(0.6, 0.4, 0.2)
        seat.name = "Seat"
        seat.set_color(0.1, 0.1, 0.1)  # Black
        self.add_part(seat)
        
        # Handlebars
        handlebar = Cylinder(radius=0.02, height=0.6,
                            position=(position[0] + length * 0.35,
                                    position[1],
                                    position[2] + 0.5),
                            rotation=(0, 90, 0))
        handlebar.name = "Handlebar"
        handlebar.set_color(0.3, 0.3, 0.3)
        self.add_part(handlebar)
        
    def get_specifications(self) -> dict:
        """Get motorcycle specifications."""
        return {
            "type": self.bike_type,
            "dimensions": {
                "length": self.get_property("length"),
                "width": self.get_property("width"),
                "seat_height": self.get_property("seat_height"),
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
        Simulate motorcycle movement.
        
        Args:
            distance: Distance to move
            direction: Direction vector (normalized)
        """
        import numpy as np
        dir_vector = np.array(direction)
        dir_vector = dir_vector / np.linalg.norm(dir_vector)  # Normalize
        
        movement = dir_vector * distance
        self.translate(movement[0], movement[1], movement[2])
        
        # Simulate wheel rotation
        if self.wheels:
            wheel_rotation = (distance / (2 * 3.14159 * self.wheels[0].radius)) * 360
            for wheel in self.wheels:
                wheel.rotate(0, wheel_rotation, 0)
