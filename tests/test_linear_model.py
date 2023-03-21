import json
from bpmnsignal.bpmnsignal import *

activity_list =  ['register invoice', 'check invoice', 'accept invoice']
constraint_list = [
    "(^'register invoice')",
    "(^NOT('register invoice'|'check invoice')*('register invoice'~>'check invoice')*NOT('register invoice'|'check invoice')*$)",
    "(^NOT('check invoice'|'accept invoice')*('check invoice'~>'accept invoice')*NOT('check invoice'|'accept invoice')*$)",
    "('accept invoice'$)"
    ]
path = './examples/Invoice_processing_SAP_Signavio.json'

def test_parse_bpmn():
    with open(path, 'r') as file:
        j_bpmn = json.loads(file.read())
        assert parse_bpmn(j_bpmn) == activity_list

def test_construct_linear_constraints():
    with open(path, 'r') as file:
        j_bpmn = json.loads(file.read())
        assert construct_linear_constraints(parse_bpmn(j_bpmn)) == constraint_list