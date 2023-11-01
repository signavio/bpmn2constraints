LINEAR_SEQUENCE_DIAGRAM_WITH_START_AND_END = {
    "path": "examples/linear/linear_sequence.json",
    "xmlpath": "examples/linear/linear_sequence.xml",
    "start element id": "sid-79912385-C358-446C-8EBB-07429B015548",
    "end element id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
    "successor id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
}

LINEAR_SEQUENCE_DIAGRAM_WITHOUT_START_AND_END = {
    "path": "examples/misc/no_start_no_end.json",
    "xmlpath": "examples/misc/no_start_no_end.xml",
    "start element id": "sid-E9508543-5660-4C85-9E42-1119DAAD80C2",
    "end element id": "sid-08543ADB-C8D6-4026-8A03-1228CC559A7F",
}

MULTIPLE_STARTS_DIAGRAM = {
    "path": "examples/misc/multiple_starts.json",
    "xmlpath": "examples/misc/multiple_starts.xml",
    "start elements": [
        "sid-63552E64-B2A2-4D39-A168-2C6A30BB76F7",
        "sid-AB69BFC4-A028-480F-BC16-BAC74F4A8EDD",
    ],
}

MULTIPLE_ENDINGS_DIAGRAM = {
    "path": "examples/misc/multiple_endings.json",
    "xmlpath": "examples/misc/multiple_endings.xml",
    "ending elements": [
        "sid-F54D1372-E982-4B0F-9543-F3CC3C6F595F",
        "sid-42CD2A75-895E-4E2C-9340-6CE7C5570EFF",
        "sid-E458F27F-287A-4901-BDE9-53A21534EB2F",
    ],
}

SINGLE_XOR_GATEWAY_DIAGRAM = {
    "path": "examples/xor_gates/single_xor.json",
    "xmlpath": "examples/xor_gates/single_xor.xml",
    "splitting id": "sid-E1967D7F-6A3B-40CB-A8E9-31606735C37A",
    "joining id": "sid-87FDC0D7-9BEE-4FB2-952A-FEDEA56F73AA",
}

THREE_SPLIT_XOR_GATEWAY_DIAGRAM = {
    "path": "examples/xor_gates/3_way_split_xor.json",
    "xmlpath": "examples/xor_gates/3_way_split_xor.xml",
    "splitting id": "sid-7946CDE8-E0E9-4730-8D59-E48E15C331B8",
    "successors": [
        "sid-DEEAF1CC-6862-41BE-8FE4-C9630A72A6E7",
        "sid-27B96763-D095-4BE1-8A75-3ADA952DF65B",
        "sid-C4EA710A-B1E4-4561-A8AE-03D48DD6B5A6",
    ],
}

PARALLEL_GATEWAY_DIAGRAM = {
    "path": "examples/and_gates/longer_and.json",
    "xmlpath": "examples/and_gates/longer_and.xml",
    "start element id": "sid-2FE6222A-6971-4860-AD8D-535CED93A0A2",
    "ending element id": "sid-41F52A20-F3FC-4363-9A0C-A73114841060",
    "gateway elements": [
        "sid-88D31641-1A4E-4DA6-96FB-6CDEDCD3F8C4",
        "sid-A7B7239A-5E3E-47A7-8D0F-D183CA3B421D",
        "sid-64F1770B-32AC-4C4D-B0B8-EFED88015C1E",
        "sid-7D01BA2F-0D34-4F8A-9BAA-E7271C0E8879",
        "sid-BFBA9C81-7675-4BCE-83B6-9E591C320E47",
        "sid-E1E842E0-BC33-4DB3-97E6-778B589A07A0",
    ],
    "not gateway elements": [
        "sid-2FE6222A-6971-4860-AD8D-535CED93A0A2",
        "sid-41F52A20-F3FC-4363-9A0C-A73114841060",
    ],
}

XOR_GATEWAY_DIAGRAM = {
    "path": "examples/xor_gates/longer_xor.json",
    "xmlpath": "examples/xor_gates/longer_xor.xml",
}

XOR_GATEWAY_SEQUENCE_DIAGRAM = {
    "path": "examples/xor_gates/multiple_xor.json",
    "xmlpath": "examples/xor_gates/multiple_xor.xml",
}

REQUIREMENTS_TXT = {"path": "requirements.txt"}

LINEAR_MERMAID_GRAPH = {
    "path": "examples/linear/linear_sequence.json",
    "xmlpath": "examples/linear/linear_sequence.xml",
    "output": "flowchart LR\n0:startnoneevent:((start))-->1:task:(register invoice)\n1:task:-->2:task:(check invoice)\n2:task:-->3:task:(accept invoice)\n3:task:-->4:endnoneevent:((end))",
}

GATEWAY_MERMAID_GRAPH = {
    "path": "examples/xor_gates/single_xor.json",
    "xmlpath": "examples/xor_gates/single_xor.xml",
    "output": "flowchart LR\n0:exclusive_databased_gateway:{XOR}-->1:task:(second activity)\n0:exclusive_databased_gateway:{XOR}-->2:task:(first activity)\n3:exclusive_databased_gateway:{XOR}-->4:task:(third activity)\n2:task:-->3:exclusive_databased_gateway:\n1:task:-->3:exclusive_databased_gateway:\n4:task:-->5:endnoneevent:((endnoneevent))\n6:startnoneevent:((startnoneevent))-->7:task:(zero activity)\n7:task:-->0:exclusive_databased_gateway:",
}
