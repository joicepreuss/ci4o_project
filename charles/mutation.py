from random import randint, sample


def binary_mutation(individual):
    """Binary mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """
    mut_index = randint(0, len(individual) - 1)

    if individual[mut_index] == 0:
        individual[mut_index] = 1
    elif individual[mut_index] == 1:
        individual[mut_index] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary.")
    return individual


def swap_mutation(individual):
    """
    Swap mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """

    mut_indexes = sample(range(len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual


def invertion_mutation(individual):
    """
    Invertion mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(len(individual)), 2)
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual


def mutate_structure(structure):
    """
    Mutates the structure of the representation of the individual by randomly 
    changing the number of elements of the representation.

    Args:
    --
        structure (list): A list with the structure of the representation.

    Returns:
    --
        new_structure (list): A list with the initial city and new structure of 
        the representation.
    """

    structure_path = structure[1]

    # We add here plus 1, because each car always visits the initial city.
    max_value = sum(structure_path) - len(structure_path) + 1

    new_structure_path = [0] * len(structure_path)
    for element in range(len(structure_path)):
        # Creates for each element expect the last one a random number between 1 and max_value.
        # Reduces the max_value by the number of elements left to be created.
        if element < len(new_structure_path) - 1:
            new_structure_path[element] = randint(1, max_value)
            max_value = sum(structure_path) - sum(new_structure_path) - (
                len(structure_path) - (element + 1) - 1)
        else:
            # The last element is the subtraction of the sum of the other elements from the 
            # total number of cities.
            new_structure_path[element] = sum(structure_path) - sum(new_structure_path)
    new_structure = [structure[0], new_structure_path]

    return new_structure