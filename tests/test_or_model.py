# pylint: disable=duplicate-code
# pylint: disable=wildcard-import
"""Test suite for the OR gateway"""

from json import dumps
from expected.expected_or_result import EXPECTED_PARSED_SINGLE_OR_GATEWAY_RESULT
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens


def test_parse_single_or_gateway():
    """A test for a single OR gateway"""
    test_file_path = "examples/or_gates/single_or_gateway.json"
    output = extract_parsed_tokens(test_file_path, True)

    assert dumps(output,
                 indent=2) == dumps(EXPECTED_PARSED_SINGLE_OR_GATEWAY_RESULT,
                                    indent=2)
