"""Module for extracting element tokens from a BPMN diagram."""

# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code
# pylint: disable=wildcard-import
# pylint: disable=broad-exception-raised

from json import load, JSONDecodeError
from collections import Counter
from bpmnsignal.utils.constants import *


def find_successors(elem,
                    bpmn,
                    successors,
                    seen,
                    predecessor,
                    behind_gateway=False):
    """
    Finds the next successor that is an activity from current element.
    """

    successor = get_next_element(elem, bpmn)

    if successor is None:
        successors.append({
            "type": "End",
        })

    elif is_end_event(successor):
        successors.append({
            "type": get_end_type(successor),
        })
    elif is_activity(successor):
        successors.append({
            "type": get_activity_type(successor),
            "name": get_element_name(successor),
            "id": get_id(successor)
        })

        if behind_gateway:
            successors[-1].update({"precedes": get_element_name(predecessor)})

    elif is_gateway(successor):
        for successor in get_gateway_successors(bpmn, successor):
            find_successors(successor, bpmn, successors, seen, predecessor,
                            behind_gateway)
    else:
        find_successors(successor, bpmn, successors, seen, predecessor,
                        behind_gateway)


def get_next_element(elem, bpmn):
    """
    Gets the next outgoing element from current element.
    """

    try:
        outgoing = get_outgoing(elem)

        for e_id in outgoing:
            e_id = get_id(e_id)
            s_elem = get_element_by_id(e_id, bpmn)

            if is_allowed_successor(s_elem):
                return s_elem
    except TypeError:
        return elem


def get_id(elem):
    """
    Gets the resourceId of an element.
    
    Raises:
        KeyError: If resourceID is missing.
    """
    try:
        return elem[ELEMENT_ID]
    except KeyError:
        handle_error(f"Invalid JSON format, {ELEMENT_ID} missing. Aborting.")

    except TypeError:
        return


def get_element_by_id(e_id, bpmn):
    """
    Gets an element from the BPMN diagram based on its ID.

    Raises:
        StopIteration: If not element with given ID is found.
    """
    try:
        return next(e for e in get_bpmn_elements(bpmn) if get_id(e) == e_id)
    except StopIteration:
        handle_error(f"Could not find any element with id {e_id}")


def get_element_type(elem):
    """
    Gets the type of current element.

    Raises:
        KeyError: If Stencil or Id is missing.
    """
    try:
        return elem[STENCIL][ID]
    except KeyError:
        handle_error(
            f"Invalid JSON format, {STENCIL} or {ID} missing. Aborting.")


def get_activity_type(elem):
    """
    Get what type of activity current element is.
    """
    a_type = get_element_type(elem)
    return ACTIVITY_MAPPING.get(a_type, None)


def get_end_type(elem):
    """
    Get what kind of EndEvent current element is.
    """
    e_type = get_element_type(elem)
    return END_EVENT_MAPPING.get(e_type, None)


def get_gateway_type(elem):
    """
    Get what type of gateway current element is.
    """
    g_type = get_element_type(elem)
    return GATEWAY_MAPPING.get(g_type, None)


def get_successor_activities(elem, bpmn, seen):
    """
    Gets the successor activities of the current element.
    """
    successors = []
    behind_gateway = False

    next_element = get_next_element(elem, bpmn)

    if next_element is None:
        return []

    if get_next_element(next_element, bpmn) is not None:
        if is_gateway_splitting(get_next_element(next_element, bpmn)):
            behind_gateway = True

    find_successors(elem, bpmn, successors, seen, elem, behind_gateway)
    return successors


def get_predecessors_activities(elem, seq):
    """
    Get the predecessor activities of an element. 
    """
    predecessors = []
    id_to_match = get_id(elem)

    for predecessor in seq:
        predecessor_successors = predecessor["successors"]

        for successor in predecessor_successors:
            if successor.get("id") == id_to_match:
                predecessors.append({
                    "name": predecessor.get("name"),
                })
    return predecessors


def get_bpmn_elements(bpmn):
    """
    Gets all elements (child shapes) in an BPMN diagram.
    """
    try:
        return bpmn[CHILD_SHAPES]
    except KeyError:
        handle_error(f"Invalid JSON format, {CHILD_SHAPES} missing. Aborting.")


