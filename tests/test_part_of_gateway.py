from file_constants import PARALLEL_GATEWAY_DIAGRAM
from test_utils import init_test_setup_for_parser


def test_element_in_gateway_construct_is_marked_as_part_of_gateway():
    res = init_test_setup_for_parser(PARALLEL_GATEWAY_DIAGRAM)
    num_elems_in_gateway = 0
    for elem in res:
        if elem.get("id") in PARALLEL_GATEWAY_DIAGRAM.get("gateway elements"):
            num_elems_in_gateway += 1
    assert num_elems_in_gateway == len(PARALLEL_GATEWAY_DIAGRAM.get("gateway elements"))


def test_element_outside_gateway_construct_is_not_marked_as_part_of_gateway():
    res = init_test_setup_for_parser(PARALLEL_GATEWAY_DIAGRAM)
    num_elems_not_in_gateway = 0
    for elem in res:
        if elem.get("id") in PARALLEL_GATEWAY_DIAGRAM.get("not gateway elements"):
            num_elems_not_in_gateway += 1
    assert num_elems_not_in_gateway == len(
        PARALLEL_GATEWAY_DIAGRAM.get("not gateway elements")
    )


def test_element_in_gateway_construct_is_marked_as_part_of_gateway_xml():
    res = init_test_setup_for_parser(PARALLEL_GATEWAY_DIAGRAM, True)
    num_elems_in_gateway = 0
    for elem in res:
        if elem.get("id") in PARALLEL_GATEWAY_DIAGRAM.get("gateway elements"):
            num_elems_in_gateway += 1
    assert num_elems_in_gateway == len(PARALLEL_GATEWAY_DIAGRAM.get("gateway elements"))


def test_element_outside_gateway_construct_is_not_marked_as_part_of_gateway_xml():
    res = init_test_setup_for_parser(PARALLEL_GATEWAY_DIAGRAM, True)
    num_elems_not_in_gateway = 0
    for elem in res:
        if elem.get("id") in PARALLEL_GATEWAY_DIAGRAM.get("not gateway elements"):
            num_elems_not_in_gateway += 1
    assert num_elems_not_in_gateway == len(
        PARALLEL_GATEWAY_DIAGRAM.get("not gateway elements")
    )
