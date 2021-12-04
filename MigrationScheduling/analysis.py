"""This module contains a collection of functions to help with high level
analysis of results.

"""
import os
import numpy as np
import pandas as pd
import multiprocessing as mp
from timeit import default_timer as timer
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


def build_results_string(input_dir, instance_file, output_idx, run_optimizer):
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
        A string specifying the name of a file containing the instance to
        be solved.
    output_idx: int
        An integer identifying the index of the instance being output.
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
    results_str = "{0} {1} {2}".format(
        output_idx, optimizer.get_size_string(),
        build_heuristics_string(optimizer.instance_data()))
    if run_optimizer:
        results_str = "{0} {1}".format(
            results_str, build_optimal_string(optimizer))
    return results_str + "\n"


def get_results_for_instances(results_list, instance_files,
                              file_pattern, input_dir):
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
    file_pattern: str
        A string representing the pattern used for the instance files.
    input_dir: str
        A string specifying the directory from which the instances are read.

    Returns
    -------
    None

    """
    for instance_file in instance_files:
        output_idx = utils.extract_file_idx(instance_file, file_pattern)
        results_list.append(build_results_string(
            input_dir, instance_file, output_idx, False))

def write_optimal_results(instance_file, input_dir, result_idx, output_dir):
    """Writes the results of solving `instance_file` optimally.

    The instance specified in `instance_file` is solved optimally and with
    the heuristic algorithms and the results are written to `output_dir`.

    Parameters
    ----------
    instance_file: str
        A string specifying the name of a file containing the instance to
        be solved.
    input_dir: str
        A string specifying the name of the directory from which the instance
        file is read.
    result_idx: int
        An integer identifying the result file to be created for the instance.
    output_dir: str
        A string identifying the directory to which the results will be
        written.

    Returns
    -------
    None

    """
    output_file = os.path.join(
        output_dir, "results{}.txt".format(result_idx))
    with open(output_file, 'w') as results_file:
        results_file.write(utils.get_results_header(True))
        results_file.write(build_results_string(
            input_dir, instance_file, result_idx, True))

def solve_instances_optimally(instance_files, input_dir,
                              file_pattern, output_dir):
    """Finds the optimal solution for each instance in `instance_files`.

    Each file in `instance_files` is read from `input_dir` and the
    corresponding instance is solved optimally and with the heuristic
    algorithms. The results are then written to `output_dir`.

    Parameters
    ----------
    instance_files: list
        A list of strings specifying the names of the instance files to be
        solved optimally.
    input_dir: str
        A string representing the name of the directory from which the
        instances are read.
    file_pattern: str
        A string identifying the pattern of the instance files.
    output_dir: str
        A string representing the name of the directory to which the results
        will be written.

    Returns
    -------
    None

    """
    for instance_file in instance_files:
        curr_idx = utils.extract_file_idx(instance_file, file_pattern)
        write_optimal_results(instance_file, input_dir, curr_idx, output_dir)


def write_results_to_file(results_list, output_file):
    """Write the results in `results_list` to `output_file`.

    Parameters
    ----------
    results_list: list
        A list of strings representing the result strings for the instances
        that have been analyzed.
    output_file: str
        A string representing the name of the file to which the results will
        be written.

    Returns
    -------
    None

    """
    with open(output_file, 'w') as results_file:
        results_file.write(utils.get_results_header(False))
        results_file.writelines(results_list)


def calculate_heuristic_results_for_instances(input_dir, file_pattern,
                                              instance_files, output_file):
    """Gets the heuristic results for each instance in `instance_files`.

    For each instance in `instance_files`, the instance is solved with the
    vector first fit and current bottleneck first algorithms. A string
    is generated of the results and the results of all instances are
    written to `output_file` with 1 result per line.

    Parameters
    ----------
    input_dir: str
        A string representing the name of the directory from which the
        instance files are read.
    file_pattern: str
        A string identifying the pattern of the instance files.
    instance_files: list
        A list of strings representing the names of the files specifying the
        instances for which the results are calculated.
    output_file: str
        A string representing the name of the file to which the results will
        be written.

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
                                      file_pattern, input_dir)))
    initialize_and_join_processes(procs)
    write_results_to_file(list(results), output_file)


def calculate_optimal_results_for_instances(input_dir, file_pattern,
                                            instance_files, output_dir):
    """Gets the optimal results for each instance in `instance_files`.

    For each instance in `instance_files`, the instance is solved optimally
    and with the vector first fit and current bottleneck first algorithms. A
    string is generated of the results and the results of all instances are
    written to `output_file` with 1 result per line.

    Parameters
    ----------
    input_dir: str
        A string representing the name of the directory from which the
        instance files are read.
    file_pattern: str
        A string identifying the pattern of the instance files.
    instance_files: list
        A list of strings representing the names of the files specifying the
        instances for which the results are calculated.
    output_file: str
        A string representing the name of the file to which the results will
        be written.

    Returns
    -------
    None

    """
    procs = []
    cores, instances_per_core = get_cores_and_instances_per_core(
        len(instance_files))
    for core_num in range(cores):
        instances = get_instances_for_core(
            instance_files, instances_per_core, core_num)
        procs.append(mp.Process(target=solve_instances_optimally,
                                args=(instances, input_dir,
                                      file_pattern, output_dir)))
    initialize_and_join_processes(procs)


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


