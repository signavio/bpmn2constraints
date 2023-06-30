from json import JSONDecodeError
from pytest import raises
from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END_XML,
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
    REQUIREMENTS_TXT,
)
from test_utils import init_test_setup_for_compiler


def test_xml_file_is_identified():
    try:
        xml = init_test_setup_for_compiler(
            LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END_XML
        )
    except JSONDecodeError:
        assert False


def test_unsupported_file_extension_is_rejected():
    with raises(Exception):
        xml = init_test_setup_for_compiler(REQUIREMENTS_TXT)


def test_that_xml_and_json_parsing_generates_same_output():
    json = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    xml = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END_XML)

    assert sorted(json) == sorted(xml)
