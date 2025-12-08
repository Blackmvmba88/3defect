#!/usr/bin/env python3
"""
Ejemplo de optimización evolutiva / Evolutionary optimization example

Demuestra la optimización de un péndulo para precisión temporal.
Demonstrates optimization of a pendulum for time precision.
"""

from defect3d.clock_mechanisms import Pendulum
from defect3d.evolutionary import ClockOptimizer, EvolutionaryOptimizer


def main():
    print("=== NIVEL 7: EVOLUCIÓN / LEVEL 7: EVOLUTION ===\n")
    
    # 1. Optimización de péndulo para período de 1 segundo
    print("1. Optimizando péndulo para período de 1 segundo")
    print("   Optimizing pendulum for 1 second period\n")
    
    def create_pendulum(length, mass):
        return Pendulum(length=length, mass=mass, position=(0, 0, 2))
    
    # Estado inicial aleatorio / Random initial state
    print("   Estado inicial / Initial state:")
    initial_pendulum = Pendulum(length=1.0, mass=0.5)
    print(f"     Longitud / Length: {initial_pendulum.length:.3f} m")
    print(f"     Período / Period: {initial_pendulum.period:.4f} s")
    print(f"     Error / Error: {abs(initial_pendulum.period - 1.0)*1000:.2f} ms")
    
    # Optimizar / Optimize
    print("\n   Evolucionando / Evolving...")
    best_pendulum, fitness, history = ClockOptimizer.optimize_for_precision(
        clock_creator=create_pendulum,
        target_period=1.0,
        generations=30
    )
    
    print(f"\n   ✅ Resultado / Result:")
    print(f"     Longitud óptima / Optimal length: {best_pendulum.length:.3f} m")
    print(f"     Masa / Mass: {best_pendulum.mass:.3f} kg")
    print(f"     Período / Period: {best_pendulum.period:.4f} s")
    print(f"     Error / Error: {abs(best_pendulum.period - 1.0)*1000:.2f} ms")
    print(f"     Fitness final / Final fitness: {fitness:.6f}")
    
    # 2. Mostrar progreso evolutivo / Show evolutionary progress
    print("\n2. Progreso Evolutivo / Evolutionary Progress")
    print(f"\n   Generación | Mejor Fitness")
    print(f"   Generation | Best Fitness")
    print(f"   " + "-"*30)
    
    for gen in [0, 5, 10, 15, 20, 25, 29]:
        if gen < len(history):
            print(f"   {gen:10d} | {history[gen]:13.6f}")
    
    # Mejora / Improvement
    improvement = ((history[-1] - history[0]) / history[0]) * 100
    print(f"\n   Mejora total / Total improvement: {improvement:.2f}%")
    
    # 3. Optimización personalizada / Custom optimization
    print("\n3. Optimización Personalizada de Múltiples Parámetros")
    print("   Custom Multi-Parameter Optimization\n")
    
    def create_clock_component(length, mass, coil_stiffness):
        """Crear componente de reloj complejo / Create complex clock component"""
        from defect3d.clock_mechanisms import Spring
        pendulum = Pendulum(length=length, mass=mass)
        spring = Spring(coils=10, stiffness=coil_stiffness)
        
        # Combinar período de péndulo y resorte / Combine pendulum and spring period
        spring_period = 2 * 3.14159 * (mass / coil_stiffness) ** 0.5
        
        return {
            'pendulum': pendulum,
            'spring': spring,
            'combined_period': (pendulum.period + spring_period) / 2
        }
    
    def fitness_complex(component):
        """Fitness para sistema complejo / Fitness for complex system"""
        # Objetivo: período combinado de 1.5 segundos
        # Objective: combined period of 1.5 seconds
        target = 1.5
        error = abs(component['combined_period'] - target)
        return 1.0 / (1.0 + error)
    
    optimizer = EvolutionaryOptimizer(
        population_size=20,
        mutation_rate=0.12,
        elite_size=2
    )
    
    print("   Optimizando sistema péndulo-resorte...")
    print("   Optimizing pendulum-spring system...")
    
    best_component, best_fit, hist = optimizer.optimize(
        create_individual=create_clock_component,
        fitness_function=fitness_complex,
        parameter_ranges={
            'length': (0.5, 2.0),
            'mass': (0.2, 1.5),
            'coil_stiffness': (50, 200)
        },
        generations=30,
        verbose=False
    )
    
    print(f"\n   ✅ Sistema Óptimo / Optimal System:")
    print(f"     Longitud péndulo / Pendulum length: {best_component['pendulum'].length:.3f} m")
    print(f"     Masa / Mass: {best_component['pendulum'].mass:.3f} kg")
    print(f"     Rigidez resorte / Spring stiffness: {best_component['spring'].stiffness:.1f} N/m")
    print(f"     Período combinado / Combined period: {best_component['combined_period']:.4f} s")
    print(f"     Error / Error: {abs(best_component['combined_period'] - 1.5)*1000:.2f} ms")
    
    # 4. Comparación de estrategias / Strategy comparison
    print("\n4. Comparación de Estrategias Evolutivas")
    print("   Evolutionary Strategy Comparison\n")
    
    strategies = [
        ("Conservadora / Conservative", 0.05, 20, 4),
        ("Balanceada / Balanced", 0.12, 20, 2),
        ("Agresiva / Aggressive", 0.25, 30, 1),
    ]
    
    print(f"   Estrategia          | Fitness Final")
    print(f"   Strategy            | Final Fitness")
    print(f"   " + "-"*42)
    
    for name, mut_rate, pop_size, elite in strategies:
        opt = EvolutionaryOptimizer(
            population_size=pop_size,
            mutation_rate=mut_rate,
            elite_size=elite
        )
        
        _, fit, _ = opt.optimize(
            create_individual=create_pendulum,
            fitness_function=lambda p: 1.0 / (1.0 + abs(p.period - 1.0)),
            parameter_ranges={'length': (0.5, 2.0), 'mass': (0.2, 1.5)},
            generations=20,
            verbose=False
        )
        
        print(f"   {name:20s} | {fit:.6f}")
    
    print("\n✅ Nivel 7 completado / Level 7 completed!")
    print("   La evolución automática mejora tus diseños sin intervención manual.")
    print("   Automatic evolution improves your designs without manual intervention.")
    print("\n   'La máquina deja de ser estática, se convierte en organismo que aprende.'")
    print("   'The machine stops being static, it becomes an organism that learns.'")


if __name__ == "__main__":
    main()
