"""
Script for testing parser
"""
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=too-many-arguments
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-locals
# pylint: disable=import-error
import json
import os

from tqdm import tqdm
from pandas import read_csv
import matplotlib.pyplot as plt

from bpmnsignal.parser.bpmn_element_parser import (
    extract_parsed_tokens,
    flatten_bpmn,
    count_activities,
    count_elements,
    count_element_types,
    get_unique_element_types,
    get_start_element,
    count_num_of_pools,
)

from bpmnsignal.utils.plot import create_scatter_plot, create_bar_plot

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
        f"In total, {total_models} were parsed containing {total_elements} elements."
    )


def is_model_valid(model, filtered_models):
    """
    Checks whether model is valid or not.
    """
    try:
        if model["stencil"]["id"] != "BPMNDiagram":
            filtered_models["Model is not of BPMN format"] += 1
            return False

        if count_elements(model) < 5:
            filtered_models["Model contains less than five elements"] += 1
            return False

        if get_start_element(model) is None:
            filtered_models["Model has no starting point"] += 1
            return False

        if count_num_of_pools(model) > 1:
            filtered_models["Model has more than two pools"] += 1
            return False

        return True
    except KeyError:
        filtered_models["JSON formatting error"] += 1
        return False


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
        "type": model_outcome,
        "element_count": element_count,
        "element_type_count": type_count
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

    unique_elements = set()

    plot_models = []
    partial_models = []
    parsed_models = []

    filtered_models = {
        "Model is not of BPMN format": 0,
        "Model contains less than five elements": 0,
        "Model has no starting point": 0,
        "Model has more than two pools": 0,
        "JSON formatting error": 0
    }

    for file_name in tqdm(get_files(dir_path), desc="Parsing Progress"):

        csv_file = get_file(file_name, dir_path)

        if is_file(csv_file):
            for chunk in read_csv_chunk(csv_file):

                models = load_chunked_models(chunk)

                for model in models:

                    try:
                        if not is_model_valid(model, filtered_models):
                            continue

                        flatten_bpmn(model)
                        total_models = inc(total_models, 1)
                        result = extract_parsed_tokens(model, False)
                        count_result = len(result)
                        total_activities = count_activities(model)

                        parsed_elements = inc(parsed_elements, count_result)
                        total_elements = inc(total_elements, total_activities)

                        num_elements = count_elements(model)
                        types = count_element_types(model)
                        num_types = len(types)

                        unique_elements = unique_elements.union(
                            get_unique_element_types(model))

                        obj = create_parsed_object(count_result, num_elements,
                                                   num_types)
                        parsed_models.append(obj)

                        if count_result != total_activities:
                            partial_parsed_models = inc(
                                partial_parsed_models, 1)

                            obj = create_scatter_object(
                                "partial", num_elements, num_types)

                            plot_models.append(obj)

                            percentage = 100 * float(count_result) / float(
                                total_activities)
                            obj = create_partial_object(
                                percentage, num_elements, num_types)

                            partial_models.append(obj)
                            continue

                        successful_models = inc(successful_models, 1)
                        obj = create_scatter_object("successful", num_elements,
                                                    num_types)

                        plot_models.append(obj)

                    except Exception:
                        failed_models = inc(failed_models, 1)

                        plot_models.append(
                            create_scatter_object("failed", num_elements,
                                                  num_types))
        break
    create_scatter_plot(partial_models)
    create_scatter_plot(parsed_models)
    create_bar_plot(filtered_models)

    print_result(failed_models, successful_models, total_models,
                 parsed_elements, total_elements, partial_parsed_models)
