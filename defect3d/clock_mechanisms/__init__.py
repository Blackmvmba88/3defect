"""
Mecanismos de relojería / Clock Mechanisms

Este módulo implementa los componentes fundamentales de relojería.
This module implements the fundamental clockwork components.
"""

import math
from defect3d import Cylinder, Torus, Sphere, CompositePart


class Gear:
    """
    Rueda dentada / Gear wheel
    
    Una rueda con dientes que transmite movimiento rotacional.
    A wheel with teeth that transmits rotational movement.
    """
    
    def __init__(self, teeth=20, module=1.0, thickness=0.5, position=(0, 0, 0)):
        """
        Crear un engranaje / Create a gear
        
        Args:
            teeth: Número de dientes / Number of teeth
            module: Módulo del engranaje (tamaño diente) / Gear module (tooth size)
            thickness: Grosor del engranaje / Gear thickness
            position: Posición 3D / 3D position
        """
        self.teeth = teeth
        self.module = module
        self.thickness = thickness
        self.position = position
        
        # Calcular diámetro primitivo / Calculate pitch diameter
        self.pitch_diameter = module * teeth
        self.pitch_radius = self.pitch_diameter / 2.0
        
        # Crear geometría / Create geometry
        self.part = CompositePart(name=f"gear_{teeth}t")
        
        # Disco principal / Main disc
        disc = Cylinder(radius=self.pitch_radius, height=thickness, position=position)
        disc.set_color(0.7, 0.7, 0.8, 1.0)
        self.part.add_part(disc)
        
        # Eje central / Central shaft
        shaft_radius = self.pitch_radius * 0.15
        shaft = Cylinder(radius=shaft_radius, height=thickness * 1.2, position=position)
        shaft.set_color(0.5, 0.5, 0.6, 1.0)
        self.part.add_part(shaft)
        
    def volume(self):
        """Volumen aproximado / Approximate volume"""
        return math.pi * self.pitch_radius**2 * self.thickness
    
    def gear_ratio(self, other_gear):
        """
        Calcular relación de engranajes / Calculate gear ratio
        
        Args:
            other_gear: Otro engranaje / Another gear
            
        Returns:
            Relación de transmisión / Transmission ratio
        """
        return self.teeth / other_gear.teeth
    
    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Gear",
            "teeth": self.teeth,
            "module": self.module,
            "pitch_diameter": self.pitch_diameter,
            "thickness": self.thickness,
            "position": self.position
        }


class Escapement:
    """
    Escape / Escapement mechanism
    
    Mecanismo que controla la liberación de energía en pulsos regulares.
    Mechanism that controls the release of energy in regular pulses.
    """
    
    def __init__(self, frequency=1.0, position=(0, 0, 0)):
        """
        Crear un escape / Create an escapement
        
        Args:
            frequency: Frecuencia de escape (Hz) / Escapement frequency (Hz)
            position: Posición 3D / 3D position
        """
        self.frequency = frequency
        self.position = position
        self.period = 1.0 / frequency
        
        # Crear geometría simplificada / Create simplified geometry
        self.part = CompositePart(name="escapement")
        
        # Rueda de escape / Escape wheel
        escape_wheel = Cylinder(radius=0.3, height=0.1, position=position)
        escape_wheel.set_color(0.8, 0.6, 0.3, 1.0)
        self.part.add_part(escape_wheel)
        
        # Áncora / Anchor
        anchor_pos = (position[0] + 0.35, position[1], position[2])
        anchor = Cylinder(radius=0.15, height=0.15, position=anchor_pos)
        anchor.set_color(0.7, 0.4, 0.3, 1.0)
        self.part.add_part(anchor)
    
    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Escapement",
            "frequency": self.frequency,
            "period": self.period,
            "position": self.position
        }


class Pendulum:
    """
    Péndulo / Pendulum
    
    Oscilador que regula el tiempo mediante oscilación gravitacional.
    Oscillator that regulates time through gravitational oscillation.
    """
    
    def __init__(self, length=1.0, mass=0.5, position=(0, 0, 0)):
        """
        Crear un péndulo / Create a pendulum
        
        Args:
            length: Longitud del péndulo / Pendulum length
            mass: Masa de la lenteja / Bob mass
            position: Posición del pivote / Pivot position
        """
        self.length = length
        self.mass = mass
        self.position = position
        
        # Calcular período / Calculate period (T = 2π√(L/g))
        g = 9.81  # m/s²
        self.period = 2 * math.pi * math.sqrt(length / g)
        self.frequency = 1.0 / self.period
        
        # Crear geometría / Create geometry
        self.part = CompositePart(name="pendulum")
        
        # Varilla / Rod
        rod_pos = (position[0], position[1], position[2] - length/2)
        rod = Cylinder(radius=0.02, height=length, position=rod_pos)
        rod.set_color(0.5, 0.5, 0.5, 1.0)
        self.part.add_part(rod)
        
        # Lenteja (masa) / Bob (mass)
        bob_radius = (mass * 0.3) ** (1/3)  # Aproximación / Approximation
        bob_pos = (position[0], position[1], position[2] - length)
        bob = Sphere(radius=bob_radius, position=bob_pos)
        bob.set_color(0.8, 0.6, 0.2, 1.0)
        self.part.add_part(bob)
        
        # Pivote / Pivot
        pivot = Sphere(radius=0.05, position=position)
        pivot.set_color(0.3, 0.3, 0.3, 1.0)
        self.part.add_part(pivot)
    
    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Pendulum",
            "length": self.length,
            "mass": self.mass,
            "period": self.period,
            "frequency": self.frequency,
            "position": self.position
        }


