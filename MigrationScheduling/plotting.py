"""This module implements a collection of functions used to visualize the
results of experiments.

"""
import matplotlib.pyplot as plt
from MigrationScheduling import analysis, specs


def adjust_y_axis(results_df, result_cols, log_scale=False, bound_y=False):
    """Makes adjustments to the y axis according to `log_scale` and `bound_y`.

    Parameters
    ----------
    results_df: pd.DataFrame
        The pandas DataFrame containing the data being plotted.
    results_cols: list
        A list of strings representing the names of the columns containing
        the data being plotted.
    log_scale: bool
        A boolean value indicating whether a logarithmic scale should be used
        for the y axis. The default value is False.
    bound_y: bool
        A boolean value indicating whether explicit upper and lower bounds
        should be computed for the y axis. The default value is False.

    Returns
    -------
    None

    """
    if log_scale:
        plt.yscale("log")
    if bound_y:
        y_min = results_df[result_cols].min(axis=1).min(axis=0)
        y_max = results_df[result_cols].max(axis=1).max(axis=0)
        plt.yticks(range(y_min, y_max + 1))

def add_plot_formatting(x_title, y_title, output_file):
    """Performs plot formatting and outputs the plot to `output_file`.

    Parameters
    ----------
    x_title: str
        A string representing the title for the x axis.
    y_title: str
        A string representing the title for the y axis.
    output_file: str
        A string representing the name of the file to which the plot will
        be output.

    Returns
    -------
    None

    """
    plt.legend()
    plt.xlabel(x_title)
    if len(y_title):
        plt.ylabel(y_title)
    plt.savefig(output_file)
    plt.show()

def plot_results(results_df, result_cols, x_title, y_title, output_file):
    """Prints the values of `results_df` according to `result_cols`.

    A plot is created having a line for each column of `results_col` from
    `results_df` and the x-values are the indices of `results_df`.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame containing the data being plotted.
    result_cols: list
        A list of strings representing the names of columns being plotted.
    x_title: str
        A string representing the title for the x axis.
    y_title: str
        A string representing the title for the y axis.
    output_file: str
        A string representing the name of the file to which the plot will
        be output.

    Returns
    -------
    None

    """
    plt.figure(figsize=(10, 7))
    for result_col in result_cols:
        col_name = result_col.split("_")[0].upper()
        plt.plot(results_df.index, results_df[result_col],
                 specs.STYLE_MAP[col_name], label=col_name)
    add_plot_formatting(x_title, y_title, output_file)

def plot_runtimes(results_df, x_var, time_vars,
                  x_title, y_title, output_file):
    """Plots the runtimes for `results_df` across values of `x_var`.

    Each variable in `time_vars` is plotted against `x_var` based on the
    values in `results_df`.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame containing the data for plotting.
    x_var: str
        A string representing the name of a column in `results_df` which will
        be used as the variable on the x-axis in the resulting plot.
    time_vars: list
        A list of strings representing the names of the columns in
        `results_df` corresponding to runtimes that will be plotted.
    x_title: str
        A string representing the title for the plot's x axis.
    y_title: str
        A string representing the title for the plot's y axis.
    output_file: str
        A string representing the name of the file to which the plot will
        be output.

    Returns
    -------
    None

    """
    time_df = analysis.get_time_df(results_df, x_var, time_vars)
    plot_results(time_df, time_vars, x_title, y_title, output_file)


def plot_results_comparison(results_df, result_cols, compare_col,
                            x_title, y_title, output_file):
    """Plots the comparison of `results_cols` to `compare_col`.

    Each column in `result_cols` is standardized by `compare_col` based on
    the values in `results_df`. Each standardized column is then plotted
    against the index of `results_df`.

    Parameters
    ----------
    results_df: pd.DataFrame
        A pandas DataFrame containing the data for plotting.
    result_cols: list
        A list of strings representing the names of the columns being
        compared.
    compare_col: str
        A string representing the name of the column used to standardize
        the results for comparison.
    x_title: str
        A string representing the title for the plot's x axis.
    y_title: str
        A string representing the title for the plot's y axis.
    output_file: str
        A string representing the name of the file to which the plot will
        be output.

    Returns
    -------
    None

    """
    std_cols = ["{}_standardized".format(col_name)
                for col_name in result_cols]
    for idx in range(len(result_cols)):
        results_df[std_cols[idx]] = (
            results_df[result_cols[idx]] / results_df[compare_col])
    plot_results(results_df, std_cols, x_title, y_title, output_file)
