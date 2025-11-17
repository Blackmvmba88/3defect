"""
Common vehicle components.

This module re-exports components from the mechanics module for backward compatibility.
New code should import from defect3d.mechanics directly.
"""

# Import from mechanics module
from ..mechanics import Wheel, Engine, Chassis, Body

# Re-export for backward compatibility
__all__ = ['Wheel', 'Engine', 'Chassis', 'Body']
