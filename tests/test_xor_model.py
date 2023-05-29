# pylint: disable=duplicate-code
# pylint: disable=wildcard-import
"""Test suite for the XOR gateway"""
from json import dumps
from expected.expected_xor_result import EXPECTED_PARSED_SINGLE_XOR_GATEWAY
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens


def test_parse_single_xor_gateway():
    """Single XOR gateway test"""
    test_file_path = "examples/xor_gates/single_xor.json"
    output = extract_parsed_tokens(test_file_path, True, False)

    assert dumps(output, indent=2) == dumps(EXPECTED_PARSED_SINGLE_XOR_GATEWAY,
                                            indent=2)
