from test_utils import init_test_setup_for_parser

from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
    LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END,
    MULTIPLE_STARTS_DIAGRAM,
)


def test_element_is_marked_as_start_if_it_has_no_predecessors():
    res = init_test_setup_for_parser(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END)
    for elem in res:
        if elem.get("is start"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END.get(
                "start element id"
            )


def test_element_is_marked_as_start_if_predecessor_is_start_event():
    res = init_test_setup_for_parser(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    for elem in res:
        if elem.get("is start"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END.get(
                "start element id"
            )


def test_all_start_elements_are_marked_as_starts_if_multiple_starts():
    res = init_test_setup_for_parser(MULTIPLE_STARTS_DIAGRAM)
    start_count = 0
    for elem in res:
        if elem.get("is start") and elem.get("id") in MULTIPLE_STARTS_DIAGRAM.get(
            "start elements"
        ):
            start_count += 1
    assert start_count == len(MULTIPLE_STARTS_DIAGRAM.get("start elements"))


def test_element_is_marked_as_start_if_it_has_no_predecessors_xml():
    res = init_test_setup_for_parser(
        LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END, True
    )
    for elem in res:
        if elem.get("is start"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END.get(
                "start element id"
            )


def test_element_is_marked_as_start_if_predecessor_is_start_event_xml():
    res = init_test_setup_for_parser(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, True)
    for elem in res:
        if elem.get("is start"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END.get(
                "start element id"
            )


def test_all_start_elements_are_marked_as_starts_if_multiple_starts_xml():
    res = init_test_setup_for_parser(MULTIPLE_STARTS_DIAGRAM, True)
    start_count = 0
    for elem in res:
        if elem.get("is start") and elem.get("id") in MULTIPLE_STARTS_DIAGRAM.get(
            "start elements"
        ):
            start_count += 1
    assert start_count == len(MULTIPLE_STARTS_DIAGRAM.get("start elements"))
