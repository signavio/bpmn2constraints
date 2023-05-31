
# pylint: disable=bare-except
from tqdm import tqdm
import traceback

from bpmnsignal.parser.bpmn_parser import Parser
from bpmnsignal.utils.script_utils import Setup
from bpmnsignal.utils.plot import Plot


def create_scatter_object(model_outcome, element_count, type_count):
    return {
        "outcome": model_outcome,
        "number of elements": element_count,
        "number of element types": type_count
    }


def create_partial_object(percentage, element_count, type_count):
    return {
        "variable": percentage,
        "number of elements": element_count,
        "number of element types": type_count
    }


def run_script(dir_path):
    setup = Setup(dir_path)
    plot = Plot()

    failed_models = 0
    successful_models = 0

    total_parsed_elements = 0
    total_elements = 0
    total_models = 0

    all_models = []

    for filename in tqdm(setup.get_files()):
        csv_file = setup.get_file(filename)

        if setup.is_file(csv_file):
            for chunk in setup.read_csv_chunk(csv_file):
                models = setup.load_models(chunk)

                for model in models:
                    try:
                        parser = Parser(model, False, False)

                        # Check for pools before parser flattens diagram.
                        if parser.count_pools() > 1:
                            continue

                        result = parser.run()

                        # Check for starts after parser has flattened diagram.
                        if not parser.has_start():
                            continue
                        # Check for elements after parser has flattened diagram.
                        if parser.count_model_elements() < 5:
                            continue

                        model_elements = parser.count_model_elements()
                        model_element_types = parser.count_model_element_types()

                        total_models += 1
                        parsed = len(result)
                        parsable = parser.count_parsable_elements()

                        total_parsed_elements += parsed
                        total_elements += parsable

                        if parsed == parsable:
                            # Success
                            successful_models += 1
                            all_models.append(create_scatter_object(
                                "successful", model_elements, model_element_types))

                    except Exception:
                        # Failed
                        failed_models += 1
                        # For some reason, I have to subtract here..
                        successful_models -= 1
                        all_models.append(create_scatter_object(
                            "failed", model_elements, model_element_types))

    plot.scatter_plot_model_outcomes(all_models, "All Parsed Models")
    plot.bar_plot_model_outcomes(all_models)

    print(f"Successful: {successful_models} out of {total_models}")
    print(f"Failed: {failed_models} out of {total_models}")
    print(f"Parsed {total_parsed_elements} out of {total_elements} elements.")


if __name__ == "__main__":
    run_script("../../Downloads/sap_sam_2022/models")
