from test_utils import init_test_setup_for_compiler
from file_constants import XOR_GATEWAY_DIAGRAM, XOR_GATEWAY_SEQUENCE_DIAGRAM


def test_response_constraint_is_generated_for_joining_gateway():
    res = init_test_setup_for_compiler(XOR_GATEWAY_DIAGRAM)
    expected_response_constraints = [
        "Response[forth activity upper, last activity]",
        "Response[forth activity lower, last activity]",
        "Alternate Response[forth activity upper, last activity]",
        "Alternate Response[forth activity lower, last activity]",
    ]
    assert all(constraint in res for constraint in expected_response_constraints)


def test_response_constraint_is_generated_for_element_between_two_gateway_constructs():
    res = init_test_setup_for_compiler(XOR_GATEWAY_SEQUENCE_DIAGRAM)
    expected_response_constraints = [
        "Response[activity one, activity three]",
        "Response[activity two, activity three]",
        "Alternate Response[activity one, activity three]",
        "Alternate Response[activity two, activity three]",
    ]
    assert all(constraint in res for constraint in expected_response_constraints)


def test_response_constraint_is_generated_for_joining_gateway_xml():
    res = init_test_setup_for_compiler(XOR_GATEWAY_DIAGRAM, True)
    expected_response_constraints = [
        "Response[forth activity upper, last activity]",
        "Response[forth activity lower, last activity]",
        "Alternate Response[forth activity upper, last activity]",
        "Alternate Response[forth activity lower, last activity]",
    ]
    assert all(constraint in res for constraint in expected_response_constraints)


def test_response_constraint_is_generated_for_element_between_two_gateway_constructs_xml():
    res = init_test_setup_for_compiler(XOR_GATEWAY_SEQUENCE_DIAGRAM, True)
    expected_response_constraints = [
        "Response[activity one, activity three]",
        "Response[activity two, activity three]",
        "Alternate Response[activity one, activity three]",
        "Alternate Response[activity two, activity three]",
    ]
    assert all(constraint in res for constraint in expected_response_constraints)
