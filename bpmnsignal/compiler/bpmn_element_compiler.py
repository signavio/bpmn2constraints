"""
Module for compiling BPMN diagrams to atomic constraints.
"""
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-branches

from json import dumps
from itertools import combinations
from bpmnsignal.templates.declare_templates import *
from bpmnsignal.templates.matching_templates import *


def add_starts_with(token, seq):
    """
    Adds a compiled 'starts_with' constraint, in
    1. Natural Language
    2. DECLARE
    3. SIGNAL
    """

    token_name = token.get("name")

    if not token_name or token_name == "":
        token_name = token.get("type")

    seq_elem = {
        "desc": f"Starts with {token_name}",
        "declare": d_init(token_name),
        "signal": s_init(token_name),
    }

    seq.append(seq_elem)


def add_ends_with(token, seq):
    """
    Adds a compiled 'ends_with' constraint, in
    1. Natural Language
    2. DECLARE
    3. SIGNAL
    """

    token_name = token.get("name")
    seq_elem = {
        "desc": f"Ends with {token_name}",
        "declare": d_end(token_name),
        "signal": s_end(token_name),
    }
    seq.append(seq_elem)


def add_succession(token, seq):
    """
    Adds a compiled 'leads_to' constraint, in
    1. Natural Language
    2. DECLARE
    3. SIGNAL
    """
    successors = token["successors"]
    token_name = token.get("name")

    for successor in successors:

        successor_name = successor.get("name")

        seq_elem = {
            "desc": f"{token_name} leads to {successor_name}",
            "declare": d_succession(token_name, successor_name),
            "signal": s_succession(token_name, successor_name)
        }
        seq.append(seq_elem)


def add_precedes(token, seq):
    """
    Adds a compiled 'precedes' constraint 
    for every successor in current token, in
    
    1. Natural Language
    2. DECLARE
    3. SIGNAL
    """
    successors = token["successors"]
    token_name = token.get("name")

    for successor in successors:

        successor_name = successor.get("name")

        seq_elem = {
            "desc": f"{token.get('name')} precedes {successor_name}",
            "declare": d_precedence(token_name, successor_name),
            "signal": s_precedence(token_name, successor_name)
        }
        seq.append(seq_elem)


def add_response(token, seq):
    """
    Adds a compiled 'response' constraint 
    for every predecessor in current token, in
    
    1. Natural Language
    2. DECLARE
    3. SIGNAL
    """

    predecessors = token["predecessors"]
    token_name = token.get("name")

    for predecessor in predecessors:

        predecessor_name = predecessor.get("name")

        seq_elem = {
            "desc": f"{predecessor_name} responds to {token_name}",
            "declare": d_response(predecessor_name, token_name),
            "signal": s_response(predecessor_name, token_name),
        }
        seq.append(seq_elem)


def add_exclusive_choice(token, seq):
    """
    Adds a compiled 'xor' constraint 
    for every gateway combination in current token, in
    
    1. Natural Language
    2. DECLARE
    3. SIGNAL
    """

    gateway_successors = [e.get("name") for e in token["successors"]]

    xor_gates = combinations(gateway_successors, 2)
    for gate in xor_gates:
        seq_elem = {
            "desc": f"{gate[0]} xor {gate[1]}",
            "declare": d_exclusive_choice(gate[0], gate[1]),
            "signal": s_exclusive_choice(gate[0], gate[1]),
        }
        seq.append(seq_elem)


def add_choice(token, seq):
    """
    Adds a compiled 'or' constraint 
    for every gateway combination in current token, in
    
    1. Natural Language
    2. DECLARE
    3. SIGNAL
    """

    gateway_successors = [e.get("name") for e in token["successors"]]

    or_gates = combinations(gateway_successors, 2)
    for gate in or_gates:
        seq_elem = {
            "desc": f"{gate[0]} xor {gate[1]}",
            "declare": d_choice(gate[0], gate[1]),
            "signal": s_choice(gate[0], gate[1]),
        }
        seq.append(seq_elem)


def add_co_existence(token, seq):
    """ 
    If we have co-existence, we need to parse it differently.
    1. Instead of succession, all successions should be responses.
    2. All should be responses, until we find ending gateway?
    """
    print(token)
    print(seq)


def compile_parsed_tokens(parsed_tokens):
    """
    Main loop for compiling. Compiles in order they were parsed.
    """
    seq = []

    for token in parsed_tokens:

        if token.get("is_start"):
            add_starts_with(token, seq)

        if token.get("is_end"):
            if token.get("succeeds_gateway"):
                add_response(token, seq)
            add_ends_with(token, seq)
            continue

        if token.get("leads_to_gateway"):

            if token.get("type_of_gateway") == "XOR":
                add_precedes(token, seq)
                add_exclusive_choice(token, seq)
                continue

            if token.get("type_of_gateway") == "AND":
                add_precedes(token, seq)
                add_exclusive_choice(token, seq)
                continue

            if token.get("type_of_gateway") == "OR":
                add_precedes(token, seq)
                add_exclusive_choice(token, seq)
                continue

        if token.get("succeeds_gateway"):
            add_response(token, seq)
            continue

        if token.get("is_loop"):
            print("Skipping..")

        if len(token["successors"]) > 0:

            if "leads_to_joining_gateway" in token:
                print(dumps(token, indent=2))
                continue
            add_succession(token, seq)
        else:
            pass
    return seq
