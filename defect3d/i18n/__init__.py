"""
Internacionalización (i18n) para 3defect.
Internationalization (i18n) module for 3defect.

Este módulo proporciona detección automática de idioma y localización.
This module provides automatic language detection and localization.
"""

from .translator import Translator, set_language, get_language, _

__all__ = ['Translator', 'set_language', 'get_language', '_']
