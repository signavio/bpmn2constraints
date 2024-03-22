"""Setup for running the bpmnconstraints script."""

import setuptools

with open("README.md", encoding="utf-8") as file:
    long_description = file.read().strip()

setuptools.setup(
    name="bpmnconstraints",
    version="0.0.2",
    description="Compiles BPMN models to SIGNAL queries and LTL constraints",
    long_description=long_description,
    author="Arvid Bergman, Timotheus Kampik, Adrian Rebmann",
    author_email="timotheus.kampik@sap.com",
    url="https://github.com/signavio/bpmn2constraints",
    py_modules=["bpmnconstraints"],
    entry_points={"console_scripts": ["bpmnconstraints=bpmnconstraints.script:run"]},
    install_requires=["pylogics", "xmltodict"],
    keywords="BPMN Conformance",
    classifiers=["BPMN", "Conformance Checking"],
)
