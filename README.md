# bpmn-to-signal

![CI status](https://github.com/signavio/bpmn-to-signal/actions/workflows/pylint.yml/badge.svg)
![CI status](https://github.com/signavio/bpmn-to-signal/actions/workflows/main.yml/badge.svg)

A work-in-progress prototype tool for compiling BPMN diagrams directly to declarative constraints.
Currently, the tool only works with SAP Signavio files of BPMN process diagrams.

Install with:
```terminal
pip install .
```
 or:
 ```terminal
pip install -e .
```
When developing.

## Using the tool.
The CLI tool offers several options. Here is some of the options available.

1. Parsing a BPMN process diagram.
```terminal
bpmnsignal --parse path/to/process/diagram
```
2. Compiling a BPMN process diagram.
```terminal
bpmnsignal --compile path/to/process/diagram
```
3. Parsing a dataset.
```terminal
bpmnsignal --parse_dataset path/to/folder/which/contains/dataset
```
> Note: The script requires the path to be towards the folder in which the CSV files are stored, not to a CSV file directly.
4. Comparing constraints.
The tool can be used to compare it's generated constraints through the metrics of precision and recall.
```terminal
bpmnsignal --compare_constraints True --dataframe path/to/dataframe --dataset path/to/dataset
```
> Note: The dataframe must be a pickled dataframe, containing a "model_id" column aswell as a "constraints" column. The dataset should be a CSV file.

Optional flags:
1.  `--transitivity` (set to True) for generating constraints with transitive closure.
2. `--plot` (set to True) for generating plots.
> Note: The `--plot` flag will only generate plots for ``--parse_dataset`` and `--compare_constraints`