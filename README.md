# BPMN2Constraints

![CI status](https://github.com/signavio/bpmn-to-signal/actions/workflows/pylint.yml/badge.svg)
![CI status](https://github.com/signavio/bpmn-to-signal/actions/workflows/main.yml/badge.svg)

Tool for compiling BPMN diagrams in JSON format directly to declarative constraints.

Install with:
```terminal
pip install .
```
 or:
 ```terminal
pip install -e .
```
When developing.

## Video


https://github.com/signavio/bpmn-to-signal/assets/126496635/4b9a027d-e502-4b35-9f34-91bc5253a5eb

The original (high-resolution) video file is also contained in this repository and can be downloaded.

## Using the tool.
The CLI tool offers several options. Here is some of the options available.

1. Parsing a BPMN process diagram.
```terminal
bpmnconstraints --parse path/to/process/diagram
```
2. Compiling a BPMN process diagram.
```terminal
bpmnconstraints --compile path/to/process/diagram
```
3. Parsing a dataset.
```terminal
bpmnconstraints --parse_dataset path/to/folder/which/contains/dataset
```
> Note: The script requires the path to be towards the folder in which the CSV files are stored, not to a CSV file directly.
4. Comparing constraints.
The tool can be used to compare it's generated constraints through the metrics of precision and recall.
```terminal
bpmnconstraints --compare_constraints True --dataframe path/to/dataframe --dataset path/to/dataset
```
> Note: The dataframe must be a pickled dataframe, containing a "model_id" column aswell as a "constraints" column. The dataset should be a CSV file.

Optional flags:
1.  `--transitivity` (set to True) for generating constraints with transitive closure.
2. `--plot` (set to True) for generating plots.
> Note: The `--plot` flag will only generate plots for ``--parse_dataset`` and `--compare_constraints`

## Examples:
1. Parsing a linear diagram, without transitivity.
```json
[
  {
    "name": "register invoice",
    "type": "Task",
    "id": "sid-79912385-C358-446C-8EBB-07429B015548",
    "successor": [
      {
        "name": "check invoice",
        "type": "Task",
        "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
        "gateway successor": false
      }
    ],
    "predecessor": [
      {
        "name": "start",
        "type": "StartNoneEvent",
        "id": "sid-8FB33325-7680-4AAD-A043-3C38D2758329",
        "gateway successor": false
      }
    ],
    "is start": true,
    "is end": false
  },
  {
    "name": "check invoice",
    "type": "Task",
    "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
    "successor": [
      {
        "name": "accept invoice",
        "type": "Task",
        "id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
        "gateway successor": false
      }
    ],
    "predecessor": [
      {
        "name": "register invoice",
        "type": "Task",
        "id": "sid-79912385-C358-446C-8EBB-07429B015548",
        "gateway successor": false
      }
    ],
    "is start": false,
    "is end": false
  },
  {
    "name": "accept invoice",
    "type": "Task",
    "id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
    "successor": [
      {
        "name": "end",
        "type": "EndNoneEvent",
        "id": "sid-EFFF67BA-ECAB-4A2F-ADE8-A97373DF23F1",
        "gateway successor": false
      }
    ],
    "predecessor": [
      {
        "name": "check invoice",
        "type": "Task",
        "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
        "gateway successor": false
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
    "SIGNAL": "(^NOT(register invoice|check invoice)*((register invoiceANY*check invoiceANY*)|(check invoiceANY* 'register invoice' ANY*))* NOT('register invoice'|'check invoice')*$)",
    "DECLARE": "Co-Existence[check invoice, register invoice]",
    "LTLf": "((F(check_invoice)) -> (F(register_invoice))) & ((F(register_invoice)) -> (F(check_invoice)))"
  },
  {
    "description": "register invoice leads to check invoice",
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
    "SIGNAL": "(^NOT(check invoice|accept invoice)*((check invoiceANY*accept invoiceANY*)|(accept invoiceANY* 'check invoice' ANY*))* NOT('check invoice'|'accept invoice')*$)",
    "DECLARE": "Co-Existence[accept invoice, check invoice]",
    "LTLf": "((F(accept_invoice)) -> (F(check_invoice))) & ((F(check_invoice)) -> (F(accept_invoice)))"
  },
  {
    "description": "check invoice leads to accept invoice",
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
