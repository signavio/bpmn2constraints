"""
Parser.
I'll document it.. Later..
"""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wildcard-import
# pylint: disable=inconsistent-return-statements

from json import load, JSONDecodeError
from bpmnsignal.utils.constants import *
from bpmnsignal.utils.sanitizer import Sanitizer


class Parser():

    def __init__(self, bpmn, is_file, transitivity) -> None:
        self.transitivity = transitivity
        self.model = self._create_model(bpmn, is_file)
        self.diagram = self.model
        self.sanitizer = Sanitizer()
        self.sequence = []

    def _flatten_model(self):
        self.model[CHILD_SHAPES] = self._flatten(self.model)

    def _create_model(self, bpmn, is_file):
        if is_file:
            try:
                with open(bpmn, "r", encoding="utf-8") as file:
                    return load(file)

            except JSONDecodeError:
                raise Exception("Something wrong with format of JSON file.")
            except OSError:
                raise Exception("Something went wrong reading the file.")
        else:
            return bpmn

    def _flatten(self, model):
        elements = []
        for elem in model[CHILD_SHAPES]:
            if self._get_element_type(elem) not in ALLOWED_SWIMLANES:
                elements.append(elem)
            else:
                elements += self._flatten(elem)
        return elements

    def run(self):
        self._flatten_model()
        self._parse()
        if self.transitivity:
            self._add_transitivity()

        return self.sequence

    def _get_cfo_by_id(self, successor_id):
        for cfo in self.sequence:
            if successor_id == cfo.get("id"):
                return cfo

    def _find_transitive_closure(self, cfo, transitivity):
        if cfo:
            for successor in cfo.get("successor"):
                if successor and successor.get("name") not in EXCLUDED_TRANSITIVE_NAMES:
                    transitivity.append(successor)
                successor_cfo = self._get_cfo_by_id(successor.get("id"))
                self._find_transitive_closure(successor_cfo, transitivity)

    def _add_transitivity(self):
        for cfo in self.sequence:
            transitivity = []
            self._find_transitive_closure(cfo, transitivity)
            if transitivity:
                cfo.update(
                    {
                        "transitivity": transitivity
                    }
                )

    def _parse(self):
        for elem in self._get_diagram_elements():
            cfo = self._create_cfo(elem)
            if cfo:
                self.sequence.append(cfo)

    def _create_cfo(self, elem):

        if self._valid_cfo_element(elem):
            successor = self._get_successors(elem)
            predecessor = self._get_predecessors(elem)

            cfo = {
                "name": self._get_label(elem),
                "type": self._get_element_type(elem),
                "id": self._get_id(elem),
                "successor": self._format_list(successor),
                "predecessor": self._format_list(predecessor),
                "is start": len(predecessor) == 0 or self._is_predecessor_start_event(predecessor),
                "is end": len(successor) == 0 or self._is_successor_end_event(successor),
            }

            if self._is_element_gateway(elem):
                cfo.update({
                    "joining":
                    len(self._get_outgoing_connection(elem)) == 1,
                    "splitting":
                    len(self._get_outgoing_connection(elem)) >= 2,
                })

            if cfo["successor"]:
                for successor in cfo["successor"]:
                    if successor.get("type") in ALLOWED_GATEWAYS:
                        elem_id = successor.get("id")
                        elem = self._get_element_by_id(elem_id)
                        gateway_successors = self._get_successors(elem)
                        successor.update({
                            "gateway successors": self._format_list(gateway_successors)
                        })

            return cfo

    def _valid_cfo_element(self, elem):
        if elem is None:
            return False
        if self._is_element_activity(elem):
            return True
        if self._is_element_gateway(elem):
            return True
        if self._is_element_start_event(elem) and self._valid_start_name(elem):
            return True
        
        return False
        
    
    def _valid_start_name(self, elem):
        if PROPERTIES in elem and NAME in PROPERTIES:
            start_name = self._get_name(elem)
            if start_name in DISCARDED_START_EVENT_NAMES:
                return False
            if len(start_name.strip()) == 0:
                return False
            if len(start_name) < VALID_START_NAME_LENGTH:
                return False
            if start_name.isspace():
                return False

    def _get_successors(self, elem):
        try:
            connection_objects = self._get_outgoing_connection(elem)
            if len(connection_objects) == 0:
                return []
            activities = []
            for connection in connection_objects:
                if connection:
                    connection_id = self._get_id(connection)
                    elem = self._get_element_by_id(connection_id)

                    if self._get_element_type(elem) in ALLOWED_CONNECTING_OBJECTS:
                        connection = self._get_outgoing_connection(elem)
                        if connection:
                            connection_id = self._get_id(connection[0])
                            elem = self._get_element_by_id(connection_id)
                            activities.append(elem)
            return activities
        except TypeError:
            raise Exception

    def _get_predecessors(self, current_elem):
        predecessors = []
        current_elem_id = self._get_id(current_elem)

        for elem in self._get_diagram_elements():
            successors = self._get_successors(elem)
            if successors:
                for successor in successors:
                    if successor:
                        if self._get_id(successor) == current_elem_id:
                            predecessors.append(elem)

        return predecessors

    def _format_list(self, elems):
        formatted = []
        for elem in elems:
            if elem:
                elem = {
                    "name": self._get_label(elem),
                    "type": self._get_element_type(elem),
                    "id": self._get_id(elem),
                }

                formatted.append(elem)
        return formatted

    def _get_id(self, elem):
        return elem[ELEMENT_ID]

    def _get_element_by_id(self, connection_id):
        try:
            return next(e for e in self._get_diagram_elements()
                        if self._get_id(e) == connection_id)
        except StopIteration:
            raise Exception(f"Could not find element with ID {connection_id}")
            
    def _get_element_type(self, elem):
        return elem[STENCIL][ID]

    def _get_activity_type(self, elem):
        return ACTIVITY_MAPPING.get(self._get_element_type(elem), "Activity")

    def _get_gateway_type(self, elem):
        return GATEWAY_MAPPING.get(self._get_element_type(elem), "Gateway")

    def _get_end_type(self, elem):
        return END_EVENT_MAPPING.get(self._get_element_type(elem), "EndEvent")

    def _get_diagram_elements(self):
        try:
            return self.model[CHILD_SHAPES]
        except KeyError:
            raise Exception("Could not find any child elements to diagram.")

    def _get_outgoing_connection(self, elem):
        return elem[OUTGOING]

    def _get_name(self, elem):
        return elem[PROPERTIES][NAME]

    def _get_label(self, elem):
        try:
            if self._is_element_activity(elem):
                return self.sanitizer.sanitize_label(self._get_name(elem))
            if self._is_element_gateway(elem):
                return self._get_gateway_type(elem)
        except KeyError:
            # If not label or gateway type can be used, use type as label.
            return self._get_element_type(elem)

    def _is_element_start_event(self, elem):
        return self._get_element_type(elem) in ALLOWED_START_EVENTS

    def _is_element_end_event(self, elem):
        return self._get_element_type(elem) in ALLOWED_END_EVENTS

    def _is_element_activity(self, elem):
        return self._get_element_type(elem) in ALLOWED_ACTIVITIES

    def _is_element_gateway(self, elem):
        return self._get_element_type(elem) in ALLOWED_GATEWAYS

    def _is_predecessor_start_event(self, predecessors):
        for predecessor in predecessors:
            if predecessor:
                if self._get_element_type(predecessor) in ALLOWED_START_EVENTS:
                    return True
        return False

    def _is_successor_end_event(self, successors):
        for successor in successors:
            if successor:
                if self._get_element_type(successor) in ALLOWED_END_EVENTS:
                    return True
        return False

    def count_parsable_elements(self):
        count = 0
        for elem in self._get_diagram_elements():
            elem_type = self._get_element_type(elem)
            if elem_type in ALLOWED_ACTIVITIES or elem_type in ALLOWED_GATEWAYS:
                count += 1
        return count

    def count_model_elements(self):
        return len(self.model[CHILD_SHAPES])

    def count_model_element_types(self):
        return len(self.get_element_types())
    
    def count_pools(self):
        count = 0
        for elem in self.diagram[CHILD_SHAPES]:
            if self._get_element_type(elem) == "Pool":
                count += 1
        return count
    
    def has_start(self):
        for elem in self.sequence:
            if elem.get("is start"):
                return True
        return False
    
    def get_element_types(self):
        elem_types = {}

        for elem in self._get_diagram_elements():
            elem_type = self._get_element_type(elem)

            if elem_type in elem_types:
                elem_types[elem_type] += 1
            else:
                elem_types[elem_type] = 1

        return elem_types
