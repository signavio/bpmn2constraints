# pylint: disable=duplicate-code
"""Test suite for the AND gateway"""
from json import dumps
from expected.expected_and_result import EXPECTED_SINGLE_AND_GATEWAY_RESULT
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens


def test_single_and_gateway():
    """A test for a single AND gateway"""
    test_file_path = "examples/and_gates/single_and.json"
    output = extract_parsed_tokens(test_file_path)

    assert dumps(output, indent=2) == dumps(EXPECTED_SINGLE_AND_GATEWAY_RESULT,
                                            indent=2)
