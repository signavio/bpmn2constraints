"""Entry point for bpmnsignal command. Verifies argument and runs parser."""
# pylint: disable=import-error
import os
import argparse
from pathlib import Path
from json import dumps
import pytest
from bpmnsignal.parser.bpmn_element_parser import extract_parsed_tokens
from bpmnsignal.compiler.bpmn_element_compiler import compile_parsed_tokens
from bpmnsignal.compiler_comparison_script import run_comparison_script
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
    parser.add_argument('--parse_dataset', type=str, help='path to directory')
    parser.add_argument('--cc_df', type=str, help='path to dataframe')
    parser.add_argument('--cc_ds', type=str, help='path to dataset to compile')
    parser.add_argument('--test', action='store_true', help='run test')
    parser.add_argument('--path', action='store_true', help='run test')
    parser.add_argument('--compile', type=str, help='Runs the compiler')
    parser.add_argument('--transitivity',
                        type=bool,
                        help='Adds transitive constraints to compiler')

    args = parser.parse_args()
    if args.test:
        run_test()

    elif args.compile:
        path = Path(args.compile)
        if is_file(path):
            parsed_tokens = extract_parsed_tokens(path, True,
                                                  args.transitivity)
            compiled_tokens = compile_parsed_tokens(parsed_tokens)
            print(dumps(compiled_tokens, indent=2))

    elif args.parse:
        path = Path(args.parse)
        if is_file(path):
            parsed_tokens = extract_parsed_tokens(path, True, False)
            print(dumps(parsed_tokens, indent=2))

    elif args.parse_dataset:
        path = Path(args.parse_dataset)
        if is_dir(path):
            run_script(path)
    elif args.cc_df and args.cc_ds:
        dataset_path = Path(args.cc_ds)
        dataframe_path = Path(args.cc_df)

        if is_file(dataset_path) and is_file(dataframe_path):
            run_comparison_script(dataframe_path, dataset_path,
                                  args.transitivity)
    else:
        parser.print_help()
