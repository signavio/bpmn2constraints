from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, 
    SINGLE_XOR_GATEWAY_DIAGRAM, 
    XOR_GATEWAY_DIAGRAM
)
from test_utils import init_test_setup_for_compiler

def test_choice_constraint_is_not_generated_for_elements_in_gateway_constructs():
    res = init_test_setup_for_compiler(XOR_GATEWAY_DIAGRAM)
    not_allowed_choice_constraints = [
        "Choice[Second Activity Upper, Third Activity Upper]",
        "Choice[Third Activity Upper, Second Activity Upper]",
        "Choice[Third Activity Upper, Forth Activity Upper]",
        "Choice[Forth Activity Upper, Third Activity Upper]",
        "Choice[Second Activity Lower, Third Activity Lower]",
        "Choice[Third Activity Lower, Second Activity Lower]",
        "Choice[Third Activity Lower, Forth Activity Lower]",
        "Choice[Forth Activity Lower, Third Activity Lower]",
    ]
    assert all(constraint not in res for constraint in not_allowed_choice_constraints)

def test_choice_constraints_generated_for_sequential_flow():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    expected_choice_constraints = [
        "Choice[check invoice, register invoice]",
        "Choice[accept invoice, check invoice]",
    ]
    assert all(constraint in res for constraint in expected_choice_constraints)

def test_succession_constraints_generated_for_sequential_flow():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    expected_succession_constraints = [
        "Succession[register invoice, check invoice]",
        "Succession[check invoice, accept invoice]",
    ]
    assert all(constraint in res for constraint in expected_succession_constraints)

def test_co_existence_constraints_generated_for_sequential_flow():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    expected_co_existence_constraints = [
        "Co-Existence[check invoice, register invoice]",
        "Co-Existence[accept invoice, check invoice]",
    ]
    assert all(constraint in res for constraint in expected_co_existence_constraints) 

def test_no_succession_between_element_and_gateway_element():
    res = init_test_setup_for_compiler(SINGLE_XOR_GATEWAY_DIAGRAM)

    assert "Succession[Zero Activity, First Activity]" not in res
    assert "Succession[Zero Activity, Second Activity]" not in res

def test_no_co_existence_between_element_and_gateway_element():
    res = init_test_setup_for_compiler(SINGLE_XOR_GATEWAY_DIAGRAM)

    assert "Co-Existence[Zero Activity, First Activity]" not in res
    assert "Co-Existence[First Activity, Zero Activity]" not in res