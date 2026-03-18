"""
Biomimetic Mesh Generator / Generador de Malla Biomimética

Genera mallas maestras inspiradas en formas orgánicas como coral, hueso y conchas.
Generates master meshes inspired by organic forms like coral, bone, and shells.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from ..core.composite import CompositePart
from ..core.shapes import Cylinder, Sphere, Cube
from .scales import BuildingScale, get_scale_config


class BiomimeticMesh:
    """
    Generador de malla biomimética maestro / Master biomimetic mesh generator

    Crea estructuras arquitectónicas inspiradas en patrones naturales.
    Creates architectural structures inspired by natural patterns.
    """

    def __init__(self, scale: BuildingScale, height: Optional[float] = None):
        """
        Inicializa el generador de malla biomimética.
        Initializes the biomimetic mesh generator.

        Args:
            scale: Escala del edificio / Building scale
            height: Altura específica (usa rango por defecto si None) / Specific height
        """
        self.scale = scale
        self.config = get_scale_config(scale)

        # Determinar altura / Determine height
        if height is None:
            height_min, height_max = self.config["height_range"]
            self.height = (height_min + height_max) / 2
        else:
            self.height = height

        self.base_radius = self.config["base_radius"]

        # Crear estructura principal / Create main structure
        self.structure = CompositePart(name=f"BiomimeticBuilding_{scale.value}")

        # Generar componentes / Generate components
        self._generate_base_form()
        self._generate_exoskeleton()
        self._generate_ventilation()
        self._generate_reactive_skin()

    def _generate_base_form(self):
        """
        Genera la forma base biomimética inspirada en coral y hueso.
        Generates biomimetic base form inspired by coral and bone.
        """
        # Forma base orgánica / Organic base form
        # Usamos múltiples cilindros deformados para simular crecimiento orgánico
        # Use multiple deformed cylinders to simulate organic growth

        segments = 12  # Segmentos verticales / Vertical segments
        segment_height = self.height / segments

        for i in range(segments):
            # Radio variable (más ancho en base, estrecho en cima)
            # Variable radius (wider at base, narrower at top)
            progress = i / segments
            radius_factor = 1.0 - (progress * 0.3)  # Reduce 30% hacia arriba
            current_radius = self.base_radius * radius_factor

            # Añadir variación orgánica / Add organic variation
            phase = i * 0.5
            organic_variation = np.sin(phase) * 0.1 * current_radius

            segment = Cylinder(
                radius=current_radius + organic_variation,
                height=segment_height,
                position=(0, i * segment_height, 0)
            )
            segment.set_color(0.9, 0.9, 0.85, 1.0)  # Color base / Base color

            self.structure.add_part(segment)

    def _generate_exoskeleton(self):
        """
        Genera el exoesqueleto estructural tipo "ribs" fractales.
        Generates structural exoskeleton with fractal "ribs".
        """
        rib_count = self.config["rib_count"]

        for i in range(rib_count):
            angle = (2 * np.pi * i) / rib_count

            # Generar costilla fractal / Generate fractal rib
            rib = self._generate_fractal_rib(angle, depth=2)
            self.structure.add_part(rib)

    def _generate_fractal_rib(self, angle: float, depth: int) -> CompositePart:
        """
        Genera una costilla con patrón fractal.
        Generates a rib with fractal pattern.

        Args:
            angle: Ángulo alrededor del edificio / Angle around building
            depth: Profundidad de recursión fractal / Fractal recursion depth

        Returns:
            CompositePart representando la costilla / CompositePart representing the rib
        """
        rib = CompositePart(name=f"fractal_rib_{angle:.2f}")

        # Costilla principal / Main rib
        rib_length = self.height * 0.8
        rib_width = 0.3

        x = np.cos(angle) * self.base_radius
        z = np.sin(angle) * self.base_radius

        main_bone = Cylinder(
            radius=rib_width,
            height=rib_length,
            position=(x, rib_length / 2, z),
            rotation=(0, 0, 90)
        )
        main_bone.set_color(0.95, 0.95, 0.9, 1.0)

        rib.add_part(main_bone)

        # Añadir ramificaciones fractales si depth > 0
        # Add fractal branches if depth > 0
        if depth > 0:
            branch_count = 3
            for j in range(branch_count):
                branch_height = rib_length * (j + 1) / (branch_count + 1)
                branch_angle = angle + (np.pi / 6) * (1 if j % 2 == 0 else -1)

                branch_length = rib_length * 0.3
                branch_x = x + np.cos(branch_angle) * branch_length * 0.5
                branch_z = z + np.sin(branch_angle) * branch_length * 0.5

                branch = Cylinder(
                    radius=rib_width * 0.6,
                    height=branch_length,
                    position=(branch_x, branch_height, branch_z),
                    rotation=(0, np.degrees(branch_angle), 45)
                )
                branch.set_color(0.95, 0.95, 0.9, 1.0)

                rib.add_part(branch)

        return rib

    def _generate_ventilation(self):
        """
        Genera canalizaciones internas para ventilación tipo termitero.
        Generates internal ventilation channels like termite mounds.
        """
        channel_count = self.config["ventilation_channels"]

        for i in range(channel_count):
            # Distribución en espiral / Spiral distribution
            angle = (2 * np.pi * i) / channel_count
            height_offset = (self.height * i) / channel_count

            radius_offset = self.base_radius * 0.7

            x = np.cos(angle) * radius_offset
            z = np.sin(angle) * radius_offset

            # Canal vertical / Vertical channel
            channel = Cylinder(
                radius=0.5,
                height=self.height * 0.3,
                position=(x, height_offset, z)
            )
            channel.set_color(0.3, 0.5, 0.7, 0.5)  # Semi-transparente / Semi-transparent

            self.structure.add_part(channel)

    def _generate_reactive_skin(self):
        """
        Genera piel reactiva con panales hexagonales inspirados en hojas.
        Generates reactive skin with hexagonal panels inspired by leaves.
        """
        hexagon_size = self.config["hexagon_size"]

        # Distribuir hexágonos en la superficie / Distribute hexagons on surface
        # Simplificado: usar esferas pequeñas para representar hexágonos
        # Simplified: use small spheres to represent hexagons

        rows = int(self.height / (hexagon_size * 1.5))
        cols_base = int(2 * np.pi * self.base_radius / (hexagon_size * 2))

        for row in range(rows):
            y = row * hexagon_size * 1.5
            progress = row / rows
            current_radius = self.base_radius * (1.0 - progress * 0.3)

            cols = int(cols_base * (1.0 - progress * 0.3))

            for col in range(cols):
                angle = (2 * np.pi * col) / cols

                x = np.cos(angle) * current_radius
                z = np.sin(angle) * current_radius

                # Hexágono como pequeña esfera / Hexagon as small sphere
                hexagon = Sphere(
                    radius=hexagon_size * 0.4,
                    position=(x, y, z)
                )
                hexagon.set_color(0.4, 0.8, 0.5, 1.0)  # Verde para fotosíntesis / Green for photosynthesis

                self.structure.add_part(hexagon)

    def get_mesh(self) -> CompositePart:
        """
        Obtiene la estructura completa de la malla.
        Gets the complete mesh structure.

        Returns:
            CompositePart con toda la estructura / CompositePart with entire structure
        """
        return self.structure

    def get_lod(self, level: str) -> CompositePart:
        """
        Genera un nivel de detalle específico (LOD0, LOD1, LOD2).
        Generates a specific level of detail (LOD0, LOD1, LOD2).

        Args:
            level: "LOD0", "LOD1", o "LOD2"

        Returns:
            CompositePart con nivel de detalle ajustado
            CompositePart with adjusted level of detail
        """
        if level not in self.config["lod_levels"]:
            raise ValueError(f"LOD level {level} no soportado / not supported")

        # Por ahora retornar estructura completa
        # For now return complete structure
        # En implementación completa, simplificar geometría según LOD
        # In complete implementation, simplify geometry based on LOD
        return self.structure

    def get_specifications(self) -> Dict:
        """
        Obtiene las especificaciones del edificio.
        Gets the building specifications.

        Returns:
            Dict con especificaciones completas / Dict with complete specifications
        """
        # Try to get language, default to English
        try:
            from ..i18n import get_language
            lang = get_language()
            lang_code = 'es' if lang == 'es' else 'en'
        except (ImportError, ModuleNotFoundError):
            lang_code = 'en'

        specs = {
            "scale": self.config[f"name_{lang_code}"],
            "height": f"{self.height}m",
            "base_radius": f"{self.base_radius}m",
            "floors": self.config["floors"],
            "ribs": self.config["rib_count"],
            "ventilation_channels": self.config["ventilation_channels"],
            "hexagon_size": f"{self.config['hexagon_size']}m",
            "lod_levels": list(self.config["lod_levels"].keys()),
            "materials": list(self.config["materials"].keys()),
        }

        return specs
