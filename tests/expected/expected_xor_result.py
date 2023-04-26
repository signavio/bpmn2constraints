"""Expected results for XOR tests"""
# pylint: disable=duplicate-code

EXPECTED_SINGLE_XOR_GATEWAY = [{
    "type":
    "Task",
    "name":
    "activity0",
    "id":
    "sid-FBAC8519-FC55-4A05-B903-F6E79713FDDC",
    "leads_to_gateway":
    True,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "activity2",
        "id": "sid-3D6E85B2-C493-4A89-9583-42CF2400E8EF",
        "precedes": "activity0"
    }, {
        "type": "Task",
        "name": "activity1",
        "id": "sid-FA542405-840E-4DF8-BCCE-D9D3E122EED5",
        "precedes": "activity0"
    }],
    "predecessors": [],
    "type_of_gateway":
    "XOR",
    "is_start":
    True,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "activity2",
    "id":
    "sid-3D6E85B2-C493-4A89-9583-42CF2400E8EF",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "activity3",
        "id": "sid-98FAE708-4E10-4373-BD3D-72443CA5B619"
    }],
    "predecessors": [{
        "name": "activity0"
    }],
    "is_start":
    False,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "activity3",
    "id":
    "sid-98FAE708-4E10-4373-BD3D-72443CA5B619",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    True,
    "successors": [{
        "type": "EndNoneEvent"
    }],
    "predecessors": [{
        "name": "activity2"
    }, {
        "name": "activity1"
    }],
    "is_start":
    False,
    "is_end":
    True
}, {
    "type":
    "Task",
    "name":
    "activity1",
    "id":
    "sid-FA542405-840E-4DF8-BCCE-D9D3E122EED5",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "activity3",
        "id": "sid-98FAE708-4E10-4373-BD3D-72443CA5B619"
    }],
    "predecessors": [{
        "name": "activity0"
    }],
    "is_start":
    False,
    "is_end":
    False
}]
