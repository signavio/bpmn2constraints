"""Module for extracting element tokens from a BPMN diagram."""

# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=duplicate-code
# pylint: disable=wildcard-import

import sys
from json import load, JSONDecodeError
from bpmnsignal.utils.constants import *
from bpmnsignal.utils.log import log_critical_error


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

    if is_end_event(successor):
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
    outgoing = get_outgoing(elem)

    for e_id in outgoing:
        e_id = get_id(e_id)
        s_elem = get_element_by_id(e_id, bpmn)

        if is_allowed_successor(s_elem):
            return s_elem


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
    if is_gateway_splitting(
            get_next_element(get_next_element(elem, bpmn), bpmn)):
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


def get_element_name(elem):
    """
    Gets the name of a element.
    
    Raises:
        KeyError: If name is not found, use elements activity type instead.
    """
    try:
        return elem[PROPERTIES][NAME]
    except KeyError:
        return get_activity_type(elem)


def get_start_element(bpmn):
    """
    Searches through the BPMN diagram for a start element.
    """
    try:
        return next(e for e in get_bpmn_elements(bpmn) if is_start_event(e))
    except StopIteration:
        log_critical_error("No start element found, merging childShapes..")


def merge_child_shapes(bpmn):
    """
    Merges all elements child shapes together, i.e., flattens the
    diagram.
    """
    merged_list = []
    merged_list += bpmn["childShapes"]
    for elem in get_bpmn_elements(bpmn):
        if get_element_type(elem) in ['Pool', 'Lane']:
            for inner_element in elem["childShapes"]:
                merged_list += merge_child_shapes(inner_element)

    return merged_list


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


def add_element(elem, seq, seen, bpmn):
    """
    Adds an element to sequence.
    """
    e_id = get_id(elem)

    if not is_element_seen(seen, elem):

        seen.add(e_id)

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

        if seq_elem["leads_to_gateway"]:
            seq_elem.update({
                "type_of_gateway":
                get_next_gateway_type(elem, bpmn,
                                      len(successors) > 1)
            })

        seq.append(seq_elem)


def parse_bpmn(elem, seq, seen, bpmn, predecessor):
    """
    Main parsing loop. Parses the diagram until it hits its end event.
    """
    if is_end_event(elem):
        # This may potentially lead to unfinished parsing.
        return seq

    if is_gateway(elem) and is_gateway_splitting(elem):

        if not is_element_seen(seen, elem):
            split_paths(elem, seq, seen, bpmn, predecessor)
            seen.add(get_id(elem))

    elif is_activity(elem):
        add_element(elem, seq, seen, bpmn)

    successor = get_next_element(elem, bpmn)

    return parse_bpmn(successor, seq, seen, bpmn, predecessor)


def handle_error(msg):
    """
    Logs an error message and exits with exit code 1.
    """
    log_critical_error(msg)
    sys.exit(1)


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


def extract_parsed_tokens(file_path):
    """
    Entry point for the diagram parsing.
    """
    bpmn = load_bpmn(file_path)
    merged_list = merge_child_shapes(bpmn)
    bpmn["childShapes"] = merged_list
    start_elem = get_start_element(bpmn)
    seen = set()

    if start_elem is None:
        handle_error("No start element found!")

    parsed_tokens = parse_bpmn(start_elem, [], seen, bpmn, None)
    replay_tokens(parsed_tokens)
    update_tokens(parsed_tokens)

    return parsed_tokens
