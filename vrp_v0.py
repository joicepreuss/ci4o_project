import random

from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from data.vrp_data import distance_matrix
from random import choices, sample
from copy import deepcopy

def get_representation(max_num_vehicles,cities, initial_city):
    """A function to create a random representation of the problem
    Args:
        num_vehicles (int): number of vehicles
        num_cities (int): number of cities
    Returns:
        matrix: a matrix representing

    """
    cities = set(cities) # convert to set to remove duplicates
    representation = []
    cities.remove(initial_city) # remove the initial city from the list - it is accounted in the fitness function
    for i in range(1,max_num_vehicles):
        selected_cities = [initial_city] + sample([i for i in cities], k= random.randint(0, len(cities))) # select random cities
        cities = [i for i in cities if i not in selected_cities] # remove selected cities from the list
        representation.append(selected_cities)
    representation.append([initial_city] + cities) # add the remaining cities to the last vehicle
    return representation


def get_fitness(self):
    """A simple objective function to calculate distances
    for the TSP problem.

    Returns:
        int: the total distance of the path
    """
    fitness = 0
    num_vehicles = len(self.representation)
    for vehicles in range(num_vehicles):
        for city in range(len(self.representation[vehicles])):
            fitness += distance_matrix[self.representation[vehicles][city - 1]][self.representation[vehicles][city]]
    return int(fitness)

#
# def get_neighbours(self):
#     """A neighbourhood function for the TSP problem. Switches
#     indexes around in pairs.
#
#     Returns:
#         list: a list of individuals
#     """
#     n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]
#
#     for count, i in enumerate(n):
#         i[count], i[count + 1] = i[count + 1], i[count]
#
#     n = [Individual(i) for i in n]
#     return n
#
#
# # Monkey patching
# Individual.get_fitness = get_fitness
# Individual.get_neighbours = get_neighbours
#
#
# pop = Population(
#     representation = get_representation(3, [i for i in range(len(distance_matrix[0]))], 0),
#     optim="min")
#
#hill_climb(pop)
#sim_annealing(pop)