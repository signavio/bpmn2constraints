"""Expected results for linear tests"""
# pylint: disable=duplicate-code
# pylint: disable=line-too-long

EXPECTED_PARSED_LINEAR_SEQUENCE_RESULT = [{
    "type":
    "Task",
    "name":
    "register invoice",
    "id":
    "sid-79912385-C358-446C-8EBB-07429B015548",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "check invoice",
        "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593"
    }],
    "predecessors": [],
    "is_start":
    True,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "check invoice",
    "id":
    "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "accept invoice",
        "id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54"
    }],
    "predecessors": [{
        "name": "register invoice"
    }],
    "is_start":
    False,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "accept invoice",
    "id":
    "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "EndNoneEvent"
    }],
    "predecessors": [{
        "name": "check invoice"
    }],
    "is_start":
    False,
    "is_end":
    True
}]

EXPECTED_COMPILED_LINEAR_SEQUENCE_RESULT = [{
    "desc": "Starts with register invoice",
    "declare": "Init(register invoice)",
    "signal": "(^'register invoice')"
}, {
    "desc":
    "register invoice leads to check invoice",
    "declare":
    "Succession(register invoice,check invoice)",
    "signal":
    "(^NOT('register invoice'|'check invoice')*('register invoice'~>'check invoice')*NOT('register invoice'|'check invoice')*$)"
}, {
    "desc":
    "check invoice leads to accept invoice",
    "declare":
    "Succession(check invoice,accept invoice)",
    "signal":
    "(^NOT('check invoice'|'accept invoice')*('check invoice'~>'accept invoice')*NOT('check invoice'|'accept invoice')*$)"
}, {
    "desc": "Ends with accept invoice",
    "declare": "End(accept invoice)",
    "signal": "('accept invoice'$)"
}]
