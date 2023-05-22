# CAPACITY CONSTRAINT VEHICLE ROUTING PROBLEM (CVRP)

import math
import yaml
from random import choice, sample, randint

from charles.charles import Population, Individual
from charles.utils import flatten, unflatten, generate_random_distance_matrix
from charles.crossover import cycle_xo, pmx
from charles.mutation import swap_mutation, invertion_mutation, mutate_structure
from charles.experiments import experiment, generate_experiments
from charles.selection import fps, tournament_sel


def custom_representation(self):
    """
    - Function to create a random representation of the capacity constraint vehicle routing problem;
    - Creates a list of lists where each list represents a vehicle. The elements of the list are 
    tuples in form (city, demand), which are the cities to be visited by that vehicle and the city
    demand;
    - Each city is visited by only one vehicle;
    - Each vehicle has a predefined capacity constraint, which is not allowed to be exceeded;
    - The first element of each list is the initial city with demand of 0.

    Args:
    --
        cities (list): A list of cities to be visited
        initial_city (int): The initial city from where the vehicles start
        max_num_vehicles (int): The maximum number of vehicles available
        car_capacity (int): The capacity of the vehicles
        demand (list): A list of demands per city
    
    Returns:
    --
        representation (list): List of lists where each list represents a vehicle. The elements of
        the list are tuples in form (city, demand), which are the cities to be visited by that 
        vehicle and the city demand.
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

    for _ in range(1, max_num_vehicles):
        carried_capacity = 0    
        selected_cities = [(initial_city, 0)]
        cities_to_be_visited = randint(0, len(cities))

        for city in range(cities_to_be_visited):
            city = choice(list(cities))
            if carried_capacity + city[1] <= car_capacity:
                selected_cities.append(city)
                carried_capacity += city[1]
                cities.remove(city)
        cities = [city for city in cities if city not in selected_cities]
        representation.append(selected_cities)
    representation.append([(initial_city,0)] + cities)

    return representation


def get_fitness(self):
    """
    Function to calculate distances for the CVRP problem. If the capacity of the vehicle is 
    exceeded, each iteration of exceeding adds 100000 to the fitness.

    Args:
    --
        self.representation (Individual): An individual from charles.py

    Returns:
    --
        fitness (int): The total distance
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
                fitness += distance_matrix[self.representation[
                    vehicles][city - 1][0]][self.representation[vehicles][city][0]]

    return int(fitness)

def calculate_demand(max_cars, car_capacity, cities):
    """
    - Function to calculate the demand of each city. The demand of each city is a random number
    between 10 and the highest demand possible;
    - the highest demand is the number of cars multiplied by the car capacity divided 
    by the number of cities minus the initial city.

    Args:
    --
        max_cars (int): The maximum number of vehicles available
        car_capacity (int): The capacity of the vehicles
        cities (list): A list of cities to be visited
        initial_city (int): The initial city from where the vehicles start

    Returns:
    --
        demand (list): A list of demands per city
    """

    higehst_demand = math.floor((max_cars * car_capacity) / len(cities))
    demand = [randint(10, higehst_demand) for city in range(len(cities)) if city != initial_city]

    return demand

# Monkey patching.
Individual.get_fitness = get_fitness
Individual.custom_representation = custom_representation


# reading configuration experiment file
with open('experiments_configuration.yaml') as f:
    experiments_configuration = yaml.load(f, Loader=yaml.loader.SafeLoader)


# Experiment Parameters
experimentation_name = 'cvrp_experiments'
version = 'v1'
N = 50 # number of times to run each experiment
stats_test = 'parametric' #statistical test to use

# Parameters of the CVRP Problem
nb_cities = 250
distance_matrix = generate_random_distance_matrix(nb_cities)
cities = [i for i in range(len(distance_matrix))]
initial_city = 4
max_cars = math.floor(nb_cities/20) # we take 5% of the number of cities as the number of cars
car_capacity = 100
higehst_demand = math.floor((max_cars * car_capacity) / len(cities))
demand = [randint(1, higehst_demand) for city in range(len(cities)) if city != initial_city]

# Parameter for GA experiments
gens = 100
pop_size = 100

mapping_dict = {
    'cities': cities,
    'initial_city': initial_city,
    'max_cars': max_cars,
    'car_capacity': car_capacity,
    'demand': demand,
    'stats_test': stats_test,
    'N': N,
    'pop_size': pop_size,
    'tournament_sel': tournament_sel,
    'fps': fps,
    'cycle_xo': cycle_xo,
    'pmx': pmx,
    'invertion_mutation': invertion_mutation,
    'swap_mutation': swap_mutation,
    'flatten': flatten,
    'unflatten': unflatten,
    'mutate_structure': mutate_structure,
    'gens': gens
}

generate_experiments(
    experiments_configuration, 
    experimentation_name, 
    version, 
    mapping_dict, 
    N, 
    stats_test,
    show_figure=False
    )