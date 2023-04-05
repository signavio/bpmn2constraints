"""
Module for parsing JSON objects in Signavio's propertiery format.
"""
import json

GATEWAYS = ['Exclusive_Databased_Gateway',
            'ParallelGateway', 'InclusiveGateway']
TASK = 'Task'
START = 'StartNoneEvent'
END = 'EndNoneEvent'
EXPECTED_ARGS_COUNT = 1
RIGHT = 0
LEFT = 1
GATEWAY_IDX = 0


def verify_bpmn(bpmn):
    """Verifies format of the BPMN diagram."""

    has_start = False
    has_end = False
    splitting_gateways = 0
    joining_gateways = 0

    for element in get_bpmn_elements(bpmn):
        if not has_start and get_element_type(element) == START:
            has_start = True

        if not has_end and get_element_type(element) == END:
            has_end = True

        if get_element_type(element) in GATEWAYS and gateway_is_splitting(element):
            splitting_gateways += 1

        if get_element_type(element) in GATEWAYS and gateway_is_joining(element):
            joining_gateways += 1

    if has_start:
        print(f'has_start: {has_start}')
    else:
        raise SystemExit(2)

    print(f'has_end: {has_end}')
    print(f'balanced gateways: {splitting_gateways-joining_gateways == 0}')


def visit_element(element, visited):
    """Adds current elements id to the visited list"""

    visited.add(get_element_id(element))


def element_is_visited(element, visited):
    """Checks if current elemented is in visited list"""

    return get_element_id(element) in visited


def all_elements_is_visited(bpmn, visited):
    """Checks whether we visited all elements in diagram"""

    return len(get_bpmn_elements(bpmn)) == len(visited)


def gateway_is_splitting(element):
    """Checks if gateway element is splitting"""

    return get_number_of_successors(element) >= 2


def gateway_is_joining(element):
    """Checks if gateway element is joining"""

    return get_number_of_successors(element) == 1


def is_task(element):
    """Checks if element is a task"""

    return get_element_type(element) == TASK


def is_gateway(element):
    """Checks if element is a gateway"""

    return get_element_type(element) in GATEWAYS


def get_number_of_successors(element):
    """Gets the number of successors of element"""

    return len(get_element_successors(element))


def get_element_successors(element):
    """Gets a list of successors to element"""

    return element['outgoing']


def get_element_id(element):
    """Gets the id of current element"""

    return element['resourceId']


def get_element_type(element):
    """Gets the type of the element, i.e., Task."""

    return element['stencil']['id']


def get_bpmn_elements(bpmn):
    """Gets all elements from JSON object"""

    return bpmn['childShapes']


def get_root_element(bpmn):
    """Gets the element in diagram marked as start"""

    return next(
        element for element in get_bpmn_elements(bpmn) if get_element_type(element) == START)


def get_list_type(sequence):
    """Gets the of gateway the list belongs to"""
    gateway_type = sequence[GATEWAY_IDX]
    return gateway_type


def get_element_by_id(successor_element_id, bpmn):
    """Gets element by id"""

    return next(
        (
            element for element in get_bpmn_elements(bpmn)
            if get_element_id(element) == successor_element_id
        ), None)


def get_gateway_outgoing_elements(bpmn, element):
    """Gets outgoing elements to the left and right of gateway"""

    return [get_element_by_id(get_element_id(
        successor), bpmn) for successor in get_element_successors(element)]


def load_bpmn(path):
    """Loads the JSON file containing the diagram"""

    with open(path, "r", encoding='utf-8') as file:
        return json.load(file)


def add_to_path(path, element):
    """If element is a task, add its name to path"""

    if is_task(element):
        path.append(element['properties']['name'])


def handle_gateway_split(bpmn, element, path, visited):
    """Handles a gateway split"""
    if get_element_type(element) == GATEWAYS[0]:
        handle_gateway(bpmn, element, path, visited, 'XOR')

    if get_element_type(element) == GATEWAYS[1]:
        handle_gateway(bpmn, element, path, visited, 'AND')

    if get_element_type(element) == GATEWAYS[2]:
        handle_gateway(bpmn, element, path, visited, 'OR')


