import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np

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

def generate_random_distance_matrix(n):
    matrix = np.random.randint(1, 1001, size=(n, n))
    symmetric_matrix = (matrix + matrix.T) / 2
    np.fill_diagonal(symmetric_matrix, 0)
    return symmetric_matrix.tolist()