from pathlib import Path
from bpmnconstraints.parser.bpmn_parser import Parser
from bpmnconstraints.utils.script_utils import Setup

from file_constants import LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END

def test_element_is_marked_as_start_if_it_has_no_predecessors():
    path = Path(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END.get("path"))
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, False).run()

def test_element_is_marked_as_start_if_predecessor_is_start_event():
    path = Path(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END.get("path"))
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, False).run()
        

def test_all_start_elements_are_marked_as_starts_if_multiple_starts():
    pass