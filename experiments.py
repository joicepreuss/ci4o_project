import os
from charles.charles import Population, Individual
import numpy as np
import pandas as pd
import scipy.stats as stats
from statannotations.Annotator import Annotator
from scikit_posthocs import posthoc_dunn, posthoc_tukey
import seaborn as sns
import matplotlib.pyplot as plt

def perform_statistical_test(df, test_type, level, column='value'):
    """
    Perform a statistical test on a dataframe with multiple levels
    Args:
        df:
        test_type:
        level:
        column:

    Returns:

    """
    def plot_post_hoc_tests(original_df,df_post_hoc):
        # Converting to long format
        remove = np.tril(np.ones(df_post_hoc.shape), k=0).astype("bool") # removing lower diagonal
        df_post_hoc[remove] = np.nan

        molten_df = df_post_hoc.melt(ignore_index=False).reset_index().dropna()

        # Plotting
        ax_ = sns.boxplot(data=original_df, x=f"{level}", y=f"{column}", order=unique_levels)

        pairs = [(i[1]["index"], i[1]["variable"]) for i in molten_df.iterrows()]
        p_values = [i[1]["value"] for i in molten_df.iterrows()]

        annotator = Annotator(
            ax_, pairs, data=original_df, x=f"{level}", y=f"{column}", order=unique_levels
        )
        annotator.configure(text_format="star", loc="inside")
        annotator.set_pvalues_and_annotate(p_values)
        return ax_

    if test_type not in ['parametric', 'non-parametric']:
        raise ValueError("test_type must be either 'parametric' or 'non-parametric'")

    unique_levels = df[level].unique()

    if len(unique_levels) < 2:
        raise ValueError(f"Insufficient unique levels in column '{level}' for comparison")

    data_groups = [df[df[level] == lvl][column] for lvl in unique_levels]

    if test_type == 'parametric':
        f_stat, p_value = stats.f_oneway(*data_groups)
        print(f"One-way ANOVA results for general significance :\nF-statistic: {f_stat}\nP-value: {p_value}")
        # Post-hoc test
        tukey_results = posthoc_tukey(df, val_col=column, group_col=level)
        ax_ = plot_post_hoc_tests(df, tukey_results)
        ax_.set_title(f"Post-hoc Tukey test for evaluated models for last generation")
        return ax_

    else:
        h_stat, p_value = stats.kruskal(*data_groups)
        print(f"Kruskal-Wallis H-test resultsfor general significance :\nH-statistic: {h_stat}\nP-value: {p_value}")
        # Post-hoc test
        dunn_results = posthoc_dunn(df, val_col=column, group_col=level)
        ax_ = plot_post_hoc_tests(df, dunn_results)
        ax_.set_title(f"Post-hoc Dunn test for evaluated models for last generation")
        return ax_


def experiment(experiment_name,pop_params,N,stats_test, *args):
    """

    Args:
        N:
        *args: (version, GA)

    Returns:

    """
    # Create a folder for the experiment in the results folder
    results_folder = os.path.join(os.getcwd(), 'results')
    experiment_folder = os.path.join(results_folder, experiment_name)
    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)

    # Data collection
    results = {}
    for arg in args:
        version,GA_dict = arg
        runs = []
        for _ in range(N):
            pop = Population(**pop_params)
            best_individuals = pop.evolve(**GA_dict)
            best_fitness = [ind.fitness for ind in best_individuals]
            runs.append(best_fitness)
        results[version] = runs

    # Transform into a pandas dataframe
    rows = []

    for version, runs in results.items():
        for run_index, run in enumerate(runs):
            for gen,value in enumerate(run):
                rows.append({'version': version, 'run': run_index + 1, 'generation': gen + 1, 'value': value})
    results_df = pd.DataFrame(rows)
    # Store the results in a csv file
    results_df.to_csv(os.path.join(experiment_folder, f'{experiment_name}.csv'), index=False)
    # Plot the results
    f,ax = plt.subplots(2,1,figsize=(10,10))
    sns.set_theme(style="darkgrid")
    sns.lineplot(data=results_df, x="generation", y="value", hue="version",ax= ax[0])
    ax[0].set_title("Fitness evolution of all evaluated models")


    # Perform statistical test
    last_gen_df = results_df[results_df['generation'] == results_df['generation'].max()]
    ax[1] = perform_statistical_test(last_gen_df, test_type=stats_test, level='version')
    # Save the figure
    f.savefig(os.path.join(experiment_folder, f'{experiment_name}.png'))
    plt.show()




