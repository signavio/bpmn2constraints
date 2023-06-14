from pathlib import Path
from bpmnconstraints.parser.bpmn_parser import Parser
from bpmnconstraints.utils.script_utils import Setup

def init_test_setup_for_parser(diagram_constant):
    path = Path(diagram_constant.get("path"))
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, True).run()
        return res