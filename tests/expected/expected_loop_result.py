"""Expected results for loop tests"""
# pylint: disable=duplicate-code

EXPECTED_SIMPLE_LOOP_RESULT = [{
    "type":
    "Task",
    "name":
    "a",
    "id":
    "sid-F053B1F0-9893-4286-A676-9504E8901E45",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "Task",
        "name": "b",
        "id": "sid-07735648-495B-411E-BD2D-3191A4DD79A6"
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
    "b",
    "id":
    "sid-07735648-495B-411E-BD2D-3191A4DD79A6",
    "leads_to_gateway":
    False,
    "succeeds_gateway":
    True,
    "successors": [{
        "type": "Task",
        "name": "c",
        "id": "sid-CF4371BA-AC7D-47AA-B6C0-AB3F78751467"
    }],
    "predecessors": [{
        "name": "a"
    }, {
        "name": "c"
    }],
    "is_start":
    False,
    "is_end":
    False
}, {
    "type":
    "Task",
    "name":
    "c",
    "id":
    "sid-CF4371BA-AC7D-47AA-B6C0-AB3F78751467",
    "leads_to_gateway":
    True,
    "succeeds_gateway":
    False,
    "successors": [{
        "type": "EndNoneEvent",
        "precedes": "c"
    }, {
        "type": "Task",
        "name": "b",
        "id": "sid-07735648-495B-411E-BD2D-3191A4DD79A6",
        "precedes": "c"
    }],
    "predecessors": [{
        "name": "b"
    }],
    "type_of_gateway":
    "XOR",
    "is_loop":
    True,
    "is_start":
    False,
    "is_end":
    True
}]
