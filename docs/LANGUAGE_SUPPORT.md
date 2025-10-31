# Language Support / Soporte de Idiomas

## 🌍 Detección Automática de Idioma

El sistema 3defect incluye detección automática de idioma que adapta completamente la interfaz, mensajes y especificaciones según el idioma del sistema operativo del desarrollador.

The 3defect system includes automatic language detection that fully adapts the interface, messages, and specifications based on the developer's operating system language.

---

## Idiomas Soportados / Supported Languages

- 🇪🇸 **Español** (Spanish) - Detección automática / Automatic detection
- 🇬🇧 **English** - Automatic detection / Detección automática

---

## Cómo Funciona / How It Works

### Detección Automática / Automatic Detection

El sistema detecta automáticamente el idioma del sistema operativo al importar el módulo:

The system automatically detects the operating system language when importing the module:

```python
from defect3d import Car

# El sistema detecta el idioma automáticamente
# The system detects the language automatically
coche = Car(car_type="sedan")
specs = coche.get_specifications()

# Si tu sistema está en español, verás:
# If your system is in Spanish, you'll see:
# {
#     'tipo': 'sedan',
#     'dimensiones': {'longitud': 4.5, 'ancho': 1.8, 'altura': 1.5},
#     'motor': {'cilindros': 4, 'potencia': 200}
# }

# Si tu sistema está en inglés, verás:
# If your system is in English, you'll see:
# {
#     'type': 'sedan',
#     'dimensions': {'length': 4.5, 'width': 1.8, 'height': 1.5},
#     'engine': {'cylinders': 4, 'power': 200}
# }
```

### Control Manual / Manual Control

Puedes forzar un idioma específico:

You can force a specific language:

```python
from defect3d.i18n import set_language

# Forzar español / Force Spanish
set_language('es')

# Forzar inglés / Force English
set_language('en')
```

### Variable de Entorno / Environment Variable

También puedes configurar el idioma mediante una variable de entorno:

You can also configure the language via an environment variable:

```bash
# Establecer español / Set Spanish
export DEFECT3D_LANG=es

# Establecer inglés / Set English
export DEFECT3D_LANG=en

# Ejecutar ejemplo / Run example
python examples/create_car.py
```

---

## Elementos Traducidos / Translated Elements

### Especificaciones de Vehículos / Vehicle Specifications

**Español:**
```python
{
    'tipo': 'sports',
    'dimensiones': {
        'longitud': 4.2,
        'ancho': 1.9,
        'altura': 1.2
    },
    'ruedas': 4,
    'motor': {
        'cilindros': 6,
        'potencia': 300
    },
    'total_partes': 7
}
```

**English:**
```python
{
    'type': 'sports',
    'dimensions': {
        'length': 4.2,
        'width': 1.9,
        'height': 1.2
    },
    'wheels': 4,
    'engine': {
        'cylinders': 6,
        'power': 300
    },
    'parts_count': 7
}
```

### Mensajes del Sistema / System Messages

| Español | English |
|---------|---------|
| Creando un coche deportivo... | Creating a sports car... |
| Especificaciones del Coche: | Car Specifications: |
| Simulando movimiento... | Simulating movement... |
| Nueva posición | New position |
| Exportando a Blender... | Exporting to Blender... |
| ¡Hecho! Para visualizar en Blender: | Done! To visualize in Blender: |
| Abrir Blender | Open Blender |
| Ir a la pestaña de Scripting | Go to Scripting tab |
| Ejecutar el script | Run the script |

---

## Ejemplos / Examples

### Ejemplo en Español / Spanish Example

```python
from defect3d.i18n import set_language
set_language('es')

from defect3d import Car, Motorcycle

# Crear un coche
coche = Car(car_type="deportivo", color=(0.9, 0.1, 0.1))
print(f"Tipo: {coche.get_specifications()['tipo']}")

# Crear una motocicleta
moto = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))
print(f"Motor: {moto.get_specifications()['motor']['cilindros']} cilindros")
```

### Example in English

```python
from defect3d.i18n import set_language
set_language('en')

from defect3d import Car, Motorcycle

# Create a car
car = Car(car_type="sports", color=(0.9, 0.1, 0.1))
print(f"Type: {car.get_specifications()['type']}")

# Create a motorcycle
bike = Motorcycle(bike_type="sport", color=(0.1, 0.3, 0.9))
print(f"Engine: {bike.get_specifications()['engine']['cylinders']} cylinders")
```

---

## Archivos de Ejemplo / Example Files

### Para Desarrolladores Españoles / For Spanish Developers

- **`examples/ejemplo_español.py`** - Ejemplo completo en español con todos los features
- **README_ES.md** - Documentación completa en español
- **USAGE.md** - Guía de uso bilingüe

### For English Developers

- **`examples/create_car.py`** - Complete car example (auto-detects language)
- **`examples/create_motorcycle.py`** - Motorcycle example (auto-detects language)
- **README.md** - Complete documentation in English
- **USAGE.md** - Bilingual usage guide

---

## Prioridad de Detección / Detection Priority

El sistema sigue este orden de prioridad para determinar el idioma:

The system follows this priority order to determine the language:

1. **Variable de entorno** / **Environment variable**: `DEFECT3D_LANG`
2. **Configuración manual** / **Manual configuration**: `set_language()`
3. **Locale del sistema** / **System locale**: Detecta automáticamente
4. **Por defecto** / **Default**: Inglés / English

---

## Implementación Técnica / Technical Implementation

### Módulo i18n

El sistema de internacionalización está implementado en `defect3d/i18n/`:

The internationalization system is implemented in `defect3d/i18n/`:

- **`translator.py`** - Sistema de traducción principal / Main translation system
- **Detección automática** de locale del sistema / Automatic system locale detection
- **Diccionario de traducciones** completo / Complete translation dictionary
- **API simple** para uso en todo el código / Simple API for use throughout the code

### Uso en el Código / Usage in Code

```python
from defect3d.i18n import get_language

def get_specifications(self):
    """Obtiene especificaciones adaptadas al idioma."""
    lang = get_language()
    
    if lang == 'es':
        return {
            'tipo': self.car_type,
            'dimensiones': {...},
            'motor': {...}
        }
    else:
        return {
            'type': self.car_type,
            'dimensions': {...},
            'engine': {...}
        }
```

---

## Contribuir / Contributing

¿Quieres añadir soporte para otro idioma? / Want to add support for another language?

1. Añade traducciones al diccionario en `defect3d/i18n/translator.py`
2. Actualiza los métodos `get_specifications()` en vehículos
3. Crea ejemplos en el nuevo idioma
4. Añade documentación

---

## Soporte / Support

Si tienes problemas con el idioma o quieres sugerir mejoras:

If you have issues with language or want to suggest improvements:

- Abre un issue en GitHub / Open an issue on GitHub
- Propón mejoras a las traducciones / Propose translation improvements
- Sugiere nuevos idiomas / Suggest new languages

---

**¡El sistema está completamente adaptado para desarrolladores en español!**

**The system is fully adapted for Spanish-speaking developers!**

🌍 🇪🇸 🇬🇧 ✨
