"""
Implementación de vehículo tipo motocicleta.
Motorcycle vehicle implementation.

Este módulo proporciona un modelo completo de motocicleta con ruedas, motor, bastidor y carrocería.
This module provides a complete motorcycle model with wheels, engine, frame, and body.
"""

import math
from typing import Tuple, Optional
from ..core.composite import CompositePart
from ..core.shapes import Cylinder, Cube
from .components import Wheel, Engine
from ..i18n import get_language


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
        # Usar la posición de la clase padre / Use parent class position
        self.position[:] = position

        # Establecer dimensiones según el tipo de moto / Set dimensions based on bike type
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

        # Crear bastidor / Create frame
        frame_pos = (
            position[0],
            position[1],
            position[2] +
            wheel_radius +
            0.2)
        self._create_frame(frame_pos, length, width)

        # Crear motor / Create engine
        engine_pos = (position[0], position[1], frame_pos[2])
        cylinders = 2 if bike_type == "cruiser" else 4
        self.engine = Engine(cylinders=cylinders, position=engine_pos)
        self.engine.name = "MotorcycleEngine"
        self.engine.add_tag("propulsion")
        self.engine.add_tag("engine")
        # Reducir tamaño del motor para motocicleta / Scale down engine for motorcycle
        for part in self.engine.parts:
            part.set_scale(0.6, 0.6, 0.6)
        self.add_part(self.engine)

        # Crear ruedas / Create wheels
        self.wheels = []
        wheel_positions = [
            (position[0] + length * 0.4, position[1],
             position[2] + wheel_radius * 0.5),   # Rueda delantera / Front wheel
            (position[0] - length * 0.4, position[1],
             position[2] + wheel_radius * 0.5),   # Rueda trasera / Rear wheel
        ]

        for i, wheel_pos in enumerate(wheel_positions):
            wheel = Wheel(radius=wheel_radius, width=0.12, position=wheel_pos)
            wheel.name = f"Wheel_{i + 1}"
            wheel.add_tag("locomotion")
            wheel.add_tag("wheel")
            self.wheels.append(wheel)
            self.add_part(wheel)

        # Crear tanque de combustible y carrocería / Create fuel tank and body
        self._create_body(frame_pos, length, width, seat_height, color)

        # Establecer propiedades / Set properties
        self.set_property("type", bike_type)
        self.set_property("length", length)
        self.set_property("width", width)
        self.set_property("seat_height", seat_height)
        self.set_property("wheel_count", 2)
        self.set_property(
            "engine_power",
            self.engine.get_property(
                "power",
                150))

    def _create_frame(self, position: Tuple[float, float, float],
                      length: float, width: float):
        """Create the motorcycle frame."""
        # Tubo principal del bastidor / Main frame tube
        main_frame = Cylinder(radius=0.03, height=length * 0.8,
                              position=position, rotation=(0, 90, 0))
        main_frame.name = "MainFrame"
        main_frame.add_tag("structural")
        main_frame.add_tag("frame")
        main_frame.set_color(0.2, 0.2, 0.2)  # Gris oscuro / Dark gray
        self.add_part(main_frame)

        # Subbastidor / Subframe
        subframe = Cube(size=0.05, position=(position[0] - length * 0.2,
                                             position[1],
                                             position[2] + 0.2))
        subframe.set_scale(length * 0.4, width * 0.5, 0.4)
        subframe.name = "Subframe"
        subframe.add_tag("structural")
        subframe.set_color(0.2, 0.2, 0.2)
        self.add_part(subframe)

    def _create_body(self, position: Tuple[float, float, float],
                     length: float, width: float, seat_height: float,
                     color: Optional[Tuple[float, float, float]]):
        """Create the motorcycle body and fuel tank."""
        # Tanque de combustible / Fuel tank
        tank = Cube(size=0.4, position=(position[0] + length * 0.1,
                                        position[1],
                                        position[2] + 0.3))
        tank.set_scale(0.8, 0.5, 0.4)
        tank.name = "FuelTank"
        tank.add_tag("storage")
        tank.add_tag("fuel")
        if color:
            tank.set_color(color[0], color[1], color[2])
        else:
            tank.set_color(0.1, 0.3, 0.8)  # Azul / Blue
        self.add_part(tank)

        # Asiento / Seat
        seat = Cube(size=0.3, position=(position[0] - length * 0.15,
                                        position[1],
                                        position[2] + 0.3))
        seat.set_scale(0.6, 0.4, 0.2)
        seat.name = "Seat"
        seat.add_tag("ergonomics")
        seat.add_tag("seat")
        seat.set_color(0.1, 0.1, 0.1)  # Negro / Black
        self.add_part(seat)

        # Manubrio / Handlebars
        handlebar = Cylinder(radius=0.02, height=0.6,
                             position=(position[0] + length * 0.35,
                                       position[1],
                                       position[2] + 0.5),
                             rotation=(0, 90, 0))
        handlebar.name = "Handlebar"
        handlebar.add_tag("control")
        handlebar.add_tag("steering")
        handlebar.set_color(0.3, 0.3, 0.3)
        self.add_part(handlebar)

    def get_specifications(self) -> dict:
        """
        Obtener especificaciones de la motocicleta.
        Get motorcycle specifications.
        """
        lang = get_language()
        if lang == 'es':
            return {
                "tipo": self.bike_type,
                "dimensiones": {
                    "longitud": self.get_property("length"),
                    "ancho": self.get_property("width"),
                    "altura_asiento": self.get_property("seat_height"),
                },
                "ruedas": self.get_property("wheel_count"),
                "motor": {
                    "cilindros": self.engine.get_property("cylinders"),
                    "potencia": self.engine.get_property("power"),
                },
                "total_partes": self.get_part_count(),
            }
        else:
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

    def simulate_movement(self, distance: float,
                          direction: Tuple[float, float, float] = (1, 0, 0)):
        """
        Simulate motorcycle movement.

        Args:
            distance: Distance to move
            direction: Direction vector (normalized)
        """
        import numpy as np
        dir_vector = np.array(direction)
        dir_vector = dir_vector / np.linalg.norm(dir_vector)  # Normalizar / Normalize

        movement = dir_vector * distance
        self.translate(movement[0], movement[1], movement[2])

        # Simular rotación de ruedas / Simulate wheel rotation
        if self.wheels:
            wheel_rotation = (
                distance / (2 * math.pi * self.wheels[0].radius)) * 360
            for wheel in self.wheels:
                wheel.rotate(0, wheel_rotation, 0)
