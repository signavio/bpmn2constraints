from bpmnsignal.utils.script_utils import Setup
from bpmnsignal.parser.bpmn_parser import Parser
from bpmnsignal.compiler.bpmn_compiler import Compiler
from bpmnsignal.utils.plot import Plot
from bpmnsignal.utils.constants import DISCARDED_CONSTRAINTS
import json


def parse_dataframe(path):
    setup = Setup(None)
    df = setup.load_dataframe(path)
    models = []

    for _, row in df.iterrows():
        model = {
            "model id" : row["model_id"],
            "constraints" : [],
        }

        for constraint in row["constraints"]:

            constraint = constraint[:constraint.find("|")].strip()
            
            discarded_constraint = constraint
            if discarded_constraint.split("[")[0] in DISCARDED_CONSTRAINTS:
                continue

            model["constraints"].append(constraint)
        models.append(model)
    return models

def parse_dataset(path, transitivity):
    setup = Setup(None)
    compiled_models = []

    for chunk in setup.read_csv_chunk(path):
        models = setup.load_models(chunk)
        model_id = chunk["Model ID"]

        for i, model in enumerate(models):
            compiled_model = {
                "model id" : model_id.iloc[i],
                "constraints" : [],
            }

            try:
                parser = Parser(model, False, transitivity)

                if parser.count_pools() > 1:
                    continue

                result = parser.run()

                if not parser.has_start():
                    continue
                if parser.count_model_elements() < 5:
                    continue

                num_model_elements = parser.count_model_elements()
                num_model_element_types = parser.count_model_element_types()
                element_types = parser.get_element_types()

                compiled_model.update({
                    "number of elements" : num_model_elements,
                    "number of element types" : num_model_element_types,
                    "element types" : element_types
                })

                compiler = Compiler(result, transitivity)
                result = compiler.run()

                for constraint in result:
                    compiled_model["constraints"].append(constraint.get("DECLARE"))
                
                compiled_models.append(compiled_model)

            except Exception:
                continue
    return compiled_models

def combine_models(petri_net_models, compiler_models):
    combined_models = []
    
    for petri_net_model in petri_net_models:
        model_id = petri_net_model.get("model id")
        petri_net_constraints = petri_net_model.get("constraints")
        found_matching_model = False

        for compiler_model in compiler_models:

            if compiler_model.get("model id") == model_id:
                compiler_constraints =  compiler_model.get("constraints")
                number_of_elements = compiler_model.get("number of elements")
                number_of_element_types = compiler_model.get("number of element types")
                element_types = compiler_model.get("element types")
                found_matching_model = True
                break
        
        if found_matching_model and len(compiler_constraints) > 0 and len(petri_net_constraints) > 0:
            combined_models.append({
                "model id" : model_id,
                "petri net constraints" : list(set(petri_net_constraints)),
                "compiler constraints" : list(set(compiler_constraints)),
                "number of elements" : number_of_elements,
                "number of element types" : number_of_element_types,
                "element types" : element_types,
                "precision" : calculate_precision(petri_net_constraints, compiler_constraints),
                "recall" : calculate_recall(petri_net_constraints, compiler_constraints)
            })

    return combined_models

def calculate_precision(petri_net_constraints, compiler_constraints):
    return len(set(petri_net_constraints).intersection(set(compiler_constraints))) / len(set(compiler_constraints))

def calculate_recall(petri_net_constraints, compiler_constraints):
    return len(set(compiler_constraints).intersection(set(petri_net_constraints))) / len(set(petri_net_constraints))

def run_script():
    plot = Plot()
    # path_to_dataframe = "../../Downloads/dataframes/opalmodel_id_to_constraints.pkl"
    # path_to_dataset = "../../Downloads/opal/OPALdataset.csv"
    path_to_dataset = "../../Downloads/update_sapsam/sap_sam_filtered.csv"
    path_to_dataframe = "../../Downloads/dataframes/sap_sam_filteredmodel_id_to_constraints.pkl"
    
    petri_net_models = parse_dataframe(path_to_dataframe)
    compiler_models = parse_dataset(path_to_dataset, True)

    models = combine_models(petri_net_models, compiler_models)

    recall = []
    precision = []

    for model in models:
        print(json.dumps(model, indent=2))
        recall.append(model.get("recall"))
        precision.append(model.get("precision"))
    
    mean_recall = sum(recall) / len(recall)
    mean_precision = sum(precision) / len(precision)

    print(mean_precision)
    print(mean_recall)

    # plot.bar_plot_total_generated_constraints(models)
    # plot.scatter_plot_recall_precision_combined_approaches(models)
    # plot.scatter_plot_precision_element_types(models)
    # plot.scatter_plot_recall_element_types(models)
    

if __name__ == "__main__":
    run_script()