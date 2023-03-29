"""Functions generating SIGNAL constraints from
    Declare-like abstractions.
"""


def starts_with(element):
    """Declare constraint for the first element in diagram"""
    return f"(^'{element}')"


def ends_with(element):
    """Declare constraint for the last element in diagram"""
    return f"('{element}'$)"


def precedes(predecessor, successor):
    """Kind of like leads_to."""
    return f"(^ (NOT '{predecessor}' | ('{predecessor}' (NOT '{predecessor}')* '{successor}'))*$)"


def leads_to(predecessor, successor):
    """Declare constraint for one element being another elements successor"""
    return f"(^NOT('{predecessor}'|'{successor}')*('{predecessor}'~>'{successor}')\
*NOT('{predecessor}'|'{successor}')*$)"


def lor(element_right, element_left):
    """Declare function for the OR gateway"""
    return f"({element_right}|{element_left})"


def lxor(element_right, element_left):
    """Declare function for the XOR gateway"""
    return f"(^(((NOT('{element_right}')*) ('{element_left}' NOT('{element_right}')*)*)|\
((NOT('{element_left}')*)('{element_right}' NOT('{element_left}')*)*))$)"
