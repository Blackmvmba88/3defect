"""
Fractal Exoskeleton System / Sistema de Exoesqueleto Fractal

Genera estructuras de exoesqueleto con patrones fractales.
Generates exoskeleton structures with fractal patterns.
"""

import numpy as np
from typing import Tuple
from ..core.composite import CompositePart
from ..core.shapes import Cylinder


class FractalExoskeleton:
    """
    Sistema de exoesqueleto fractal / Fractal exoskeleton system

    Genera costillas estructurales con patrones recursivos.
    Generates structural ribs with recursive patterns.
    """

    def __init__(self, height: float, base_radius: float, rib_count: int = 24):
        """
        Inicializa el sistema de exoesqueleto.
        Initializes the exoskeleton system.

        Args:
            height: Altura total del edificio / Total building height
            base_radius: Radio de la base / Base radius
            rib_count: Número de costillas / Number of ribs
        """
        self.height = height
        self.base_radius = base_radius
        self.rib_count = rib_count

    def generate(self, fractal_depth: int = 2) -> CompositePart:
        """
        Genera el exoesqueleto completo.
        Generates the complete exoskeleton.

        Args:
            fractal_depth: Profundidad de recursión fractal / Fractal recursion depth

        Returns:
            CompositePart con exoesqueleto / CompositePart with exoskeleton
        """
        exoskeleton = CompositePart(name="fractal_exoskeleton")

        for i in range(self.rib_count):
            angle = (2 * np.pi * i) / self.rib_count
            rib = self._create_fractal_rib(angle, fractal_depth)
            exoskeleton.add_part(rib)

        return exoskeleton

    def _create_fractal_rib(self, angle: float, depth: int) -> CompositePart:
        """
        Crea una costilla con patrón fractal recursivo.
        Creates a rib with recursive fractal pattern.

        Args:
            angle: Ángulo de posición / Position angle
            depth: Profundidad de recursión / Recursion depth

        Returns:
            CompositePart representando la costilla / CompositePart representing the rib
        """
        rib = CompositePart(name=f"rib_{angle:.2f}")

        # Calcular posición base / Calculate base position
        x = np.cos(angle) * self.base_radius
        z = np.sin(angle) * self.base_radius

        # Costilla principal vertical / Main vertical rib
        main_length = self.height * 0.9
        main_width = 0.4

        main_rib = Cylinder(
            radius=main_width,
            height=main_length,
            position=(x, main_length / 2, z),
            rotation=(0, 0, 0)
        )
        main_rib.set_color(0.95, 0.95, 0.9, 1.0)

        rib.add_part(main_rib)

        # Añadir ramas fractales / Add fractal branches
        if depth > 0:
            self._add_fractal_branches(rib, x, z, angle, main_length, main_width, depth)

        return rib

    def _add_fractal_branches(self, parent: CompositePart, x: float, z: float,
                             base_angle: float, length: float, width: float, depth: int):
        """
        Añade ramas fractales recursivamente / Adds fractal branches recursively
        """
        branch_count = 3

        for i in range(branch_count):
            height_pos = length * (i + 1) / (branch_count + 1)

            # Alternar dirección de ramas / Alternate branch direction
            angle_offset = (np.pi / 8) * (1 if i % 2 == 0 else -1)
            branch_angle = base_angle + angle_offset

            branch_length = length * 0.4
            branch_width = width * 0.7

            # Calcular posición de rama / Calculate branch position
            branch_x = x + np.cos(branch_angle) * branch_length * 0.3
            branch_z = z + np.sin(branch_angle) * branch_length * 0.3

            branch = Cylinder(
                radius=branch_width,
                height=branch_length,
                position=(branch_x, height_pos, branch_z),
                rotation=(0, np.degrees(branch_angle), 30)
            )
            branch.set_color(0.95, 0.95, 0.9, 1.0)

            parent.add_part(branch)

            # Recursión para sub-ramas / Recursion for sub-branches
            if depth > 1:
                sub_branch = CompositePart(name=f"sub_branch_{i}")
                self._add_fractal_branches(
                    sub_branch, branch_x, branch_z, branch_angle,
                    branch_length * 0.6, branch_width * 0.7, depth - 1
                )
                parent.add_part(sub_branch)
