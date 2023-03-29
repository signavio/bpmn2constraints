# bpmn-to-signal

Work-in-progress prototype for compiling BPMN control flow to SIGNAL constraints.
Works with SAP Signavio JSON files of BPMN process diagrams.

Install with `pip install .` or `pip install -e .` when developing.

Run as command line tool: `bpmnsignal <path_to_file>`, e.g.
`bpmnsignal ./examples/Invoice_processing_SAP_Signavio.json`
for the example provided.

Run tests with `pytest`.

## Linting and Formatting

This project uses PyLint for linting, and PEP 8 guidelines ([Read here](https://peps.python.org/pep-0008/)) for formatting.
