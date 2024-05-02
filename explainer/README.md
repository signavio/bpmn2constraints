# Symbolic Explanations of Process Conformance Violations
This module is made by Marcus Rost, for his thesis subject, **Symbolic Explanations for Control-Flow Objects**. 

The code should work properly, with some hard-coded parts that requires the data set for the signal code to function. This module is more seen as a proof of concept, where some core functions from explainability theory is utilized.

## Overview
The module mainly consists of 2 classes, ExplainerRegex and ExplainerSignal.

**ExplainerRegex** is meant to simulate a real event log and system, with traces and constraints, using regex patterns.

**ExplainerSignal** uses real event logs to calculate the explanations. This uses SAP Signavio's API to do so, but should in reality have it's own interpreter for the Signal queries, instead of having to make API calls. 

Currently, the Signal code is sort of bad and specialized for the specific data set used. Hopefully, someone can see the value of what it done, and generalize it further.

There is also 2 Notebook's located in `explainer/tutorial`, but I recommend doing `bpmn2constraints/tutorial/tutorial.ipynb` first, to see how to do the configuration for the API works.