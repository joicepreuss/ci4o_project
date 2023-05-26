from random import uniform,sample,choice
from operator import attrgetter

def fps(population):
    """
    Fitness proportionate selection implementation.

    Args:
    --
        population (Population): The population we want to select from.

    Returns:
    --
        Individual: selected individual.
    """

    if population.optim == "max":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual
    
    elif population.optim == "min":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        inverse_total_fitness = sum([total_fitness/i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, inverse_total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += total_fitness/individual.fitness
            if position > spin:
                return individual
    
    else:
        raise Exception("No optimization specified (min or max).")

def tournament_sel(population, size = 4):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): The size of the tournament.

    Returns:
        Individual: selected individual.
    """
    #tournament = sample(population.individuals, size)
    tournament = [choice(population.individuals) for i in range(size)]
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