def simulate_instance(sim_cls, sim_args, instance_idx, size, output_dir):
    """Simulates `instance_idx` having `size` migrations with `sim_cls`.

    An instance is simulated using `sim_cls` with `sim_args` as arguments
    and the result is written to `output_dir`. The instance number is
    `instance_idx` and it has `size` migrations.

    Parameters
    ----------
    sim_cls: Simulator.class
        A `Simulator` class object specifying the type of simulation being
        performed.
    sim_args: dict
        A dictionary specifying arguments for `sim_cls`. The keys are
        strings specifying the argument names and the corresponding value
        is the argument value to be passed to `sim_cls`
    instance_idx: int
        An integer representing the index of the instance being simulated.
    size: int
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
    simulator = sim_cls(**sim_args)
    simulator.run(size, output_file)


def simulate_all_instances(sim_cls, sim_args, sim_tuples, output_dir):
    """An instance is simulated for each instance specified in `sim_tuples`.

    The simulation is done using `sim_cls` with arguments `sim_args`.

    Parameters
    ----------
    sim_cls: Simulator.class
        A `Simulator` class object specifying the type of simulation being
        performed.
    sim_args: dict
        A dictionary specifying arguments for `sim_cls`. The keys are
        strings specifying the argument names and the corresponding value
        is the argument value to be passed to `sim_cls`
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
        simulate_instance(
            sim_cls, sim_args, sim_tuple[0], sim_tuple[1], output_dir)


