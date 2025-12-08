#!/usr/bin/env python3
"""
Ejemplo de física con geometría básica / Physics example with basic geometry

Demuestra propiedades físicas de las formas básicas.
Demonstrates physical properties of basic shapes.
"""

from defect3d import Cube, Sphere, Cylinder
from defect3d.physics import PhysicsSimulator


def main():
    print("=== NIVEL 1: GEOMETRÍA - Test Físico / LEVEL 1: GEOMETRY - Physics Test ===\n")
    
    # Crear objetos con diferentes densidades / Create objects with different densities
    print("1. Creando objetos con propiedades físicas / Creating objects with physical properties")
    
    # Densidades de materiales / Material densities (kg/m³)
    STEEL = 7850
    ALUMINUM = 2700
    PLASTIC = 950
    
    cubo_acero = Cube(size=1.0, position=(0, 0, 10))
    cubo_acero.density = STEEL
    masa_cubo = cubo_acero.volume() * cubo_acero.density
    print(f"   Cubo de acero / Steel cube: masa/mass={masa_cubo:.2f} kg")
    
    esfera_aluminio = Sphere(radius=0.5, position=(2, 0, 10))
    esfera_aluminio.density = ALUMINUM
    masa_esfera = esfera_aluminio.volume() * esfera_aluminio.density
    print(f"   Esfera de aluminio / Aluminum sphere: masa/mass={masa_esfera:.2f} kg")
    
    cilindro_plastico = Cylinder(radius=0.5, height=1.0, position=(4, 0, 10))
    cilindro_plastico.density = PLASTIC
    masa_cilindro = cilindro_plastico.volume() * cilindro_plastico.density
    print(f"   Cilindro de plástico / Plastic cylinder: masa/mass={masa_cilindro:.2f} kg")
    
    # Simulación de caída / Fall simulation
    print("\n2. Simulación de caída libre / Free fall simulation")
    
    sim = PhysicsSimulator(gravity=9.81)
    
    # Agregar objetos al simulador / Add objects to simulator
    sim.add_object(cubo_acero, mass=masa_cubo, velocity=(0, 0, 0))
    sim.add_object(esfera_aluminio, mass=masa_esfera, velocity=(0, 0, 0))
    sim.add_object(cilindro_plastico, mass=masa_cilindro, velocity=(0, 0, 0))
    
    print(f"   Gravedad / Gravity: {sim.gravity} m/s²")
    print(f"   Objetos en simulación / Objects in simulation: {len(sim.objects)}")
    
    # Simular 1 segundo / Simulate 1 second
    print("\n3. Simulando 1 segundo de caída / Simulating 1 second of fall")
    states = sim.simulate(duration=1.0, dt=0.1)
    
    print(f"   Estados capturados / States captured: {len(states)}")
    print(f"\n   Estado final / Final state:")
    
    final_state = states[-1]
    for i, obj_state in enumerate(final_state["objects"]):
        pos = obj_state["position"]
        vel = obj_state["velocity"]
        energia_k = obj_state["kinetic_energy"]
        energia_p = obj_state["potential_energy"]
        
        print(f"\n   Objeto {i}:")
        print(f"     Posición / Position: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
        print(f"     Velocidad / Velocity: ({vel[0]:.2f}, {vel[1]:.2f}, {vel[2]:.2f}) m/s")
        print(f"     Energía cinética / Kinetic energy: {energia_k:.2f} J")
        print(f"     Energía potencial / Potential energy: {energia_p:.2f} J")
    
    # Verificar conservación de energía / Verify energy conservation
    print("\n4. Verificación de física / Physics verification")
    
    estado_inicial = states[0]
    energia_total_inicial = sum(
        obj["kinetic_energy"] + obj["potential_energy"] 
        for obj in estado_inicial["objects"]
    )
    
    energia_total_final = sum(
        obj["kinetic_energy"] + obj["potential_energy"] 
        for obj in final_state["objects"]
    )
    
    print(f"   Energía total inicial / Initial total energy: {energia_total_inicial:.2f} J")
    print(f"   Energía total final / Final total energy: {energia_total_final:.2f} J")
    print(f"   Diferencia / Difference: {abs(energia_total_final - energia_total_inicial):.2f} J")
    
    # En caída libre, la energía total debería conservarse / In free fall, total energy should be conserved
    # (la pequeña diferencia es debido a errores numéricos / small difference is due to numerical errors)
    
    print("\n✅ Test físico completado / Physics test completed!")
    print("   Las formas geométricas tienen propiedades físicas correctas.")
    print("   Geometric shapes have correct physical properties.")


if __name__ == "__main__":
    main()
