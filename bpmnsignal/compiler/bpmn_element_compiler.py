"""
Module for compiling BPMN diagrams to atomic constraints.
"""
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-branches
# pylint: disable=use-maxsplit-arg
# pylint: disable=anomalous-backslash-in-string

import re
from itertools import combinations
from bpmnsignal.templates.declare_templates import *
from bpmnsignal.templates.matching_templates import *

SANITIZE = True
NON_ALPHANUM = re.compile('[^a-zA-Z]')
CAMEL_PATTERN_1 = re.compile('(.)([A-Z][a-z]+)')
CAMEL_PATTERN_2 = re.compile('([a-z0-9])([A-Z])')


def sanitize_label(label):
    """
    Sanitize element labels.

    Credit: Adrian Rebmann.
    """
    # handle some special cases
    label = str(label)
    if " - " in label:
        label = label.split(" - ")[-1]
    if "&" in label:
        label = label.replace("&", "and")
    label = label.replace('\n', ' ').replace('\r', '')
    label = label.replace('(s)', 's')
    label = label.replace("'", "")
    label = re.sub(' +', ' ', label)
    # turn any non-alphanumeric characters into whitespace
    # label = re.sub("[^A-Za-z]"," ",label)
    # turn any non-alphanumeric characters into whitespace
    label = NON_ALPHANUM.sub(' ', label)
    label = label.strip()
    # remove single character parts
    label = " ".join([part for part in label.split() if len(part) > 1])
    # handle camel case
    label = camel_to_white(label)
    # make all lower case
    label = label.lower()
    # delete unnecessary whitespaces
    label = re.sub("\s{1,}", " ", label)
    return label


def camel_to_white(label):
    """
    Credit: Adrian Rebmann.
    """
    label = CAMEL_PATTERN_1.sub(r'\1 \2', label)
    return CAMEL_PATTERN_2.sub(r'\1 \2', label)


def abort(msg):
    """
    Aborts the program.
    """
    print(f"Warning: {msg}.")


def get_name(token):
    """
    Get name of object. If it has no name, return type.
    """
    name = token.get("name")
    if not name or name == " ":
        name = token.get("type")
    if SANITIZE:
        return sanitize_label(name)
    return name


def get_gateway_type(token):
    """
    Get type of gateway.
    """
    return token.get("gateway_type")


def get_gateway_id(token):
    """
    Get ID of gateway.
    """
    return token.get("gateway_id")


def get_successors(token):
    """
    Get successors of object.
    """
    return token.get("successors")


def get_predecessors(token):
    """
    Get predecessors of object.
    """
    return token.get("predecessors")


def create_starts_with_constraint(token):
    """
    Create start constraint.
    """

    token_name = get_name(token)

    return {
        "description": f"Starts with {token_name}",
        "SIGNAL": s_init(token_name),
        "DECLARE": d_init(token_name),
    }


def create_ends_with_constraint(token):
    """
    Create end constraint.
    """

    token_name = get_name(token)

    return {
        "description": f"Ends with {token_name}",
        "SIGNAL": s_end(token_name),
        "DECLARE": d_end(token_name),
    }


def create_succession(token, concurrent):
    """
    Create succession constraint.
    """

    successors = get_successors(token)
    token_name = get_name(token)
    compiled_tokens = []

    for successor in successors:

        successor_name = get_name(successor)

        if concurrent:
            compiled_tokens.append({
                "description":
                f"{token_name} leads to {successor_name}",
                "SIGNAL":
                s_alternate_succession(token_name, successor_name),
                "DECLARE":
                d_alternate_succession(token_name, successor_name),
            })
        else:
            compiled_tokens.append({
                "description":
                f"{token_name} leads to {successor_name}",
                "SIGNAL":
                s_succession(token_name, successor_name),
                "DECLARE":
                d_succession(token_name, successor_name),
            })

    if 'transitivity' in token:
        for transitivity in token['transitivity']:
            successor_name = sanitize_label(transitivity)
            if concurrent:
                compiled_tokens.append({
                    "description":
                    f"{token_name} leads to {successor_name}",
                    "SIGNAL":
                    s_alternate_succession(token_name, successor_name),
                    "DECLARE":
                    d_alternate_succession(token_name, successor_name),
                })
            else:
                compiled_tokens.append({
                    "description":
                    f"{token_name} leads to {successor_name}",
                    "SIGNAL":
                    s_succession(token_name, successor_name),
                    "DECLARE":
                    d_succession(token_name, successor_name),
                })

    return compiled_tokens


def create_precedence(token, concurrent):
    """
    Create precedence constraint.
    """
    successors = get_successors(token)
    token_name = get_name(token)
    compiled_tokens = []

    for successor in successors:

        successor_name = get_name(successor)

        if concurrent:
            compiled_tokens.append({
                "description":
                f"{token_name} precedes {successor_name}",
                "SIGNAL":
                s_alternate_precedence(token_name, successor_name),
                "DECLARE":
                d_alternate_precedence(token_name, successor_name),
            })
        else:
            compiled_tokens.append({
                "description":
                f"{token_name} precedes {successor_name}",
                "SIGNAL":
                s_precedence(token_name, successor_name),
                "DECLARE":
                d_precedence(token_name, successor_name),
            })

    return compiled_tokens


