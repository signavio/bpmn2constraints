"""Entry point for bpmnsignal command. Verifies argument and runs parser."""
# pylint: disable=import-error
import os
import argparse
from pathlib import Path
from json import dumps
import pytest
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens
from bpmnsignal.dataset_script import run_script


def run_test():
    """
    Runs the pytest.
    NOTE: Needs to be in root directory.
    """
    pytest.main(["-x", "tests"])


def is_dir(path):
    """
    Checks if path leads to a directory.
    """
    return os.path.isdir(path)


def is_file(path):
    """
    Checks if path leads to a file.
    """
    return os.path.isfile(path)


def run():
    """Takes the provided BPMN JSON file and returns a list
    of extracted SIGNAL constraints
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--parse', type=str, help='Runs the parser')
    parser.add_argument('--script', type=str, help='path to directory')
    parser.add_argument('--test', action='store_true', help='run test')
    parser.add_argument('--path', action='store_true', help='run test')

    args = parser.parse_args()
    if args.test:
        run_test()

    elif args.parse:
        path = Path(args.parse)
        if is_file(path):
            parsed_tokens = extract_parsed_tokens(path, True)
            print(dumps(parsed_tokens, indent=2))
        else:
            print(f"{path} is not a file.")

    elif args.script:
        path = Path(args.script)
        if is_dir(path):
            run_script(path)
        else:
            print(f"{path} is not a directory.")

    else:
        parser.print_help()
