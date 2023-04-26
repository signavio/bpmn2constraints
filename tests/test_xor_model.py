# pylint: disable=too-many-lines
# pylint: disable=duplicate-code
"""Test suite for the XOR gateway"""
from json import dumps
from expected.expected_xor_result import EXPECTED_SINGLE_XOR_GATEWAY
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens


def test_single_xor_gateway():
    """Single XOR gateway test"""
    test_file_path = "examples/xor_gates/single_xor.json"
    output = extract_parsed_tokens(test_file_path)

    assert dumps(output, indent=2) == dumps(EXPECTED_SINGLE_XOR_GATEWAY,
                                            indent=2)
