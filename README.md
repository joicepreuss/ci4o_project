# CI40 Project

Welcome! This is a repository for CI4O project ! 

| Student Number | Student Names |
|---|---|
| 20220593 | Joice Preuss | 
| 20220594 | Jaime Kuei | 
| 20220595 | Maxwell Marcos | 
| 20220630 | Jannik Kickler | 
|  | Bianca Victor |

## Contents
This repository is organanized as follows:

## How to configure the local environment for the project

 ```
python3 -m venv .ci4o-env
source .ci40-env/bin/activate
pip install --upgrade pip
pip install requirements.txt
 ```

## What is our optimization problem? 

The project is focused to solve the vehicle routing problem. 

It's possible to see the references in this reference from google:
[Vehicle Routing Problem](https://developers.google.com/optimization/routing/vrp)


## Modelling the Problem 

For this problem we modelled our problem putting the following inputs: 

- max_cars: represents the maximum number of cars available to make a path
- cities: the cities that the cars/car need to visit
- initial_city: the initial city that the cars/car will start

Taking as example: 
- max_cars = 3
- cities = [0,1,2,3,4,5,6,7,8,9]
- initial_city = 4

Some possible representations can be: 
- Representation 1: [[4, 3, 8, 6, 7, 5, 0, 1, 2], [4], [4, 9]]
- Representation 2: [[4, 5, 8, 3, 7, 9, 2, 6, 1], [4, 0], [4]]
- Representation 3: [[4, 7, 8, 0, 9, 5], [4, 2, 3], [4, 1, 6]]
- Representation 4: [[4, 0], [4, 1, 8, 3, 6], [4, 2, 5, 7, 9]]
- Representation 5: [[4, 5], [4, 0, 3, 2, 6, 8], [4, 1, 7, 9]]

Let's take as example the Representation 4: 
- Representation 4: [[4, 0], [4, 1, 8, 3, 6], [4, 2, 5, 7, 9]]
    - This representation is saying that: 
        - car 1: will visit just the city 0 (with initial and end city as 4)
        - car 2: will visit the cities 1, 8, 3 and 6 (with initial and end city as 4)
        - car 3: will visit the cities 2, 5, 7 and 9 (with initial and end city as 4)
- For the fitness we'll calculate the distance made by the cars and then sum up all total distances. In our case the fitness is 6252

## How to test it? 

In `vrp_v0.py`, it's possible to test some parameters and GA algorithms. To do that it's just necessary to set the parameters, create a population object and evolve the population, see an example below: 

````
max_cars = 3
cities = [0,1,2,3,4,5,6,7,8,9]
initial_city = 4

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
    optim="min")

pop.evolve(
    gens=200, 
    select=tournament_sel, 
    crossover=pmx, 
    xo_prob=0.95, 
    mutate=invertion_mutation, 
    mut_prob=0.4,
    elitism=True,
    flatten=flatten,
    unflatten=unflatten
    )
````

Just remembering that for the VRP problem, it's possible to set different mutations and crossovers.

In our library we have the options: 

For crossover:
- cycle_xo
- pmx

For mutation:
- swap_mutation
- invertion_mutation
