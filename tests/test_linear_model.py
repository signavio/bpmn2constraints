# pylint: disable=duplicate-code
# pylint: disable=wildcard-import
"""Test suite for linear sequences"""
from json import dumps
from expected.expected_linear_result import *
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens
from bpmnsignal.compiler.bpmn_element_compiler import compile_parsed_tokens


def test_parse_linear_sequence():
    """Test for a linear sequence"""
    test_file_path = "examples/linear/linear_sequence.json"
    output = extract_parsed_tokens(test_file_path)

    assert dumps(output,
                 indent=2) == dumps(EXPECTED_PARSED_LINEAR_SEQUENCE_RESULT,
                                    indent=2)


def test_compile_linear_sequence():
    """Test for a linear sequence"""
    test_file_path = "examples/linear/linear_sequence.json"
    parsed_tokens = extract_parsed_tokens(test_file_path)
    output = compile_parsed_tokens(parsed_tokens)

    assert dumps(output,
                 indent=2) == dumps(EXPECTED_COMPILED_LINEAR_SEQUENCE_RESULT,
                                    indent=2)
