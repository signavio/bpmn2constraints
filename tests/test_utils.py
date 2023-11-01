from pathlib import Path
from bpmnconstraints.parser.bpmn_parser import Parser
from bpmnconstraints.compiler.bpmn_compiler import Compiler
from bpmnconstraints.utils.script_utils import Setup
from bpmnconstraints.mermaid.mermaidtranslation import Mermaid


def init_test_setup_for_parser(diagram_constant, test_xml=False):
    path = Path(diagram_constant["xmlpath" if test_xml else "path"])
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, True).run()
        return res


def init_test_setup_for_compiler(diagram_constant, test_xml=False):
    path = Path(diagram_constant["xmlpath" if test_xml else "path"])
    constraints = []
    setup = Setup(None)
    if setup.is_file(path):
        res = Parser(path, True, False).run()
        res = Compiler(res, True, False).run()
        for con in res:
            constraints.append(con.get("DECLARE"))
        return constraints


def init_test_setup_for_mermaid(diagram_constant, test_xml=False):
    path = Path(diagram_constant["xmlpath" if test_xml else "path"])
    setup = Setup(None)
    if setup.is_file(path):
        bpmn = Parser(path, True, False).run()
        return Mermaid(bpmn).translate()
