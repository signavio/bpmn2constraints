"""
Module for plotting functions.
"""

# pylint: disable=import-error

import matplotlib.pyplot as plt
import numpy as np


def create_scatter_plot(data):
    """
    Creates a scatter plot.
    """
    x_axis = [d['number of element types'] for d in data]
    y_axis = [d['number of elements'] for d in data]
    colour = np.array([d['variable'] for d in data])

    _, fig = plt.subplots(figsize=(10, 6))
    fig.scatter(x_axis, y_axis, c=colour, cmap='RdYlGn')

    fig.set_xlabel('Number of Element Types')
    fig.set_ylabel('Number of Elements')
    fig.set_title('Plot of Data')

    plt.show()


def create_bar_plot(data):
    """
    Creates a bar plot.
    """
    plt.bar(data.keys(), data.values())

    plt.title("Filtered Models")
    plt.xlabel("Reasons for Filtering")
    plt.ylabel("Number of Models")

    plt.show()
