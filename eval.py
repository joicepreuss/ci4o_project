import pandas as pd
import os

# get name of folders inside the folder results
folders = [experiment for experiment in os.listdir('results') if 'vrp_experiments' in experiment]
print('Folders: ', folders)

name_problems = [experiment.split('_')[0] for experiment in folders]
name_experiments = [experiment.split('v1_')[-1] for experiment in folders]

print(name_problems)
print(name_experiments)

# result = pd.read_csv('results/vrp_experiments_v1_selection/vrp_experiments_v1_selection.csv')

# #filter column generation == 100, group by version, and calculate mean, median, and std
# result = result[result['generation'] == 100]

# result = result.groupby(['version']).agg({'value': ['mean', 'median', 'std']})

# print(result)


## Questions
# 1. Should we explain in more detail flatten or unflatten?
# explicar brevemente sobre flatten e unflatten: mostrar que mudamos de uma estrutura para outra
# 2. How many crossover and mutation do we need to implement? 
# crossover = 2, mutation = 3
# 3. FPS code to minimization problem, see if it's correct. 
# neeed to implement correctly
# 4. How detail should we need to write about the evaluation? Statistical theory?
# tweet about explanation of the evaluation
# 5. Is it enough have three variations for mut_prob and cross_prob?
# yes

