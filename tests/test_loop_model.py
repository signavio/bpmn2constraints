# pylint: disable=duplicate-code
# pylint: disable=wildcard-import
"""Test suite for the OR gateway"""
from json import dumps
from expected.expected_loop_result import *
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens
from bpmnsignal.compiler.bpmn_element_compiler import compile_parsed_tokens


def test_parse_single_or_gateway():
    """A test for a single OR gateway"""
    test_file_path = "examples/loops/simple_loop.json"
    output = extract_parsed_tokens(test_file_path)

    assert dumps(output, indent=2) == dumps(EXPECTED_PARSED_SIMPLE_LOOP_RESULT,
                                            indent=2)


def test_compile_single_or_gateway():
    """A test for a single OR gateway"""
    test_file_path = "examples/loops/simple_loop.json"
    parsed_tokens = extract_parsed_tokens(test_file_path)
    output = compile_parsed_tokens(parsed_tokens)

    assert dumps(output,
                 indent=2) == dumps(EXPECTED_COMPILED_SIMPLE_LOOP_RESULT,
                                    indent=2)
