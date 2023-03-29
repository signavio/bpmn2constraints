"""Functions generating SIGNAL constraints from
    Declare-like abstractions.
"""


def starts_with(a):
    return f"(^'{a}')"


def ends_with(a):
    return f"('{a}'$)"


def precedes(a, b):
    return f"(^ (NOT '{a}' | ('{a}' (NOT '{a}')* '{b}'))*$)"


def leads_to(a, b):
    return f"(^NOT('{a}'|'{b}')*('{a}'~>'{b}')*NOT('{a}'|'{b}')*$)"


def lor(a, b):
    return f"({a}|{b})"


def lxor(a, b):
    return f"(^(((NOT('{a}')*) ('{b}' NOT('{a}')*)*)|((NOT('{b}')*)('{a}' NOT('{b}')*)*))$)"
