"""Entry point for bpmnsignal command. Verifies argument and runs parser."""
import json
import sys
import os
from pathlib import Path
from bpmnsignal.bpmn_parser import generate_sequence

EXPECTED_ARGS_COUNT = 1


def verify_arg():
    """
    Verifies the argument supplied to program

    Raises:
        SystemExit: Incorrect number of arguments provided
    """

    if len(sys.argv) != EXPECTED_ARGS_COUNT + 1:
        print(
            f'Expected {EXPECTED_ARGS_COUNT} arg(s), got {len(sys.argv) - 1}')
        raise SystemExit(2)

    path = Path(sys.argv[1])
    if not os.path.isfile(path):
        print(f'File {path} does not exist.')
        raise SystemExit(2)

    try:
        with open(path, "r", encoding='utf-8') as file:
            json.load(file)
    except ValueError as exc:
        print(f'File {path} is not of JSON format.')
        raise SystemExit(2) from exc


def run():
    """ Takes the provided BPMN JSON file and returns a list
    of extracted SIGNAL constraints
    """

    path = Path(sys.argv[1])
    verify_arg()
    sequence, json_output = generate_sequence(path)
    print(json.dumps(json_output, indent=2))
    print(sequence)
