from test_utils import init_test_setup_for_compiler
from file_constants import THREE_SPLIT_XOR_GATEWAY_DIAGRAM


def test_that_all_gateway_constraints_are_generated():
    res = init_test_setup_for_compiler(THREE_SPLIT_XOR_GATEWAY_DIAGRAM)
    expected_gateway_constraints = [
        "Exclusive Choice[activity four, activity two]",
        "Exclusive Choice[activity three, activity two]",
        "Exclusive Choice[activity three, activity four]",
    ]
    # assert res == expected_gateway_constraints
    assert all(constraint in res for constraint in expected_gateway_constraints)


def test_that_all_gateway_constraints_are_generated_XML():
    res = init_test_setup_for_compiler(THREE_SPLIT_XOR_GATEWAY_DIAGRAM, True)
    expected_gateway_constraints = [
        "Exclusive Choice[activity four, activity two]",
        "Exclusive Choice[activity three, activity two]",
        "Exclusive Choice[activity three, activity four]",
    ]
    assert all(constraint in res for constraint in expected_gateway_constraints)