def traverse_outgoing_path(bpmn, element, path, visited):
    """Traverses an internal path"""

    if is_gateway(element):
        if gateway_is_splitting(element):
            handle_gateway_split(bpmn, element, path, visited)

        elif gateway_is_joining(element):
            return path

    if not element_is_visited(element, visited):
        add_to_path(path, element)
        visit_element(element, visited)

    successor = get_element_by_id(
        get_element_id(get_element_successors(element)[0]), bpmn)

    return traverse_outgoing_path(bpmn, successor, path, visited)


def generate_left_and_right_paths(bpmn, element, visited):
    """Traverses the right and left paths."""
    successors = get_gateway_outgoing_elements(bpmn, element)
    right_path = []
    left_path = []

    right_path = traverse_outgoing_path(bpmn,
                                        successors[RIGHT], right_path, visited)
    left_path = traverse_outgoing_path(bpmn,
                                       successors[LEFT], left_path, visited)

    return right_path, left_path


def handle_gateway(bpmn, element, path, visited, gateway_type):
    """Explores both outgoing AND paths and adds them to path."""
    successors = get_gateway_outgoing_elements(bpmn, element)

    paths = []
    for successor in successors:
        alt_path = []
        alt_path = traverse_outgoing_path(
            bpmn, successor, alt_path, visited)
        if not alt_path:
            continue
        paths.append(alt_path)

    if paths:
        paths.insert(0, gateway_type)
        path.append(paths)


def parse_bpmn(bpmn, path, visited, element):
    """Parses the BPMN diagram"""

    if get_element_type(element) == END and all_elements_is_visited(bpmn, visited):
        return path

    if is_gateway(element) and gateway_is_splitting(element):
        handle_gateway_split(bpmn, element, path, visited)

    elif not element_is_visited(element, visited):
        add_to_path(path, element)
        visit_element(element, visited)

    successors = get_element_successors(element)
    if successors:
        successor_id = get_element_id(successors[0])
        successor = get_element_by_id(successor_id, bpmn)
        return parse_bpmn(bpmn, path, visited, successor)
    return path


def create_json_task(element):
    """Creates a JSON task element"""
    return {"type": "task", "name": element}


def create_json_gateway(gateway_type):
    """Creates a JSON gateway element"""
    return {"type": "gateway",
            "gatewaytype": gateway_type, "children": []}


def generate_json_from_sequence(path):
    """Generates a JSON object based upon a sequence list."""
    sequence = []
    for element in path:
        if isinstance(element, str):
            task = create_json_task(element)
            sequence.append(task)

        elif isinstance(element, list) and element[0] not in ['XOR', 'AND', 'OR']:
            task = create_json_task(element[0])
            sequence.append([task])

        elif isinstance(element, list) and element[0] in ['XOR', 'AND', 'OR']:
            gateway_type = element[0]
            gateway = create_json_gateway(gateway_type)
            for gateway_list in element[1:]:
                child_sequence = generate_json_from_sequence(gateway_list)
                gateway['children'].append(child_sequence)
            sequence.append(gateway)
    return sequence


def list_to_string(sequence):
    """Converts a list to a string"""
    if isinstance(sequence, str):
        return sequence
    if isinstance(sequence, list):
        return "[" + ", ".join([list_to_string(x) for x in sequence]) + "]"
    return str(sequence)


def generate_sequence(path):
    """Generates a sequence"""
    bpmn = load_bpmn(path)
    verify_bpmn(bpmn)
    visited = set()
    start_element = get_root_element(bpmn)
    sequence = parse_bpmn(bpmn, [], visited, start_element)

    json_output = {
        "path": list_to_string(sequence),
        "sequence": generate_json_from_sequence(sequence)
    }

    return sequence, json_output