def create_response(token, concurrent):
    """
    Create response constraint.
    """
    predecessors = get_predecessors(token)
    token_name = get_name(token)
    compiled_tokens = []

    for predecessor in predecessors:

        predecessor_name = get_name(predecessor)

        if concurrent:
            compiled_tokens.append({
                "description":
                f"{predecessor_name} responds to {token_name}",
                "SIGNAL":
                s_alternate_response(predecessor_name, token_name),
                "DECLARE":
                d_alternate_response(predecessor_name, token_name),
            })
        else:
            compiled_tokens.append({
                "description":
                f"{predecessor_name} responds to {token_name}",
                "SIGNAL":
                s_response(predecessor_name, token_name),
                "DECLARE":
                d_response(predecessor_name, token_name),
            })

    return compiled_tokens


def get_all_successor_names(token):
    """
    Gets the name of all successors to token.
    """
    successor_names = []
    successors = get_successors(token)

    for successor in successors:
        successor_names.append(get_name(successor))
    return successor_names


def create_exclusive_gateway(token):
    """
    Generate all possible combinations of exclusive (XOR) gateways.
    """
    compiled_tokens = []

    successors = get_all_successor_names(token)
    for gateway in combinations(successors, 2):

        compiled_tokens.append({
            "description":
            f"{gateway[0]} XOR {gateway[1]}",
            "SIGNAL":
            s_exclusive_choice(gateway[0], gateway[1]),
            "DECLARE":
            d_exclusive_choice(gateway[0], gateway[1]),
        })

    return compiled_tokens


def create_parallel_gateway(token):
    """
    Generate all possible combinations of parallel (AND) gateways.
    """
    compiled_tokens = []

    successors = get_all_successor_names(token)
    for gateway in combinations(successors, 2):

        compiled_tokens.append({
            "description":
            f"{gateway[0]} AND {gateway[1]}",
            "SIGNAL":
            s_co_existence(gateway[0], gateway[1]),
            "DECLARE":
            d_co_existence(gateway[0], gateway[1]),
        })

    return compiled_tokens


def create_inclusive_gateway(token):
    """
    Generate all possible combinations of inclusive (OR) gateways.
    """

    compiled_tokens = []

    successors = get_all_successor_names(token)
    for gateway in combinations(successors, 2):

        compiled_tokens.append({
            "description": f"{gateway[0]} OR {gateway[1]}",
            "SIGNAL": s_choice(gateway[0], gateway[1]),
            "DECLARE": d_choice(gateway[0], gateway[1]),
        })

    return compiled_tokens


def is_start(token):
    """
    Checks if object is start.
    """
    return token.get("is_start")


def is_end(token):
    """
    Checks if object is end.
    """
    return token.get("is_end")


def token_succeeds_gateway(token):
    """
    Checks if object succeeds gateway.
    """
    return token.get("succeeds_gateway")


def token_leads_to_gateway(token):
    """
    Checks if object lets to gateway.
    """
    return token.get("leads_to_gateway")


def get_succeeding_gateway(token):
    """
    Gets the succeeding gateway(s).
    """
    return token.get("type_of_gateway")


def token_leads_to_joining_gateway(token):
    """
    Checks if token leads to a joining gateway.
    """
    return token.get("leads_to_joining_gateway")


def put_ending_tokens_in_end(parsed_tokens):
    """
    Puts tokens marked as 'is_end' in the end of sequence.
    """
    new_tokens = []
    ending_tokens = []

    for token in parsed_tokens:
        if is_end(token):
            ending_tokens.append(token)
        else:
            new_tokens.append(token)

    new_tokens += ending_tokens
    return new_tokens


def put_starting_tokens_in_front(parsed_tokens):
    """
    Puts tokens marked as 'is_start' in the beginning of sequence.
    """
    new_tokens = []
    starting_tokens = []

    for token in parsed_tokens:
        if is_start(token):
            starting_tokens.append(token)
        else:
            new_tokens.append(token)

    starting_tokens += new_tokens
    return starting_tokens


def compile_parsed_tokens(parsed_tokens):
    """
    Main compiler loop.
    """

    tokens = put_ending_tokens_in_end(parsed_tokens)
    tokens = put_starting_tokens_in_front(tokens)

    seq = []

    concurrent = False
    for token in parsed_tokens:
        if is_start(token):
            compiled_token = create_starts_with_constraint(token)
            seq.append(compiled_token)

        if is_end(token):
            compiled_token = create_ends_with_constraint(token)

            if token_succeeds_gateway(token):
                compiled_tokens = create_response(token, concurrent)
                seq.extend(compiled_tokens)
            seq.append(compiled_token)
            continue

        if token_leads_to_gateway(token):

            gateways = get_succeeding_gateway(token)

            for gateway in gateways:
                gateway_type = get_gateway_type(gateway)
                if gateway_type == "XOR":
                    compiled_tokens = create_exclusive_gateway(token)
                elif gateway_type == "AND":
                    concurrent = True
                    compiled_tokens = create_parallel_gateway(token)
                elif gateway_type == "OR":
                    compiled_tokens = create_inclusive_gateway(token)

            seq.extend(compiled_tokens)
            compiled_tokens = create_precedence(token, concurrent)
            seq.extend(compiled_tokens)
            continue

        if token_succeeds_gateway(token):
            concurrent = False
            compiled_tokens = create_response(token, concurrent)
            seq.extend(compiled_tokens)

        else:
            if not token_leads_to_joining_gateway(token):
                compiled_token = create_succession(token, concurrent)
                seq.extend(compiled_token)

    return seq
