from json import JSONDecodeError
from pytest import raises
from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
    REQUIREMENTS_TXT,
)
from test_utils import init_test_setup_for_compiler, init_test_setup_for_parser


def test_xml_file_is_identified():
    try:
        xml = init_test_setup_for_compiler(
            LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, test_xml=True
        )
    except JSONDecodeError:
        assert False


def test_unsupported_file_extension_is_rejected():
    with raises(Exception):
        xml = init_test_setup_for_compiler(REQUIREMENTS_TXT, False)


def are_dicts_equal(dict1, dict2, attribute_to_compare):
    if len(dict1) != len(dict2):
        return False

    for item1, item2 in zip(dict1, dict2):
        if item1[attribute_to_compare] != item2[attribute_to_compare]:
            return False

    return True


def test_that_xml_and_json_parsing_generates_same_output():
    json_data = init_test_setup_for_parser(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    xml_data = init_test_setup_for_parser(
        LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, test_xml=True
    )

    assert are_dicts_equal(json_data, xml_data, "name")


def test_that_xml_and_json_compiling_generates_same_output():
    json = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    xml = init_test_setup_for_compiler(
        LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, test_xml=True
    )

    assert sorted(json) == sorted(xml)
