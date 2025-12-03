"""
Ventilation System / Sistema de Ventilación

Sistema de canalizaciones inspirado en termiteros.
Ventilation channel system inspired by termite mounds.
"""

import numpy as np
from typing import List, Tuple
from ..core.composite import CompositePart
from ..core.shapes import Cylinder, Sphere


class VentilationSystem:
    """
    Sistema de ventilación tipo termitero / Termite-inspired ventilation system
    
    Crea canales de ventilación natural que regulan temperatura y humedad.
    Creates natural ventilation channels that regulate temperature and humidity.
    """
    
    def __init__(self, height: float, base_radius: float, channel_count: int = 16):
        """
        Inicializa el sistema de ventilación.
        Initializes the ventilation system.
        
        Args:
            height: Altura total del edificio / Total building height
            base_radius: Radio de la base / Base radius
            channel_count: Número de canales / Number of channels
        """
        self.height = height
        self.base_radius = base_radius
        self.channel_count = channel_count
        
    def generate(self) -> CompositePart:
        """
        Genera el sistema completo de ventilación.
        Generates the complete ventilation system.
        
        Returns:
            CompositePart con todos los canales / CompositePart with all channels
        """
        ventilation = CompositePart(name="ventilation_system")
        
        # Canales verticales principales / Main vertical channels
        for i in range(self.channel_count):
            channel = self._create_vertical_channel(i)
            ventilation.add_part(channel)
            
        # Canales horizontales de conexión / Horizontal connecting channels
        connection_levels = int(self.height / 10)  # Cada 10m / Every 10m
        for level in range(connection_levels):
            connections = self._create_connection_level(level)
            ventilation.add_part(connections)
            
        return ventilation
        
    def _create_vertical_channel(self, index: int) -> CompositePart:
        """
        Crea un canal vertical de ventilación.
        Creates a vertical ventilation channel.
        
        Args:
            index: Índice del canal / Channel index
            
        Returns:
            CompositePart representando el canal / CompositePart representing the channel
        """
        channel = CompositePart(name=f"channel_{index}")
        
        # Distribución en espiral / Spiral distribution
        angle = (2 * np.pi * index) / self.channel_count
        height_offset = (self.height * index) / (self.channel_count * 2)
        
        radius_offset = self.base_radius * 0.6
        
        x = np.cos(angle) * radius_offset
        z = np.sin(angle) * radius_offset
        
        # Canal principal / Main channel
        channel_height = self.height * 0.7
        channel_radius = 0.6
        
        main_channel = Cylinder(
            radius=channel_radius,
            height=channel_height,
            position=(x, height_offset + channel_height / 2, z)
        )
        main_channel.set_color(0.3, 0.5, 0.7, 0.6)  # Azul semi-transparente / Blue semi-transparent
        
        channel.add_part(main_channel)
        
        # Aberturas de ventilación / Ventilation openings
        opening_count = 5
        for j in range(opening_count):
            opening_height = height_offset + (channel_height * (j + 1)) / (opening_count + 1)
            
            opening = Sphere(
                radius=channel_radius * 1.5,
                position=(x, opening_height, z)
            )
            opening.set_color(0.2, 0.4, 0.6, 0.5)
            
            channel.add_part(opening)
            
        return channel
        
    def _create_connection_level(self, level: int) -> CompositePart:
        """
        Crea un nivel de conexiones horizontales.
        Creates a level of horizontal connections.
        
        Args:
            level: Nivel de altura / Height level
            
        Returns:
            CompositePart con conexiones / CompositePart with connections
        """
        connections = CompositePart(name=f"connections_level_{level}")
        
        y = level * 10  # Cada 10m / Every 10m
        connection_count = 8
        
        for i in range(connection_count):
            angle = (2 * np.pi * i) / connection_count
            next_angle = (2 * np.pi * (i + 1)) / connection_count
            
            # Calcular posiciones / Calculate positions
            radius = self.base_radius * 0.6
            x1, z1 = np.cos(angle) * radius, np.sin(angle) * radius
            x2, z2 = np.cos(next_angle) * radius, np.sin(next_angle) * radius
            
            # Canal de conexión / Connection channel
            mid_x, mid_z = (x1 + x2) / 2, (z1 + z2) / 2
            length = np.sqrt((x2 - x1)**2 + (z2 - z1)**2)
            
            connection = Cylinder(
                radius=0.4,
                height=length,
                position=(mid_x, y, mid_z),
                rotation=(0, np.degrees(angle + np.pi/2), 90)
            )
            connection.set_color(0.3, 0.5, 0.7, 0.6)
            
            connections.add_part(connection)
            
        return connections
