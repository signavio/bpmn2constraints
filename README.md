# BPMN2Constraints
[![REUSE status](https://api.reuse.software/badge/github.com/signavio/bpmn2constraints)](https://api.reuse.software/info/github.com/signavio/bpmn2constraints)
![Python](https://img.shields.io/badge/python-3.8-blue.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Test](https://github.com/signavio/bpmn2constraints/actions/workflows/main.yml/badge.svg)](https://github.com/signavio/bpmn2constraints/actions/workflows/main.yml/badge.svg)
[![Lint](https://github.com/signavio/bpmn2constraints/actions/workflows/lint.yml/badge.svg)](https://github.com/signavio/bpmn2constraints/actions/workflows/lint.yml/badge.svg)




Tool for compiling BPMN models directly to constraints. Currently, BPMN2Constraints can compile BPMN models stored in both `JSON` and `XML` format and output to `DECLARE`, `SIGNAL` and `Linear Temporal Logic on Finite Traces` (LTLf). BPMN2Constraints can also compile BPMN diagrams to Mermaid.js compatible flowcharts.

## Installation.
Install with:
```terminal
pip install .
```
 or:
 ```terminal
pip install -e .
```
When developing.

## Video & Tutorial.


https://github.com/signavio/bpmn2constraints/assets/5434565/2539b3b4-3e32-4c4b-b211-100e256b9ace


The original (high-resolution) video file is also contained in this repository and can be downloaded.

A tutorial that provides a walk-through of how to use the tool in an SAP Signavio context is provided [here](./tutorial/tutorial.ipynb).

## Using the tool.
Currently, the tool is only available as a CLI tool. To use it, follow these instructions:
1. Parsing a BPMN process diagram.
```bash
bpmnconstraints --parse path/to/process/diagram[.xml, .json]
```
2. Compiling a BPMN process diagram.
```bash
bpmnconstraints --compile path/to/process/diagram[.xml, .json]
```
3. Parsing a dataset.
```bash
bpmnconstraints --parse_dataset path/to/folder/which/contains/dataset[.xml, .json]
```
> Note: The script requires the path to be towards the folder in which the CSV files are stored, not to a CSV file directly.
4. Comparing constraints.
The tool can be used to compare it's generated constraints through the metrics of precision and recall.
```bash
bpmnconstraints --compare_constraints True --dataframe path/to/dataframe --dataset path/to/dataset
```
> Note: The dataframe must be a pickled dataframe, containing a "model_id" column aswell as a "constraints" column. The dataset should be a CSV file.

5. Compiling to a Mermaid.js flowchart.
```bash
bpmnconstraints --compile_to_mermaid path/to/process/diagram[.xml, .json]
```

Optional flags:
1.  `--transitivity` (set to True) for generating constraints with transitive closure.
2. `--plot` (set to True) for generating plots.
> Note: The `--plot` flag will only generate plots for ``--parse_dataset`` and `--compare_constraints`

### Parsing and Compiling Datasets.
To parse an dataset, the CSV file must contain a column which is named `Model JSON`, in which the model is stored.

## Examples:
![Linear BPMN diagram](/assets/linear.png)
1. Parsing a linear diagram, without transitivity.
```json
[
  {
    "name": "register invoice",
    "type": "task",
    "id": "sid-79912385-C358-446C-8EBB-07429B015548",
    "successor": [
      {
        "name": "check invoice",
        "type": "task",
        "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
        "gateway successor": false,
        "splitting": false,
        "is end": false
      }
    ],
    "predecessor": [
      {
        "name": "start",
        "type": "startnoneevent",
        "id": "sid-8FB33325-7680-4AAD-A043-3C38D2758329",
        "gateway successor": false,
        "splitting": false,
        "is end": false
      }
    ],
    "is start": true,
    "is end": false
  },
  {
    "name": "check invoice",
    "type": "task",
    "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
    "successor": [
      {
        "name": "accept invoice",
        "type": "task",
        "id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
        "gateway successor": false,
        "splitting": false,
        "is end": true
      }
    ],
    "predecessor": [
      {
        "name": "register invoice",
        "type": "task",
        "id": "sid-79912385-C358-446C-8EBB-07429B015548",
        "gateway successor": false,
        "splitting": false,
        "is end": false
      }
    ],
    "is start": false,
    "is end": false
  },
  {
    "name": "accept invoice",
    "type": "task",
    "id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
    "successor": [
      {
        "name": "end",
        "type": "endnoneevent",
        "id": "sid-EFFF67BA-ECAB-4A2F-ADE8-A97373DF23F1",
        "gateway successor": false,
        "splitting": false,
        "is end": true
      }
    ],
    "predecessor": [
      {
        "name": "check invoice",
        "type": "task",
        "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
        "gateway successor": false,
        "splitting": false,
        "is end": false
      }
    ],
    "is start": false,
    "is end": true
  }
]
```

2. Compiling (the same) linear diagram.
```json
[
  {
    "description": "starts with register invoice",
    "SIGNAL": "(^'register invoice')",
    "DECLARE": "Init[register invoice]",
    "LTLf": "register_invoice"
  },
  {
    "description": "register invoice leads to check invoice",
    "SIGNAL": "(^NOT('register invoice'|'check invoice')*('register invoice'~>'check invoice')*NOT('register invoice'|'check invoice')*$)",
    "DECLARE": "Succession[register invoice, check invoice]",
    "LTLf": "(G((register_invoice) -> (F(check_invoice)))) & (((~(check_invoice)) U (register_invoice)) | (G(~(check_invoice))))"
  },
  {
    "description": "register invoice and check invoice",
    "SIGNAL": "(^NOT('register invoice'|'check invoice')*(('register invoice'ANY*'check invoice'ANY*)|('check invoice'ANY* 'register invoice' ANY*))* NOT('register invoice'|'check invoice')*$)",
    "DECLARE": "Co-Existence[check invoice, register invoice]",
    "LTLf": "((F(check_invoice)) -> (F(register_invoice))) & ((F(register_invoice)) -> (F(check_invoice)))"
  },
  {
    "description": "register invoice or check invoice",
    "SIGNAL": "(('register invoice'|'check invoice'))",
    "DECLARE": "Choice[check invoice, register invoice]",
    "LTLf": "(F(check_invoice)) | (F(register_invoice))"
  },
  {
    "description": "register invoice leads to (with loops) check invoice",
    "SIGNAL": "( ^ NOT('register invoice'|'check invoice')* ('register invoice'NOT('register invoice'|'check invoice')*'check invoice'NOT('register invoice'|'check invoice')*)*NOT('register invoice'|'check invoice')* $)",
    "DECLARE": "Alternate Succession[register invoice, check invoice]",
    "LTLf": "(G((register_invoice) -> (X[!]((~(register_invoice)) U (check_invoice))))) & (((~(check_invoice)) U (register_invoice)) | (G(~(check_invoice)))) & (G((check_invoice) -> (((~(check_invoice)) U (register_invoice)) | (G(~(check_invoice))))))"
  },
  {
    "description": "check invoice leads to accept invoice",
    "SIGNAL": "(^NOT('check invoice'|'accept invoice')*('check invoice'~>'accept invoice')*NOT('check invoice'|'accept invoice')*$)",
    "DECLARE": "Succession[check invoice, accept invoice]",
    "LTLf": "(G((check_invoice) -> (F(accept_invoice)))) & (((~(accept_invoice)) U (check_invoice)) | (G(~(accept_invoice))))"
  },
  {
    "description": "check invoice and accept invoice",
    "SIGNAL": "(^NOT('check invoice'|'accept invoice')*(('check invoice'ANY*'accept invoice'ANY*)|('accept invoice'ANY* 'check invoice' ANY*))* NOT('check invoice'|'accept invoice')*$)",
    "DECLARE": "Co-Existence[accept invoice, check invoice]",
    "LTLf": "((F(accept_invoice)) -> (F(check_invoice))) & ((F(check_invoice)) -> (F(accept_invoice)))"
  },
  {
    "description": "check invoice or accept invoice",
    "SIGNAL": "(('check invoice'|'accept invoice'))",
    "DECLARE": "Choice[accept invoice, check invoice]",
    "LTLf": "(F(accept_invoice)) | (F(check_invoice))"
  },
  {
    "description": "check invoice leads to (with loops) accept invoice",
    "SIGNAL": "( ^ NOT('check invoice'|'accept invoice')* ('check invoice'NOT('check invoice'|'accept invoice')*'accept invoice'NOT('check invoice'|'accept invoice')*)*NOT('check invoice'|'accept invoice')* $)",
    "DECLARE": "Alternate Succession[check invoice, accept invoice]",
    "LTLf": "(G((check_invoice) -> (X[!]((~(check_invoice)) U (accept_invoice))))) & (((~(accept_invoice)) U (check_invoice)) | (G(~(accept_invoice)))) & (G((accept_invoice) -> (((~(accept_invoice)) U (check_invoice)) | (G(~(accept_invoice))))))"
  },
  {
    "description": "ends with accept invoice",
    "SIGNAL": "('accept invoice'$)",
    "DECLARE": "End[accept invoice]",
    "LTLf": "F((accept_invoice) & (X[!](false)))"
  }
]
```
3. Translating the diagram to Mermaid.js.
```yaml
    flowchart LR
    0:startnoneevent:((start))-->1:task:(register invoice)
    1:task:-->2:task:(check invoice)
    2:task:-->3:task:(accept invoice)
    3:task:-->4:endnoneevent:((end))
```
Which results in the following graph, if interpreted by Mermaid.js.
<img width="836" alt="MicrosoftTeams-image (4)" src="https://github.com/signavio/bpmn2constraints/assets/80515896/c26e81c3-4f4c-4d5c-8abb-2bae40cacc42">

## Acknowledgements.
This project has been authored by:
- Arvid Bergman ([@arvidbt](https://github.com/arvidbt)),
- Timotheus Kampik ([@TimKam](https://github.com/TimKam)),
- Adrian Rebmann ([@adrianrebmann](https://github.com/adrianrebmann)).


