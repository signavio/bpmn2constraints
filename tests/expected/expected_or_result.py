"""Expected results for OR tests"""
# pylint: disable=duplicate-code

EXPECTED_SINGLE_OR_GATEWAY_RESULT = [{
    "type":
    "Task",
    "name":
    "0",
    "id":
    "sid-EDFCFD39-8583-45B8-91B3-8E1A9CE45900",
    "leads_to_gateway":
    True,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "1",
        "id": "sid-AD61A674-0B58-41F2-B14D-53A0F6A0ED9A",
        "precedes": "0"
    }, {
        "type": "Task",
        "name": "2",
        "id": "sid-D76A99F6-2768-4ED0-841C-171162FB9077",
        "precedes": "0"
    }, {
        "type": "Task",
        "name": "3",
        "id": "sid-29940651-400D-43AD-BA8D-7EC276331D33",
        "precedes": "0"
    }],
    "predecessors": [],
    "type_of_gateway":
    "OR",
    "is_start":
    True,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "1",
    "id":
    "sid-AD61A674-0B58-41F2-B14D-53A0F6A0ED9A",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "4",
        "id": "sid-8E60DB04-AFC4-4DF3-A18B-D81050A3A43E"
    }],
    "predecessors": [{
        "name": "0"
    }],
    "is_start":
    False,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "4",
    "id":
    "sid-8E60DB04-AFC4-4DF3-A18B-D81050A3A43E",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    True,
    "successors": [{
        "type": "EndNoneEvent"
    }],
    "predecessors": [{
        "name": "1"
    }, {
        "name": "2"
    }, {
        "name": "3"
    }],
    "is_start":
    False,
    "is_end":
    True
}, {
    "type":
    "Task",
    "name":
    "2",
    "id":
    "sid-D76A99F6-2768-4ED0-841C-171162FB9077",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "4",
        "id": "sid-8E60DB04-AFC4-4DF3-A18B-D81050A3A43E"
    }],
    "predecessors": [{
        "name": "0"
    }],
    "is_start":
    False,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "3",
    "id":
    "sid-29940651-400D-43AD-BA8D-7EC276331D33",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "4",
        "id": "sid-8E60DB04-AFC4-4DF3-A18B-D81050A3A43E"
    }],
    "predecessors": [{
        "name": "0"
    }],
    "is_start":
    False,
    "is_end":
    False
}]
