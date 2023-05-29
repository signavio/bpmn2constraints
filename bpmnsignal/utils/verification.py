"""
Module for verification
"""

from bpmnsignal.parser.bpmn_element_parser import (count_elements,
                                                   get_start_element,
                                                   count_num_of_pools)


def is_model_valid(model):
    """
    Checks whether model is valid or not.
    """
    try:
        if model["stencil"]["id"] != "BPMNDiagram":
            return False

        if count_elements(model) < 5:
            return False

        if get_start_element(model) is None:
            return False

        if count_num_of_pools(model) > 1:
            return False

        return True
    except KeyError:
        return False
