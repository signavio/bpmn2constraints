from bpmnconstraints.utils.constants import *

DEFAULT_DIRECTION = "LR"
SEQUENCE_FLOW = "-->"


class Mermaid:
    def __init__(self, bpmn) -> None:
        self.bpmn = bpmn
        self.ids = {}

    def translate(self):
        rows = []
        for elem in self.bpmn:
            if elem["is start"]:
                rows.extend(self.__create_node(elem, self.__gen_event_str))

            elif elem["type"] in ALLOWED_ACTIVITIES and not elem["is end"]:
                rows.extend(self.__create_node(elem, self.__gen_activity_str))

            elif elem["type"] in ALLOWED_GATEWAYS:
                rows.extend(self.__create_node(elem, self.__gen_gateway_str))

        return self.__gen_flowchart(rows)

    def __get_node_name(self, elem):
        successor_name = elem["name"]
        if successor_name == "":
            successor_name = elem["type"]
        return successor_name

    def __match_successor_str(self, successor):
        successor_id = self.__gen_new_id(successor["id"])
        successor_name = self.__get_node_name(successor)
        if successor["is end"]:
            return self.__gen_event_str(successor_id, successor_name)
        elif successor["type"] in ALLOWED_ACTIVITIES:
            return self.__gen_activity_str(successor_id, successor_name)
        elif successor["type"] in ALLOWED_GATEWAYS:
            return self.__gen_gateway_str(successor_id, successor_name)

    def __create_node(self, elem, gen_str_func):
        rows = []
        for successor in elem["successor"]:
            node_id = self.__gen_new_id(elem["id"])
            node_name = self.__get_node_name(elem)
            row = f"{gen_str_func(node_id, node_name)}{SEQUENCE_FLOW}{self.__match_successor_str(successor)}"
            rows.append(row)
        return rows

    def __gen_new_id(self, old_id):
        if old_id not in self.ids:
            index = len(self.ids)
            self.ids[old_id] = "id" + str(index)
        return self.ids[old_id]

    def __gen_flowchart(self, rows):
        flowchart = f"flowchart {DEFAULT_DIRECTION}\n"
        for row in rows:
            flowchart += f"    {row}\n"
        return flowchart

    def __gen_event_str(self, node_id, msg):
        return f"{node_id}(({msg}))"

    def __gen_gateway_str(self, node_id, msg):
        return "{}{{{}}}".format(node_id, msg)

    def __gen_activity_str(self, node_id, msg):
        return f"{node_id}({msg})"
