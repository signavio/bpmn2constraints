"""Entry point for bpmnsignal command. Verifies argument and runs parser."""
# pylint: disable=import-error
import argparse
from pathlib import Path
from json import dumps
from bpmnsignal.parser.bpmn_parser import Parser
from bpmnsignal.compiler.bpmn_compiler import Compiler
from bpmnsignal.utils.script_utils import Setup
from bpmnsignal.compiler_script import CompilerScript
from bpmnsignal.parser_script import ParserScript



def run():
    """Takes the provided BPMN JSON file and returns a list
    of extracted SIGNAL constraints
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--parse", type=str, help="Runs the parser")
    parser.add_argument("--compile", type=str, help="Runs the compiler")
    parser.add_argument("--transitivity", type=bool, help="Adds transitivity")
    parser.add_argument("--compare_constraints")
    parser.add_argument("--dataset", type=str, help="Path to dataset to compile")
    parser.add_argument("--dataframe", type=str, help="Path to dataframe of compiled constraints")
    parser.add_argument("--parse_dataset", type=str, help="Path to dataset folder")
    parser.add_argument("--plot", type=bool, help="True if you want plots")


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
            res = Compiler(res, args.transitivity).run()
            print(dumps(res, indent=2))
    
    elif args.compare_constraints:
        dataframe_path = None
        dataset_path = None
        setup = Setup(None)
        plot = args.plot

        if args.dataframe:
            dataframe_path = Path(args.dataframe)
        if args.dataset:
            dataset_path = Path(args.dataset)

        if dataframe_path is None or dataset_path is None:
            return

        if setup.is_file(dataframe_path) and setup.is_file(dataset_path):
            script = CompilerScript(dataset_path, dataframe_path, plot)
            script.run()
    
    elif args.parse_dataset:
        dataset_path = Path(args.parse_dataset)
        setup = Setup(None)
        plot = args.plot

        if dataset_path is None:
            return
        
        if setup.is_directory(dataset_path):
            script = ParserScript(dataset_path, plot)
            script.run()
    else:
        parser.print_help()
