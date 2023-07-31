from bpmnconstraints.utils.constants import *
DEFAULT_DIRECTION = "LR"
SEQUENCE_FLOW = "-->"

# EXAMPLE = [
#   {
#     "name": "register invoice",
#     "type": "task",
#     "id": "sid-79912385-C358-446C-8EBB-07429B015548",
#     "successor": [
#       {
#         "name": "check invoice",
#         "type": "task",
#         "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "start",
#         "type": "startnoneevent",
#         "id": "sid-8FB33325-7680-4AAD-A043-3C38D2758329",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "is start": True,
#     "is end": False
#   },
#   {
#     "name": "check invoice",
#     "type": "task",
#     "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
#     "successor": [
#       {
#         "name": "accept invoice",
#         "type": "task",
#         "id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": True
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "register invoice",
#         "type": "task",
#         "id": "sid-79912385-C358-446C-8EBB-07429B015548",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "is start": False,
#     "is end": False
#   },
#   {
#     "name": "accept invoice",
#     "type": "task",
#     "id": "sid-BEA0DEB9-2482-42D9-9846-9E6C5541FA54",
#     "successor": [
#       {
#         "name": "end",
#         "type": "endnoneevent",
#         "id": "sid-EFFF67BA-ECAB-4A2F-ADE8-A97373DF23F1",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": True
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "check invoice",
#         "type": "task",
#         "id": "sid-338230CF-C52B-4C83-9B4E-A8388E336593",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "is start": False,
#     "is end": True
#   }
# ]

# EXAMPLE = [
#   {
#     "name": "XOR",
#     "type": "exclusive_databased_gateway",
#     "id": "sid-E1967D7F-6A3B-40CB-A8E9-31606735C37A",
#     "successor": [
#       {
#         "name": "second activity",
#         "type": "task",
#         "id": "sid-3D6E85B2-C493-4A89-9583-42CF2400E8EF",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       },
#       {
#         "name": "first activity",
#         "type": "task",
#         "id": "sid-FA542405-840E-4DF8-BCCE-D9D3E122EED5",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "zero activity",
#         "type": "task",
#         "id": "sid-FBAC8519-FC55-4A05-B903-F6E79713FDDC",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "is start": False,
#     "is end": False,
#     "joining": False,
#     "splitting": True
#   },
#   {
#     "name": "XOR",
#     "type": "exclusive_databased_gateway",
#     "id": "sid-87FDC0D7-9BEE-4FB2-952A-FEDEA56F73AA",
#     "successor": [
#       {
#         "name": "third activity",
#         "type": "task",
#         "id": "sid-98FAE708-4E10-4373-BD3D-72443CA5B619",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": True
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "first activity",
#         "type": "task",
#         "id": "sid-FA542405-840E-4DF8-BCCE-D9D3E122EED5",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       },
#       {
#         "name": "second activity",
#         "type": "task",
#         "id": "sid-3D6E85B2-C493-4A89-9583-42CF2400E8EF",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "is start": False,
#     "is end": False,
#     "joining": True,
#     "splitting": False
#   },
#   {
#     "name": "first activity",
#     "type": "task",
#     "id": "sid-FA542405-840E-4DF8-BCCE-D9D3E122EED5",
#     "successor": [
#       {
#         "name": "XOR",
#         "type": "exclusive_databased_gateway",
#         "id": "sid-87FDC0D7-9BEE-4FB2-952A-FEDEA56F73AA",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False,
#         "gateway successors": [
#           {
#             "name": "third activity",
#             "type": "task",
#             "id": "sid-98FAE708-4E10-4373-BD3D-72443CA5B619",
#             "gateway successor": True,
#             "splitting": False,
#             "is end": True
#           }
#         ]
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "XOR",
#         "type": "exclusive_databased_gateway",
#         "id": "sid-E1967D7F-6A3B-40CB-A8E9-31606735C37A",
#         "gateway successor": False,
#         "splitting": True,
#         "is end": False
#       }
#     ],
#     "is start": False,
#     "is end": False,
#     "is in gateway": True
#   },
#   {
#     "name": "second activity",
#     "type": "task",
#     "id": "sid-3D6E85B2-C493-4A89-9583-42CF2400E8EF",
#     "successor": [
#       {
#         "name": "XOR",
#         "type": "exclusive_databased_gateway",
#         "id": "sid-87FDC0D7-9BEE-4FB2-952A-FEDEA56F73AA",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False,
#         "gateway successors": [
#           {
#             "name": "third activity",
#             "type": "task",
#             "id": "sid-98FAE708-4E10-4373-BD3D-72443CA5B619",
#             "gateway successor": True,
#             "splitting": False,
#             "is end": True
#           }
#         ]
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "XOR",
#         "type": "exclusive_databased_gateway",
#         "id": "sid-E1967D7F-6A3B-40CB-A8E9-31606735C37A",
#         "gateway successor": False,
#         "splitting": True,
#         "is end": False
#       }
#     ],
#     "is start": False,
#     "is end": False,
#     "is in gateway": True
#   },
#   {
#     "name": "third activity",
#     "type": "task",
#     "id": "sid-98FAE708-4E10-4373-BD3D-72443CA5B619",
#     "successor": [
#       {
#         "name": "endnoneevent",
#         "type": "endnoneevent",
#         "id": "sid-EEC2FF0E-3491-42F6-835E-F3602E0F47DF",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": True
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "XOR",
#         "type": "exclusive_databased_gateway",
#         "id": "sid-87FDC0D7-9BEE-4FB2-952A-FEDEA56F73AA",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "is start": False,
#     "is end": True
#   },
#   {
#     "name": "zero activity",
#     "type": "task",
#     "id": "sid-FBAC8519-FC55-4A05-B903-F6E79713FDDC",
#     "successor": [
#       {
#         "name": "XOR",
#         "type": "exclusive_databased_gateway",
#         "id": "sid-E1967D7F-6A3B-40CB-A8E9-31606735C37A",
#         "gateway successor": False,
#         "splitting": True,
#         "is end": False,
#         "gateway successors": [
#           {
#             "name": "second activity",
#             "type": "task",
#             "id": "sid-3D6E85B2-C493-4A89-9583-42CF2400E8EF",
#             "gateway successor": True,
#             "splitting": False,
#             "is end": False
#           },
#           {
#             "name": "first activity",
#             "type": "task",
#             "id": "sid-FA542405-840E-4DF8-BCCE-D9D3E122EED5",
#             "gateway successor": True,
#             "splitting": False,
#             "is end": False
#           }
#         ]
#       }
#     ],
#     "predecessor": [
#       {
#         "name": "startnoneevent",
#         "type": "startnoneevent",
#         "id": "sid-9AB02290-AD8C-433E-AEBC-BC32A1CCBF31",
#         "gateway successor": False,
#         "splitting": False,
#         "is end": False
#       }
#     ],
#     "is start": True,
#     "is end": False
#   }
# ]

