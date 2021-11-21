"""This module implements a collection of functions used to visualize the
results of experiments.

"""
import matplotlib.pyplot as plt
from MigrationScheduling import analysis


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

def add_plot_formatting(x_title, y_title):
    """Performs plot formatting.

    Parameters
    ----------
    x_title: str
        A string representing the title for the x axis.
    y_title: str
        A string representing the title for the y axis.

    Returns
    -------
    None

    """
    plt.legend()
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()

def plot_result_vals(results_df, result_cols, x_title,
                     y_title, log_scale=False, bound_y=False):
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
    log_scale: bool
        A boolean value indicating whether the y axis should be on a
        logarithmic scale. The default value is False.
    bound_y: bool
        A boolean value indicating whether explicit bounds should be
        calculated for the y axis. The default value is False.

    Returns
    -------
    None

    """
    plt.figure(figsize=(10, 10))
    for result_col in result_cols:
        plt.plot(results_df.index, results_df[result_col],
                 label=result_col.split("_")[0])
    adjust_y_axis(results_df, result_cols, log_scale, bound_y)
    add_plot_formatting(x_title, y_title)
