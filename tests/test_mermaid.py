from file_constants import LINEAR_MERMAID_GRAPH, GATEWAY_MERMAID_GRAPH
from test_utils import init_test_setup_for_mermaid


def test_linear_mermaid_graph():
    res = init_test_setup_for_mermaid(LINEAR_MERMAID_GRAPH)
    assert LINEAR_MERMAID_GRAPH.get("output") == res


def test_gateway_mermaid_graph():
    res = init_test_setup_for_mermaid(GATEWAY_MERMAID_GRAPH)
    assert GATEWAY_MERMAID_GRAPH.get("output") == res
