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
    Mutate the structure of the representation
    """
    #[[4,2,3], [4], [4,1,5,0]] -> [2,3,1,5,0], [4, [3,1,4]]
    #[[4,2,3], [4], [4,1,5,0]] -> [2,3,1,5,0], [4, [3,1,4,2]]

    structure_path = structure[1]
    # Max value of the structure. It is the sum of the elements minus the number of elements plus 1.
    max_value = sum(structure_path) - len(structure_path) + 1
    # new structure path which not exceed the max value and not less than 1 and random numbers of elements
    new_structure_path = [0] * len(structure_path)
    for element in range(len(structure_path)):
        if element < len(new_structure_path)-1:
            new_structure_path[element] = randint(1, max_value)
            max_value = sum(structure_path) - sum(new_structure_path) - (len(structure_path) - (element + 1) - 1)
        else:
            new_structure_path[element] = sum(structure_path) - sum(new_structure_path)
    
    return [structure[0], new_structure_path]


if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6]
    # test = binary_mutation(test)
    test = swap_mutation(test)

