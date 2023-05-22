# VEHICLE ROUTING PROBLEM (VRP)

from random import sample, randint
import yaml
import math

from charles.charles import Population, Individual
from charles.utils import flatten, unflatten, generate_random_distance_matrix
from charles.crossover import cycle_xo, pmx
from charles.mutation import swap_mutation, invertion_mutation, mutate_structure
from charles.experiments import generate_experiments
from charles.selection import fps, tournament_sel


def custom_representation(self):
    """
    - Function to create a random representation of the vehicle routing problem;
    - Creates a list of lists where each list represents a vehicle and the 
    elements of the list are the cities to be visited by that vehicle; 
    - The first element of each list is the initial city;
    - Each city is visited by only one vehicle.

    Args:
    --
        cities (list): A list of cities to be visited
        initial_city (int): The initial city from where the vehicles start
        max_num_vehicles (int): The maximum number of vehicles available
    
    Returns:
    --
        representation (list): A list of lists where each list represents 
        a vehicle and the elements of the list are the cities to be visited
    """

    cities = self.custom_representation_kwargs['cities']
    initial_city = self.custom_representation_kwargs['initial_city']
    max_num_vehicles = self.custom_representation_kwargs['max_num_vehicles']

    cities = set(cities)
    representation = []
    cities.remove(initial_city)

    for _ in range(1,max_num_vehicles):
        selected_cities = [initial_city] + sample([city for city in cities], 
                                                  k= randint(0, len(cities)))
        cities = [city for city in cities if city not in selected_cities]
        representation.append(selected_cities)
    representation.append([initial_city] + cities)

    return representation


def get_fitness(self):
    """
    Function to calculate distances for the VRP problem.

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
        for city in range(len(self.representation[vehicles])):
            fitness += distance_matrix[
                self.representation[vehicles][city - 1]][self.representation[vehicles][city]]
   
    return int(fitness)

# Monkey patching.
Individual.get_fitness = get_fitness
Individual.custom_representation = custom_representation


# reading configuration experiment file
with open('experiments_configuration.yaml') as f:
    experiments_configuration = yaml.load(f, Loader=yaml.loader.SafeLoader)

# Experiment Parameters
experimentation_name = 'vrp_experiments'
version = 'v1'
N = 50 # number of times to run each experiment
stats_test = 'parametric' #statistical test to use

# Parameters of the VRP Problem
nb_cities = 250
distance_matrix = generate_random_distance_matrix(nb_cities)
max_cars = math.floor(nb_cities/20) # we take 5% of the number of cities as the number of cars
cities = [i for i in range(len(distance_matrix))]
initial_city = 4

# Parameter for GA experiments
pop_size = 100
gens = 100

# Mappinf of variables and functions to be parsed by the experiments
mapping_dict = {
    'cities': cities,
    'initial_city': initial_city,
    'max_cars': max_cars,
    'stats_test': stats_test,
    'pop_size': pop_size,
    'N': N,
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