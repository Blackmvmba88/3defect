#!/usr/bin/env python3
"""
Ejemplo completo en español: Demostración del sistema 3defect.

Este ejemplo muestra todas las capacidades del sistema en español,
incluyendo creación de vehículos, simulación física y exportación a Blender.
"""

import sys
import os

# Agregar directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Forzar idioma español
from defect3d.i18n import set_language
set_language('es')

from defect3d import Car, Motorcycle
from defect3d.blender_integration import export_to_blender
from defect3d.physics import PhysicsSimulator


def ejemplo_coche():
    """Ejemplo de creación de un coche."""
    print("\n" + "=" * 60)
    print("EJEMPLO 1: CREACIÓN DE COCHES")
    print("=" * 60)
    
    # Crear un sedán
    print("\n1. Creando un sedán azul...")
    sedan = Car(car_type="sedan", position=(0, 0, 0), color=(0.2, 0.3, 0.9))
    
    specs = sedan.get_specifications()
    print(f"\nEspecificaciones del sedán:")
    print(f"  • Tipo: {specs['tipo']}")
    print(f"  • Dimensiones: {specs['dimensiones']['longitud']:.2f}m x {specs['dimensiones']['ancho']:.2f}m x {specs['dimensiones']['altura']:.2f}m")
    print(f"  • Ruedas: {specs['ruedas']}")
    print(f"  • Motor: {specs['motor']['cilindros']} cilindros, {specs['motor']['potencia']} HP")
    print(f"  • Total de partes: {specs['total_partes']}")
    
    # Crear un deportivo
    print("\n2. Creando un deportivo rojo...")
    deportivo = Car(car_type="sports", color=(0.9, 0.1, 0.1))
    
    specs = deportivo.get_specifications()
    print(f"\nEspecificaciones del deportivo:")
    print(f"  • Tipo: {specs['tipo']}")
    print(f"  • Motor: {specs['motor']['cilindros']} cilindros, {specs['motor']['potencia']} HP")
    print(f"  • Dimensiones: {specs['dimensiones']['longitud']:.2f}m x {specs['dimensiones']['ancho']:.2f}m")
    
    return sedan, deportivo


def ejemplo_motocicleta():
    """Ejemplo de creación de una motocicleta."""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: CREACIÓN DE MOTOCICLETAS")
    print("=" * 60)
    
    # Crear moto deportiva
    print("\n1. Creando una moto deportiva amarilla...")
    moto = Motorcycle(bike_type="sport", color=(0.9, 0.9, 0.1))
    
    specs = moto.get_specifications()
    print(f"\nEspecificaciones de la motocicleta:")
    print(f"  • Tipo: {specs['tipo']}")
    print(f"  • Dimensiones: {specs['dimensiones']['longitud']:.2f}m x {specs['dimensiones']['ancho']:.2f}m")
    print(f"  • Altura del asiento: {specs['dimensiones']['altura_asiento']:.2f}m")
    print(f"  • Ruedas: {specs['ruedas']}")
    print(f"  • Motor: {specs['motor']['cilindros']} cilindros, {specs['motor']['potencia']} HP")
    
    return moto


def ejemplo_simulacion_fisica():
    """Ejemplo de simulación física."""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: SIMULACIÓN FÍSICA")
    print("=" * 60)
    
    # Crear coche
    print("\n1. Simulando aceleración de un coche...")
    coche = Car(car_type="sedan")
    
    # Crear simulador
    sim = PhysicsSimulator(gravity=(0, 0, -9.81))
    masa_coche = 1500  # kg
    sim.add_object(coche, mass=masa_coche, velocity=(0, 0, 0))
    
    print(f"   Masa del coche: {masa_coche} kg")
    print(f"   Posición inicial: {coche.position}")
    
    # Aplicar fuerza de motor
    print("\n2. Aplicando fuerza del motor (5000 N)...")
    for i in range(30):  # 30 pasos = ~0.5 segundos
        sim.apply_force(0, (5000, 0, 0))
        sim.step()
    
    velocidad = sim.objects[0]['velocity']
    rapidez = (velocidad[0]**2 + velocidad[1]**2 + velocidad[2]**2)**0.5
    
    print(f"   Posición final: {coche.position}")
    print(f"   Velocidad final: {velocidad}")
    print(f"   Rapidez: {rapidez:.2f} m/s ({rapidez * 3.6:.2f} km/h)")
    
    # Energía cinética
    energia = sim.get_kinetic_energy(0)
    print(f"   Energía cinética: {energia:.2f} Julios")


def ejemplo_exportacion():
    """Ejemplo de exportación a Blender."""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: EXPORTACIÓN A BLENDER")
    print("=" * 60)
    
    print("\n1. Creando coche para exportar...")
    coche = Car(car_type="sports", color=(0.9, 0.1, 0.1))
    
    print("2. Exportando a Blender...")
    output_file = os.path.join(os.path.dirname(__file__), "ejemplo_español_export.py")
    export_to_blender(coche, output_file, also_json=True)
    
    print(f"\n¡Archivo guardado! {output_file}")
    print("\nPara visualizar en Blender:")
    print("  1. Abrir Blender")
    print("  2. Ir a la pestaña de Scripting")
    print("  3. Abrir el archivo generado")
    print("  4. Ejecutar el script (Alt+P)")


def main():
    """Función principal."""
    print("\n" + "=" * 60)
    print("SISTEMA 3DEFECT - EJEMPLOS EN ESPAÑOL")
    print("Sistema de modelado 3D para vehículos y sistemas mecánicos")
    print("=" * 60)
    
    # Ejecutar ejemplos
    sedan, deportivo = ejemplo_coche()
    moto = ejemplo_motocicleta()
    ejemplo_simulacion_fisica()
    ejemplo_exportacion()
    
    print("\n" + "=" * 60)
    print("¡EJEMPLOS COMPLETADOS!")
    print("=" * 60)
    print("\nEl sistema 3defect está completamente localizado en español.")
    print("Todos los mensajes, especificaciones y documentación se adaptan")
    print("automáticamente según el idioma del sistema operativo.")
    print("\nPara forzar el idioma español:")
    print("  from defect3d.i18n import set_language")
    print("  set_language('es')")
    print("\nPara forzar el idioma inglés:")
    print("  set_language('en')")
    print("\n¡Diviértete creando vehículos en 3D! 🚗🏍️✨")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
