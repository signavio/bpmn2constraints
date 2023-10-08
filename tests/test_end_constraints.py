from test_utils import init_test_setup_for_compiler, init_test_setup_for_parser
from file_constants import (
    MULTIPLE_ENDINGS_DIAGRAM,
    LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END,
    XOR_GATEWAY_SEQUENCE_DIAGRAM,
    LINEAR_MERMAID_GRAPH,
)


def test_end_constraint_is_generated_when_multiple_endings():
    res = init_test_setup_for_compiler(MULTIPLE_ENDINGS_DIAGRAM)
    expected_ending_constraints = [
        "End[ending one]",
        "End[ending two]",
        "End[ending three]",
    ]
    assert all(constraint in res for constraint in expected_ending_constraints)

def test_end_constraint_is_generated_with_linear_parser():
    res = init_test_setup_for_parser(LINEAR_MERMAID_GRAPH)
    assert res[-1]["is end"] == True


def test_end_constraint_is_generated_without_explicit_end_event():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END)
    assert "End[second element]" in res


def test_end_constraint_is_generated_when_multiple_endings():
    res = init_test_setup_for_parser(XOR_GATEWAY_SEQUENCE_DIAGRAM)

    assert res[-1]["is end"] and res[-2]["is end"] and not res[3]["is end"]


def test_end_constraint_is_generated_when_xor_gateway():
    res = init_test_setup_for_compiler(XOR_GATEWAY_SEQUENCE_DIAGRAM)
    expected_ending_constraints = [
        "End[activity four]",
        "End[activity five]",
    ]
    assert all(constraint in res for constraint in expected_ending_constraints)
