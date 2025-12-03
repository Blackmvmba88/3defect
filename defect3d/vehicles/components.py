"""
Common vehicle components.

This module re-exports components from the mechanics module for backward compatibility.
New code should import from defect3d.mechanics directly.
"""

# Import from mechanics module
from ..mechanics import Wheel, Engine, Chassis, Body

__all__ = ['Wheel', 'Engine', 'Chassis', 'Body']

# All classes are imported from mechanics module above
# Keeping this file for backward compatibility only
