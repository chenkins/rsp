"""Tools and Methods to analyse the data generated by the experiments.

Methods
-------
average_over_trials
    Average over all the experiment trials
"""
from typing import List
from typing import Optional
from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import axes
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame

matplotlib.use('Qt5Agg')
# Dummy import currently because otherwise the import is removed all the time but used by 3d scatter plot
axes3d = Axes3D


# https://stackoverflow.com/questions/25649429/how-to-swap-two-dataframe-columns
def swap_columns(df: DataFrame, c1: int, c2: int):
    """Swap columns in a data frame.

    Parameters
    ----------
    df: DataFrame
        The data frame.
    c1: int
        the column index
    c2: int
        the other column index.
    """
    df['temp'] = df[c1]
    df[c1] = df[c2]
    df[c2] = df['temp']
    df.drop(columns=['temp'], inplace=True)


def average_over_trials(experimental_data: DataFrame) -> Tuple[DataFrame, DataFrame]:
    """
    Average over all the experiment trials
    Parameters
    ----------
    experimental_data

    Returns
    -------
    DataFrame of mean data and DataFram of standard deviations
    """

    averaged_data = experimental_data.groupby(['experiment_id']).mean().reset_index()
    standard_deviation_data = experimental_data.groupby(['experiment_id']).std().reset_index()
    return averaged_data, standard_deviation_data


def three_dimensional_scatter_plot(data: DataFrame,
                                   columns: DataFrame.columns,
                                   error: DataFrame = None,
                                   file_name: str = "",
                                   fig: Optional[matplotlib.figure.Figure] = None,
                                   subplot_pos: str = '111',
                                   subplot_title: str = '',
                                   colors: Optional[List[str]] = None):
    """Adds a 3d-scatterplot as a subplot to a figure.

    Parameters
    ----------
    data: DataFrame
        DataFrame containing data to be plotted
    error: DataFrame
        DataFrame containing error of z values to plot
    columns: DataFrame.columns
        Three columns of that data frame to be plotted against each other, x_values, y_values,z_values
    file_name: string
        If provided the plot is stored to figure instead of shown
    fig: Optional[matplotlib.figure.Figure]
        If given, adds the subplot to this figure without showing it, else creates a new one and shows it.
    subplot_pos: str
        a 3-digit integer describing the position of the subplot.
    colors: List[str]
        List of colors for the data points.

    Returns
    -------
    """
    x_values = data[columns[0]].values
    y_values = data[columns[1]].values
    z_values = data[columns[2]].values
    experiment_ids = data['experiment_id'].values

    show = False
    if fig is None:
        show = True
        fig = plt.figure()

    ax: axes.Axes = fig.add_subplot(subplot_pos, projection='3d')
    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])
    ax.set_zlabel(columns[2])
    if not subplot_title:
        ax.set_title(str(columns))
    else:
        ax.set_title(subplot_title)

    ax.scatter(x_values, y_values, z_values, color=colors)
    for i in np.arange(0, len(z_values)):
        ax.text(x_values[i], y_values[i], z_values[i], "{}".format(experiment_ids[i]))
    if error is not None:
        # plot errorbars
        z_error = error[columns[2]].values
        for i in np.arange(0, len(z_values)):
            ax.plot([x_values[i], x_values[i]], [y_values[i], y_values[i]],
                    [z_values[i] + z_error[i], z_values[i] - z_error[i]], marker="_")

    if len(file_name) > 1:
        plt.savefig(file_name)
    elif show:
        plt.show()


def two_dimensional_scatter_plot(data: DataFrame,
                                 columns: DataFrame.columns,
                                 error: DataFrame = None,
                                 baseline: DataFrame = None,
                                 file_name: str = "",
                                 fig: Optional[matplotlib.figure.Figure] = None,
                                 subplot_pos: str = '111',
                                 title: str = None,
                                 colors: Optional[List[str]] = None):
    """Adds a 2d-scatterplot as a subplot to a figure.

    Parameters
    ----------
    data: DataFrame
        DataFrame containing data to be plotted
    error: DataFrame
        DataFrame containing error of z values to plot
    columns: DataFrame.columns
        Three columns of that data frame to be plotted against each other, x_values, y_values,z_values
    file_name: string
        If provided the plot is stored to figure instead of shown
    fig: Optional[matplotlib.figure.Figure]
        If given, adds the subplot to this figure without showing it, else creates a new one and shows it.
    subplot_pos: str
        a 3-digit integer describing the position of the subplot.
    colors: List[str]
        List of colors for the data points.

    Returns
    -------
    """
    x_values = data[columns[0]].values
    y_values = data[columns[1]].values
    experiment_ids = data['experiment_id'].values

    show = False
    if fig is None:
        show = True
        fig = plt.figure()

    ax: axes.Axes = fig.add_subplot(subplot_pos)
    if title:
        ax.set_title(title)
    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])

    ax.scatter(x_values, y_values, color=colors)
    for i in np.arange(0, len(y_values)):
        ax.text(x_values[i], y_values[i], "{}".format(experiment_ids[i]))
    if error is not None:
        # plot errorbars
        y_error = error[columns[1]].values
        for i in np.arange(0, len(y_values)):
            ax.plot([x_values[i], x_values[i]],
                    [y_values[i] + y_error[i], y_values[i] - y_error[i]], marker="_")
    if baseline is not None:
        for i in np.arange(0, len(y_values)):
            ax.plot([x_values[i], x_values[i]],
                    [baseline[i], y_values[i]], marker="_")

    if len(file_name) > 1:
        plt.savefig(file_name)
    elif show:
        plt.show()
