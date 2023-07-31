from bpmnconstraints.utils.constants import *
DEFAULT_DIRECTION = "LR"
SEQUENCE_FLOW = "-->"
        
class Mermaid:
    def __init__(self, bpmn) -> None:
        self.bpmn = bpmn

    def __gen_flowchart(self):
        pass

    def translate(self):
        rows = []
        for elem in self.bpmn:
            if elem["is start"]:
                rows.extend(self.__create_start_node(elem))
            
            elif elem["type"] in ALLOWED_ACTIVITIES and not elem["is end"]:
                rows.extend(self.__create_activity_node(elem))

            elif elem["type"] in ALLOWED_GATEWAYS:
                rows.extend(self.__create_gateway_node(elem))

        return self.__gen_flowchart(rows)

    def __create_gateway_node(self, elem):
        rows = []
        for successor in elem["successor"]:
            row = ""
            row += self.__gen_gateway_str(elem["id"], elem["name"])
            row += SEQUENCE_FLOW
            if successor["is end"]:
                row += self.__gen_event_str(successor["id"], successor["name"])
            elif successor["type"] in ALLOWED_ACTIVITIES:
                row += self.__gen_activity_str(successor["id"], successor["name"])
            elif successor["type"] in ALLOWED_GATEWAYS:
                row += self.__gen_gateway_str(successor["id"], successor["name"])
            rows.append(row)
        return rows
    
    def __create_activity_node(self, elem):
        rows = []
        for successor in elem["successor"]:
            row = ""
            row += self.__gen_activity_str(elem["id"], elem["name"])
            row += SEQUENCE_FLOW

            if successor["is end"]:
                row += self.__gen_event_str(successor["id"], successor["name"])
            elif successor["type"] in ALLOWED_ACTIVITIES:
                row += self.__gen_activity_str(successor["id"], successor["name"])
            elif successor["type"] in ALLOWED_GATEWAYS:
                row += self.__gen_gateway_str(successor["id"], successor["name"])
            rows.append(row)
        return rows
    
    def __create_start_node(self, elem):
        rows = []
        for succcessor in elem["successor"]:
            row = ""
            row += self.__gen_event_str(elem["id"], elem["name"])
            row += SEQUENCE_FLOW
            row += self.__gen_activity_str(succcessor["id"], succcessor["name"])
            rows.append(row)
        return rows
    
    def __gen_new_id(self):
        pass

    def __gen_flowchart(self, rows):
        flowchart = "flowchart TD\n"
        for row in rows:
            flowchart += f"    {row}\n"
        return flowchart

    def __gen_event_str(self, id, msg):
        return f"{id}(({msg}))"

    def __gen_gateway_str(self, id, msg):
        # Can't use formatted string because of the { } required by mermaid.
        return id + "{" + msg + "}"

    def __gen_activity_str(self, id, msg):
        return f"{id}({msg})"