class Spring:
    """
    Resorte / Spring
    
    Almacena energía mediante deformación elástica.
    Stores energy through elastic deformation.
    """
    
    def __init__(self, coils=10, wire_diameter=0.05, coil_diameter=0.5, 
                 free_length=1.0, stiffness=100.0, position=(0, 0, 0)):
        """
        Crear un resorte / Create a spring
        
        Args:
            coils: Número de espiras / Number of coils
            wire_diameter: Diámetro del alambre / Wire diameter
            coil_diameter: Diámetro de la espira / Coil diameter
            free_length: Longitud libre / Free length
            stiffness: Rigidez (N/m) / Stiffness (N/m)
            position: Posición 3D / 3D position
        """
        self.coils = coils
        self.wire_diameter = wire_diameter
        self.coil_diameter = coil_diameter
        self.free_length = free_length
        self.stiffness = stiffness
        self.position = position
        
        # Energía almacenada (con compresión x) / Stored energy (with compression x)
        # E = 0.5 * k * x²
        
        # Crear geometría simplificada / Create simplified geometry
        self.part = CompositePart(name="spring")
        
        # Representar con toros apilados / Represent with stacked tori
        coil_radius = coil_diameter / 2.0
        spacing = free_length / (coils + 1)
        
        for i in range(coils):
            z_pos = position[2] + spacing * (i + 1)
            torus_pos = (position[0], position[1], z_pos)
            torus = Torus(major_radius=coil_radius, minor_radius=wire_diameter/2, 
                         position=torus_pos)
            torus.set_color(0.6, 0.6, 0.7, 1.0)
            self.part.add_part(torus)
    
    def energy(self, compression):
        """
        Energía almacenada / Stored energy
        
        Args:
            compression: Compresión del resorte / Spring compression
            
        Returns:
            Energía en Joules / Energy in Joules
        """
        return 0.5 * self.stiffness * compression**2
    
    def force(self, compression):
        """
        Fuerza ejercida / Force exerted
        
        Args:
            compression: Compresión del resorte / Spring compression
            
        Returns:
            Fuerza en Newtons / Force in Newtons
        """
        return self.stiffness * compression
    
    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "Spring",
            "coils": self.coils,
            "wire_diameter": self.wire_diameter,
            "coil_diameter": self.coil_diameter,
            "free_length": self.free_length,
            "stiffness": self.stiffness,
            "position": self.position
        }


class GearTrain:
    """
    Tren de engranajes / Gear train
    
    Sistema de múltiples engranajes que modifica velocidad y torque.
    System of multiple gears that modifies speed and torque.
    """
    
    def __init__(self, name="gear_train"):
        """Crear un tren de engranajes / Create a gear train"""
        self.name = name
        self.gears = []
        self.part = CompositePart(name=name)
    
    def add_gear(self, gear, connects_to=None):
        """
        Agregar un engranaje al tren / Add a gear to the train
        
        Args:
            gear: Engranaje a agregar / Gear to add
            connects_to: Índice del engranaje con el que conecta / Index of gear it connects to
        """
        self.gears.append({
            "gear": gear,
            "connects_to": connects_to
        })
        self.part.add_part(gear.part)
    
    def total_ratio(self):
        """
        Relación de transmisión total / Total transmission ratio
        
        Returns:
            Relación de entrada/salida / Input/output ratio
        """
        if len(self.gears) < 2:
            return 1.0
        
        ratio = 1.0
        for i in range(1, len(self.gears)):
            current = self.gears[i]["gear"]
            previous = self.gears[i-1]["gear"]
            ratio *= current.gear_ratio(previous)
        
        return ratio
    
    def output_speed(self, input_speed):
        """
        Velocidad de salida / Output speed
        
        Args:
            input_speed: Velocidad de entrada (RPM) / Input speed (RPM)
            
        Returns:
            Velocidad de salida (RPM) / Output speed (RPM)
        """
        return input_speed / self.total_ratio()
    
    def to_dict(self):
        """Exportar a diccionario / Export to dictionary"""
        return {
            "type": "GearTrain",
            "name": self.name,
            "gears": [g["gear"].to_dict() for g in self.gears],
            "total_ratio": self.total_ratio()
        }


__all__ = ['Gear', 'Escapement', 'Pendulum', 'Spring', 'GearTrain']
