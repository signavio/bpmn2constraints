"""
A script for comparing precision and recall of the BPMN compiler vs. a Petri net replay-based tool.
"""
# pylint: skip-file

# pylint: disable=broad-exception-caught
# pylint: disable=import-error

import json
import pandas as pd

from bpmnsignal.parser.bpmn_element_parser import (extract_parsed_tokens,
                                                   count_elements,
                                                   count_element_types)
from bpmnsignal.compiler.bpmn_element_compiler import compile_parsed_tokens
from bpmnsignal.utils.plot import (combined_scatter_plot,
                                   plot_total_constraints,
                                   plot_precision_num_elements,
                                   plot_recall_num_elements)
from bpmnsignal.utils.verification import is_model_valid

PATH_TO_DATAFRAMES = ""

CHUNK = 10**8


def load_dataframe(path_to_dataframe):
    """
    Unpickle a pickled dataframe.
    """
    return pd.read_pickle(path_to_dataframe)


def load_csv_chunk(path_to_dataset):
    """
    Loads a dataset as CSV file.
    """
    return pd.read_csv(path_to_dataset, chunksize=CHUNK)


def parse_dataframes(dataframe_path):
    """
    Parses dataframe.
    """
    dataframe = load_dataframe(dataframe_path)
    parsed_models = []
    for _, row in dataframe.iterrows():
        model = {
            "model_id": row["model_id"],
            "constraints": [],
        }

        skipped_constraints = ['Exactly1', 'Responded Existence', 'Absence2']

        for con in row['constraints']:
            spliced_con = con[:con.find("|")].strip()

            constraint = spliced_con
            constraint = constraint.split('[')[0]

            if constraint in skipped_constraints:
                continue

            model["constraints"].append(spliced_con)

        parsed_models.append(model)
    return parsed_models


def compile_models(path_to_dataset, transitivity):
    """
    Compiles models from dataset
    """

    compiled_models = []
    for chunk in load_csv_chunk(path_to_dataset):
        models = chunk["Model JSON"].apply(json.loads)
        model_id = chunk["Model ID"]

        for i, model in enumerate(models):
            _model = {
                "model_id": model_id[i],
                "constraints": [],
            }
            try:
                if not is_model_valid(model):
                    continue
                parsed = extract_parsed_tokens(model, False, transitivity)
                _model.update({
                    'num_elem_types': count_element_types(model),
                    'num_elems': count_elements(model),
                })
                compiled = compile_parsed_tokens(parsed)
                for constraint in compiled:
                    _model["constraints"].append(constraint.get("DECLARE"))

                compiled_models.append(_model)
            except Exception:
                continue
    return compiled_models


def filter_constraints(num_elem_types, petri_net_cons):
    """
    Filters constraints.
    """
    if 'Exclusive_Databased_Gateway' not in num_elem_types and any(
            con.startswith("Exclusive Choice") for con in petri_net_cons):
        petri_net_cons = [
            con for con in petri_net_cons
            if not con.startswith('Exclusive Choice')
        ]

    if 'ParallelGateway' not in num_elem_types and any(
            con.startswith("Co-Existence") for con in petri_net_cons):
        petri_net_cons = [
            con for con in petri_net_cons if not con.startswith('Co-Existence')
        ]
        petri_net_cons = [
            con for con in petri_net_cons if not con.startswith('Alternate')
        ]

    if ('ParallelGateway' not in num_elem_types
            or 'Exclusive_Databased_Gateway' not in num_elem_types):
        petri_net_cons = [
            con for con in petri_net_cons if not con.startswith('Response')
        ]
        petri_net_cons = [
            con for con in petri_net_cons if not con.startswith('Precedence')
        ]

    return petri_net_cons


def combine_models(parsed_models_dataframe, parsed_models_compiler):
    """
    Combined models from petri net replay and compiler.
    """
    combined_models = []
    for df_model in parsed_models_dataframe:
        model_id = df_model['model_id']
        petri_net_cons = df_model['constraints']

        num_elems = None
        num_elem_types = []

        for ds_model in parsed_models_compiler:
            if ds_model['model_id'] == model_id:
                compiler_cons = ds_model['constraints']
                num_elem_types = ds_model['num_elem_types']
                num_elems = ds_model['num_elems']
                break
            compiler_cons = []

        if len(compiler_cons) > 0 and len(petri_net_cons) > 0:

            combined_models.append({
                'model_id':
                model_id,
                'petri_net_constraints':
                list(set(petri_net_cons)),
                'compiler_constraints':
                list(set(compiler_cons)),
                'num_elem_types':
                num_elem_types,
                'num_elems':
                num_elems,
                'precision':
                len(set(petri_net_cons).intersection(set(compiler_cons))) /
                len(set(compiler_cons)),
                'recall':
                len(set(compiler_cons).intersection(set(petri_net_cons))) /
                len(set(petri_net_cons)),
            })
    return combined_models


def run_comparison_script(path_to_dataframe, path_to_dataset, transitivity):
    """
    Runs the script for comparing our compiler against the result of a Petri-net replay based tool.
    Measures in:
        - Precision: How many of our constraints are in the Petri-Net version?
        - Recall: How many of the Petri Net are in our?
    """
    parsed_models_dataframe = parse_dataframes(path_to_dataframe)
    parsed_models_compiler = compile_models(path_to_dataset, transitivity)

    combined = combine_models(parsed_models_dataframe.copy(),
                              parsed_models_compiler.copy())

    for combo in combined:
        print(json.dumps(combo, indent=2))
    plot_total_constraints(combined)
    combined_scatter_plot(combined)
    plot_precision_num_elements(combined)
    plot_recall_num_elements(combined)
