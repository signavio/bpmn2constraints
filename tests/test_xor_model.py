"""Test suite for bpmn_parser"""
from bpmnsignal.bpmn_parser import load_bpmn, get_root_element, parse_bpmn

PATHS = [
    'examples/single_xor_gate.json',
    'examples/multiple_xor_gates.json',
    'examples/nested_XOR_gateways.json',
]

SEQUENCES = [
    ['activity0', ['XOR', ['activity2'], ['activity1']], 'activity3'],
    [['XOR', ['activity2'], ['activity1']], 'activity3',
        ['XOR', ['activity4'], ['activity5']]],
    ['0', ['XOR', [['XOR', ['3'], ['4']]], [['XOR', ['1'], ['2']]]], '5']
]


def run_test(bpmn):
    """Runs a test on current JSON object representing a BPMN diagram"""
    visited = set()
    start_element = get_root_element(bpmn)
    path = parse_bpmn(bpmn, [], visited, start_element)
    return path


def test_xor_constraints():
    """Performs three tests:
        1. Single XOR gateway,
        2. Multiple XOR gateways,
        3. Nested XOR gateways

        TODO: Create working XOR constriants.
    """
    for i, path in enumerate(PATHS):
        bpmn = load_bpmn(path)
        sequence = run_test(bpmn)
        assert sequence == SEQUENCES[i]
