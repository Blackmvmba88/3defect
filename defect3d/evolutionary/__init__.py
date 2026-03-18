"""
Diseño evolutivo / Evolutionary Design

Optimización automática de sistemas mecánicos mediante algoritmos evolutivos.
Automatic optimization of mechanical systems using evolutionary algorithms.
"""

import random
import copy
from typing import List, Callable, Any, Dict


class EvolutionaryOptimizer:
    """
    Optimizador evolutivo / Evolutionary optimizer

    Mejora automáticamente diseños mediante evolución simulada.
    Automatically improves designs through simulated evolution.
    """

    def __init__(self,
                 population_size=20,
                 mutation_rate=0.1,
                 elite_size=2):
        """
        Inicializar optimizador / Initialize optimizer

        Args:
            population_size: Tamaño de la población / Population size
            mutation_rate: Tasa de mutación (0-1) / Mutation rate (0-1)
            elite_size: Individuos élite a preservar / Elite individuals to preserve
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.generation = 0
        self.best_fitness_history = []

    def optimize(self,
                 create_individual: Callable,
                 fitness_function: Callable,
                 parameter_ranges: Dict[str, tuple],
                 generations=50,
                 verbose=True) -> tuple:
        """
        Ejecutar optimización evolutiva / Run evolutionary optimization

        Args:
            create_individual: Función que crea un individuo / Function that creates an individual
            fitness_function: Función de aptitud / Fitness function
            parameter_ranges: Rangos de parámetros {nombre: (min, max)}
            generations: Número de generaciones / Number of generations
            verbose: Mostrar progreso / Show progress

        Returns:
            (mejor_individuo, mejor_fitness, historial)
            (best_individual, best_fitness, history)
        """
        # Crear población inicial / Create initial population
        population = self._create_initial_population(
            create_individual, parameter_ranges
        )

        best_individual = None
        best_fitness = float('-inf')

        for gen in range(generations):
            self.generation = gen

            # Evaluar aptitud / Evaluate fitness
            fitness_scores = [
                fitness_function(individual)
                for individual in population
            ]

            # Encontrar mejor / Find best
            max_fitness = max(fitness_scores)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_idx = fitness_scores.index(max_fitness)
                best_individual = copy.deepcopy(population[best_idx])

            self.best_fitness_history.append(best_fitness)

            if verbose and gen % 10 == 0:
                avg_fitness = sum(fitness_scores) / len(fitness_scores)
                print(f"Generación {gen}: mejor={best_fitness:.4f}, "
                      f"promedio={avg_fitness:.4f}")

            # Selección y reproducción / Selection and reproduction
            population = self._evolve_population(
                population, fitness_scores, parameter_ranges
            )

        if verbose:
            print(f"\n✅ Optimización completa / Optimization complete")
            print(f"   Mejor fitness / Best fitness: {best_fitness:.4f}")

        return best_individual, best_fitness, self.best_fitness_history

    def _create_initial_population(self, create_fn, param_ranges):
        """Crear población inicial aleatoria / Create random initial population"""
        population = []
        for _ in range(self.population_size):
            # Parámetros aleatorios / Random parameters
            params = {}
            for param_name, (min_val, max_val) in param_ranges.items():
                params[param_name] = random.uniform(min_val, max_val)

            individual = create_fn(**params)
            population.append(individual)

        return population

    def _evolve_population(self, population, fitness_scores, param_ranges):
        """Evolucionar población / Evolve population"""
        # Ordenar por fitness / Sort by fitness
        sorted_pop = [x for _, x in sorted(
            zip(fitness_scores, population),
            key=lambda pair: pair[0],
            reverse=True
        )]

        # Preservar élite / Preserve elite
        new_population = sorted_pop[:self.elite_size]

        # Reproducción / Reproduction
        while len(new_population) < self.population_size:
            # Selección por torneo / Tournament selection
            parent1 = self._tournament_select(population, fitness_scores)
            parent2 = self._tournament_select(population, fitness_scores)

            # Cruzamiento / Crossover
            child = self._crossover(parent1, parent2)

            # Mutación / Mutation
            if random.random() < self.mutation_rate:
                child = self._mutate(child, param_ranges)

            new_population.append(child)

        return new_population[:self.population_size]

    def _tournament_select(self, population, fitness_scores, tournament_size=3):
        """Selección por torneo / Tournament selection"""
        tournament = random.sample(list(zip(population, fitness_scores)),
                                  min(tournament_size, len(population)))
        winner = max(tournament, key=lambda x: x[1])
        return winner[0]

    def _crossover(self, parent1, parent2):
        """Cruzamiento de dos padres / Crossover two parents"""
        # Cruzamiento simple: copiar padre 1 y mezclar algunos atributos
        # Simple crossover: copy parent 1 and mix some attributes
        child = copy.deepcopy(parent1)

        # Mezclar atributos numéricos / Mix numerical attributes
        for attr in dir(parent1):
            if not attr.startswith('_') and hasattr(parent2, attr):
                val1 = getattr(parent1, attr)
                val2 = getattr(parent2, attr)

                if isinstance(val1, (int, float)):
                    # Promedio con variación / Average with variation
                    new_val = (val1 + val2) / 2.0
                    setattr(child, attr, new_val)

        return child

    def _mutate(self, individual, param_ranges):
        """Mutar un individuo / Mutate an individual"""
        mutated = copy.deepcopy(individual)

        # Mutar un parámetro aleatorio / Mutate a random parameter
        if param_ranges:
            param_name = random.choice(list(param_ranges.keys()))
            min_val, max_val = param_ranges[param_name]

            if hasattr(mutated, param_name):
                current_val = getattr(mutated, param_name)
                # Mutación gaussiana / Gaussian mutation
                mutation_amount = random.gauss(0, (max_val - min_val) * 0.1)
                new_val = current_val + mutation_amount
                new_val = max(min_val, min(max_val, new_val))  # Clamp
                setattr(mutated, param_name, new_val)

        return mutated


class ClockOptimizer:
    """Optimizador especializado para relojes / Specialized optimizer for clocks"""

    @staticmethod
    def optimize_for_precision(clock_creator, target_period=1.0, generations=30):
        """
        Optimizar reloj para precisión / Optimize clock for precision

        Args:
            clock_creator: Función que crea el reloj / Function that creates the clock
            target_period: Período objetivo en segundos / Target period in seconds
            generations: Generaciones a evolucionar / Generations to evolve
        """
        def fitness(pendulum):
            # Mejor fitness = más cerca del período objetivo
            # Better fitness = closer to target period
            error = abs(pendulum.period - target_period)
            return 1.0 / (1.0 + error)  # Invertir error / Invert error

        optimizer = EvolutionaryOptimizer(population_size=20, mutation_rate=0.15)

        param_ranges = {
            'length': (0.5, 2.0),
            'mass': (0.1, 2.0)
        }

        best, fitness_val, history = optimizer.optimize(
            create_individual=clock_creator,
            fitness_function=fitness,
            parameter_ranges=param_ranges,
            generations=generations,
            verbose=True
        )

        return best, fitness_val, history


class EngineOptimizer:
    """Optimizador especializado para motores / Specialized optimizer for engines"""

    @staticmethod
    def optimize_for_efficiency(engine_creator, generations=30):
        """
        Optimizar motor para eficiencia / Optimize engine for efficiency

        Args:
            engine_creator: Función que crea el motor / Function that creates engine
            generations: Generaciones / Generations
        """
        def fitness(engine):
            # Fitness basado en cilindros (más = más potencia pero menos eficiencia)
            # Fitness based on cylinders (more = more power but less efficiency)
            # Buscamos balance / We seek balance
            power_score = engine.cylinders * 50  # HP aproximado / Approximate HP
            efficiency_penalty = engine.cylinders * 0.1
            return power_score / (1.0 + efficiency_penalty)

        optimizer = EvolutionaryOptimizer(population_size=15, mutation_rate=0.2)

        param_ranges = {
            'cylinders': (2, 12)
        }

        # Nota: engine_creator debe manejar cylinders como parámetro
        # Note: engine_creator must handle cylinders as parameter

        return optimizer


class VehicleOptimizer:
    """Optimizador especializado para vehículos / Specialized optimizer for vehicles"""

    @staticmethod
    def optimize_for_stability(vehicle_creator, generations=30):
        """
        Optimizar vehículo para estabilidad / Optimize vehicle for stability

        Args:
            vehicle_creator: Función que crea el vehículo / Function creating vehicle
            generations: Generaciones / Generations
        """
        def fitness(vehicle):
            # Estabilidad basada en dimensiones / Stability based on dimensions
            # Relación ancho/largo ideal / Ideal width/length ratio
            specs = vehicle.get_specifications()
            dims = specs.get('dimensions', specs.get('dimensiones', {}))

            length = dims.get('length', dims.get('longitud', 4.5))
            width = dims.get('width', dims.get('ancho', 1.8))

            # Centro de masa bajo = más estable / Low center of mass = more stable
            ratio = width / length
            ideal_ratio = 0.4  # Aproximadamente / Approximately

            error = abs(ratio - ideal_ratio)
            return 1.0 / (1.0 + error * 10)

        optimizer = EvolutionaryOptimizer(population_size=20, mutation_rate=0.15)

        return optimizer


__all__ = [
    'EvolutionaryOptimizer',
    'ClockOptimizer',
    'EngineOptimizer',
    'VehicleOptimizer'
]
