"""Entry point for bpmnsignal command. Verifies argument and runs parser."""

# pylint: disable=import-error
import argparse
import logging
import sys
from pathlib import Path
from json import dumps
from tqdm import tqdm
from bpmnconstraints.parser.bpmn_parser import Parser
from bpmnconstraints.compiler.bpmn_compiler import Compiler
from bpmnconstraints.utils.script_utils import Setup
from bpmnconstraints.mermaid.mermaidtranslation import Mermaid
from bpmnconstraints.script_utils.constraint_comparison import ComparisonScript
from bpmnconstraints.script_utils.dataset_parsing import ParserScript
from bpmnconstraints.script_utils.dataset_compiling import CompilingScript

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


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
    parser.add_argument(
        "--dataframe", type=str, help="Path to dataframe of compiled constraints"
    )
    parser.add_argument("--parse_dataset", type=str, help="Path to dataset folder")
    parser.add_argument("--plot", type=bool, help="True if you want plots")
    parser.add_argument(
        "--constraint_type", type=str, help="type of constraint to be generated"
    )
    parser.add_argument("--compile_dataset", type=str, help="Path to dataset folder")
    parser.add_argument(
        "--skip_named_gateways", type=bool, help="Skips adding gateways as tokens."
    )
    parser.add_argument(
        "--compile_to_mermaid",
        type=str,
        help="Outputs BPMN diagram in parsable mermaid format",
    )

    args = parser.parse_args()

    if args.parse:
        path = Path(args.parse)
        setup = Setup(None)
        if setup.is_file(path):
            res = Parser(path, True, args.transitivity).run()
            if res:
                print(dumps(res, indent=2))

    elif args.compile:
        if not args.constraint_type:
            path = Path(args.compile)
            setup = Setup(None)
            if setup.is_file(path):
                res = Parser(path, True, args.transitivity).run()
                res = Compiler(res, args.transitivity, args.skip_named_gateways).run()
                if res:
                    print(dumps(res, indent=2))
        else:
            path = Path(args.compile)
            res = compile_bpmn_diagram(
                path, args.constraint_type, args.skip_named_gateways
            )
            if res:
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
            script = ComparisonScript(dataset_path, dataframe_path, plot)
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

    elif args.compile_dataset:
        dataset_path = Path(args.compile_dataset)
        setup = Setup(None)
        plot = args.plot

        if dataset_path is None:
            return
        if setup.is_directory(dataset_path):
            script = CompilingScript(dataset_path, True, False)
            script.run()

    elif args.compile_to_mermaid:
        path = Path(args.compile_to_mermaid)
        setup = Setup(None)
        if setup.is_file(path):
            res = Parser(path, True, False).run()
            if res:
                flowchart = Mermaid(res).translate()
                print(flowchart)

    else:
        parser.print_help()


def compile_bpmn_diagram(path_to_bpmn_diagram, constraint_type, skip_named_gateways):
    constraints = []
    setup = Setup(None)
    path_to_bpmn_diagram = Path(path_to_bpmn_diagram)
    if setup.is_file(path_to_bpmn_diagram):
        res = Parser(path_to_bpmn_diagram, True, True).run()
        res = Compiler(res, True, skip_named_gateways).run()

        if constraint_type == "SIGNAL":
            logging.info("Generating SIGNAL constraints...")
            for constraint in tqdm(res):
                constraints.append(constraint.get("SIGNAL"))

        elif constraint_type == "DECLARE":
            logging.info("Generating DECLARE constraints...")
            for constraint in tqdm(res):
                constraints.append(constraint.get("DECLARE"))

        elif constraint_type == "LTLF":
            logging.info("Generating LTLF constraints...")
            for constraint in tqdm(res):
                constraints.append(constraint.get("LTLf"))

        else:
            logging.warning(
                "Unknown constraint type. Use 'SIGNAL', 'DECLARE' or 'LTLF'."
            )
    return constraints
