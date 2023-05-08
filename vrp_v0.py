import random

from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from data.vrp_data import distance_matrix
from random import choices, sample
from copy import deepcopy

def custom_representation(self):
    """A function to create a random representation of the problem
    Args:
        num_vehicles (int): number of vehicles
        num_cities (int): number of cities
    Returns:
        matrix: a matrix representing

    """
    cities = self.custom_representation_kwargs['cities']
    initial_city = self.custom_representation_kwargs['initial_city']
    max_num_vehicles = self.custom_representation_kwargs['max_num_vehicles']

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
    print(f'Representation: {self.representation} Fitness: {fitness}')
    return int(fitness)

# Monkey patching
Individual.get_fitness = get_fitness
Individual.custom_representation = custom_representation
# Individual.get_neighbours = get_neighbours

max_cars = 3
cities = [0,1,2,3,4,5,6,7,8]
initial_city = 4

pop = Population(
    size=25,
    sol_size=None,
    replacement=None,
    valid_set=None,
    custom_representation=True,
    custom_representation_kwargs = {
        'cities': cities, 
        'initial_city': initial_city, 
        'max_num_vehicles': max_cars
    },
    optim="min")

print(pop.__repr__)

# pop = Population(
#     representation = get_representation(3, [i for i in range(len(distance_matrix[0]))], 0),
#     optim="min")
#
#hill_climb(pop)
#sim_annealing(pop)