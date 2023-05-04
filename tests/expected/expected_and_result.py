"""Expected results for AND tests"""
# pylint: disable=duplicate-code

EXPECTED_PARSED_SINGLE_AND_GATEWAY_RESULT = [{
    "type":
    "Task",
    "name":
    "activity1",
    "id":
    "sid-E0E3854E-E7CB-4224-A771-2D7B103F5FD9",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "EndNoneEvent"
    }],
    "predecessors": [],
    "leads_to_joining_gateway":
    True,
    "is_start":
    True,
    "is_end":
    True
}, {
    "type":
    "Task",
    "name":
    "activity2",
    "id":
    "sid-863DA24E-9776-4EB3-AB1E-BC9AEF60CF33",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "EndNoneEvent"
    }],
    "predecessors": [],
    "leads_to_joining_gateway":
    True,
    "is_start":
    True,
    "is_end":
    True
}]

EXPECTED_COMPILED_SINGLE_AND_GATEWAY_RESULT = [{
    "desc": "Starts with activity1",
    "declare": "Init(activity1)",
    "signal": "(^'activity1')"
}, {
    "desc": "Ends with activity1",
    "declare": "End(activity1)",
    "signal": "('activity1'$)"
}, {
    "desc": "Starts with activity2",
    "declare": "Init(activity2)",
    "signal": "(^'activity2')"
}, {
    "desc": "Ends with activity2",
    "declare": "End(activity2)",
    "signal": "('activity2'$)"
}]
