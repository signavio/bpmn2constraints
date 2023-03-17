from pathlib import Path
from bpmnsignal.matching_templates import *

def construct_linear_constraints(sequence):
    """Generates SIGNAL constraints from a linear sequence of activities

    Args:
        sequence (List): Activity sequence

    Returns:
        List: List of SIGNAL constraints
    """
    constraints = []
    for index, element in enumerate(sequence):
        if index == 0:
            constraints.append(starts_with(element))
        if index == len(sequence) - 1:
            constraints.append(ends_with(element))
            break
        constraints.append(leads_to(element, sequence[index + 1]))
    return constraints
