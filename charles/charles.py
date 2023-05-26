from random import shuffle, choice, sample,random
from operator import attrgetter
from copy import deepcopy

class Individual:
    def __init__(
        self,
        representation=None,
        custom_representation=False,
        custom_representation_kwargs=None,
        size=None,
        replacement=True,
        valid_set=None,
    ):
        if representation:
            self.custom_representation_kwargs = custom_representation_kwargs
            self.representation = representation
        else:
            if custom_representation == False:
                if replacement == True:
                    self.representation = [choice(valid_set) for i in range(size)]
                elif replacement == False:
                    self.representation = sample(valid_set, size)
            else:
                self.custom_representation_kwargs = custom_representation_kwargs
                self.representation = self.custom_representation()
        self.fitness = self.get_fitness()

    def custom_representation(self):
        raise Exception("You need to monkey patch the representation path.")            

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness path.")

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self,value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"

class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.is_custom_representation = kwargs["custom_representation"]
        self.custom_representation_kwargs = kwargs["custom_representation_kwargs"]
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                    custom_representation=kwargs["custom_representation"],
                    custom_representation_kwargs=kwargs["custom_representation_kwargs"]
                )
            )

    def evolve(self, gens, select, mutate, crossover, xo_prob, mut_prob, elitism, flatten=None, 
               unflatten=None, mutate_structure=None):
        """
        Evolve the population for a number of generations applying the genetic operators.

        Args:
        --
            gens (int): The number of generations to evolve.
            select (function): The selection function to be used.
            crossover (function): The crossover function to be used.
            xo_prob (float): The probability of crossover.
            mutate (function): The mutation function to be used.
            mut_prob (float): The probability of mutation.
            elitism (bool): If True the best individual will be kept safe from generation to generation.
            flatten (function): The function to flatten the representation of the individual.
            unflatten (function): The function to unflatten the representation of the individual.
            mutate_structure (function): The function to mutate the structure of the representation 
            of the individual.

        Returns:
        --
            best_individuals (list): A list with the best individuals from each generation.
        """
        
        best_individuals = []
        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == 'max':
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == 'min':
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)

                # As we have a custom representation we need to flatten the representation
                # to be able to apply the crossover and mutation operators.
                if self.is_custom_representation:
                    parent1, structure1 = flatten(parent1)
                    parent2, structure2 = flatten(parent2)

                # XO
                if random() < xo_prob:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                # Mutation
                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                # Mutation of the structure of the representation.
                if mutate_structure:
                    if random() < mut_prob:
                        structure1 = mutate_structure(structure1)
                    if random() < mut_prob:
                        structure2 = mutate_structure(structure2)

                # As we applied the mutation and crossover operators to the flattened representation
                # we need to unflatten the representation to be able to create the new individuals.
                if self.is_custom_representation:
                    offspring1 = unflatten(offspring1, structure1)
                    offspring2 = unflatten(offspring2, structure2)

                new_pop.append(
                    Individual(representation=offspring1, 
                               custom_representation=self.is_custom_representation, 
                               custom_representation_kwargs=self.custom_representation_kwargs)
                               )
                if len(new_pop) < self.size:
                    new_pop.append(
                        Individual(representation=offspring2, 
                                   custom_representation=self.is_custom_representation, 
                                   custom_representation_kwargs=self.custom_representation_kwargs)
                                   )

            if elitism:
                if self.optim == 'max':
                    worst = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == 'min':
                    worst = max(new_pop, key=attrgetter("fitness"))
                new_pop.pop(new_pop.index(worst))
                new_pop.append(elite)
            self.individuals = new_pop
            if self.optim == 'max':
                print(f'Best individual: {max(self, key=attrgetter("fitness"))}')
                best_individuals.append(max(self, key=attrgetter("fitness")))

            elif self.optim == 'min':
                print(f'Best individual: {min(self, key=attrgetter("fitness"))}')
                best_individuals.append(min(self, key=attrgetter("fitness")))
                
        return best_individuals

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
