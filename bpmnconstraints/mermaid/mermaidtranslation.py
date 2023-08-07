from bpmnconstraints.utils.constants import *


class Mermaid:
    """
    Converts a parsed BPMN diagram to a format thats interpretable by the Mermaid.js interpreter.
    Prioritizes minimal tokens over readability, thus ID's will be digits, there is no indenting and
    no duplicates of strings.

    #### Example output:
    ```yaml
    flowchart LR
    0((register invoice))-->1(check invoice)
    1-->2((accept invoice))
    ```
    """

    def __init__(self, bpmn) -> None:
        self.bpmn = bpmn
        self.ids = {}
        self.generated_nodes = []

    def translate(self):
        rows = []
        for elem in self.bpmn:
            if elem["is start"]:
                if len(elem["predecessor"]) > 0:
                    for predecessor in elem["predecessor"]:
                        rows.append(
                            f"{self.__match_successor_str(predecessor)}{SEQUENCE_FLOW}{self.__match_successor_str(elem)}"
                        )
                rows.extend(self.__create_node(elem, self.__gen_event_str))

            elif elem["is end"]:
                rows.extend(self.__create_node(elem, self.__gen_event_str))

            elif elem["type"] in ALLOWED_ACTIVITIES and not elem["is end"]:
                rows.extend(self.__create_node(elem, self.__gen_activity_str))

            elif elem["type"] in ALLOWED_GATEWAYS:
                rows.extend(self.__create_node(elem, self.__gen_gateway_str))
        return self.__gen_flowchart(rows)

    def __get_node_name(self, elem):
        if elem["type"] in ALLOWED_GATEWAYS:
            return (
                elem["name"]
                if elem["name"] in GATEWAY_NAMES
                else f"{GATEWAY_MAPPING.get(elem['type'])}: {elem['name']}"
            )
        return elem["name"] if elem["name"] != "" else elem["type"]

    def __match_successor_str(self, successor):
        successor_id = self.__gen_new_id(successor)
        successor_name = self.__get_node_name(successor)
        if successor["type"] in ALLOWED_ACTIVITIES:
            successor_str = self.__gen_activity_str(successor_id, successor_name)
        elif successor["type"] in ALLOWED_GATEWAYS:
            successor_str = self.__gen_gateway_str(successor_id, successor_name)
        elif (
            successor["type"] in ALLOWED_START_EVENTS
            or successor["type"] in ALLOWED_END_EVENTS
        ):
            successor_str = self.__gen_event_str(successor_id, successor_name)
        self.generated_nodes.append(successor_id)
        return successor_str

    def __create_node(self, elem, gen_str_func):
        id = self.__gen_new_id(elem)
        rows = [
            f"{gen_str_func(id, self.__get_node_name(elem))}{SEQUENCE_FLOW}{self.__match_successor_str(successor)}"
            for successor in elem["successor"]
        ]
        self.generated_nodes.append(id)
        return rows

    def __gen_new_id(self, elem):
        id = self.ids.setdefault(elem["id"], str(len(self.ids)))
        id += f":{elem['type']}:"
        return id

    def __gen_flowchart(self, rows):
        flowchart = f"flowchart {DEFAULT_DIRECTION}\n"
        flowchart += "\n".join(rows)
        return flowchart

    def __gen_event_str(self, node_id, msg):
        return node_id if node_id in self.generated_nodes else f"{node_id}(({msg}))"

    def __gen_gateway_str(self, node_id, msg):
        return (
            node_id
            if node_id in self.generated_nodes
            else "{}{{{}}}".format(node_id, msg)  # Can't use f-string 'cus {}.
        )

    def __gen_activity_str(self, node_id, msg):
        return node_id if node_id in self.generated_nodes else f"{node_id}({msg})"
