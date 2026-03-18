"""
Building Scales Configuration / Configuración de Escalas de Edificio

Define las escalas disponibles para edificios biomiméticos.
Defines available scales for biomimetic buildings.
"""

from enum import Enum
from typing import Dict, Tuple


class BuildingScale(Enum):
    """
    Escalas de edificio disponibles / Available building scales
    """
    S = "pavilion"      # Pabellón biomimético 8-12m / Biomimetic pavilion 8-12m
    M = "cultural"      # Centro cultural/museo 40-60m / Cultural center/museum 40-60m
    L = "tower"         # Torre orgánica 120-200m / Organic tower 120-200m
    XL = "megastructure"  # Megaestructura fractal 300-800m / Fractal megastructure 300-800m


def get_scale_config(scale: BuildingScale) -> Dict:
    """
    Obtiene la configuración para una escala específica.
    Gets the configuration for a specific scale.

    Args:
        scale: BuildingScale enum value

    Returns:
        Dict con configuración de dimensiones, LODs, y parámetros
        Dict with dimension, LOD, and parameter configuration
    """
    configs = {
        BuildingScale.S: {
            "name_es": "Pabellón Biomimético",
            "name_en": "Biomimetic Pavilion",
            "height_range": (8, 12),  # metros / meters
            "base_radius": 6,
            "floors": 1,
            "rib_count": 12,
            "hexagon_size": 0.3,
            "ventilation_channels": 8,
            "lod_levels": {
                "LOD0": {"vertices": 50000, "detail": 1.0},
                "LOD1": {"vertices": 20000, "detail": 0.6},
                "LOD2": {"vertices": 5000, "detail": 0.3},
            },
            "materials": {
                "skin": {"roughness": 0.4, "metallic": 0.1},
                "ribs": {"roughness": 0.6, "metallic": 0.0},
                "vegetation": {"roughness": 0.8, "metallic": 0.0},
                "glass": {"roughness": 0.0, "metallic": 0.0, "transmission": 0.95},
            },
        },
        BuildingScale.M: {
            "name_es": "Centro Cultural Orgánico",
            "name_en": "Organic Cultural Center",
            "height_range": (40, 60),
            "base_radius": 25,
            "floors": 3,
            "rib_count": 24,
            "hexagon_size": 0.5,
            "ventilation_channels": 16,
            "lod_levels": {
                "LOD0": {"vertices": 150000, "detail": 1.0},
                "LOD1": {"vertices": 60000, "detail": 0.6},
                "LOD2": {"vertices": 15000, "detail": 0.3},
            },
            "materials": {
                "skin": {"roughness": 0.4, "metallic": 0.1},
                "ribs": {"roughness": 0.6, "metallic": 0.0},
                "vegetation": {"roughness": 0.8, "metallic": 0.0},
                "glass": {"roughness": 0.0, "metallic": 0.0, "transmission": 0.95},
            },
        },
        BuildingScale.L: {
            "name_es": "Torre Orgánica",
            "name_en": "Organic Tower",
            "height_range": (120, 200),
            "base_radius": 40,
            "floors": 40,
            "rib_count": 36,
            "hexagon_size": 0.8,
            "ventilation_channels": 32,
            "lod_levels": {
                "LOD0": {"vertices": 300000, "detail": 1.0},
                "LOD1": {"vertices": 120000, "detail": 0.6},
                "LOD2": {"vertices": 30000, "detail": 0.3},
            },
            "materials": {
                "skin": {"roughness": 0.4, "metallic": 0.1},
                "ribs": {"roughness": 0.6, "metallic": 0.0},
                "vegetation": {"roughness": 0.8, "metallic": 0.0},
                "glass": {"roughness": 0.0, "metallic": 0.0, "transmission": 0.95},
            },
        },
        BuildingScale.XL: {
            "name_es": "Megaestructura Fractal",
            "name_en": "Fractal Megastructure",
            "height_range": (300, 800),
            "base_radius": 150,
            "floors": 150,
            "rib_count": 72,
            "hexagon_size": 1.5,
            "ventilation_channels": 64,
            "lod_levels": {
                "LOD0": {"vertices": 500000, "detail": 1.0},
                "LOD1": {"vertices": 200000, "detail": 0.6},
                "LOD2": {"vertices": 50000, "detail": 0.3},
            },
            "materials": {
                "skin": {"roughness": 0.4, "metallic": 0.1},
                "ribs": {"roughness": 0.6, "metallic": 0.0},
                "vegetation": {"roughness": 0.8, "metallic": 0.0},
                "glass": {"roughness": 0.0, "metallic": 0.0, "transmission": 0.95},
            },
        },
    }

    return configs[scale]


def get_all_scales() -> Dict[str, Tuple[str, str]]:
    """
    Obtiene información de todas las escalas disponibles.
    Gets information about all available scales.

    Returns:
        Dict mapeando escala a (nombre_es, nombre_en, rango_altura)
        Dict mapping scale to (name_es, name_en, height_range)
    """
    return {
        "S": ("Pabellón Biomimético (8-12m)", "Biomimetic Pavilion (8-12m)", (8, 12)),
        "M": ("Centro Cultural/Museo (40-60m)", "Cultural Center/Museum (40-60m)", (40, 60)),
        "L": ("Torre Orgánica (120-200m)", "Organic Tower (120-200m)", (120, 200)),
        "XL": ("Megaestructura Fractal (300-800m)", "Fractal Megastructure (300-800m)", (300, 800)),
    }
