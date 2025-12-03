"""
Biomimetic Architecture Module / Módulo de Arquitectura Biomimética

Este módulo implementa un sistema de modelado arquitectónico biomimético
inspirado en formas orgánicas como coral, hueso y conchas.

This module implements a biomimetic architectural modeling system
inspired by organic forms like coral, bone, and shells.
"""

from .scales import BuildingScale, get_scale_config, get_all_scales
from .biomimetic_mesh import BiomimeticMesh
from .exoskeleton import FractalExoskeleton
from .ventilation import VentilationSystem
from .reactive_skin import ReactiveSkin

__all__ = [
    'BuildingScale',
    'get_scale_config',
    'get_all_scales',
    'BiomimeticMesh',
    'FractalExoskeleton',
    'VentilationSystem',
    'ReactiveSkin',
]
