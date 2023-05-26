import numpy as np

def flatten(representation):
    """
    Function to flatten the representation to be able to apply the crossover and 
    mutation operators. It transform a list of lists in a list of cities and 
    creates another list with the structure of the representation, formed by 
    first element as the initial city and the second element as a list with the 
    number of cities to be visited by each vehicle.

    Args:
    --
        representation (Individual): An individual from charles.py

    Returns:
    --
        flat_representation (list): A list with the representation flattened.
        flat_structure (list): A list with the structure of the representation. 
        First element is the initial city and the second element is a list with 
        the number of cities to be visited by each vehicle. 
    """

    inital_city = representation[0][0]
    structure_representation = [len(car) for car in representation]
    flat_representation = [city for car in representation for idx, city in enumerate(car) if idx != 0]
    flat_structure = [inital_city, structure_representation]

    return flat_representation, flat_structure

def unflatten(flat_representation, structure):
    """
    Function to unflatten the representation to be able to create the new individuals.
    Args:
    --
        flat_representation (list): A list with the representation flattened.
        structure (list): A list with the structure of the representation.
        
    Returns:
    --
    representation (list): A list with the representation unflattened.
    """

    representation = []
    count = 0
    for car in structure[1]:
        representation.append([structure[0]] + flat_representation[count:count+(car-1)])
        count += car-1
    
    return representation

def generate_random_distance_matrix(n):
    """
    Function to generate a random distance matrix.
    
    Args:
    --
        n (int): The size of the distance matrix.

    Returns:
    --
        symmetric_matrix (list): A list with the distance matrix.
    """

    matrix = np.random.randint(1, 1001, size=(n, n))
    symmetric_matrix = (matrix + matrix.T) / 2
    np.fill_diagonal(symmetric_matrix, 0)

    return symmetric_matrix.tolist()