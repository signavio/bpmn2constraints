from test_utils import init_test_setup_for_parser

from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
    LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END,
    MULTIPLE_ENDINGS_DIAGRAM,
)


def test_element_is_marked_as_end_if_it_has_no_successors():
    res = init_test_setup_for_parser(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END)
    for elem in res:
        if elem.get("is end"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END.get(
                "end element id"
            )


def test_element_is_marked_as_end_if_successor_is_end_event():
    res = init_test_setup_for_parser(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    for elem in res:
        if elem.get("is end"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END.get(
                "end element id"
            )


def test_all_start_elements_are_marked_as_ending_if_multiple_endings():
    res = init_test_setup_for_parser(MULTIPLE_ENDINGS_DIAGRAM)
    end_count = 0
    for elem in res:
        if elem.get("is end") and elem.get("id") in MULTIPLE_ENDINGS_DIAGRAM.get(
            "ending elements"
        ):
            end_count += 1
    assert end_count == len(MULTIPLE_ENDINGS_DIAGRAM.get("ending elements"))


def test_element_is_marked_as_end_if_it_has_no_successors_xml():
    res = init_test_setup_for_parser(
        LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END, True
    )
    for elem in res:
        if elem.get("is end"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END.get(
                "end element id"
            )


def test_element_is_marked_as_end_if_successor_is_end_event_xml():
    res = init_test_setup_for_parser(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, True)
    for elem in res:
        if elem.get("is end"):
            assert elem.get("id") == LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END.get(
                "end element id"
            )


def test_all_start_elements_are_marked_as_ending_if_multiple_endings_xml():
    res = init_test_setup_for_parser(MULTIPLE_ENDINGS_DIAGRAM, True)
    end_count = 0
    for elem in res:
        if elem.get("is end") and elem.get("id") in MULTIPLE_ENDINGS_DIAGRAM.get(
            "ending elements"
        ):
            end_count += 1
    assert end_count == len(MULTIPLE_ENDINGS_DIAGRAM.get("ending elements"))
