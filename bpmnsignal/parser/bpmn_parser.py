"""
Parser.
I'll document it.. Later..
"""

from json import load, JSONDecodeError, dumps
from bpmnsignal.utils.constants import *
from bpmnsignal.utils.sanitizer import Sanitizer


class Parser():

    def __init__(self, bpmn, is_file, transitivity) -> None:
        self.transitivity = transitivity
        self.model = self.__create_model(bpmn, is_file)
        self.diagram = self.model
        self.sanitizer = Sanitizer()
        self.sequence = []

    def __flatten_model(self):
        self.model[CHILD_SHAPES] = self.__flatten(self.model)

    def __create_model(self, bpmn, is_file):
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

    def __flatten(self, model):
        elements = []
        for elem in model[CHILD_SHAPES]:
            if self.__get_element_type(elem) not in ALLOWED_SWIMLANES:
                elements.append(elem)
            else:
                elements += self.__flatten(elem)
        return elements

    def run(self):
        self.__flatten_model()
        self.__parse()
        if self.transitivity:
            self.__add_transitivity()

        return self.sequence

    def __get_cfo_by_id(self, successor_id):
        for cfo in self.sequence:
            if successor_id == cfo.get("id"):
                return cfo

    def __find_transitive_closure(self, cfo, transitivity):
        if cfo:
            for successor in cfo.get("successor"):
                try:
                    if successor.get("type") in ALLOWED_GATEWAYS:
                        continue
                except Exception:
                    pass
                if successor and successor.get("name") not in EXCLUDED_TRANSITIVE_NAMES:
                    transitivity.append(successor)
                successor_cfo = self.__get_cfo_by_id(successor.get("id"))
                self.__find_transitive_closure(successor_cfo, transitivity)

    def __add_transitivity(self):
        for cfo in self.sequence:
            transitivity = []
            self.__find_transitive_closure(cfo, transitivity)
            if transitivity:
                cfo.update(
                    {
                        "transitivity": transitivity
                    }
                )

    def __parse(self):
        for elem in self.__get_diagram_elements():
            cfo = self.__create_cfo(elem)
            if cfo:
                self.sequence.append(cfo)

    def __create_cfo(self, elem):

        if self.__valid_cfo_element(elem):
            successor = self.__get_successors(elem)
            predecessor = self.__get_predecessors(elem)

            cfo = {
                "name": self.__get_label(elem),
                "type": self.__get_element_type(elem),
                "id": self.__get_id(elem),
                "successor": self.__format_list(successor),
                "predecessor": self.__format_list(predecessor),
                "is start": len(predecessor) == 0 or self.__is_predecessor_start_event(predecessor),
                "is end": len(successor) == 0 or self.__is_successor_end_event(successor),
            }

            if self.__is_element_gateway(elem):
                cfo.update({
                    "joining":
                    len(self.__get_outgoing_connection(elem)) == 1,
                    "splitting":
                    len(self.__get_outgoing_connection(elem)) >= 2,
                })

            if cfo["successor"]:
                for successor in cfo["successor"]:
                    if successor.get("type") in ALLOWED_GATEWAYS:
                        elem_id = successor.get("id")
                        elem = self.__get_element_by_id(elem_id)
                        gateway_successors = self.__get_successors(elem)
                        successor.update({
                            "gateway successors": self.__format_list(gateway_successors, True)
                        })

            return cfo

    def __valid_cfo_element(self, elem):
        if elem is None:
            return False
        if self.__is_element_activity(elem):
            return True
        if self.__is_element_gateway(elem):
            return True
        if self.__is_element_start_event(elem) and self.__valid_start_name(elem):
            return True
        if self.__is_element_end_event(elem) and self.__valid_end_name(elem):
            return True
        
        return False
        
    
    def __valid_start_name(self, elem):
        try:
            start_name = self.__get_name(elem)
            if start_name in DISCARDED_START_EVENT_NAMES:
                return False
            if len(start_name.strip()) == 0:
                return False
            if len(start_name) < VALID_NAME_LENGTH:
                return False
            if start_name.isspace():
                return False
        except KeyError:
            return False
            
    def __valid_end_name(self, elem):
        try:
            end_name = self.__get_name(elem)
            if end_name in DISCARDED_END_EVENT_NAMES:
                return False
            if len(end_name.strip()) == 0:
                return False
            if len(end_name) < VALID_NAME_LENGTH:
                return False
            if end_name.isspace():
                return False
        except KeyError:
            return False

    def __get_successors(self, elem):
        try:
            connection_objects = self.__get_outgoing_connection(elem)
            if len(connection_objects) == 0:
                return []
            activities = []
            for connection in connection_objects:
                if connection:
                    connection_id = self.__get_id(connection)
                    elem = self.__get_element_by_id(connection_id)

                    if self.__get_element_type(elem) in ALLOWED_CONNECTING_OBJECTS:
                        connection = self.__get_outgoing_connection(elem)
                        if connection:
                            connection_id = self.__get_id(connection[0])
                            elem = self.__get_element_by_id(connection_id)
                            activities.append(elem)
            return activities
        except TypeError:
            raise Exception

    def __get_predecessors(self, current_elem):
        predecessors = []
        current_elem_id = self.__get_id(current_elem)

        for elem in self.__get_diagram_elements():
            successors = self.__get_successors(elem)
            if successors:
                for successor in successors:
                    if successor:
                        if self.__get_id(successor) == current_elem_id:
                            predecessors.append(elem)

        return predecessors

    def __format_list(self, elems, gateway=False):
        formatted = []
        for elem in elems:
            if elem:
                elem = {
                    "name": self.__get_label(elem),
                    "type": self.__get_element_type(elem),
                    "id": self.__get_id(elem),
                    "gateway successor" : gateway
                }

                formatted.append(elem)
        return formatted

    def __get_id(self, elem):
        return elem[ELEMENT_ID]

    def __get_element_by_id(self, connection_id):
        try:
            return next(e for e in self.__get_diagram_elements()
                        if self.__get_id(e) == connection_id)
        except StopIteration:
            raise Exception(f"Could not find element with ID {connection_id}")
            
    def __get_element_type(self, elem):
        return elem[STENCIL][ID]

    def __get_activity_type(self, elem):
        return ACTIVITY_MAPPING.get(self.__get_element_type(elem), "Activity")

    def __get_gateway_type(self, elem):
        return GATEWAY_MAPPING.get(self.__get_element_type(elem), "Gateway")

    def __get_end_type(self, elem):
        return END_EVENT_MAPPING.get(self.__get_element_type(elem), "EndEvent")

    def __get_diagram_elements(self):
        try:
            return self.model[CHILD_SHAPES]
        except KeyError:
            raise Exception("Could not find any child elements to diagram.")

    def __get_outgoing_connection(self, elem):
        return elem[OUTGOING]

    def __get_name(self, elem):
        return elem[PROPERTIES][NAME]

    def __get_label(self, elem):
        try:
            if self.__is_element_activity(elem):
                try:
                    return self.sanitizer.sanitize_label(self.__get_name(elem))
                except KeyError:
                    return self.__get_activity_type(elem)
            
            if self.__is_element_gateway(elem):
                try:
                    return self.sanitizer.sanitize_label(self.__get_name(elem))
                except KeyError:
                    return self.__get_gateway_type(elem)

            if self.__is_element_start_event(elem) or self.__is_element_end_event(elem):
                try:
                    return self.sanitizer.sanitize_label(self.__get_name(elem))
                except KeyError:
                    return self.__get_element_type(elem)
        except KeyError:
            return self.__get_element_type(elem)

    def __is_element_start_event(self, elem):
        return self.__get_element_type(elem) in ALLOWED_START_EVENTS

    def __is_element_end_event(self, elem):
        return self.__get_element_type(elem) in ALLOWED_END_EVENTS

    def __is_element_activity(self, elem):
        return self.__get_element_type(elem) in ALLOWED_ACTIVITIES

    def __is_element_gateway(self, elem):
        return self.__get_element_type(elem) in ALLOWED_GATEWAYS

    def __is_predecessor_start_event(self, predecessors):
        for predecessor in predecessors:
            if predecessor:
                predecessor_type = self.__get_element_type(predecessor)
                if predecessor_type in ALLOWED_START_EVENTS and predecessor_type not in DISCARDED_START_EVENT_NAMES:
                    if self.__valid_start_name(predecessor):
                        return False
                    return True
        return False

    def __is_successor_end_event(self, successors):
        for successor in successors:
            if successor:
                if self.__get_element_type(successor) in ALLOWED_END_EVENTS:
                    if self.__valid_end_name(successor):
                        return False
                    return True
        return False

    def count_parsable_elements(self):
        count = 0
        for elem in self.__get_diagram_elements():
            elem_type = self.__get_element_type(elem)
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
            if self.__get_element_type(elem) == "Pool":
                count += 1
        return count
    
    def has_start(self):
        for elem in self.sequence:
            if elem.get("is start"):
                return True
        return False
    
    def get_element_types(self):
        elem_types = {}

        for elem in self.__get_diagram_elements():
            elem_type = self.__get_element_type(elem)

            if elem_type in elem_types:
                elem_types[elem_type] += 1
            else:
                elem_types[elem_type] = 1

        return elem_types
