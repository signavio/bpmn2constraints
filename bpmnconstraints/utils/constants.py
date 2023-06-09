"""Constants for the parser"""

ALLOWED_GATEWAYS = [
    "Exclusive_Databased_Gateway",
    "ParallelGateway",
    "InclusiveGateway",
    'ComplexGateway',
    'EventbasedGateway',
]

ALLOWED_ACTIVITIES = [
    "Task",
    "Event",
    "CollapsedSubprocess",
    "BusinessRole",
    "EventSubprocess",
    "CollapsedEventSubprocess",
    "Subprocess",
    "Process",
    "IntermediateMessageEventCatching",
    "IntermediateTimerEvent",
    "IntermediateEscalationEvent",
    "IntermediateConditionalEvent",
    "IntermediateLinkEventCatching",
    "IntermediateErrorEvent",
    "IntermediateCancelEvent",
    "IntermediateCompensationEventCatching",
    "IntermediateSignalEventCatching",
    "IntermediateMultipleEventCatching",
    "IntermediateParallelMultipleEventCatching",
    "IntermediateEvent",
    "IntermediateMessageEventThrowing",
    "IntermediateEscalationEventThrowing",
    "IntermediateLinkEventThrowing",
    "IntermediateCompensationEventThrowing",
    "IntermediateSignalEventThrowing",
    "IntermediateMultipleEventThrowing",
]

ALLOWED_START_EVENTS = [
    "StartNoneEvent",
    "StartMessageEvent",
    "StartTimerEvent",
    "StartErrorEvent",
    "StartCompensationEvent",
    "StartParallelMultipleEvent",
    "StartEscalationEvent",
    "StartConditionalEvent",
    "StartSignalEvent",
    "StartMultipleEvent",
]

ALLOWED_END_EVENTS = [
    "End",
    "EndNoneEvent",
    "EndEscalationEvent",
    "EndMessageEvent",
    "EndErrorEvent",
    "EndCancelEvent",
    "EndCompensationEvent",
    "EndSignalEvent",
    "EndMultipleEvent",
    "EndTerminateEvent",
]

ALLOWED_SWIMLANES = [
    "Pool",
    "Lane",
]

ALLOWED_CONNECTING_OBJECTS = ["SequenceFlow"]

GATEWAY_MAPPING = {
    ALLOWED_GATEWAYS[0]: "XOR",
    ALLOWED_GATEWAYS[1]: "AND",
    ALLOWED_GATEWAYS[2]: "OR",
    ALLOWED_GATEWAYS[3]: 'COMPLEX',
    ALLOWED_GATEWAYS[4]: 'EVENT_BASED'
}

END_EVENT_MAPPING = {
    "EndNoneEvent": "EndNoneEvent",
    "EndEscalationEvent": "EndEscalationEvent",
    "EndMessageEvent": "EndMessageEvent",
    "EndErrorEvent": "EndErrorEvent",
    "EndCancelEvent": "EndCancelEvent",
    "EndCompensationEvent": "EndCompensationEvent",
    "EndSignalEvent": "EndSignalEvent",
    "EndMultipleEvent": "EndMultipleEvent",
    "EndTerminateEvent": "EndTerminateEvent",
}

ACTIVITY_MAPPING = {
    "Task": 'Task',
    "Event": 'Event',
    "CollapsedSubprocess": 'Subprocess',
    "EventSubprocess": 'Subprocess',
    "CollapsedEventSubprocess": 'Subprocess',
    "Subprocess": 'Subprocess',
    "IntermediateMessageEventCatching": 'CatchActivity',
    "IntermediateTimerEvent": 'IntermediateEvent',
    "IntermediateEscalationEvent": 'IntermediateEvent',
    "IntermediateConditionalEvent": 'IntermediateEvent',
    "IntermediateLinkEventCatching": 'CatchActivity',
    "IntermediateErrorEvent": 'IntermediateEvent',
    "IntermediateCancelEvent": 'IntermediateEvent',
    "IntermediateCompensationEventCatching": 'CatchActivity',
    "IntermediateSignalEventCatching": 'CatchActivity',
    "IntermediateMultipleEventCatching": 'CatchActivity',
    "IntermediateParallelMultipleEventCatching": 'CatchActivity',
    "IntermediateEvent": 'IntermediateEvent',
    "IntermediateMessageEventThrowing": 'ThrowActivity',
    "IntermediateEscalationEventThrowing": 'ThrowActivity',
    "IntermediateLinkEventThrowing": 'ThrowActivity',
    "IntermediateCompensationEventThrowing": 'ThrowActivity',
    "IntermediateSignalEventThrowing": 'ThrowActivity',
    "IntermediateMultipleEventThrowing": 'ThrowActivity',
}

EXCLUDED_TRANSITIVE_NAMES = [
    "AND",
    "XOR",
    "OR",
    "COMPLEX",
    "EVENT_BASED",
]

DISCARDED_CONSTRAINTS = [
    "Exactly1",
    "Responded Existence",
    "Absence2",
    "Existence1",
    "Existence2",
    "Exactly2"
]

DISCARDED_START_EVENT_NAMES = [
    "start",
    "Start",
    "START",
    "AND",
    "XOR",
    "OR"
]

DISCARDED_END_EVENT_NAMES = [
    "end",
    "End",
    "END",
    "AND",
    "XOR",
    "OR",
]

VALID_NAME_LENGTH = 5

CHILD_SHAPES = "childShapes"
OUTGOING = "outgoing"
ELEMENT_ID = "resourceId"
STENCIL = "stencil"
ID = "id"
PROPERTIES = "properties"
NAME = "name"

DECLARE_CONSTRAINT_REGEX_PATTERN = r'(\w+(?:-\w+)?(?: \w+)?)(?: \w+)?\[(.*?)\]'

DECLARE_GATEWAYS = [
    "Co-Existence",
    "Choice",
    "Exclusive Choice"
]