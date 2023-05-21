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
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = total_fitness
        # Find individual in the position of the spin
        for individual in population:
            position -= individual.fitness
            if position < spin:
                return individual
    
    else:
        raise Exception("No optimization specified (min or max).")
    

# def roulette_wheel_selection(population):
#     """Roulette wheel selection implementation.
#     https://stackoverflow.com/questions/177271/roulette-selection-in-genetic-algorithms/177278#177278
#     """

#     total_fitness = sum([i.fitness for i in population])

#     selection_probs = [individual.fitness / total_fitness for individual in population]
#     print(f"selection_probs: \n {selection_probs}")

#     cumulative_probs = [sum(selection_probs[:i+1]) for i in range(len(selection_probs))]
#     print(f"cumulative_probs: \n {cumulative_probs}")

#     # spin = uniform(0, 1)
#     spin = 0.02
#     print(f"spin: {spin}")

#     selected_index = 0
#     for i in range(len(cumulative_probs)):
#         print(f"cumulative probs: {cumulative_probs[i]} Individual: {population[i]}")
#         if cumulative_probs[i] >= spin:
#             selected_index = i
#             break
#     print(f"Picked individual: {population[selected_index]}")

#     return population[selected_index]


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
