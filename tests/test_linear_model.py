"""Simple test for the bpmnsignal_mwe program"""
import json
from bpmnsignal.bpmnsignal_mwe import parse_bpmn, construct_linear_constraints

ACTIVITY_LIST = ['register invoice', 'check invoice', 'accept invoice']
CONSTRAINT_LIST = [
    "(^'register invoice')",
    "(^NOT('register invoice'|'check invoice')*('register invoice'~>'check invoice')\
        *NOT('register invoice'|'check invoice')*$)",
    "(^NOT('check invoice'|'accept invoice')*('check invoice'~>'accept invoice')\
        *NOT('check invoice'|'accept invoice')*$)",
    "('accept invoice'$)"
]
PATH = './examples/Invoice_processing_SAP_Signavio.json'


def test_parse_bpmn():
    """Testing parsing the BPMN diagram"""
    with open(PATH, 'r', encoding='utf-8') as file:
        j_bpmn = json.loads(file.read())
        assert parse_bpmn(j_bpmn) == ACTIVITY_LIST


def test_construct_linear_constraints():
    """Testing constructing constraitns from the sequence"""
    with open(PATH, 'r', encoding='utf-8') as file:
        j_bpmn = json.loads(file.read())
        assert construct_linear_constraints(
            parse_bpmn(j_bpmn)) == CONSTRAINT_LIST
