"""Entry point for bpmnsignal command. Verifies argument and runs parser."""
import sys
from pathlib import Path
from json import dumps
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens
from bpmnsignal.compiler.bpmn_element_compiler import compile_parsed_tokens

EXPECTED_ARGS_COUNT = 1


def run():
    """Takes the provided BPMN JSON file and returns a list
    of extracted SIGNAL constraints
    """

    path = Path(sys.argv[1])
    parsed_bpmn = extract_parsed_tokens(path)
    compiled_bpmn = compile_parsed_tokens(parsed_bpmn)
    print(dumps(compiled_bpmn, indent=4))
