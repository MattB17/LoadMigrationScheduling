"""This module contains a collection of functions to help with high level
analysis of results.

"""
import os
import numpy as np
import pandas as pd
import multiprocessing as mp
from timeit import default_timer as timer
from MigrationScheduling.Data import Simulator
from MigrationScheduling.Model import Optimizer
from MigrationScheduling import algorithms, specs, utils


def get_cores_and_instances_per_core(instance_count):
    """Gets the number of cores to use and the number of instances per core.

    The number of cores to use is based on the system and `instance_count`.
    Then, based on the number of cores, the number of instances per core is
    calculated using `instance_count`.

    Parameters
    ----------
    instance_count: int
        A count of the number of instances to be analyzed.

    Returns
    -------
    int, int
        Two integers. The first represents the number of cores to be used and
        the second represents the number of instances that will be analyzed
        on each core.

    """
    core_count = min(instance_count, mp.cpu_count() - 1)
    instances_per_core = int(np.ceil(instance_count / core_count))
    return core_count, instances_per_core


def get_instances_for_core(instance_files, instances_per_core, core_num):
    """Gets the instances from `instance_files` to be analyzed on `core_num`.

    A subset of `instance_files` is taken so that `core_num` processes roughly
    `instances_per_core` instances.

    Parameters
    ----------
    instance_files: list
        A list of strings representing the filenames of the instances to be
        analyzed.
    instances_per_core: int
        An integer representing the number of instances to be processed on
        each machine core.
    core_num: int
        An integer representing the core number for which the instances are
        retrieved.

    Returns
    -------
    list
        A subset of `instance_files` representing the instances to be
        processed on `core_num`.

    """
    start = instances_per_core * core_num
    end = min(len(instance_files), instances_per_core * (core_num + 1))
    return instance_files[start:end]


def initialize_and_join_processes(procs):
    """Initializes and joins all the processes in `procs`.

    Parameters
    ----------
    procs
        A list of `mp.Process` objects representing the processes to be
        initialized and joined.

    Returns
    -------
    None

    """
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()


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


def get_results_for_instances(results_list, instance_files,
                              input_dir, run_optimizer):
    """Gets results for all the instances specified in `instance_files`.

    For each instance in `instance_files` the result string is computed and
    appended to `results_list`.

    Parameters
    ----------
    results_list: mp.Manager().list
        A multiprocessing list to which the result strings are appended.
    instance_files: list
        A list of strings representing the names of files specifying the
        instances to be analyzed.
    input_dir: str
        A string specifying the directory from which the instances are read.
    run_optimizer: bool
        A boolean value indicating whether the ILP model will be solved and
        included in the result string for each instance.

    Returns
    -------
    None

    """
    for instance_file in instance_files:
        results_list.append(build_results_string(
            input_dir, instance_file, run_optimizer))

def write_results_to_file(results_list, output_file, run_optimizer):
    """Write the results in `results_list` to `output_file`.

    Parameters
    ----------
    results_list: list
        A list of strings representing the result strings for the instances
        that have been analyzed.
    output_file: str
        A string representing the name of the file to which the results will
        be written.
    run_optimizer: bool
        A boolean value indicating whether the ILP model is solved and
        included in the results of `results_list`.

    Returns
    -------
    None

    """
    with open(output_file, 'w') as results_file:
        results_file.write(utils.get_results_header(run_optimizer))
        results_file.writelines(results_list)


def calculate_results_for_instances(input_dir, instance_files,
                                    output_file, run_optimizer):
    """Calculates the results for each instance in `instance_files`.

    For each instance in `instance_files`, the instance is solved with the
    vector first fit and current bottleneck first algorithms. If
    `run_optimizer` is True, then the ILP model is also solved directly. A
    string is generated of the results and the results of all instances are
    written to `output_file` with 1 result per line.

    Parameters
    ----------
    input_dir: str
        A string representing the name of the directory from which the
        instance files are read.
    instance_files: list
        A list of strings representing the names of the files specifying the
        instances for which the results are calculated.
    output_file: str
        A string representing the name of the file to which the results will
        be written.
    run_optimizer: bool
        A boolean value indicating whether the ILP model will be solved
        directly so that the optimal solution can be included in the results
        for each instance.

    Returns
    -------
    None

    """
    results = mp.Manager().list()
    procs = []
    cores, instances_per_core = get_cores_and_instances_per_core(
        len(instance_files))
    for core_num in range(cores):
        instances = get_instances_for_core(
            instance_files, instances_per_core, core_num)
        procs.append(mp.Process(target=get_results_for_instances,
                                args=(results, instances,
                                      input_dir, run_optimizer)))
    initialize_and_join_processes(procs)
    write_results_to_file(list(results), output_file, run_optimizer)


