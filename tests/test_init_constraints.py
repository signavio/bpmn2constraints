from test_utils import init_test_setup_for_compiler
from file_constants import LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END, MULTIPLE_STARTS_DIAGRAM

def test_init_constraint_is_generated_without_explicit_start_event():
    res = init_test_setup_for_compiler(LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END)
    assert "Init[first element]" in res

def test_that_each_start_has_init_constraint():
    res = init_test_setup_for_compiler(MULTIPLE_STARTS_DIAGRAM)
    assert ["Init[path one]", "Init[path two]"] == res