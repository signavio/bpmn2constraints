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
        elements = j_bpmn['childShapes']
        sequence = []
        for element in elements:
            if element['stencil']['id'] == 'StartNoneEvent':
                successors = element['outgoing']
                has_successor = len(successors) > 0
                while has_successor:
                    successor = successors[0]['resourceId']
                    element = [element for element in elements if element['resourceId'] == successor][0]
                    if not element['stencil']['id'] in ['SequenceFlow', 'EndNoneEvent']:
                        sequence.append(element['properties']['name'])
                    successors = element['outgoing']
                    has_successor = len(successors) > 0
        print('Sequence: ', sequence)
        print('Constraints: ', construct_linear_constraints(sequence))
