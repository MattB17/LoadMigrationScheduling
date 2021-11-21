"""This module contains a collection of functions to help with high level
analysis of results.

"""
import os
import numpy as np
import pandas as pd
from timeit import default_timer as timer
from MigrationScheduling.Model import Optimizer
from MigrationScheduling import algorithms, specs


def build_heuristics_string(instance_data):
    """Builds the heuristics string for `instance_data`.

    The heuristics string is a space separated string containing the results
    of running the heuristic algorithms on `instance_data`.

    Parameters
    ----------
    instance_data: InstanceData
        An `InstanceData` object specifying an instance of the load migration
        scheduling problem.

    Returns
    -------
    str
        The heuristics string for `instance_data`.

    """
    start = timer()
    vff = algorithms.vector_first_fit(instance_data)
    vff_time = timer() - start

    start = timer()
    cbf = algorithms.current_bottleneck_first(
        instance_data, specs.CBF_CHOICES)
    cbf_time = timer() - start

    return "{0} {1} {2} {3}".format(vff, vff_time, cbf, cbf_time)


def build_optimal_string(optimizer):
    """Builds the optimal string from the optimizer.

    The optimal string is a space-separated string reporting the optimal
    result and time taken by the optimizer to find the optimal solution.

    Parameters
    ----------
    optimizer: Optimizer
        An `Optimizer` object used to find the optimal solution for an
        instance of the load migration scheduling problem.

    Returns
    -------
    str
        The optimal string obtained from the optimizer.

    """
    start = timer()
    try:
        opt = int(optimizer.build_ip_model(verbose=False)) + 1
    except:
        opt = np.nan
    opt_time = timer() - start

    return "{0} {1}".format(opt, opt_time)


def build_results_string(input_dir, instance_file, run_optimizer):
    """Builds the results string for the instance given in `instance_file`.

    The results string is a space separated string specifying the size of the
    instance being solved followed by the results and time used to compute
    each result.

    Parameters
    ----------
    input_dir: str
        A string specifying the name of the directory from which the
        instance will be read.
    instance_file: str
        A string specifying the name of the file containing the instance.
    run_optimizer: bool
        A bool specifying whether the optimizer will be run to find the
        optimal solution of the instance. Otherwise, just the heuristic
        algorithms are run.

    Returns
    -------
    str
        A string representing the results for `instance_file`.

    """
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(input_dir, instance_file))
    results_str = "{0} {1}".format(
        optimizer.get_size_string(),
        build_heuristics_string(optimizer.instance_data()))
    if run_optimizer:
        results_str = "{0} {1}".format(
            results_str, build_optimal_string(optimizer))
    return results_str + "\n"


def load_results_df(results_file, sort_col):
    """Loads a results dataframe from `results_file`.

    The results dataframe contains the results of solving load migration
    scheduling instances and is sorted according to `sort_col`.

    Parameters
    ----------
    results_file: str
        A string representing the location of the file containing the results.
    sort_col: str
        A string representing the name of the column by which the results
        will be sorted.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the results loaded from `results_file`.

    """
    results_df = pd.read_csv(results_file, sep=' ')
    results_df = results_df.sort_values(by=[sort_col]).reset_index(drop=True)
    return results_df

def get_time_df(results_df, group_col, time_cols):
    """Generates a time dataframe from `results_df`.

    A dataframe is created from `results_df` when restricted to `time_cols`
    and grouping by `group_col`, where the values are averages per distinct
    value of `group_col`.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas dataframe of experimental results which is used to create
        the time dataframe.
    group_col: str
        A string representing the column to group by when creating the time
        dataframe.
    time_cols: list
        A list of strings representing the names of the columns of the time
        variables from `results_df` to be included in the time dataframe.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame representing the time dataframe generated from
        `results_df`.

    """
    return results_df[[group_col] + time_cols].groupby(group_col).mean()