def get_outgoing(elem):
    """
    Gets a list of outgoing elements.
    """
    try:
        return elem[OUTGOING]
    except KeyError:
        handle_error(f"Invalid JSON format, {OUTGOING} missing. Aborting.")

    except TypeError:
        return []


def get_element_name(elem):
    """
    Gets the name of a element.
    
    Raises:
        KeyError: If name is not found, use elements activity type instead.
    """
    try:
        if PROPERTIES in elem:
            return elem[PROPERTIES][NAME]
        return get_activity_type(elem)
    except KeyError:
        return get_activity_type(elem)


def get_start_element(bpmn):
    """
    Searches through the BPMN diagram for a start element.
    """
    starts = []
    for elem in get_bpmn_elements(bpmn):
        if is_start_event(elem):
            starts.append(elem)
    # if len(starts) == 0:
    #     return find_first_element(bpmn)
    starts.extend(find_first_element(bpmn))
    return starts


def flatten_swimlanes(bpmn):
    """
    Flattens swimlanes to one list.
    """
    flattened = []
    for elem in get_bpmn_elements(bpmn):
        if get_element_type(elem) in ["Pool", "Lane"]:
            for swim_lane_elem in get_bpmn_elements(elem):
                if get_element_type(swim_lane_elem) in ["Pool", "Lane"]:
                    flattened += flatten_swimlanes(swim_lane_elem)
                else:
                    flattened.append(swim_lane_elem)
        else:
            flattened.append(elem)
    return flattened


def get_gateway_successors(bpmn, elem):
    """
    Gets the elements of outgoing connections.
    """
    return [get_element_by_id(get_id(e), bpmn) for e in get_outgoing(elem)]


def get_next_gateway_type(elem, bpmn, leads_to_gateway):
    """
    Gets the type of the next gateway, if next element is a gateway.
    """
    next_element = get_next_element(get_next_element(elem, bpmn), bpmn)

    if leads_to_gateway:
        if is_gateway(next_element):
            return get_gateway_type(next_element)

    return None


def is_gateway_joining(elem):
    """
    Checks if a gateway is joining, i.e., only having one
    outgoing connection.
    """
    return len(get_outgoing(elem)) == 1


def is_gateway_splitting(elem):
    """
    Checks if a gateway is splitting, i.e., having two or
    more outgoing connections.
    """
    return len(get_outgoing(elem)) >= 2


def is_end_event(elem):
    """
    Checks if an element is an end event.
    """
    return get_element_type(elem) in ALLOWED_END_EVENTS


def is_start_event(elem):
    """
    Checks if an element is a start element.
    """
    return get_element_type(elem) in ALLOWED_START_EVENTS


def is_activity(elem):
    """
    Checks if an element is an activity.
    """
    return get_element_type(elem) in ALLOWED_ACTIVITIES


def is_gateway(elem):
    """
    Checks if an element is a gateway.
    """
    return get_element_type(elem) in ALLOWED_GATEWAYS


def is_allowed_successor(elem):
    """
    Checks if a successor is allowed, i.e., its type is in either:
    - ALLOWED_ACTIVITIES,
    - ALLOWED_CONNECTING_OBJECTS,
    - ALLOWED_END_EVENTS,
    - ALLOWED_GATEWAYS,
    - ALLOWED_START_EVENTS
    """
    elem_type = get_element_type(elem)
    return (elem_type in ALLOWED_ACTIVITIES
            or elem_type in ALLOWED_CONNECTING_OBJECTS
            or elem_type in ALLOWED_END_EVENTS or elem_type in ALLOWED_GATEWAYS
            or elem_type in ALLOWED_START_EVENTS)


def is_element_seen(seen, elem):
    """
    Checks if an element has been visited.
    """
    return get_id(elem) in seen


def parse_branch(elem, seq, seen, bpmn, predecessor):
    """
    Parses an outgoing gateway branch.
    """
    if elem is None:
        return []

    if is_end_event(elem):
        return []

    if is_element_seen(seen, elem):
        return []

    if is_gateway(elem):

        if is_gateway_splitting(elem):

            if not is_element_seen(seen, elem):
                split_paths(elem, seq, seen, bpmn, predecessor)

                seen.add(get_id(elem))

    elif is_activity(elem):
        add_element(elem, seq, seen, bpmn)

    successor = get_next_element(elem, bpmn)

    return parse_branch(successor, seq, seen, bpmn, predecessor)


