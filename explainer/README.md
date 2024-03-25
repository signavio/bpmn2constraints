# Symbolic Explanations of Process Conformance Violations
## Introduction


# Regex usage for the first iteration of the software

## 1. Sequence Constraint
Pattern: `'A.*B.*C'`

Explanation: This regex specifies that for a trace to be conformant, it must contain the nodes 'A', 'B', and 'C' in that order, though not necessarily consecutively. The .* allows for any number of intervening nodes between the specified nodes.

> Example: A trace ['A', 'X', 'B', 'Y', 'C'] would be conformant, while ['A', 'C', 'B'] would not.

## 2. Immediate Succession
Pattern: `'AB'`

Explanation: This regex specifies that node 'A' must be immediately followed by node 'B' with no intervening nodes.

> Example: A trace ['A', 'B', 'C'] would be conformant, while ['A', 'X', 'B'] would not.

## 3. Optional Node
Pattern: `'A(B)?C'`

Explanation: This regex specifies that the node 'B' is optional between 'A' and 'C'. The node 'C' must follow 'A', but 'B' can either be present or absent.

> Example: Both traces ['A', 'B', 'C'] and ['A', 'C'] would be conformant.

## 4. Excluding Specific Nodes
Pattern: `'A[^D]*B'`

Explanation: This regex specifies that 'A' must be followed by 'B' without the occurrence of 'D' in between them. The [^D] part matches any character except 'D'.

> Example: A trace ['A', 'C', 'B'] would be conformant, while ['A', 'D', 'B'] would not.

## 5. Repetition of Nodes
Pattern: `'A(B{2,3})C'`

Explanation: This regex specifies that 'A' must be followed by 'B' repeated 2 to 3 times and then followed by 'C'.

> Example: Traces ['A', 'B', 'B', 'C'] and ['A', 'B', 'B', 'B', 'C'] would be conformant, while ['A', 'B', 'C'] or ['A', 'B', 'B', 'B', 'B', 'C'] would not.

## 6. Alternative Paths
Pattern: `'A(B|D)C'`

Explanation: This regex specifies that after 'A', there must be either a 'B' or a 'D', followed by a 'C'.

> Example: Both traces ['A', 'B', 'C'] and ['A', 'D', 'C'] would be conformant.
