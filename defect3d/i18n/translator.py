"""
Sistema de traducción con detección automática de idioma.
Translation system with automatic language detection.
"""

import locale
import os
from typing import Dict, Optional


class Translator:
    """
    Traductor con detección automática de idioma del sistema.
    Translator with automatic system language detection.
    """

    def __init__(self):
        """Inicializa el traductor con detección automática de idioma."""
        self._current_language = None
        self._translations = self._load_translations()
        self._detect_language()

    def _detect_language(self) -> str:
        """
        Detecta el idioma del sistema operativo.
        Detects the operating system language.
        """
        if self._current_language:
            return self._current_language

        # Check environment variable first
        env_lang = os.environ.get('DEFECT3D_LANG')
        if env_lang in ['es', 'en']:
            self._current_language = env_lang
            return env_lang

        # Detect from system locale
        try:
            system_locale = locale.getlocale()[0]
            if system_locale:
                # Check if Spanish
                if system_locale.startswith('es'):
                    self._current_language = 'es'
                    return 'es'
        except (ValueError, TypeError):
            pass

        # Default to English
        self._current_language = 'en'
        return 'en'

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Carga las traducciones. Loads translations."""
        return {
            'es': {
                # Core system
                'position': 'posición',
                'rotation': 'rotación',
                'scale': 'escala',
                'color': 'color',
                'material': 'material',

                # Shapes
                'cube': 'cubo',
                'sphere': 'esfera',
                'cylinder': 'cilindro',
                'cone': 'cono',
                'torus': 'toroide',

                # Vehicle parts
                'wheel': 'rueda',
                'tire': 'llanta',
                'rim': 'rin',
                'engine': 'motor',
                'chassis': 'chasis',
                'body': 'carrocería',
                'frame': 'bastidor',
                'fuel_tank': 'tanque de combustible',
                'seat': 'asiento',
                'handlebar': 'manubrio',

                # Vehicle types
                'car': 'coche',
                'motorcycle': 'motocicleta',
                'sedan': 'sedán',
                'sports': 'deportivo',
                'suv': 'camioneta',
                'sport': 'deportiva',
                'cruiser': 'crucero',
                'touring': 'turismo',

                # Properties
                'type': 'tipo',
                'dimensions': 'dimensiones',
                'length': 'longitud',
                'width': 'ancho',
                'height': 'altura',
                'radius': 'radio',
                'cylinders': 'cilindros',
                'power': 'potencia',
                'mass': 'masa',
                'velocity': 'velocidad',
                'acceleration': 'aceleración',
                'force': 'fuerza',
                'gravity': 'gravedad',
                'energy': 'energía',
                'kinetic': 'cinética',
                'potential': 'potencial',

                # Actions
                'create': 'crear',
                'creating': 'creando',
                'export': 'exportar',
                'exporting': 'exportando',
                'simulate': 'simular',
                'simulating': 'simulando',
                'move': 'mover',
                'rotate': 'rotar',
                'translate': 'trasladar',

                # Messages
                'specifications': 'especificaciones',
                'total_parts': 'partes totales',
                'new_position': 'nueva posición',
                'distance': 'distancia',
                'duration': 'duración',
                'saved_to': 'guardado en',
                'done': 'hecho',
                'complete': 'completo',
                'ready': 'listo',

                # Instructions
                'to_visualize': 'Para visualizar en Blender',
                'open_blender': 'Abrir Blender',
                'go_to_scripting': 'Ir a la pestaña de Scripting',
                'open_file': 'Abrir el archivo',
                'run_script': 'Ejecutar el script',

                # Physics
                'initial_position': 'posición inicial',
                'final_position': 'posición final',
                'initial_velocity': 'velocidad inicial',
                'final_velocity': 'velocidad final',
                'simulation': 'simulación',
                'physics': 'física',
                'steps': 'pasos',

                # Errors and warnings
                'error': 'error',
                'warning': 'advertencia',
                'not_found': 'no encontrado',
                'invalid': 'inválido',
            },
            'en': {}  # English uses the original keys
        }

    def set_language(self, lang: str):
        """
        Establece el idioma manualmente.
        Sets the language manually.

        Args:
            lang: 'es' for Spanish, 'en' for English
        """
        if lang in ['es', 'en']:
            self._current_language = lang

    def get_language(self) -> str:
        """
        Obtiene el idioma actual.
        Gets the current language.
        """
        return self._current_language or self._detect_language()

    def translate(self, key: str, default: Optional[str] = None) -> str:
        """
        Traduce una clave al idioma actual.
        Translates a key to the current language.

        Args:
            key: Translation key
            default: Default value if translation not found

        Returns:
            Translated string or original key
        """
        lang = self.get_language()

        if lang == 'en':
            return default or key

        translations = self._translations.get(lang, {})
        return translations.get(key, default or key)

    def format(self, template: str, **kwargs) -> str:
        """
        Formatea un string con traducciones.
        Formats a string with translations.
        """
        lang = self.get_language()

        if lang == 'es':
            # Translate template keys
            for key, value in kwargs.items():
                if isinstance(value,
                              str) and value in self._translations['es']:
                    kwargs[key] = self._translations['es'][value]

        return template.format(**kwargs)


# Global translator instance
_translator = Translator()


def set_language(lang: str):
    """
    Establece el idioma globalmente.
    Sets the language globally.

    Args:
        lang: 'es' para español, 'en' para inglés
              'es' for Spanish, 'en' for English
    """
    _translator.set_language(lang)


def get_language() -> str:
    """
    Obtiene el idioma actual.
    Gets the current language.
    """
    return _translator.get_language()


def _(key: str, default: Optional[str] = None) -> str:
    """
    Función de traducción abreviada.
    Short translation function.

    Args:
        key: Translation key
        default: Default value if not found

    Returns:
        Translated string
    """
    return _translator.translate(key, default)