def split_paths(elem, seq, seen, bpmn, predecessor):
    """
    Gets the successors of element and visits each branch.
    """
    successors = get_gateway_successors(bpmn, elem)

    for successor in successors:

        parse_branch(successor, seq, seen, bpmn, predecessor)


def split_loop_paths(elem, seq, seen, bpmn, starting_point):
    """
    Gets the successor of potential loop element and visits each branch.
    """
    successors = get_gateway_successors(bpmn, elem)

    for successor in successors:

        parse_loop(successor, seq, seen, bpmn, starting_point)


def parse_loop(elem, seq, seen, bpmn, starting_point):
    """
    Parses outgoing connection. If an element matches the starting element,
    a loop has been detected.
    """

    if is_end_event(elem):
        return None

    if elem == starting_point:
        return True

    if is_gateway(elem) and is_gateway_splitting(elem):
        split_loop_paths(elem, seq, seen, bpmn, starting_point)

    successor = get_next_element(elem, bpmn)

    return parse_loop(successor, seq, seen, bpmn, starting_point)


def detect_loop(elem, seq, seen, bpmn, starting_point):
    """
    Detects if there is an outgoing loop from given element.
    """

    successors = get_gateway_successors(bpmn, elem)

    outgoing_loops = []

    for successor in successors:
        successor_is_loop = parse_loop(successor, seq, seen, bpmn,
                                       starting_point)
        if successor_is_loop:
            outgoing_loops.append([successor_is_loop, successor])
    return outgoing_loops


def add_element(elem, seq, seen, bpmn):
    """
    Adds an element to sequence.
    """
    e_id = get_id(elem)

    if not is_element_seen(seen, elem):
        seen.add(e_id)
        successors = []
        if len(get_outgoing(elem)) > 0:
            successors = get_successor_activities(elem, bpmn, seen)
        predecessors = get_predecessors_activities(elem, seq)

        seq_elem = {
            "type": get_activity_type(elem),
            "name": get_element_name(elem),
            "id": e_id,
            "leads_to_gateway": len(successors) > 1,
            "succeeds_gateway": len(predecessors) > 1,
            "successors": successors,
            "predecessors": predecessors,
        }

        successor = get_next_element(get_next_element(elem, bpmn), bpmn)
        if is_gateway(successor) and is_gateway_joining(successor):
            seq_elem.update({"leads_to_joining_gateway": True})

        if seq_elem["leads_to_gateway"]:
            seq_elem.update({
                "type_of_gateway":
                get_next_gateway_type(elem, bpmn,
                                      len(successors) > 1)
            })

            next_element = get_next_element(elem, bpmn)

            if next_element is not None:
                gateway = get_next_element(next_element, bpmn)
                if gateway is not None:
                    has_loop = detect_loop(gateway, seq, seen, bpmn, elem)

                    if has_loop:
                        seq_elem.update({"is_loop": len(has_loop) > 0})

        seq.append(seq_elem)


def parse_bpmn(elem, seq, seen, bpmn, predecessor):
    """
    Main parsing loop. Parses the diagram until it hits its end event.
    """

    try:
        if elem is None:
            return seq

        if count_elements(bpmn) == len(seen):
            if get_element_type(elem) in ALLOWED_ACTIVITIES:
                add_element(elem, seq, seen, bpmn)

            return seq

        if is_gateway(elem) and is_gateway_splitting(elem):

            if not is_element_seen(seen, elem):
                split_paths(elem, seq, seen, bpmn, predecessor)
                seen.add(get_id(elem))

        elif is_activity(elem):
            add_element(elem, seq, seen, bpmn)

        successor = get_next_element(elem, bpmn)
        return parse_bpmn(successor, seq, seen, bpmn, predecessor)
    except RecursionError:
        # Return the so-far parsed sequence.
        return seq


def handle_error(msg):
    """
    Logs an error message and returns.
    """
    raise Exception(msg)


def load_bpmn(f_path):
    """
    Loads an JSON file with UTF-8 encoding.

    Raises:
        - JSONDecodeError: If file is not a JSON file, or is an invalid JSON file.
        - OSError: General errors with opening and reading file.
    """
    try:
        with open(f_path, "r", encoding="utf-8") as file:
            return load(file)

    except JSONDecodeError:
        handle_error("JSON file could not be decoded.")
    except OSError:
        handle_error("Something wrong with handling file.")


