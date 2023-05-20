# VEHICLE ROUTING PROBLEM (VRP)

from random import sample, randint

from data.vrp_data import distance_matrix

from charles.crossover import cycle_xo, pmx
from charles.utils import flatten, unflatten
from charles.selection import fps, tournament_sel
from charles.charles import Population, Individual
from charles.mutation import swap_mutation, invertion_mutation, mutate_structure


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

# Define the parameters to create the population.
max_cars = 5
cities = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
initial_city = 3

# Create the population.
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
                optim="min"
                )

# Evolve the population.
pop.evolve(
            gens=200, 
            select=tournament_sel, 
            crossover=pmx, 
            xo_prob=0.95, 
            mutate=invertion_mutation, 
            mut_prob=0.4,
            elitism=False,
            flatten=flatten,
            unflatten=unflatten,
            mutate_structure=mutate_structure
            )