def create_simulated_instances(sim_cls, sim_args,
                               instance_sizes, start_idx, output_dir):
    """Simulates instances of the sizes specified in `instance_sizes`.

    An instance is simulated for each element of `instance_sizes` where
    the number of migrations of the instance is equal to the corresponding
    element of `instance_sizes`. The instances are numbered contiguously
    starting from `start_idx` and written to `output_dir`. The simulation
    is performed by `sim_cls`.

    Parameters
    ----------
    sim_cls: Simulator.class
        A `Simulator` class object specifying the type of simulation being
        performed.
    sim_args: dict
        A dictionary specifying arguments for `sim_cls`. The keys are
        strings specifying the argument names and the corresponding value
        is the argument value to be passed to `sim_cls`
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
        procs.append(mp.Process(
            target=simulate_all_instances,
            args=(sim_cls, sim_args, sim_tuples, output_dir)))
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


def get_proportion_better(results_df, heuristic1, heuristic2):
    """The proportion of times `heuristic1` outperforms `heuristic2`.

    The performance of the two heuristics is taken from `results_df`.
    `heuristic1` outperforms `heuristic2` if it requires fewer rounds on
    the same instance.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame of experimental results for the heuristics.
    heuristic1: str
        A string representing the heuristic of interest.
    heuristic2: str
        A string representing the heuristic being compared against.

    Returns
    -------
    float
        A float representing the proportion of times `heuristic1`
        outperforms `heuristic2`.

    """
    outperform_indicator = np.where(
        results_df[heuristic1] < results_df[heuristic2], 1, 0)
    return 100 * outperform_indicator.mean()


def get_improvement_ratios(results_df, method1, method2):
    """Gets round improvement ratios of `method1` over `method2`.

    The round improvement ratios are calculated using `results_df` and
    represent the statistics for the times that `method1` completes in
    fewer rounds than `method2`.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame of experimental results for the methods.
    method1: str
        A string representing the method of interest.
    method2: str
        A string representing the method being compared against.

    Returns
    -------
    float, float
        A float denoting the minimum of `method1` over `method2` in
        `results_df` and a float representing the average of that ratio.
        Both ratios are restricted to the instances where `method1`
        represents an improvement over `method2`.

    """
    improvement_vals = results_df[method1] / results_df[method2]
    return (improvement_vals.min(),
            improvement_vals[improvement_vals < 1].mean())

def get_deterioration_ratios(results_df, method1, method2):
    """Gets round deterioration ratios of `method1` over `method2`.

    The round deterioration ratios are calculated using `results_df` and
    represent the statistics for the times that `method1` completes in
    more rounds than `method2`.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame of experimental results for the methods.
    method1: str
        A string representing the method of interest.
    method2: str
        A string representing the method being compared against.

    Returns
    -------
    float, float
        A float denoting the maximum of `method1` over `method2` in
        `results_df` and a float representing the average of that ratio.
        Both ratios are restricted to the instances where `method1` requires
        more rounds that `method2`

    """
    improvement_vals = results_df[method1] / results_df[method2]
    return (improvement_vals.max(),
            improvement_vals[improvement_vals > 1].mean())

def get_improvement_stats(results_df, method1, method2):
    """Gets the improvement statistics of `method1` over `method2`.

    The improvement statistics of `method1` over `method2` are based on
    `results_df` and represent statistics for the instances where `method1`
    is better than `method2`. These statistics are the percent of instances
    in which `method1` is better than `method2` as well as the minimum and
    mean ratio of the two methods in these instances.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame of experimental results for the methods.
    method1: str
        A string representing the method of interest.
    method2: str
        A string representing the method being compared against.

    Returns
    -------
    dict
        A dictionary recording the improvement statistics of `method1` over
        `method2`. The keys are strings representing the names of the various
        statistics and the corresponding value is the value of the statistic.

    """
    improve_stats = {}
    percent_str = "% of instances with {0} < {1}".format(method1, method2)
    min_str = "min {0} / {1}".format(method1, method2)
    mean_str = "improvement mean {0} / {1}".format(method1, method2)
    improve_stats[percent_str] = get_proportion_better(
        results_df, method1, method2)
    min_val, mean_val = get_improvement_ratios(results_df, method1, method2)
    improve_stats[min_str] = min_val
    improve_stats[mean_str] = mean_val
    return improve_stats


def get_deterioration_stats(results_df, method1, method2):
    """Gets the deterioration statistics of `method1` over `method2`.

    The deterioration statistics of `method1` over `method2` are based on
    `results_df` and represent statistics for the instances where `method1`
    is worse than `method2`. These statistics are the percent of instances
    in which `method1` is worse than `method2` as well as the maximum and
    mean ratio of the two methods in these instances.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame of experimental results for the methods.
    method1: str
        A string representing the method of interest.
    method2: str
        A string representing the method being compared against.

    Returns
    -------
    dict
        A dictionary recording the deterioration statistics of `method1` over
        `method2`. The keys are strings representing the names of the various
        statistics and the corresponding value is the value of the statistic.

    """
    deter_stats = {}
    percent_str = "% of instances with {0} > {1}".format(method1, method2)
    max_str = "max {0} / {1}".format(method1, method2)
    mean_str = "deterioration mean {0} / {1}".format(method1, method2)
    deter_stats[percent_str] = get_proportion_better(
        results_df, method2, method1)
    max_val, mean_val = get_deterioration_ratios(results_df, method1, method2)
    deter_stats[max_str] = max_val
    deter_stats[mean_str] = mean_val
    return deter_stats


def compare_heuristic_results(results_df, method1, method2):
    """Compares `method1` and `method2` based on `results_df`.

    A dictionary is created recording statistics of the comparison between
    `method1` and `method2` in `results_df`. The statistics calculated
    are the percent of instances where `method1` is less than `method2`, as
    well as the minimum and average ratio of `method1` to `method2` for those
    instances. Likewise, the percent of instances where `method1` is greater
    than `method2`, as well as the maximum and average ratio of `method1` to
    `method2` for those instances.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame containing experimental results for the
        heuristics.
    heuristic1: str
        A string representing the name of one of the heuristics being
        compared.
    heuristic2: str
        A string representing the name of the other heuristic being
        compared.

    Returns
    -------
    dict
        A dictionary containing the comparison statistics between the
        two heuristics.

    """
    return {**get_improvement_stats(results_df, method1, method2),
            **get_deterioration_stats(results_df, method1, method2)}


def get_heuristic_discrepancy_df(results_df, opt_col, heuristic_cols):
    """A df of the discrepancies between `heuristic_cols` and `opt_col`.

    Calculates the percentage of instances for each heuristic in
    `heuristic_cols` that deviate from the optimal value in `opt_col` based
    on the results in `results_df`. The percentages are grouped by value of
    the optimal solution. That is, for an optimal value `x` the percentages
    are calculated across all instances that have an optimal value of `x`.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame containing the results from which the
        discrepancies are calculated.
    opt_col: str
        A string representing the name of the column in `results_df` holding
        the values of the optimal solutions.
    heuristic_cols: list
        A list of strings representing the names of the heuristics for which
        the discrepancies are calculated.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the percentage of instances where the
        heuristic solution value is different than the optimal value. Results
        are grouped by optimal value and reported for each heuristic.

    """
    disc_cols = ["{}_disc".format(col_name) for col_name in heuristic_cols]
    for idx in range(len(heuristic_cols)):
        results_df[disc_cols[idx]] = np.where(
            results_df[heuristic_cols[idx]] > results_df[opt_col], 1, 0)
    disc_df = results_df[[opt_col] + disc_cols].groupby(opt_col).mean()
    disc_df.columns = heuristic_cols
    return disc_df
