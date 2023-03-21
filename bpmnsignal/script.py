import json, sys
from pathlib import Path
from bpmnsignal.bpmnsignal import *

expected_args_count = 1

def run():
    """ Takes the provided BPMN JSON file and returns a list
    of extracted SIGNAL constraints

    Raises:
        SystemExit: Incorrect number of arguments provided
    """
    if not len(sys.argv) == expected_args_count + 1:
        print(f'Expected {expected_args_count} arg(s), got {len(sys.argv) - 1}')
        raise SystemExit(2)

    path = Path(sys.argv[1])
    with open(path, 'r') as file:
        j_bpmn = json.loads(file.read())
        sequence = parse_bpmn(j_bpmn)
        print('Sequence: ', sequence)
        print('Constraints: ', construct_linear_constraints(sequence))
