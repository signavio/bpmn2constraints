from test_utils import init_test_setup_for_compiler, init_test_setup_for_parser
from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END,
    MULTIPLE_STARTS_DIAGRAM,
    XOR_GATEWAY_SEQUENCE_DIAGRAM,
)


def test_init_constraint_is_generated_without_explicit_start_event():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END)
    assert "Init[first element]" in res


def test_that_each_start_has_init_constraint():
    res = init_test_setup_for_compiler(MULTIPLE_STARTS_DIAGRAM)
    expected_init_constraints = ["Init[path one]", "Init[path two]"]
    assert all(constraint in res for constraint in expected_init_constraints)


def test_missing_init_constraints_for_XOR_gate_parser():
    res = init_test_setup_for_parser(XOR_GATEWAY_SEQUENCE_DIAGRAM)
    assert res[4]["is start"] and res[5]["is start"] and not res[0]["is start"]


def test_missing_init_constraints_for_XOR_gate():
    res = init_test_setup_for_compiler(XOR_GATEWAY_SEQUENCE_DIAGRAM)
    expected_init_constraints = [
        "Init[activity one]",
        "Init[activity two]",
    ]
    assert all(constraint in res for constraint in expected_init_constraints)


def test_init_constraint_is_generated_without_explicit_start_event_xml():
    res = init_test_setup_for_compiler(
        LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END, True
    )
    assert "Init[first element]" in res


def test_that_each_start_has_init_constraint_xml():
    res = init_test_setup_for_compiler(MULTIPLE_STARTS_DIAGRAM, True)
    expected_init_constraints = ["Init[path one]", "Init[path two]"]
    assert all(constraint in res for constraint in expected_init_constraints)


def test_missing_init_constraints_for_XOR_gate_parser_xml():
    res = init_test_setup_for_parser(XOR_GATEWAY_SEQUENCE_DIAGRAM, True)
    assert res[4]["is start"] and res[5]["is start"] and not res[0]["is start"]


def test_missing_init_constraints_for_XOR_gate_xml():
    res = init_test_setup_for_compiler(XOR_GATEWAY_SEQUENCE_DIAGRAM, True)
    expected_init_constraints = [
        "Init[activity one]",
        "Init[activity two]",
    ]
    assert all(constraint in res for constraint in expected_init_constraints)
