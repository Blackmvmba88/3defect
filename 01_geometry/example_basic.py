#!/usr/bin/env python3
"""
Ejemplo básico de geometría / Basic geometry example

Demuestra la creación y manipulación de formas básicas.
Demonstrates creation and manipulation of basic shapes.
"""

from defect3d import Cube, Sphere, Cylinder, Cone, Torus


def main():
    print("=== NIVEL 1: GEOMETRÍA / LEVEL 1: GEOMETRY ===\n")
    
    # Crear formas básicas / Create basic shapes
    print("1. Creando formas básicas / Creating basic shapes")
    
    cubo = Cube(size=2.0, position=(0, 0, 0))
    cubo.set_color(0.8, 0.2, 0.2, 1.0)  # Rojo / Red
    print(f"   Cubo / Cube: size=2.0, volumen/volume={cubo.volume():.2f}")
    
    esfera = Sphere(radius=1.5, position=(3, 0, 0))
    esfera.set_color(0.2, 0.8, 0.2, 1.0)  # Verde / Green
    print(f"   Esfera / Sphere: radius=1.5, volumen/volume={esfera.volume():.2f}")
    
    cilindro = Cylinder(radius=1.0, height=3.0, position=(6, 0, 0))
    cilindro.set_color(0.2, 0.2, 0.8, 1.0)  # Azul / Blue
    print(f"   Cilindro / Cylinder: radius=1.0, height=3.0, volumen/volume={cilindro.volume():.2f}")
    
    cono = Cone(radius=1.0, height=2.5, position=(9, 0, 0))
    cono.set_color(0.8, 0.8, 0.2, 1.0)  # Amarillo / Yellow
    print(f"   Cono / Cone: radius=1.0, height=2.5, volumen/volume={cono.volume():.2f}")
    
    toro = Torus(major_radius=1.5, minor_radius=0.5, position=(12, 0, 0))
    toro.set_color(0.8, 0.2, 0.8, 1.0)  # Magenta
    print(f"   Toro / Torus: major_radius=1.5, minor_radius=0.5, volumen/volume={toro.volume():.2f}")
    
    # Transformaciones / Transformations
    print("\n2. Aplicando transformaciones / Applying transformations")
    
    cubo2 = Cube(size=1.0, position=(0, 0, 0))
    print(f"   Posición inicial / Initial position: {cubo2.position}")
    
    cubo2.translate(5, 2, 1)
    print(f"   Después de translate(5, 2, 1): {cubo2.position}")
    
    cubo2.rotate(0, 45, 0)
    print(f"   Después de rotate(0, 45, 0): rotation={cubo2.rotation}")
    
    cubo2.set_scale(2, 1, 0.5)
    print(f"   Después de set_scale(2, 1, 0.5): scale={cubo2.scale}")
    
    # Propiedades físicas / Physical properties
    print("\n3. Propiedades físicas / Physical properties")
    
    # Densidad del acero / Steel density
    STEEL_DENSITY = 7850  # kg/m³
    
    cubo_acero = Cube(size=1.0)
    cubo_acero.density = STEEL_DENSITY
    masa = cubo_acero.volume() * cubo_acero.density
    print(f"   Cubo de acero / Steel cube: volumen/volume={cubo_acero.volume():.2f} m³")
    print(f"   Densidad / Density: {STEEL_DENSITY} kg/m³")
    print(f"   Masa / Mass: {masa:.2f} kg")
    
    # Composición / Composition
    print("\n4. Composición de formas / Composition of shapes")
    from defect3d import CompositePart
    
    pieza = CompositePart(name="pieza_ejemplo")
    
    base = Cube(size=3.0, position=(0, 0, 0))
    base.set_color(0.5, 0.5, 0.5, 1.0)
    
    columna = Cylinder(radius=0.5, height=5.0, position=(0, 0, 2.5))
    columna.set_color(0.7, 0.3, 0.3, 1.0)
    
    pieza.add_part(base)
    pieza.add_part(columna)
    
    print(f"   Pieza compuesta / Composite part: '{pieza.name}'")
    print(f"   Número de partes / Number of parts: {len(pieza.parts)}")
    
    print("\n✅ Nivel 1 completado / Level 1 completed!")
    print("   Siguiente / Next: 02_clock_mechanisms - Crear engranajes con estas formas")
    print("                                           Create gears with these shapes")


if __name__ == "__main__":
    main()