EXAMPLE = [
  {
    "name": "activity one",
    "type": "task",
    "id": "sid-8AB55396-4E84-4550-8FBE-EC45A5B43D4C",
    "successor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-7946CDE8-E0E9-4730-8D59-E48E15C331B8",
        "gateway successor": False,
        "splitting": True,
        "is end": False,
        "gateway successors": [
          {
            "name": "activity two",
            "type": "task",
            "id": "sid-DEEAF1CC-6862-41BE-8FE4-C9630A72A6E7",
            "gateway successor": True,
            "splitting": False,
            "is end": False
          },
          {
            "name": "activity four",
            "type": "task",
            "id": "sid-27B96763-D095-4BE1-8A75-3ADA952DF65B",
            "gateway successor": True,
            "splitting": False,
            "is end": False
          },
          {
            "name": "activity three",
            "type": "task",
            "id": "sid-C4EA710A-B1E4-4561-A8AE-03D48DD6B5A6",
            "gateway successor": True,
            "splitting": False,
            "is end": False
          }
        ]
      }
    ],
    "predecessor": [
      {
        "name": "startnoneevent",
        "type": "startnoneevent",
        "id": "sid-02A35A45-F552-41F7-B407-30CE5CD85799",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "is start": True,
    "is end": False
  },
  {
    "name": "XOR",
    "type": "exclusive_databased_gateway",
    "id": "sid-7946CDE8-E0E9-4730-8D59-E48E15C331B8",
    "successor": [
      {
        "name": "activity two",
        "type": "task",
        "id": "sid-DEEAF1CC-6862-41BE-8FE4-C9630A72A6E7",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      },
      {
        "name": "activity four",
        "type": "task",
        "id": "sid-27B96763-D095-4BE1-8A75-3ADA952DF65B",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      },
      {
        "name": "activity three",
        "type": "task",
        "id": "sid-C4EA710A-B1E4-4561-A8AE-03D48DD6B5A6",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "predecessor": [
      {
        "name": "activity one",
        "type": "task",
        "id": "sid-8AB55396-4E84-4550-8FBE-EC45A5B43D4C",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "joining": False,
    "splitting": True
  },
  {
    "name": "activity two",
    "type": "task",
    "id": "sid-DEEAF1CC-6862-41BE-8FE4-C9630A72A6E7",
    "successor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-1B6F689B-482D-40A7-B788-9A8C80975803",
        "gateway successor": False,
        "splitting": True,
        "is end": False,
        "gateway successors": [
          {
            "name": "activity seven",
            "type": "task",
            "id": "sid-3904ECFE-CA9F-40E1-843B-B9025A4DA7B4",
            "gateway successor": True,
            "splitting": False,
            "is end": False
          },
          {
            "name": "activity six",
            "type": "task",
            "id": "sid-382F945F-5108-417A-B315-8E8938612AAC",
            "gateway successor": True,
            "splitting": False,
            "is end": False
          }
        ]
      }
    ],
    "predecessor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-7946CDE8-E0E9-4730-8D59-E48E15C331B8",
        "gateway successor": False,
        "splitting": True,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "is in gateway": True
  },
  {
    "name": "activity four",
    "type": "task",
    "id": "sid-27B96763-D095-4BE1-8A75-3ADA952DF65B",
    "successor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-29496081-966C-4F73-99BD-F3F15870C09B",
        "gateway successor": False,
        "splitting": False,
        "is end": False,
        "gateway successors": [
          {
            "name": "activity eight",
            "type": "task",
            "id": "sid-61CF40B6-AC8E-43D7-9CC8-9C2109503906",
            "gateway successor": True,
            "splitting": False,
            "is end": True
          }
        ]
      }
    ],
    "predecessor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-7946CDE8-E0E9-4730-8D59-E48E15C331B8",
        "gateway successor": False,
        "splitting": True,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "is in gateway": True
  },
  {
    "name": "activity three",
    "type": "task",
    "id": "sid-C4EA710A-B1E4-4561-A8AE-03D48DD6B5A6",
    "successor": [
      {
        "name": "activity five",
        "type": "task",
        "id": "sid-7CB96403-386D-4674-8ABD-400FE60F55AB",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "predecessor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-7946CDE8-E0E9-4730-8D59-E48E15C331B8",
        "gateway successor": False,
        "splitting": True,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "is in gateway": True
  },
  {
    "name": "XOR",
    "type": "exclusive_databased_gateway",
    "id": "sid-29496081-966C-4F73-99BD-F3F15870C09B",
    "successor": [
      {
        "name": "activity eight",
        "type": "task",
        "id": "sid-61CF40B6-AC8E-43D7-9CC8-9C2109503906",
        "gateway successor": False,
        "splitting": False,
        "is end": True
      }
    ],
    "predecessor": [
      {
        "name": "activity four",
        "type": "task",
        "id": "sid-27B96763-D095-4BE1-8A75-3ADA952DF65B",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      },
      {
        "name": "activity five",
        "type": "task",
        "id": "sid-7CB96403-386D-4674-8ABD-400FE60F55AB",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      },
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-316470DA-C61C-4526-B747-66589BCB34EB",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "joining": True,
    "splitting": False
  },
  {
    "name": "activity five",
    "type": "task",
    "id": "sid-7CB96403-386D-4674-8ABD-400FE60F55AB",
    "successor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-29496081-966C-4F73-99BD-F3F15870C09B",
        "gateway successor": False,
        "splitting": False,
        "is end": False,
        "gateway successors": [
          {
            "name": "activity eight",
            "type": "task",
            "id": "sid-61CF40B6-AC8E-43D7-9CC8-9C2109503906",
            "gateway successor": True,
            "splitting": False,
            "is end": True
          }
        ]
      }
    ],
    "predecessor": [
      {
        "name": "activity three",
        "type": "task",
        "id": "sid-C4EA710A-B1E4-4561-A8AE-03D48DD6B5A6",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "is in gateway": True
  },
  {
    "name": "XOR",
    "type": "exclusive_databased_gateway",
    "id": "sid-1B6F689B-482D-40A7-B788-9A8C80975803",
    "successor": [
      {
        "name": "activity seven",
        "type": "task",
        "id": "sid-3904ECFE-CA9F-40E1-843B-B9025A4DA7B4",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      },
      {
        "name": "activity six",
        "type": "task",
        "id": "sid-382F945F-5108-417A-B315-8E8938612AAC",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "predecessor": [
      {
        "name": "activity two",
        "type": "task",
        "id": "sid-DEEAF1CC-6862-41BE-8FE4-C9630A72A6E7",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "joining": False,
    "splitting": True,
    "is in gateway": True
  },
  {
    "name": "activity seven",
    "type": "task",
    "id": "sid-3904ECFE-CA9F-40E1-843B-B9025A4DA7B4",
    "successor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-316470DA-C61C-4526-B747-66589BCB34EB",
        "gateway successor": False,
        "splitting": False,
        "is end": False,
        "gateway successors": [
          {
            "name": "XOR",
            "type": "exclusive_databased_gateway",
            "id": "sid-29496081-966C-4F73-99BD-F3F15870C09B",
            "gateway successor": True,
            "splitting": False,
            "is end": False
          }
        ]
      }
    ],
    "predecessor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-1B6F689B-482D-40A7-B788-9A8C80975803",
        "gateway successor": False,
        "splitting": True,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "is in gateway": True
  },
  {
    "name": "activity six",
    "type": "task",
    "id": "sid-382F945F-5108-417A-B315-8E8938612AAC",
    "successor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-316470DA-C61C-4526-B747-66589BCB34EB",
        "gateway successor": False,
        "splitting": False,
        "is end": False,
        "gateway successors": [
          {
            "name": "XOR",
            "type": "exclusive_databased_gateway",
            "id": "sid-29496081-966C-4F73-99BD-F3F15870C09B",
            "gateway successor": True,
            "splitting": False,
            "is end": False
          }
        ]
      }
    ],
    "predecessor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-1B6F689B-482D-40A7-B788-9A8C80975803",
        "gateway successor": False,
        "splitting": True,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "is in gateway": True
  },
  {
    "name": "XOR",
    "type": "exclusive_databased_gateway",
    "id": "sid-316470DA-C61C-4526-B747-66589BCB34EB",
    "successor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-29496081-966C-4F73-99BD-F3F15870C09B",
        "gateway successor": False,
        "splitting": False,
        "is end": False,
        "gateway successors": [
          {
            "name": "activity eight",
            "type": "task",
            "id": "sid-61CF40B6-AC8E-43D7-9CC8-9C2109503906",
            "gateway successor": True,
            "splitting": False,
            "is end": True
          }
        ]
      }
    ],
    "predecessor": [
      {
        "name": "activity seven",
        "type": "task",
        "id": "sid-3904ECFE-CA9F-40E1-843B-B9025A4DA7B4",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      },
      {
        "name": "activity six",
        "type": "task",
        "id": "sid-382F945F-5108-417A-B315-8E8938612AAC",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "is start": False,
    "is end": False,
    "joining": True,
    "splitting": False
  },
  {
    "name": "activity eight",
    "type": "task",
    "id": "sid-61CF40B6-AC8E-43D7-9CC8-9C2109503906",
    "successor": [
      {
        "name": "endnoneevent",
        "type": "endnoneevent",
        "id": "sid-3D19CB5E-29C5-49C0-837B-2F07EB2F0178",
        "gateway successor": False,
        "splitting": False,
        "is end": True
      }
    ],
    "predecessor": [
      {
        "name": "XOR",
        "type": "exclusive_databased_gateway",
        "id": "sid-29496081-966C-4F73-99BD-F3F15870C09B",
        "gateway successor": False,
        "splitting": False,
        "is end": False
      }
    ],
    "is start": False,
    "is end": True
  }
]
def create_event_str(id, msg):
    return f"{id}(({msg}))"

def create_gateway_str(id, msg):
    # Can't use formatted string because of the { } required by mermaid.
    return id + "{" + msg + "}"

def create_activity_str(id, msg):
    return f"{id}({msg})"

def create_start_node(elem):
    rows = []
    for succcessor in elem["successor"]:
        row = ""
        row += create_event_str(elem["id"], elem["name"])
        row += SEQUENCE_FLOW
        row += create_activity_str(succcessor["id"], succcessor["name"])
        rows.append(row)
    return rows

def create_activity_node(elem):
    rows = []
    for successor in elem["successor"]:
        row = ""
        row += create_activity_str(elem["id"], elem["name"])
        row += SEQUENCE_FLOW

        if successor["is end"]:
            row += create_event_str(successor["id"], successor["name"])
        else:
            row += create_activity_str(successor["id"], successor["name"])
        rows.append(row)
    return rows
    
def create_gateway_node(elem):
    rows = []
    for successor in elem["successor"]:
        row = ""
        row += create_gateway_str(elem["id"], elem["name"])
        row += SEQUENCE_FLOW
        if successor["is end"]:
            row += create_event_str(successor["id"], successor["name"])
        else:
            row += create_activity_str(successor["id"], successor["name"])
        rows.append(row)
    return rows


def translate_bpmn_to_mermaid():
    rows = []
    for elem in EXAMPLE:
        if elem["is start"]:
            rows.extend(create_start_node(elem))
        
        elif elem["type"] in ALLOWED_ACTIVITIES and not elem["is end"]:
            rows.extend(create_activity_node(elem))

        elif elem["type"] in ALLOWED_GATEWAYS:
            rows.extend(create_gateway_node(elem))
    for item in rows:
        print(item)
        

if __name__ == "__main__":
    translate_bpmn_to_mermaid()