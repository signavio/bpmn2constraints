"""
Module for compiling BPMN diagrams to atomic constraints.
"""
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-branches

# from json import dumps
# from itertools import combinations
from bpmnsignal.templates.declare_templates import *
from bpmnsignal.templates.matching_templates import *


def get_name(token):
    """
    Get name of object. If it has no name, return type.
    """
    name = token.get("name")
    if not name or name == " ":
        name = token.get("type")
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
    return seq
