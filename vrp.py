# VEHICLE ROUTING PROBLEM (VRP)

from random import sample, randint

from charles.charles import Population, Individual
from charles.utils import flatten, unflatten, generate_random_distance_matrix
from charles.crossover import cycle_xo, pmx
from charles.mutation import swap_mutation, invertion_mutation, mutate_structure
from charles.experiments import experiment
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

nb_cities = 100
distance_matrix = generate_random_distance_matrix(nb_cities)
max_cars = 5
cities = [i for i in range(len(distance_matrix))]
initial_city = 4

# pop = Population(
#     size=100,
#     sol_size=None,
#     replacement=None,
#     valid_set=None,
#     custom_representation=True,
#     custom_representation_kwargs = {
#         'cities': cities, 
#         'initial_city': initial_city, 
#         'max_num_vehicles': max_cars
#     },
#     optim="min"
#     )

# pop.evolve(
#     gens=200, 
#     select=tournament_sel, 
#     crossover=pmx, 
#     xo_prob=0.95, 
#     mutate=invertion_mutation, 
#     mut_prob=0.4,
#     elitism=False,
#     flatten=flatten,
#     unflatten=unflatten,
#     mutate_structure=mutate_structure
#     )

pop_params = {
    'size': 25,
    'sol_size': None,
    'replacement': None,
    'valid_set': None,
    'custom_representation': True,
    'custom_representation_kwargs': {
        'cities': cities,
        'initial_city': initial_city,
        'max_num_vehicles': max_cars
    },
    'optim': "min"
}
N = 25
stats_test = 'parametric'
gens = 10

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
    'vrp_test_mutation_probability_experiment',
    pop_params,
    N,
    stats_test,
    ('ga_095xo_01mut', ga_conf_1),
    ('ga_095xo_05mut', ga_conf_2),
    ('ga_095xo_08mut', ga_conf_3),
    ('ga_05xo_05mut', ga_conf_4)
    )
