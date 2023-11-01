from test_utils import init_test_setup_for_compiler
from file_constants import XOR_GATEWAY_DIAGRAM, XOR_GATEWAY_SEQUENCE_DIAGRAM


def test_precedence_constraint_is_generated_for_splitting_gateway():
    res = init_test_setup_for_compiler(XOR_GATEWAY_DIAGRAM)
    expected_precedence_constraints = [
        "Precedence[first activity, second activity upper]",
        "Precedence[first activity, second activity lower]",
        "Alternate Precedence[first activity, second activity upper]",
        "Alternate Precedence[first activity, second activity lower]",
    ]
    assert all(constraint in res for constraint in expected_precedence_constraints)


def test_precedence_constraint_is_generated_for_element_between_two_gateway_constructs():
    res = init_test_setup_for_compiler(XOR_GATEWAY_SEQUENCE_DIAGRAM)
    expected_precedence_constraints = [
        "Precedence[activity three, activity four]",
        "Precedence[activity three, activity five]",
        "Alternate Precedence[activity three, activity four]",
        "Alternate Precedence[activity three, activity five]",
    ]
    assert all(constraint in res for constraint in expected_precedence_constraints)


def test_precedence_constraint_is_generated_for_splitting_gateway_xml():
    res = init_test_setup_for_compiler(XOR_GATEWAY_DIAGRAM, True)
    expected_precedence_constraints = [
        "Precedence[first activity, second activity upper]",
        "Precedence[first activity, second activity lower]",
        "Alternate Precedence[first activity, second activity upper]",
        "Alternate Precedence[first activity, second activity lower]",
    ]
    assert all(constraint in res for constraint in expected_precedence_constraints)


def test_precedence_constraint_is_generated_for_element_between_two_gateway_constructs_xml():
    res = init_test_setup_for_compiler(XOR_GATEWAY_SEQUENCE_DIAGRAM, True)
    expected_precedence_constraints = [
        "Precedence[activity three, activity four]",
        "Precedence[activity three, activity five]",
        "Alternate Precedence[activity three, activity four]",
        "Alternate Precedence[activity three, activity five]",
    ]
    assert all(constraint in res for constraint in expected_precedence_constraints)
