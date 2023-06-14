from pathlib import Path
from bpmnconstraints.parser.bpmn_parser import Parser
from bpmnconstraints.utils.script_utils import Setup

from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
    LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END,
    MULTIPLE_STARTS_DIAGRAM,
)

def init_test_setup(diagram_constant):
    path = Path(diagram_constant.get("path"))
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, False).run()
        return res
    
def test_element_is_marked_as_start_if_it_has_no_predecessors():
    res = init_test_setup(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END)
    for elem in res:
        if elem.get("is start"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END.get("start element id")

def test_element_is_marked_as_start_if_predecessor_is_start_event():
    res = init_test_setup(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    for elem in res:
        if elem.get("is start"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END.get("start element id")


def test_all_start_elements_are_marked_as_starts_if_multiple_starts():
    res = init_test_setup(MULTIPLE_STARTS_DIAGRAM)
    start_count = 0
    for elem in res:
        if elem.get("is start") and elem.get("id") in MULTIPLE_STARTS_DIAGRAM.get("start elements"):
            start_count += 1
    assert start_count == len(MULTIPLE_STARTS_DIAGRAM.get("start elements"))