from file_constants import SINGLE_XOR_GATEWAY_DIAGRAM, THREE_SPLIT_XOR_GATEWAY_DIAGRAM
from test_utils import init_test_setup_for_parser


def test_element_is_marked_as_splitting_gateway_if_it_is_splitting():
    res = init_test_setup_for_parser(SINGLE_XOR_GATEWAY_DIAGRAM)
    for elem in res:
        if elem.get("id") == SINGLE_XOR_GATEWAY_DIAGRAM.get("splitting id"):
            assert elem.get("splitting")


def test_element_is_marked_as_joining_gateway_if_it_is_joining():
    res = init_test_setup_for_parser(SINGLE_XOR_GATEWAY_DIAGRAM)
    for elem in res:
        if elem.get("id") == SINGLE_XOR_GATEWAY_DIAGRAM.get("joining id"):
            assert elem.get("joining")


def test_gateway_splitting_to_three_paths():
    res = init_test_setup_for_parser(THREE_SPLIT_XOR_GATEWAY_DIAGRAM)
    for elem in res:
        if elem.get("id") == THREE_SPLIT_XOR_GATEWAY_DIAGRAM.get("splitting id"):
            successors_id = [x.get("id") for x in elem.get("successor")]
            assert sorted(successors_id) == sorted(
                THREE_SPLIT_XOR_GATEWAY_DIAGRAM.get("successors")
            )


def test_element_is_marked_as_splitting_gateway_if_it_is_splitting_xml():
    res = init_test_setup_for_parser(SINGLE_XOR_GATEWAY_DIAGRAM, True)
    for elem in res:
        if elem.get("id") == SINGLE_XOR_GATEWAY_DIAGRAM.get("splitting id"):
            assert elem.get("splitting")


def test_element_is_marked_as_joining_gateway_if_it_is_joining_xml():
    res = init_test_setup_for_parser(SINGLE_XOR_GATEWAY_DIAGRAM, True)
    for elem in res:
        if elem.get("id") == SINGLE_XOR_GATEWAY_DIAGRAM.get("joining id"):
            assert elem.get("joining")


def test_gateway_splitting_to_three_paths_xml():
    res = init_test_setup_for_parser(THREE_SPLIT_XOR_GATEWAY_DIAGRAM, True)
    for elem in res:
        if elem.get("id") == THREE_SPLIT_XOR_GATEWAY_DIAGRAM.get("splitting id"):
            successors_id = [x.get("id") for x in elem.get("successor")]
            assert sorted(successors_id) == sorted(
                THREE_SPLIT_XOR_GATEWAY_DIAGRAM.get("successors")
            )
