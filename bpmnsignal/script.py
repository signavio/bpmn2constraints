"""Entry point for bpmnsignal command. Verifies argument and runs parser."""
# pylint: disable=import-error
import os
import argparse
from pathlib import Path
from json import dumps
from bpmnsignal.parser.bpmn_parser import Parser
from bpmnsignal.compiler.bpmn_compiler import Compiler
from bpmnsignal.utils.script_utils import Setup



def run():
    """Takes the provided BPMN JSON file and returns a list
    of extracted SIGNAL constraints
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--parse', type=str, help='Runs the parser')
    parser.add_argument('--compile', type=str, help='Runs the compiler')
    parser.add_argument('--transitivity',
                        type=bool,
                        help='Adds transitive constraints to compiler')

    args = parser.parse_args()

    if args.parse:
        path = Path(args.parse)
        setup = Setup(None)
        if setup.is_file(path):
            res = Parser(path, True, args.transitivity).run()
            print(dumps(res, indent=2))

    elif args.compile:
        path = Path(args.compile)
        setup = Setup(None)
        if setup.is_file(path):
            res = Parser(path, True, args.transitivity).run()
            print("Compiler not yet implemented.")
            # res = Compiler(res, args.transitivity)
            # print(dumps(res, indent=2))

    else:
        parser.print_help()
