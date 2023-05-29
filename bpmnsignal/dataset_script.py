"""
Script for testing parser
"""
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=too-many-arguments
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-locals
# pylint: disable=import-error
# pylint: disable=too-many-statements
import json
import os

from tqdm import tqdm
from pandas import read_csv

from bpmnsignal.parser.bpmn_element_parser import (
    extract_parsed_tokens,
    count_activities,
    count_elements,
    count_element_types,
)

from bpmnsignal.utils.plot import create_scatter_plot_2, percentage_bar_plot, plot_model_outcomes
from bpmnsignal.utils.verification import is_model_valid

CHUNK_SIZE = 10**8


def get_percentage(part, whole):
    """
    Calculates the percentage of successful/failed parses.
    """
    if float(part) <= 0 or float(whole) <= 0:
        return ""
    percentage = 100 * float(part) / float(whole)
    return f"{percentage}"


def print_result(failed_models, successful_models, total_models,
                 parsed_elements, total_elements, partially_parsed_models):
    """
    Prints result of script to terminal.
    """

    successful_models = f"{get_percentage(successful_models, total_models)}"
    failed_models = f"{get_percentage(failed_models, total_models)}"
    partially_parsed_models = f"{get_percentage(partially_parsed_models, total_models)}"
    parsed_elements = f"{get_percentage(parsed_elements, total_elements)}"

    print(f"No. of % successfully parsed models: {successful_models}%.")
    print(f"No. of % models that failed to parse: {failed_models}%.")
    print(
        f"No. of % models that were partially parsed: {partially_parsed_models}%."
    )
    print(f"No. of % of elements that were parsed: {parsed_elements}")
    print(
        f"In total, {total_models} models were parsed containing {total_elements} elements."
    )


def inc(target, increment):
    """Increments the number of models that have failed"""
    return target + increment


def get_files(dir_path):
    """
    Gets all files from a directory as a list.
    """
    return os.listdir(dir_path)


def get_file(file_name, dir_path):
    """
    Get a specific file.
    """
    return os.path.join(dir_path, file_name)


def is_file(file):
    """
    Checks if file is an actual file.
    """
    return os.path.isfile(file)


def read_csv_chunk(file):
    """
    Loads a chunk of a CSV file.
    """
    return read_csv(file, chunksize=CHUNK_SIZE)


def load_chunked_models(chunk):
    """
    Loads the 'Model JSON' column in chunked CSV file.
    """
    return chunk["Model JSON"].apply(json.loads)


def create_scatter_object(model_outcome, element_count, type_count):
    """
    Creates a dictionary item for plotting.
    """
    return {
        "outcome": model_outcome,
        "number of elements": element_count,
        "number of element types": type_count
    }


def create_partial_object(percentage, element_count, type_count):
    """
    Creates a dictionary item for plotting.
    """
    return {
        "variable": percentage,
        "number of elements": element_count,
        "number of element types": type_count
    }


def create_partial_object_2(total_elements, parsed_elements, element_count,
                            type_count):
    """
    Creates a dictionary item for plotting.
    """
    return {
        "total elements": total_elements,
        "parsed_elements": parsed_elements,
        "number of elements": element_count,
        "number of element types": type_count
    }


def create_parsed_object(parsed_elements, element_count, type_count):
    """
    Creates a dictionary item for plotting.
    """
    return {
        "variable": parsed_elements,
        "number of element types": type_count,
        "number of elements": element_count
    }


def run_script(dir_path):
    """
    Runs a test script.
    """
    failed_models = 0
    successful_models = 0
    partial_parsed_models = 0
    total_models = 0

    parsed_elements = 0
    total_elements = 0

    all_models = []
    partial_models = {
        "0-10": 0,
        "11-20": 0,
        "21-30": 0,
        "31-40": 0,
        "41-50": 0,
        "51-60": 0,
        "61-70": 0,
        "71-80": 0,
        "81-90": 0,
        "91-100": 0,
    }

    partial_models_2 = []

    for file_name in tqdm(get_files(dir_path), desc="Parsing Progress"):

        csv_file = get_file(file_name, dir_path)

        if is_file(csv_file):
            for chunk in read_csv_chunk(csv_file):

                models = load_chunked_models(chunk)

                for model in models:

                    try:
                        if not is_model_valid(model):
                            continue

                        total_models += 1
                        result = extract_parsed_tokens(model, False, False)
                        count_result = len(result)
                        total_activities = count_activities(model)

                        parsed_elements += count_result
                        total_elements += total_activities

                        num_elements = count_elements(model)
                        types = count_element_types(model)

                        num_types = len(types)

                        if count_result != total_activities:
                            partial_parsed_models += 1

                            all_models.append(
                                create_scatter_object("partial", num_elements,
                                                      num_types))

                            percentage_parsed = (count_result /
                                                 total_activities) * 100

                            partial_models_2.append(
                                create_partial_object(percentage_parsed,
                                                      count_result, num_types))

                            keys = partial_models.keys()
                            for key in keys:
                                lower, upper = key.split("-")
                                if percentage_parsed in range(
                                        int(lower),
                                        int(upper) + 1):
                                    partial_models[key] += 1
                                    break
                            continue

                        successful_models += 1
                        all_models.append(
                            create_scatter_object("successful", num_elements,
                                                  num_types))

                    except Exception:
                        failed_models += 1

                        all_models.append(
                            create_scatter_object("failed", num_elements,
                                                  num_types))

    create_scatter_plot_2(all_models, "All Parsed Models")
    plot_model_outcomes(all_models)
    percentage_bar_plot(partial_models)
    print(json.dumps(partial_models, indent=2))

    print_result(failed_models, successful_models, total_models,
                 parsed_elements, total_elements, partial_parsed_models)
