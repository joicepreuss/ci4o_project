import os
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

def process_csv_file(file_path):
    df = pd.read_csv(file_path)
    df_100th_gen = df[df['generation'] == 100]
    grouped_by_version = df_100th_gen.groupby('version')['value']
    
    avg_fitness_by_version = grouped_by_version.mean()
    std_dev_by_version = grouped_by_version.std()
    conf_int_by_version = grouped_by_version.apply(lambda x: stats.t.interval(0.95, len(x)-1, loc=x.mean(), scale=stats.sem(x)))
    
    return avg_fitness_by_version, std_dev_by_version, conf_int_by_version

def main():
    results_folder = 'results'
    output_data = []

    for folder_name in os.listdir(results_folder):
        if folder_name.startswith('cvrp_experiments') or folder_name.startswith('vrp_experiments'):
            folder_path = os.path.join(results_folder, folder_name)
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    avg_fitness_by_version, std_dev_by_version, conf_int_by_version = process_csv_file(file_path)
                    print('-----------------------------------')
                    print('Experiment: ', folder_name)
                    print('-----------------------------------')
                    print('File: ', file_name)
                    print('Avg fitness by version: ', avg_fitness_by_version)
                    print('Conf int by version: ', conf_int_by_version)
                    print('-----------------------------------')

if __name__ == '__main__':
    main()