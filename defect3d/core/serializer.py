"""
Universal JSON serialization for 3D objects.

This module provides functions to export 3D objects and scenes
to structured JSON format for storage, transfer, or analysis.
"""

import json
from typing import Any, Dict, List, Union
from .shapes import Shape3D
from .composite import CompositePart


def serialize_shape(shape: Shape3D) -> Dict[str, Any]:
    """
    Serialize a single 3D shape to dictionary.

    Args:
        shape: Shape3D object to serialize

    Returns:
        Dictionary representation of the shape
    """
    data = {
        "type": shape.__class__.__name__,
        "name": shape.name,
        "position": shape.position.tolist(),
        "rotation": shape.rotation.tolist(),
        "scale": shape.scale.tolist(),
        "material": shape.material
    }

    # Add shape-specific properties
    if hasattr(shape, 'size'):
        data['size'] = shape.size
    if hasattr(shape, 'radius'):
        data['radius'] = shape.radius
    if hasattr(shape, 'height'):
        data['height'] = shape.height
    if hasattr(shape, 'major_radius'):
        data['major_radius'] = shape.major_radius
    if hasattr(shape, 'minor_radius'):
        data['minor_radius'] = shape.minor_radius

    return data


def serialize_composite(composite: CompositePart) -> Dict[str, Any]:
    """
    Serialize a composite part to dictionary.

    Args:
        composite: CompositePart object to serialize

    Returns:
        Dictionary representation of the composite
    """
    data = {
        "type": "CompositePart",
        "name": composite.name,
        "position": composite.position.tolist(),
        "rotation": composite.rotation.tolist(),
        "properties": composite.properties,
        "parts": [],
        "connections": []
    }

    # Serialize all child parts
    for part in composite.parts:
        if isinstance(part, CompositePart):
            data['parts'].append(serialize_composite(part))
        elif isinstance(part, Shape3D):
            data['parts'].append(serialize_shape(part))

    # Serialize connections
    for conn in composite.connections:
        connection_data = {
            "type": conn.get("type", "fixed"),
            "part1_index": composite.parts.index(conn["part1"]) if conn["part1"] in composite.parts else -1,
            "part2_index": composite.parts.index(conn["part2"]) if conn["part2"] in composite.parts else -1
        }
        data['connections'].append(connection_data)

    return data


def serialize_object(obj: Union[Shape3D, CompositePart]) -> Dict[str, Any]:
    """
    Serialize any 3D object (shape or composite) to dictionary.

    Args:
        obj: Object to serialize

    Returns:
        Dictionary representation
    """
    if isinstance(obj, CompositePart):
        return serialize_composite(obj)
    elif isinstance(obj, Shape3D):
        return serialize_shape(obj)
    else:
        raise TypeError(f"Cannot serialize object of type {type(obj)}")


def to_json(obj: Union[Shape3D, CompositePart, List],
            pretty: bool = True) -> str:
    """
    Convert object(s) to JSON string.

    Args:
        obj: Object or list of objects to serialize
        pretty: Whether to format JSON with indentation

    Returns:
        JSON string representation
    """
    if isinstance(obj, list):
        data = [serialize_object(item) for item in obj]
    else:
        data = serialize_object(obj)

    if pretty:
        return json.dumps(data, indent=2)
    else:
        return json.dumps(data)


def save_to_json(obj: Union[Shape3D, CompositePart, List],
                 filename: str,
                 pretty: bool = True):
    """
    Save object(s) to JSON file.

    Args:
        obj: Object or list of objects to serialize
        filename: Output file path
        pretty: Whether to format JSON with indentation
    """
    json_str = to_json(obj, pretty=pretty)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_str)


def load_from_json(filename: str) -> Dict[str, Any]:
    """
    Load object data from JSON file.

    Args:
        filename: Input file path

    Returns:
        Dictionary representation of the object(s)

    Note:
        This function returns raw dictionary data.
        Reconstruction of objects from JSON is not yet implemented.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
