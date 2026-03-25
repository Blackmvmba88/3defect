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
        elif "clock" in concept or "reloj" in concept:
            precision = kwargs.get("precision", 1.0)
            part = self.library.create_clock_system(precision=precision)
        elif "transmission" in concept or "transmisión" in concept:
            ratio = kwargs.get("ratio", 2.0)
            part = self.library.create_transmission_system(ratio=ratio)
        else:
            print(f"Concepto '{concept}' no reconocido por el arquitecto.")
            return None

        self.history.append({"concept": concept, "part": part})
        return part

    def build(self, prompt: str) -> CompositePart:
        """
        Construye un sistema completo basado en un prompt de lenguaje natural.

        Analiza el prompt, identifica componentes necesarios y los ensambla.
        """
        print(f"🧠 Analizando prompt: '{prompt}'")
        prompt = prompt.lower()

        system = CompositePart(name="AI_Generated_System")
        system.add_tag("ai_built")

        # Diccionario de mapeo semántico / Semantic mapping dictionary
        keywords = {
            "clock": "clock",
            "reloj": "clock",
            "transmission": "transmission",
            "transmisión": "transmission",
            "arm": "arm",
            "brazo": "arm",
            "thruster": "thruster",
            "propulsor": "thruster"
        }

        components_found = []
        for kw, concept in keywords.items():
            if kw in prompt:
                components_found.append(concept)

        if not components_found:
            print("⚠️ No se identificaron componentes claros en el prompt.")
            # Crear un cubo por defecto si no se entiende nada
            from ..core.shapes import Cube
            system.add_part(Cube(size=1.0))
            return system

        # Ensamblar componentes encontrados / Assemble found components
        current_offset = 0
        for concept in components_found:
            part = self.design(concept)
            if part:
                part.translate(current_offset, 0, 0)
                system.add_part(part)
                # Incrementar offset basado en bounds / Increment offset based on bounds
                min_b, max_b = part.get_bounds()
                current_offset += (max_b[0] - min_b[0]) + 1.0

        print(f"✅ Sistema ensamblado con {len(components_found)} componentes principales.")
        return system

    def get_parts_by_tag(self, composite: CompositePart, tag: str) -> List[Any]:
        """Filtra partes dentro de un compuesto usando etiquetas semánticas."""
        results = []
        if tag in composite.tags:
            results.append(composite)

        for part in composite.parts:
            if hasattr(part, "tags") and tag in part.tags:
                results.append(part)
            if isinstance(part, CompositePart):
                results.extend(self.get_parts_by_tag(part, tag))

        return results

    def validate_physics(self, composite: CompositePart) -> bool:
        """
        Realiza un chequeo de cordura física en un sistema generado.
        Checks if the generated system has valid physical properties.
        """
        print(f"🔬 Validando física de: '{composite.name}'")

        # 1. Verificar volumen / Check volume
        total_volume = 0.0
        for part in composite.parts:
            if hasattr(part, "volume"):
                total_volume += part.volume()
            elif isinstance(part, CompositePart):
                # Recursivo para compuestos anidados / Recursive for nested
                for subpart in part.parts:
                    if hasattr(subpart, "volume"):
                        total_volume += subpart.volume()

        if total_volume <= 0:
            print("❌ ERROR: El sistema tiene volumen cero o negativo.")
            return False

        # 2. Verificar conectividad mínima / Check minimum connectivity
        if len(composite.parts) == 0:
            print("❌ ERROR: El sistema no tiene partes.")
            return False

        print(f"✅ Validación física exitosa. Volumen total: {total_volume:.4f} m³")
        return True
