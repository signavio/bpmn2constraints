from file_constants import (
    LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END,
    PARALLEL_GATEWAY_DIAGRAM,
)
from test_utils import init_test_setup

def test_successor_is_also_in_transative_closure():
    res = init_test_setup(LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END)
    for elem in res:
        if elem.get("is start"):
            transitive_elems = [x.get("id") for x in elem.get("transitivity")]
            assert LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END.get("successor id") in transitive_elems

def test_transative_closure_between_elements_before_and_after_gateway_construct():
    res = init_test_setup(PARALLEL_GATEWAY_DIAGRAM)
    for elem in res:
        if elem.get("is start"):
            transitive_elems = [x.get("id") for x in elem.get("transitivity")]
            assert PARALLEL_GATEWAY_DIAGRAM.get("ending element id") in transitive_elems