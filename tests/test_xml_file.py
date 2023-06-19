from json import JSONDecodeError
from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END_XML,
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
)

from test_utils import init_test_setup_for_compiler


def test_xml_file_is_identified():
    try:
        xml = init_test_setup_for_compiler(
            LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END_XML
        )
    except JSONDecodeError:
        assert False


def test_that_xml_and_json_parsing_generates_same_output():
    json = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    xml = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END_XML)

    assert sorted(json) == sorted(xml)
