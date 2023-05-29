# pylint: disable=duplicate-code
# pylint: disable=wildcard-import
"""Test suite for linear sequences"""
from json import dumps
from expected.expected_linear_result import EXPECTED_PARSED_LINEAR_SEQUENCE_RESULT
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens


def test_parse_linear_sequence():
    """Test for a linear sequence"""
    test_file_path = "examples/linear/linear_sequence.json"
    output = extract_parsed_tokens(test_file_path, True, False)

    assert dumps(output,
                 indent=2) == dumps(EXPECTED_PARSED_LINEAR_SEQUENCE_RESULT,
                                    indent=2)
