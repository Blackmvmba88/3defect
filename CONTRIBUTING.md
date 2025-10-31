# Contributing to 3defect

¡Gracias por tu interés en contribuir a 3defect! / Thank you for your interest in contributing to 3defect!

## Cómo Contribuir / How to Contribute

### Reportar Bugs / Report Bugs

Si encuentras un bug, por favor abre un issue incluyendo:
- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs. actual
- Tu entorno (Python version, OS, etc.)

If you find a bug, please open an issue including:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (Python version, OS, etc.)

### Sugerir Características / Suggest Features

Las ideas son bienvenidas! Abre un issue con:
- Descripción de la característica
- Casos de uso
- Ejemplos si es posible

Ideas are welcome! Open an issue with:
- Feature description
- Use cases
- Examples if possible

### Enviar Pull Requests / Submit Pull Requests

1. Fork el repositorio / Fork the repository
2. Crea una rama para tu feature / Create a branch for your feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Haz tus cambios / Make your changes
4. Asegúrate de que el código funciona / Ensure code works
   ```bash
   python examples/create_car.py
   ```
5. Commit tus cambios / Commit your changes
   ```bash
   git commit -m "Add amazing feature"
   ```
6. Push a tu fork / Push to your fork
   ```bash
   git push origin feature/amazing-feature
   ```
7. Abre un Pull Request / Open a Pull Request

## Guías de Estilo / Style Guidelines

### Python Code

- Sigue PEP 8
- Usa docstrings para funciones y clases
- Nombres descriptivos para variables y funciones
- Comentarios en inglés o español

Example:
```python
def create_vehicle(vehicle_type: str, color: tuple) -> CompositePart:
    """
    Create a vehicle with specified type and color.
    
    Args:
        vehicle_type: Type of vehicle ("car" or "motorcycle")
        color: RGB color tuple (0-1 range)
        
    Returns:
        CompositePart: The created vehicle
    """
    # Implementation here
    pass
```

### Commits

- Mensajes claros y descriptivos / Clear and descriptive messages
- Usa presente ("Add feature" no "Added feature")
- Referencia issues si aplica (#123)

### Documentación

- Actualiza README.md si añades features importantes
- Añade ejemplos para nuevas funcionalidades
- Documenta parámetros y valores de retorno

## Áreas de Contribución / Contribution Areas

### Fácil / Easy
- Añadir más colores predefinidos / Add more predefined colors
- Mejorar mensajes de error / Improve error messages
- Corregir typos en documentación / Fix typos in documentation
- Añadir más ejemplos / Add more examples

### Medio / Medium
- Nuevos tipos de vehículos / New vehicle types
- Más formas 3D primitivas / More 3D primitive shapes
- Mejoras en física / Physics improvements
- Tests unitarios / Unit tests

### Avanzado / Advanced
- Colisión entre objetos / Object collision
- Animaciones / Animations
- Exportación a otros formatos / Export to other formats
- Optimizaciones de rendimiento / Performance optimizations

## Ideas de Características / Feature Ideas

Algunas ideas para contribuir:
- 🚁 Helicópteros y aviones / Helicopters and planes
- 🚂 Trenes y vagones / Trains and wagons
- 🏗️ Maquinaria de construcción / Construction machinery
- ⚙️ Sistema de transmisiones / Transmission system
- 🎨 Editor visual / Visual editor
- 📊 Gráficos de simulación / Simulation graphs
- 🌍 Terrenos y ambientes / Terrains and environments
- 🔧 Herramientas de medición / Measurement tools

## Preguntas / Questions

Si tienes preguntas sobre cómo contribuir:
- Abre un issue con la etiqueta "question"
- Revisa issues existentes
- Contacta a los maintainers

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues
- Contact the maintainers

---

## Código de Conducta / Code of Conduct

- Sé respetuoso / Be respectful
- Acepta críticas constructivas / Accept constructive criticism
- Enfócate en lo mejor para el proyecto / Focus on what's best for the project
- Ayuda a otros / Help others

---

¡Gracias por hacer de 3defect un mejor proyecto! / Thank you for making 3defect a better project! 🙏
