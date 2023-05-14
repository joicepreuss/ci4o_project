import random

from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from data.vrp_data import distance_matrix
from random import choices, sample
from copy import deepcopy
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation, invertion_mutation
from charles.crossover import cycle_xo, pmx

def flatten(representation):
    # flatten the representation for vrp [[4,2,3], [4], [4,1,5,0]] -> [2,3,1,5,0], (4, [3,1,4])
    inital_city = representation[0][0]
    structure_representation = [len(car) for car in representation]
    flat_representation = [city for car in representation for idx, city in enumerate(car) if idx != 0]
    return flat_representation, [inital_city, structure_representation]

def unflatten(flat_representation, structure):
    # unflatten the representation for vrp [2,3,1,5,0], [4], [3,1,4]] -> [[4,2,3], [4], [4,1,5,0]]
    representation = []
    count = 0
    for car in structure[1]:
        representation.append([structure[0]] + flat_representation[count:count+(car-1)])
        count += car-1
    return representation

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
    # print(f'Representation: {self.representation} Fitness: {fitness}')
    return int(fitness)

# Monkey patching
Individual.get_fitness = get_fitness
Individual.custom_representation = custom_representation
# Individual.get_neighbours = get_neighbours

max_cars = 5
cities = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
initial_city = 3

pop = Population(
    size=100,
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

pop.evolve(
    gens=200, 
    select=tournament_sel, 
    crossover=pmx, 
    xo_prob=0.95, 
    mutate=invertion_mutation, 
    mut_prob=0.4,
    elitism=True,
    flatten=flatten,
    unflatten=unflatten
    )

# pop = Population(
#     representation = get_representation(3, [i for i in range(len(distance_matrix[0]))], 0),
#     optim="min")
#
#hill_climb(pop)
#sim_annealing(pop)