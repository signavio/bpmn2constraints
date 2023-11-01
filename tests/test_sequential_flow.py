from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
    SINGLE_XOR_GATEWAY_DIAGRAM,
    XOR_GATEWAY_DIAGRAM,
)
from test_utils import init_test_setup_for_compiler


def test_choice_constraint_is_not_generated_for_elements_in_gateway_constructs():
    res = init_test_setup_for_compiler(XOR_GATEWAY_DIAGRAM)
    not_allowed_choice_constraints = [
        "Choice[second Activity Upper, third Activity Upper]",
        "Choice[third Activity Upper, second Activity Upper]",
        "Choice[third Activity Upper, forth Activity Upper]",
        "Choice[forth Activity Upper, third Activity Upper]",
        "Choice[second Activity Lower, third Activity Lower]",
        "Choice[third Activity Lower, second Activity Lower]",
        "Choice[third Activity Lower, forth Activity Lower]",
        "Choice[forth Activity Lower, third Activity Lower]",
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

    assert "Succession[zero Activity, first Activity]" not in res
    assert "Succession[zero Activity, second Activity]" not in res


def test_no_co_existence_between_element_and_gateway_element():
    res = init_test_setup_for_compiler(SINGLE_XOR_GATEWAY_DIAGRAM)

    assert "Co-Existence[zero Activity, first Activity]" not in res
    assert "Co-Existence[first Activity, zero Activity]" not in res


def test_choice_constraints_generated_for_sequential_flow_xml():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, True)
    expected_choice_constraints = [
        "Choice[check invoice, register invoice]",
        "Choice[accept invoice, check invoice]",
    ]
    assert all(constraint in res for constraint in expected_choice_constraints)


def test_succession_constraints_generated_for_sequential_flow_xml():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, True)
    expected_succession_constraints = [
        "Succession[register invoice, check invoice]",
        "Succession[check invoice, accept invoice]",
    ]
    assert all(constraint in res for constraint in expected_succession_constraints)


def test_co_existence_constraints_generated_for_sequential_flow_xml():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END, True)
    expected_co_existence_constraints = [
        "Co-Existence[check invoice, register invoice]",
        "Co-Existence[accept invoice, check invoice]",
    ]
    assert all(constraint in res for constraint in expected_co_existence_constraints)


def test_no_succession_between_element_and_gateway_element_xml():
    res = init_test_setup_for_compiler(SINGLE_XOR_GATEWAY_DIAGRAM, True)

    assert "Succession[zero Activity, first Activity]" not in res
    assert "Succession[zero Activity, second Activity]" not in res


def test_no_co_existence_between_element_and_gateway_element_xml():
    res = init_test_setup_for_compiler(SINGLE_XOR_GATEWAY_DIAGRAM)

    assert "Co-Existence[zero Activity, first Activity]" not in res
    assert "Co-Existence[first Activity, zero Activity]" not in res
