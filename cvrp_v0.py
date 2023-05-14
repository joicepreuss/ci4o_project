import random

from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from data.vrp_data import distance_matrix
from random import choices, sample
from copy import deepcopy

# CAPACITY CONSTRAINT VEHICLE ROUTING PROBLEM
# https://www.upperinc.com/glossary/route-optimization/capacitated-vehicle-routing-problem-cvrp/
# https://vrpy.readthedocs.io/en/latest/vrp_variants.html

# We need
# vehicles with capacity 
# cities with demand

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
    cities = set(cities)
    representation = []

    cars = [(car, car_capacity) for car in range(0, max_num_vehicles)]

    for i in range(1, max_num_vehicles):
        # Select random cities
        selected_cities = [(initial_city,0)] + sample([city for city in cities], k= random.randint(0, len(cities)))

        if sum([city[1] for city in selected_cities]) > car_capacity:
            custom_representation(self)
        # Remove selected cities from the list
        cities = [city for city in cities if city not in selected_cities] 
        representation.append(selected_cities)
    # Add the remaining cities to the last vehicle
    representation.append([(initial_city,0)] + cities)
    print(f"Capacity of representation: {sum([city[1] for city in representation[0]])}")
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
            # print(self.representation[vehicles][city - 1][0], self.representation[vehicles][city][0])
            fitness += distance_matrix[self.representation[vehicles][city - 1][0]][self.representation[vehicles][city][0]]
            # print(fitness)
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
# Create a list of demands per city
demand = [random.randint(10,20) for city in range(len(cities)) if city != initial_city]

pop = Population(
    size=25,
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

print(pop.__repr__)

# pop = Population(
#     representation = get_representation(3, [i for i in range(len(distance_matrix[0]))], 0),
#     optim="min")
#
#hill_climb(pop)
#sim_annealing(pop)