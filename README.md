# CI40 Project

Welcome! This is a repository for CI4O project ! 

| Student Number | Student Names |
|---|---|
| 20220593 | Joice Preuss | 
| 20220594 | Jaime Kuei | 
| 20220595 | Maxwell Marcos | 
| 20220630 | Jannik Kickler | 
| 20221036 | Bianca Victor |

## Contents
This repository is organanized as follows:

## How to configure the local environment for the project

 ```
python3 -m venv .ci4o-env
source .ci40-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
 ```

## What is our optimization problem? 

The project is focused to solve the vehicle routing problem. 

It's possible to see the references in this reference from google:
[Vehicle Routing Problem](https://developers.google.com/optimization/routing/vrp)

## Modelling the Problem 

## Vehicle Routing Problem

### Representation and Fitness function

As representation of the problem, each individual is created as a list of lists, in which each list represents a vehicle and the elements represent the cities to be visited by that vehicle. The first element of each vehicle list is the initial city.

Example: [[2,3],[2],[2,1,4]]

                            where:	vehicle 1 start in city 2 and goes to city 3

                                    vehicle 2 start in city 2 and stays

                                    vehicle 3 start in city 2 and goes to city 1 and 4
                                    
The TSP fitness function from class is used and modified as the fitness function, returning the total fitness of each individual by summing the single vehicle fitnesses. 
As previously mentioned, now a more detailed explanation of the functions flatten() and unflatten() is provided due to their significance. The function flatten() has two outputs, namely the flat_representation and the flat_structure. The flat_representation is a list that contains all the cities visited by all cars. The order of the cities in the list corresponds to the order in which the cars visited them. For instance, the first element of the list represents the first city visited by the first vehicle, the second element the second city visited by the first vehicle, followed by subsequent cities visited by other vehicles. On the other hand, the flat_structure is a list, where the first element represents the initial city in the representation, while the second element is a sublist that indicates the number of cities a particular vehicle is traveling. For example, in the provided example, vehicle 1 visits cities 2 and 3, resulting in a total of 2 cities that need to be passed.

Example: 

flatten([[2,3],[2],[2,1,4]]) → flat_representation [3,1,4]; flat_structure [[2, [2,1,3]]

The reason for introducing the flatten() function is that performing mutation and applying crossover operations becomes easier with the flattened form of the representation. Additionally, we employ the mutate_structure() function on the flat_structure to introduce greater variation among the newly created individuals. Finally, unflatten() reconstructs the modified representation by combining the altered flat_representation with the mutated structure.

## Capacity Constraint Vehicle Routing Problem

### Representation and Fitness function

In order to consider the capacity constraint, the representation of each individual is modified. Instead of a single value for each city, a tuple format (city, demand) is used, where demand represents the amount of capacity consumed by the vehicle. The initial city in this problem has a demand of 0. Each vehicle is assigned a predefined capacity restriction which should not be surpassed. However, if a vehicle exceeds its capacity through random selection, a penalty of 100,000 is added to the fitness of the individual. This penalty ensures that the individual will not survive during the generation of offspring. Otherwise the calculation of total distance is similar to VRP.

Example: [[(2,0),(3,1)],[(2,0)],[(2,0),(1,2),(4,3)]], 

                        where:  vehicle 1 start in city 2 with 0 load and goes to city 3 that has 1 load
                                
                                vehicle 2 start in city 2 with 0 load and stays

                                vehicle 3 start in city 2 with 0 load, goes to city 1 with 2 load  and 4 with 3 load

For the CVRP representation the functions flatten() and unflatten() work the same as described in the chapter VRP.

## How to test it? 

In order to evaluate differents configurations for the differents problems, it's possible to run the following commands:

````
python vrp.py
python cvrp.py
````

To set up a custom experiment for each problem it's possible to change the file `experiments_configuration.yaml` that receives all the parameters for each experiment to be runned in vrp.py file or cvrp.py.

In our library we have the options: 

For crossover:
- cycle_xo
- pmx

For mutation:
- swap_mutation
- invertion_mutation

For mutation structure:
- mutation_structure

## Experiments

In the experiments folder, it's possible to see the experiments that we did for the project. Each experiment is represented in a folder with the name of the experiment, and the results as a csv file and the 
plot of the statistical results as a png file.

### Statistical evaluation

The experiment consists in running the GA algorithm N times for each configuration and then storing the best fitness for each generation. 
This distributions are then used to plot the results into a line plot, comparing all the configurations. The bands for each plot represents
the 95% confidence interval for the mean of the distribution.

The last generation of each configuration is then used to perform a statistical test to evaluate the final performance of each configuration.
The statistical procedure consists on performing an ANOVA test (also have options to perform non-parametric test such as Kruskal-wallis). Since we can have more than two configurations to be compared, an F-test is
more appropriate than multiple t-tests. The ANOVA test outputs if there are any statistically significant difference in the means of all the configurations tested, but does not answer which one
is the different or how the multiple configurations are different between each other. In order to 
evaluate the pair-wise statistical tests, we can use a Tukey post-hoc test. This kind of test already corrects the pvalues due to the multiple-comparison problem (or family-wise erros) according to 
a predefined method (bonferroni, holchberg,etc...).

This post-hoc tests plots the pvalues originated from the comparisons between each pair-wise configuration comparison.
