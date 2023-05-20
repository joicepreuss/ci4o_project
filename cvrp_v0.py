import random
import math 

from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
# from data.vrp_data import distance_matrix
from random import choices, sample
from copy import deepcopy
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation, invertion_mutation, mutate_structure
from charles.crossover import cycle_xo, pmx
from charles.utils import flatten, unflatten, generate_random_distance_matrix
from charles.experiments import experiment

# CAPACITY CONSTRAINT VEHICLE ROUTING PROBLEM

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
    car_capacity = self.custom_representation_kwargs['car_capacity']
    demand = self.custom_representation_kwargs['demand']

    cities = list(zip(cities, demand))
    cities[initial_city] = (initial_city, 0)
    cities.remove((initial_city, 0))

    cities = set(cities) # convert to set to remove duplicates
    representation = []

    for i in range(1,max_num_vehicles):
        carried_capacity = 0    
        selected_cities = [(initial_city,0)]
        cities_to_be_visited = random.randint(0, len(cities))

        for city in range(cities_to_be_visited):
            city = random.choice(list(cities))
            if carried_capacity + city[1] <= car_capacity:
                selected_cities.append(city)
                carried_capacity += city[1]
                cities.remove(city)
        cities = [i for i in cities if i not in selected_cities] # remove selected cities from the list
        representation.append(selected_cities)
    representation.append([(initial_city,0)] + cities) # add the remaining cities to the last vehicle
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
        capacity = 0
        for city in range(len(self.representation[vehicles])):
            capacity += self.representation[vehicles][city-1][1]
            if capacity > self.custom_representation_kwargs['car_capacity']:
                fitness += 100000
            else:
                fitness += distance_matrix[self.representation[vehicles][city - 1][0]][self.representation[vehicles][city][0]]
    # print(f'Representation: {self.representation} | Fitness: {fitness}')
    return int(fitness)

# Monkey patching
Individual.get_fitness = get_fitness
Individual.custom_representation = custom_representation
# Individual.get_neighbours = get_neighbours

nb_cities = 100
distance_matrix = generate_random_distance_matrix(nb_cities)
cities = [i for i in range(len(distance_matrix))]
initial_city = 4
# we take 5% of the number of cities as the number of cars
max_cars = math.floor(nb_cities/20)
# car capacity set to 100
car_capacity = 100
# highest demand is the number of cars * car capacity divided by the number of cities
higehst_demand = math.floor((max_cars * car_capacity) / len(cities))
# Create a list of demands per city
demand = [random.randint(1, higehst_demand) for city in range(len(cities)) if city != initial_city]

print(f"NEW RUN: \nCities: {cities} \nInitial City: {initial_city} \nNumber of Cars: {max_cars} \nCar Capacity: {car_capacity}")

# pop = Population(
#     size=5,
#     sol_size=None,
#     replacement=None,
#     valid_set=None,
#     custom_representation=True,
#     custom_representation_kwargs = {
#         'cities': cities, 
#         'initial_city': initial_city, 
#         'max_num_vehicles': max_cars,
#         "car_capacity": car_capacity,
#         "demand": demand,
#         },
#     optim="min")

# pop.evolve(
#     gens=30, 
#     select=tournament_sel, 
#     crossover=pmx, 
#     xo_prob=0.95, 
#     mutate=invertion_mutation, 
#     mut_prob=0.4,
#     elitism=True,
#     flatten=flatten,
#     unflatten=unflatten,
#     mutate_structure=mutate_structure
#     )

pop_params = {
    'size': 100,
    'sol_size': None,
    'replacement': None,
    'valid_set': None,
    'custom_representation': True,
    'custom_representation_kwargs': {
        'cities': cities, 
        'initial_city': initial_city, 
        'max_num_vehicles': max_cars,
        "car_capacity": car_capacity,
        "demand": demand,
    },
    'optim': "min"
}
N = 50
stats_test = 'parametric'
gens = 100

ga_conf_1 = {
    'gens': gens,
    'select': tournament_sel,
    'crossover': pmx,
    'xo_prob': 0.95,
    'mutate': invertion_mutation,
    'mut_prob': 0.1,
    'elitism': True,
    'flatten': flatten,
    'unflatten': unflatten,
    'mutate_structure': mutate_structure
}
ga_conf_2 = {
    'gens': gens,
    'select': tournament_sel,
    'crossover': pmx,
    'xo_prob': 0.95,
    'mutate': invertion_mutation,
    'mut_prob': 0.5,
    'elitism': True,
    'flatten': flatten,
    'unflatten': unflatten,
    'mutate_structure': mutate_structure
}
ga_conf_3 = {
    'gens': gens,
    'select': tournament_sel,
    'crossover': pmx,
    'xo_prob': 0.95,
    'mutate': invertion_mutation,
    'mut_prob': 0.8,
    'elitism': True,
    'flatten': flatten,
    'unflatten': unflatten,
    'mutate_structure': mutate_structure
}
ga_conf_4 = {
    'gens': gens,
    'select': tournament_sel,
    'crossover': pmx,
    'xo_prob': 0.5,
    'mutate': invertion_mutation,
    'mut_prob': 0.5,
    'elitism': True,
    'flatten': flatten,
    'unflatten': unflatten,
    'mutate_structure': mutate_structure
}

experiment(
    pop_params,
    N,
    stats_test,
    ('ga_095xo_01mut', ga_conf_1),
    ('ga_095xo_05mut', ga_conf_2),
    ('ga_095xo_08mut', ga_conf_3),
    ('ga_05xo_05mut', ga_conf_4)
    )
