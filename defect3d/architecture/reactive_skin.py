"""
Reactive Skin System / Sistema de Piel Reactiva

Piel fotosintética con paneles hexagonales inspirados en hojas.
Photosynthetic skin with hexagonal panels inspired by leaves.
"""

import numpy as np
from typing import Tuple, List
from ..core.composite import CompositePart
from ..core.shapes import Sphere, Cylinder

# Constantes / Constants
HEXAGON_SPACING_FACTOR = 1.5  # Factor de espaciado entre hexágonos / Spacing factor between hexagons


class ReactiveSkin:
    """
    Sistema de piel reactiva fotosintética / Reactive photosynthetic skin system

    Genera paneles hexagonales que responden a luz y regulan humedad.
    Generates hexagonal panels that respond to light and regulate humidity.
    """

    def __init__(self, height: float, base_radius: float, hexagon_size: float = 0.5):
        """
        Inicializa el sistema de piel reactiva.
        Initializes the reactive skin system.

        Args:
            height: Altura total del edificio / Total building height
            base_radius: Radio de la base / Base radius
            hexagon_size: Tamaño de cada hexágono / Size of each hexagon
        """
        self.height = height
        self.base_radius = base_radius
        self.hexagon_size = hexagon_size

    def generate(self, photosynthetic: bool = True) -> CompositePart:
        """
        Genera la piel reactiva completa.
        Generates the complete reactive skin.

        Args:
            photosynthetic: Si incluir capacidad fotosintética / Whether to include photosynthetic capability

        Returns:
            CompositePart con toda la piel / CompositePart with entire skin
        """
        skin = CompositePart(name="reactive_skin")

        # Calcular distribución de hexágonos / Calculate hexagon distribution
        rows = int(self.height / (self.hexagon_size * HEXAGON_SPACING_FACTOR))

        for row in range(rows):
            row_panels = self._create_hexagon_row(row, rows, photosynthetic)
            skin.add_part(row_panels)

        return skin

    def _create_hexagon_row(self, row: int, total_rows: int,
                           photosynthetic: bool) -> CompositePart:
        """
        Crea una fila de paneles hexagonales.
        Creates a row of hexagonal panels.

        Args:
            row: Número de fila / Row number
            total_rows: Total de filas / Total rows
            photosynthetic: Si es fotosintético / If photosynthetic

        Returns:
            CompositePart con la fila / CompositePart with the row
        """
        row_comp = CompositePart(name=f"hexagon_row_{row}")

        # Calcular altura y radio / Calculate height and radius
        y = row * self.hexagon_size * HEXAGON_SPACING_FACTOR
        progress = row / total_rows
        current_radius = self.base_radius * (1.0 - progress * 0.3)

        # Calcular número de hexágonos en esta fila / Calculate number of hexagons in this row
        circumference = 2 * np.pi * current_radius
        cols = int(circumference / (self.hexagon_size * 2))

        for col in range(cols):
            angle = (2 * np.pi * col) / cols

            x = np.cos(angle) * current_radius
            z = np.sin(angle) * current_radius

            # Crear panel hexagonal / Create hexagonal panel
            hexagon = self._create_hexagon_panel(x, y, z, angle, photosynthetic)
            row_comp.add_part(hexagon)

        return row_comp

    def _create_hexagon_panel(self, x: float, y: float, z: float, angle: float,
                             photosynthetic: bool) -> CompositePart:
        """
        Crea un panel hexagonal individual.
        Creates an individual hexagonal panel.

        Args:
            x, y, z: Posición del panel / Panel position
            angle: Ángulo de rotación / Rotation angle
            photosynthetic: Si es fotosintético / If photosynthetic

        Returns:
            CompositePart representando el hexágono / CompositePart representing the hexagon
        """
        panel = CompositePart(name="hexagon_panel")

        # Panel base (simplificado como esfera) / Base panel (simplified as sphere)
        if photosynthetic:
            # Verde para fotosíntesis / Green for photosynthesis
            color = (0.3, 0.8, 0.4, 1.0)
        else:
            # Blanco para reflexión / White for reflection
            color = (0.9, 0.9, 0.85, 1.0)

        base = Sphere(
            radius=self.hexagon_size * 0.45,
            position=(x, y, z)
        )
        base.set_color(*color)

        panel.add_part(base)

        # Añadir estructura de soporte / Add support structure
        support_height = self.hexagon_size * 0.2
        support = Cylinder(
            radius=self.hexagon_size * 0.1,
            height=support_height,
            position=(x * 0.95, y - support_height / 2, z * 0.95)
        )
        support.set_color(0.7, 0.7, 0.6, 1.0)

        panel.add_part(support)

        return panel

    def get_material_config(self) -> dict:
        """
        Obtiene configuración de materiales para la piel.
        Gets material configuration for the skin.

        Returns:
            Dict con configuración de materiales / Dict with material configuration
        """
        return {
            "photosynthetic": {
                "base_color": (0.3, 0.8, 0.4, 1.0),
                "roughness": 0.6,
                "metallic": 0.0,
                "emission": (0.1, 0.3, 0.1),  # Ligero brillo verde / Light green glow
                "subsurface": 0.3,  # Scattering orgánico / Organic scattering
            },
            "reflective": {
                "base_color": (0.9, 0.9, 0.85, 1.0),
                "roughness": 0.3,
                "metallic": 0.1,
                "transmission": 0.1,
            },
            "support": {
                "base_color": (0.7, 0.7, 0.6, 1.0),
                "roughness": 0.7,
                "metallic": 0.0,
            }
        }
