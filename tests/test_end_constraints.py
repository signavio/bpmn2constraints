from test_utils import init_test_setup_for_compiler
from file_constants import (
    MULTIPLE_ENDINGS_DIAGRAM,
    LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END,
)


def test_end_constraint_is_generated_when_multiple_endings():
    res = init_test_setup_for_compiler(MULTIPLE_ENDINGS_DIAGRAM)
    expected_ending_constraints = [
        "End[ending one]",
        "End[ending two]",
        "End[ending three]",
    ]
    assert all(constraint in res for constraint in expected_ending_constraints)


def test_end_constraint_is_generated_without_explicit_end_event():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END)
    assert "End[second element]" in res
