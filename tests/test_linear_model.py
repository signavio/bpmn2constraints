# pylint: disable=duplicate-code
"""Test suite for linear sequences"""
from json import dumps
from expected.expected_linear_result import EXPECTED_LINEAR_SEQUENCE_RESULT
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens


def test_linear_diagram():
    """Test for a linear sequence"""
    test_file_path = "examples/linear/linear_sequence.json"
    output = extract_parsed_tokens(test_file_path)

    assert dumps(output, indent=2) == dumps(EXPECTED_LINEAR_SEQUENCE_RESULT,
                                            indent=2)
