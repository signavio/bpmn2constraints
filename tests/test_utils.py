from pathlib import Path
from bpmnconstraints.parser.bpmn_parser import Parser
from bpmnconstraints.compiler.bpmn_compiler import Compiler
from bpmnconstraints.utils.script_utils import Setup


def init_test_setup_for_parser(diagram_constant):
    path = Path(diagram_constant.get("path"))
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, True).run()
        return res


def init_test_setup_for_compiler(diagram_constant):
    path = Path(diagram_constant.get("path"))
    constraints = []
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, False).run()
        res = Compiler(res, True, False).run()
        for con in res:
            constraints.append(con.get("DECLARE"))
        return constraints
