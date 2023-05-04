"""Expected results for OR tests"""
# pylint: disable=duplicate-code

EXPECTED_PARSED_SINGLE_OR_GATEWAY_RESULT = [{
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
    "leads_to_joining_gateway":
    True,
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
    "leads_to_joining_gateway":
    True,
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
    "leads_to_joining_gateway":
    True,
    "is_start":
    False,
    "is_end":
    False
}]
EXPECTED_COMPILED_SINGLE_OR_GATEWAY_RESULT = [{
    "desc": "Starts with 0",
    "declare": "Init(0)",
    "signal": "(^'0')"
}, {
    "desc":
    "0 precedes 1",
    "declare":
    "Precedence(0,1)",
    "signal":
    "(^ (NOT '0' | ('0' (NOT '0')* '1'))*$)"
}, {
    "desc":
    "0 precedes 2",
    "declare":
    "Precedence(0,2)",
    "signal":
    "(^ (NOT '0' | ('0' (NOT '0')* '2'))*$)"
}, {
    "desc":
    "0 precedes 3",
    "declare":
    "Precedence(0,3)",
    "signal":
    "(^ (NOT '0' | ('0' (NOT '0')* '3'))*$)"
}, {
    "desc":
    "1 xor 2",
    "declare":
    "Exclusive Choice(2,1)",
    "signal":
    "(^(((NOT('1')*) ('2' NOT('1')*)*)|((NOT('2')*)('1' NOT('2')*)*))$)"
}, {
    "desc":
    "1 xor 3",
    "declare":
    "Exclusive Choice(3,1)",
    "signal":
    "(^(((NOT('1')*) ('3' NOT('1')*)*)|((NOT('3')*)('1' NOT('3')*)*))$)"
}, {
    "desc":
    "2 xor 3",
    "declare":
    "Exclusive Choice(3,2)",
    "signal":
    "(^(((NOT('2')*) ('3' NOT('2')*)*)|((NOT('3')*)('2' NOT('3')*)*))$)"
}, {
    "desc":
    "1 responds to 4",
    "declare":
    "Response(1,4)",
    "signal":
    "(^NOT('1')* ('1' ANY*'4')* NOT('1')*$)"
}, {
    "desc":
    "2 responds to 4",
    "declare":
    "Response(2,4)",
    "signal":
    "(^NOT('2')* ('2' ANY*'4')* NOT('2')*$)"
}, {
    "desc":
    "3 responds to 4",
    "declare":
    "Response(3,4)",
    "signal":
    "(^NOT('3')* ('3' ANY*'4')* NOT('3')*$)"
}, {
    "desc": "Ends with 4",
    "declare": "End(4)",
    "signal": "('4'$)"
}]