def update_tokens(parsed_tokens):
    """
    Updates all tokens in the parsed sequence.
    """
    for token in parsed_tokens:

        n_successors = token["successors"]
        n_predecessors = token["predecessors"]

        successors = [successor['type'] for successor in token["successors"]]

        token["leads_to_gateway"] = len(n_successors) > 1
        token["succeeds_gateway"] = len(n_predecessors) > 1
        token.update({"is_start": len(n_predecessors) == 0})
        token.update({
            "is_end":
            any(element in successors for element in ALLOWED_END_EVENTS)
            or len(token["successors"]) == 0
        })

        if token.get("leads_to_gateway"):
            for successor in token["successors"]:
                if not "precedes" in successor:
                    successor.update({"precedes": token.get("name")})


def replay_tokens(parsed_tokens):
    """
    Replays all tokens in the parsed sequence.
    """
    for token_outer in parsed_tokens:
        successors = token_outer.get("successors")

        for successor in successors:
            successor_id = successor.get("id")

            for token_inner in parsed_tokens:
                token_id = token_inner.get("id")

                if successor_id == token_id:
                    token_name = token_outer.get("name")

                    if token_name not in [
                            predecessor['name']
                            for predecessor in token_inner["predecessors"]
                    ]:
                        token_inner["predecessors"].append({
                            "name":
                            token_outer.get("name"),
                        })


def find_first_element(bpmn):
    """
    Finds element that has an ID that no other element has as outgoing ID.
    """
    all_elem_id = []

    first_elem = []

    for elem in get_bpmn_elements(bpmn):

        if get_element_type(elem) in ["Task"]:
            all_elem_id.extend(get_outgoing(elem))

    for elem in get_bpmn_elements(bpmn):

        if get_element_type(elem) in ["Task"]:
            if get_id(elem) not in all_elem_id:
                first_elem.append(elem)

    return first_elem


def flatten_bpmn(bpmn):
    """Flattens the BPMN child shapes"""
    flat = flatten_swimlanes(bpmn)

    bpmn["childShapes"].extend(flat)


def count_elements(bpmn):
    """
    Counts the number of elements that can be added to the set of seen
    elements.
    """
    count = 0
    for _ in get_bpmn_elements(bpmn):
        count += 1
    return count


def count_activities(bpmn):
    """
    Count purely the number of activities in the diagram.
    """
    count = 0
    for elem in get_bpmn_elements(bpmn):
        if get_element_type(elem) in ALLOWED_ACTIVITIES:
            count += 1
    return count


def count_element_types(bpmn):
    """
    Count the number of times an each element in diagram
    occurs.
    """
    elem_types = {}

    for elem in get_bpmn_elements(bpmn):
        elem_type = get_element_type(elem)

        if elem_type in elem_types:
            elem_types[elem_type] += 1
        else:
            elem_types[elem_type] = 1

    return elem_types


def count_num_of_pools(bpmn):
    """
    Counts the number of times a pool occurs in diagram.
    """
    count = 0
    for elem in get_bpmn_elements(bpmn):
        if get_element_type(elem) in ["Pool"]:
            count += 1

    return count


def get_unique_element_types(bpmn):
    """
    Count the unique element type identifiers in the diagram.
    """
    element_types = set()

    for elem in get_bpmn_elements(bpmn):
        element_types.add(get_element_type(elem))

    return element_types


def get_most_common_element(bpmn):
    """
    Gets the most common element in a BPMN diagram.
    """
    elem_types = []
    for elem in get_bpmn_elements(bpmn):
        if get_element_type(elem) in ALLOWED_CONNECTING_OBJECTS:
            continue
        elem_types.append(get_element_type(elem))

    count = Counter(elem_types)
    return count.most_common(1)[0][0]


def extract_parsed_tokens(bpmn, is_file):
    """
    Entry point for the diagram parsing.
    """
    if is_file:
        bpmn = load_bpmn(bpmn)

    start_elem = get_start_element(bpmn)
    seen = set()

    if start_elem is None:
        handle_error("No element is assignable as start element.")

    parsed_tokens = []
    for start in start_elem:
        parsed_tokens += parse_bpmn(start, [], seen, bpmn, None)
    replay_tokens(parsed_tokens)
    update_tokens(parsed_tokens)

    return parsed_tokens