def get_sim_tuples_for_core(instance_sizes, sims_per_core,
                            core_num, start_idx):
    """Gets the simulation tuples to be simulated on `core_num`.

    The simulation tuples identify the instance number and instance size
    taken from `instance_sizes` to be simulated on `core_num`. Roughly
    `sims_per_core` instances will be simulated on the core.

    Parameters
    ----------
    instance_sizes: list
        A list of integers representing the number of migrations in each
        simulated instance.
    sims_per_core: int
        An integer representing the number of simulations to be completed
        on each machine core.
    core_num: int
        An integer representing the index of the core for which the
        simulation tuples are retrieved.
    start_idx: int
        An integer denoting the index at which to start counting for
        the instance numbers.

    Returns
    -------
    list
        A list of two element tuples representing the simulation tuples for
        `core_num`. The first element of each tuple is an integer identifying
        the instance number and the second is an integer representing the
        number of migrations in the instance.

    """
    start = sims_per_core * core_num
    end = min(len(instance_sizes), sims_per_core * (core_num + 1))
    return [(start_idx + i, instance_sizes[i]) for i in range(start, end)]


def simulate_instance(instance_idx, instance_size, output_dir):
    """Simulates `instance_idx` having `instance_size` migrations.

    An instance is simulated and written to `output_dir`. The instance number
    is `instance_idx` and it has `instance_size` migrations.

    Parameters
    ----------
    instance_idx: int
        An integer representing the index of the instance being simulated.
    instance_size: int
        An integer representing the number of migrations in the simulated
        instance.
    output_dir: str
        A string identifying the directory to which the instance file will be
        written.

    Returns
    -------
    None

    """
    output_file = os.path.join(
        output_dir, "migrations{}.txt".format(instance_idx))
    simulator = Simulator()
    simulator.run(instance_size, output_file)


def simulate_all_instances(sim_tuples, output_dir):
    """An instance is simulated for each instance specified in `sim_tuples`.

    Parameters
    ----------
    sim_tuples: list
        A list of two element tuples specifying the parameters of each
        instance to be simulated. Both elements of each tuples are integers
        specifying the index of the instance and the number of migrations.
    output_dir: str
        A string specifying the directory to which the instance will be output.

    Returns
    -------
    None

    """
    for sim_tuple in sim_tuples:
        simulate_instance(sim_tuple[0], sim_tuple[1], output_dir)


def create_simulated_instances(instance_sizes, start_idx, output_dir):
    """Simulates instances of the sizes specified in `instance_sizes`.

    An instance is simulated for each element of `instance_sizes` where
    the number of migrations of the instance is equal to the corresponding
    element of `instance_sizes`. The instances are numbered contiguously
    starting from `start_idx` and written to `output_dir`.

    Parameters
    ----------
    instance_sizes: list
        A list of integers representing the number of migrations in each
        simulated instance.
    start_idx: int
        An integer denoting the instance number from which instances are
        numbered.
    output_dir: str
        A string specifying the directory to which the instance files will
        be written.

    Returns
    -------
    None

    """
    procs = []
    cores, sims_per_core = get_cores_and_instances_per_core(
        len(instance_sizes))
    for core_num in range(cores):
        sim_tuples = get_sim_tuples_for_core(
            instance_sizes, sims_per_core, core_num, start_idx)
        procs.append(mp.Process(target=simulate_all_instances,
                                args=(sim_tuples, output_dir)))
    initialize_and_join_processes(procs)


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
