"""
Module for plotting functions.
"""
# pylint: disable=import-error

import matplotlib.pyplot as plt
import numpy as np


def create_scatter_plot_2(data, title):
    """
    Creates a scatter plot.
    """
    x_axis = [d['number of element types'] for d in data]
    y_axis = [d['number of elements'] for d in data]
    outcome = [d['outcome'] for d in data]

    cmap = {'failed': 'red', 'partial': 'blue', 'successful': 'green'}

    colour = [cmap[o] for o in outcome]

    _, fig = plt.subplots(figsize=(10, 6))
    fig.scatter(x_axis, y_axis, c=colour)

    fig.set_xlabel('Number of Element Types')
    fig.set_ylabel('Number of Elements')
    fig.set_title(title)

    legend_elements = [
        plt.Line2D([0], [0],
                   marker='o',
                   color='w',
                   label=k,
                   markerfacecolor=v,
                   markersize=10) for k, v in cmap.items()
    ]
    fig.legend(handles=legend_elements)

    plt.show()


def create_scatter_plot(data, title):
    """
    Creates a scatter plot.
    """
    x_axis = [d['number of element types'] for d in data]
    y_axis = [d['number of elements'] for d in data]
    colour = None

    colour = np.array([d['variable'] for d in data])

    _, fig = plt.subplots(figsize=(10, 6))
    fig.scatter(x_axis, y_axis, c=colour, cmap='RdYlGn')

    fig.set_xlabel('Number of Element Types')
    fig.set_ylabel('Number of Elements')
    fig.set_title(title)

    plt.show()


def percentage_bar_plot(data):
    """
    Creates a bar plot based on percentages of partially plotted models.
    """
    keys = data.keys()
    values = data.values()

    plt.bar(keys, values)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Percentage Span Parsed')
    plt.ylabel('Number of Models')
    plt.title('Degree of Parsing on Partial Models')
    plt.show()


def percentage_lint_plot(data):
    """
    Plots a line based on percentages.
    """
    keys = list(data.keys())
    values = list(data.values())

    plt.plot(keys, values, marker='o')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Percentage Span Parsed')
    plt.ylabel('Number of Models')
    plt.title('Degree of Parsing on Partial Models')
    plt.show()


def percentage_line_plot_cumulative(data):
    """
    Creates a line plot based on percentages of partially plotted models.
    """
    keys = list(data.keys())
    values = list(data.values())

    for i in range(1, len(values)):
        values[i] += values[i - 1]

    plt.plot(keys, values, marker='o')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Percentage Span Parsed')
    plt.ylabel('Cumulative Number of Models')
    plt.title('Cumulative Degree of Parsing on Partial Models')
    plt.show()


def plot_model_outcomes(data):
    """
    Creates a bar plot based on success, partial success or failure.
    """
    element_type_counts = [d["number of element types"] for d in data]

    unique_counts = sorted(list(set(element_type_counts)))

    failed_counts = []
    partial_counts = []
    successful_counts = []

    for count in unique_counts:
        failed_count = 0
        partial_count = 0
        successful_count = 0

        for data_obj in data:
            if data_obj["number of element types"] == count:
                if data_obj["outcome"] == "failed":
                    failed_count += 1
                elif data_obj["outcome"] == "partial":
                    partial_count += 1
                elif data_obj["outcome"] == "successful":
                    successful_count += 1

        failed_counts.append(failed_count)
        partial_counts.append(partial_count)
        successful_counts.append(successful_count)

    bar_width = 0.25

    failed_count = np.arange(len(unique_counts))
    partial_count = [x + bar_width for x in failed_count]
    success_count = [x + bar_width for x in partial_count]

    plt.bar(failed_count,
            failed_counts,
            color='red',
            width=bar_width,
            edgecolor='white',
            label='failed')
    plt.bar(partial_count,
            partial_counts,
            color='blue',
            width=bar_width,
            edgecolor='white',
            label='partial')
    plt.bar(success_count,
            successful_counts,
            color='green',
            width=bar_width,
            edgecolor='white',
            label='successful')

    plt.xlabel('Number of Element Types')
    plt.ylabel('Number of Models')
    plt.title('Model Outcomes by Element Types')
    plt.xticks([r + bar_width for r in range(len(unique_counts))],
               unique_counts)
    plt.legend()
    plt.show()


def combined_scatter_plot(combined):
    """
    Creates a scatterplot of combined models.
    """
    precision_list = []
    recall_list = []

    for model in combined:
        precision_list.append(model['precision'])
        recall_list.append(model['recall'])

    mean_precision = sum(precision_list) / len(precision_list)
    mean_recall = sum(recall_list) / len(recall_list)

    print(f'Mean-Precision: {mean_precision}')
    print(f'Mean-Recall: {mean_recall}')

    plt.scatter(recall_list, precision_list)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.show()


def plot_precision_num_elements(combined):
    """
    Plots the precision in comparison to number of element types.
    """
    precision_list = []
    element_num = []

    for model in combined:
        precision_list.append(model['precision'])
        element_num.append(len(model['num_elem_types']))

    plt.scatter(element_num, precision_list)
    plt.ylabel('Precision')
    plt.xlabel('Number of Element Types')
    plt.title('Precision relative to Number of Element Types')
    plt.show()


def plot_recall_num_elements(combined):
    """
    Plots the recall in comparison to number of element types.
    """
    recall_list = []
    element_num = []

    for model in combined:
        recall_list.append(model['recall'])
        element_num.append(len(model['num_elem_types']))

    plt.scatter(element_num, recall_list)
    plt.ylabel('Recall')
    plt.xlabel('Number of Element Types')
    plt.title('Recall relative to Number of Element Types')
    plt.show()


def plot_total_constraints(combined):
    """
    Plots the total generated constraints from the petri net approach as well
    as the compiler.
    """
    compiler = []
    petri_net = []

    for model in combined:
        compiler_constraints = model['compiler_constraints']
        petri_net_constraints = model['petri_net_constraints']

        if compiler_constraints and petri_net_constraints:
            compiler.extend(list(set(compiler_constraints)))
            petri_net.extend(list(set(petri_net_constraints)))

    print(f"petri net constraints : {len(petri_net)}")
    print(f"compiler constraints : {len(compiler)}")

    x_axis = ['Petri Net Constraints', 'Compiler Constraints']
    y_axis = [len(petri_net), len(compiler)]

    plt.bar(x_axis, y_axis)
    plt.title('Unique Constraints Generated per Tool')
    plt.xlabel('Tool Type')
    plt.ylabel('Number of Unique Constraints')
    plt.show()
