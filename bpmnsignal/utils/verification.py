"""
Module for verification
"""

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class Verify():

    def __init__(self, parser) -> None:
        self.parser = parser

    def is_model_valid(self, model):
        """
        Checks whether model is valid or not.
        """
        try:
            if model["stencil"]["id"] != "BPMNDiagram":
                return False

            if self.parser.count_model_elements() < 5:
                return False
            
            if self.parser.count_pools() > 1:
                return False

            return True
        except KeyError:
            return False
