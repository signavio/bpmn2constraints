from bpmnconstraints.utils.constants import *


class XmlModel:
    def __init__(self, model) -> None:
        self.model = model  # this is root.

    def get_child_models(self):
        pass

    def get_element_type(self, elem):
        pass

    def get_diagram_elements(self):
        return []

    def get_outgoing_connection(self, elem):
        pass

    def get_name(self, elem):
        pass

    def get_id(self, elem):
        pass
