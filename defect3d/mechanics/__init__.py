"""
Mechanics module - mechanical components for building vehicles and systems.

This module provides reusable mechanical parts organized by function:
- wheels.py: Wheel and tire assemblies
- engines.py: Engine blocks and powertrains
- frames.py: Chassis, frames, and structural components
"""

from .wheels import Wheel
from .engines import Engine
from .frames import Chassis, Body

__all__ = ['Wheel', 'Engine', 'Chassis', 'Body']
