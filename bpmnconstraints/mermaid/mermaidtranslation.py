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
        self.styles = []
        self.generated_nodes = []

    def translate(self):
        rows = []
        for elem in self.bpmn:
            if elem["is start"]:
                rows.extend(self.__create_node(elem, self.__gen_event_str))

            elif elem["type"] in ALLOWED_ACTIVITIES and not elem["is end"]:
                rows.extend(self.__create_node(elem, self.__gen_activity_str))

            elif elem["type"] in ALLOWED_GATEWAYS:
                rows.extend(self.__create_node(elem, self.__gen_gateway_str))

        # Add styles in the end, less messy for humans to read.
        # rows.append(END_EVENT_STYLING_DEF)
        return self.__gen_flowchart(rows)

    def __get_node_name(self, elem):
        name = elem["name"]
        if name == "":
            name = elem["type"]
        return name

    def __match_successor_str(self, successor):
        successor_id = self.__gen_new_id(successor["id"])
        successor_name = self.__get_node_name(successor)
        if successor["is end"]:
            if successor["type"] in ALLOWED_GATEWAYS:
                successor_str = self.__gen_gateway_str(successor_id, successor_name)
            else:
                successor_str = self.__gen_event_str(
                    successor_id, successor_name
                )  # + END_EVENT_STYLE
        elif successor["type"] in ALLOWED_ACTIVITIES:
            successor_str = self.__gen_activity_str(successor_id, successor_name)
        elif successor["type"] in ALLOWED_GATEWAYS:
            successor_str = self.__gen_gateway_str(successor_id, successor_name)
        self.generated_nodes.append(successor_id)
        return successor_str

    def __create_node(self, elem, gen_str_func):
        rows = []
        for successor in elem["successor"]:
            node_id = self.__gen_new_id(elem["id"])
            node_name = self.__get_node_name(elem)
            rows.append(
                f"{gen_str_func(node_id, node_name)}{SEQUENCE_FLOW}{self.__match_successor_str(successor)}"
            )
            self.generated_nodes.append(node_id)
        return rows

    def __gen_new_id(self, old_id):
        if old_id not in self.ids:
            index = len(self.ids)
            self.ids[old_id] = str(index)
        return self.ids[old_id]

    def __gen_flowchart(self, rows):
        flowchart = f"flowchart {DEFAULT_DIRECTION}\n"
        for row in rows:
            # Skip indent to minimise use of tokens, as it's not required by the mermaid interpreter.
            flowchart += f"{row}\n"
        return flowchart

    def __gen_event_str(self, node_id, msg):
        if node_id in self.generated_nodes:
            return node_id
        return f"{node_id}(({msg}))"

    def __gen_gateway_str(self, node_id, msg):
        if node_id in self.generated_nodes:
            return node_id
        return "{}{{{}}}".format(node_id, msg)

    def __gen_activity_str(self, node_id, msg):
        if node_id in self.generated_nodes:
            return node_id
        return f"{node_id}({msg})"
