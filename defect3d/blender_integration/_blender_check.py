"""
Blender availability check and graceful degradation.

This module provides utilities to check if Blender is available
and handle graceful degradation when it's not.
"""

import warnings
from typing import Tuple

# Try to detect Blender availability
_BLENDER_AVAILABLE = False
_BLENDER_ERROR = None

try:
    import bpy
    _BLENDER_AVAILABLE = True
except ImportError as e:
    _BLENDER_ERROR = str(e)


def is_blender_available() -> bool:
    """
    Check if Blender Python API is available.
    
    Returns:
        True if bpy can be imported, False otherwise
    """
    return _BLENDER_AVAILABLE


def get_blender_error() -> str:
    """
    Get the error message from failed Blender import attempt.
    
    Returns:
        Error message if import failed, empty string if successful
    """
    return _BLENDER_ERROR or ""


def require_blender(feature_name: str = "Blender integration") -> bool:
    """
    Verify Blender is available and raise if not.
    
    Args:
        feature_name: Name of the feature requiring Blender
        
    Returns:
        True if Blender is available
        
    Raises:
        RuntimeError: If Blender is not available
    """
    if not _BLENDER_AVAILABLE:
        msg = (
            f"{feature_name} requires Blender Python API (bpy) to be installed. "
            f"Error: {_BLENDER_ERROR}"
        )
        raise RuntimeError(msg)
    return True


def warn_blender_unavailable(feature_name: str = "Blender integration"):
    """
    Warn that a Blender-dependent feature is unavailable.
    
    Args:
        feature_name: Name of the feature that requires Blender
    """
    if not _BLENDER_AVAILABLE:
        warnings.warn(
            f"{feature_name} is unavailable. Blender Python API (bpy) not found. "
            f"Error: {_BLENDER_ERROR}",
            RuntimeWarning,
            stacklevel=2
        )
