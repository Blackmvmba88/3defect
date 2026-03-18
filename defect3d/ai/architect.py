"""
Arquitecto de IA para construcción semántica.
AI Architect for semantic construction.
"""

from typing import Dict, Any, List, Optional
from .blueprints import BlueprintLibrary
from ..core.composite import CompositePart

class AIArchitect:
    """
    Puente entre descripciones de alto nivel y la API de defect3d.
    Bridge between high-level descriptions and defect3d API.
    """

    def __init__(self):
        self.library = BlueprintLibrary()
        self.history = []

    def design(self, concept: str, **kwargs) -> Optional[CompositePart]:
        """
        Diseña una pieza basada en un concepto semántico.

        Args:
            concept: El nombre del concepto (arm, thruster, etc.)
            **kwargs: Parámetros para el diseño
        """
        concept = concept.lower()

        if "arm" in concept or "brazo" in concept:
            segments = kwargs.get("segments", 3)
            part = self.library.create_mechanical_arm(segments=segments)
        elif "thruster" in concept or "motor" in concept or "propulsor" in concept:
            power = kwargs.get("power", 1.0)
            part = self.library.create_thruster(power=power)
        else:
            print(f"Concepto '{concept}' no reconocido por el arquitecto.")
            return None

        self.history.append({"concept": concept, "part": part})
        return part

    def get_parts_by_tag(self, composite: CompositePart, tag: str) -> List[Any]:
        """Filtra partes dentro de un compuesto usando etiquetas semánticas."""
        results = []
        if tag in composite.tags:
            results.append(composite)

        for part in composite.parts:
            if hasattr(part, "tags") and tag in part.tags:
                results.append(part)
            elif isinstance(part, CompositePart):
                results.extend(self.get_parts_by_tag(part, tag))

        return results
