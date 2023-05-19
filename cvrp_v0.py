import random
import math 

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

# CAPACITY CONSTRAINT VEHICLE ROUTING PROBLEM
# https://www.upperinc.com/glossary/route-optimization/capacitated-vehicle-routing-problem-cvrp/
# https://vrpy.readthedocs.io/en/latest/vrp_variants.html

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
    print(f'Representation: {self.representation} | Fitness: {fitness}')
    return int(fitness)

# Monkey patching
Individual.get_fitness = get_fitness
Individual.custom_representation = custom_representation
# Individual.get_neighbours = get_neighbours

max_cars = 3
cities = [0,1,2,3,4,5,6,7,8]
initial_city = 4
car_capacity = 50
higehst_demand = math.floor((max_cars * car_capacity) / len(cities))
# Create a list of demands per city
demand = [random.randint(10, higehst_demand) for city in range(len(cities)) if city != initial_city]

print(f"NEW RUN: \nCities: {cities} \nInitial City: {initial_city} \nNumber of Cars: {max_cars} \nCar Capacity: {car_capacity}")

pop = Population(
    size=5,
    sol_size=None,
    replacement=None,
    valid_set=None,
    custom_representation=True,
    custom_representation_kwargs = {
        'cities': cities, 
        'initial_city': initial_city, 
        'max_num_vehicles': max_cars,
        "car_capacity": car_capacity,
        "demand": demand,
        },
    optim="min")

pop.evolve(
    gens=30, 
    select=tournament_sel, 
    crossover=pmx, 
    xo_prob=0.95, 
    mutate=invertion_mutation, 
    mut_prob=0.4,
    elitism=True,
    flatten=flatten,
    unflatten=unflatten
    )