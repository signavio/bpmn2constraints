import math
import re
from itertools import combinations, product, chain


class Trace:
    def __init__(self, nodes):
        """
        Initializes a Trace instance.

        :param nodes: A list of nodes where each node is represented as a string label.
        """
        self.nodes = nodes

    def __len__(self):
        """
        Returns the number of nodes in the trace.
        """
        return len(self.nodes)

    def __iter__(self):
        """
        Initializes the iteration over the nodes in the trace.
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Returns the next node in the trace during iteration.
        """
        if self.index < len(self.nodes):
            result = self.nodes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def __split__(self):
        """
        Splits the nodes of the trace into a list.

        :return: A list containing the nodes of the trace.
        """
        spl = []
        for node in self.nodes:
            spl.append(node)
        return spl


class EventLog:
    def __init__(self, trace=None):
        """
        Initializes an EventLog instance.

        :param traces: A list of Trace instances.
        """
        self.log = {}
        if trace:
            self.add_trace(trace)

    def add_trace(self, trace, count=1):
        """
        Adds a trace to the log or increments its count if it already exists.

        :param trace: A Trace instance to add.
        """
        trace_tuple = tuple(trace.nodes)
        if trace_tuple in self.log:
            self.log[trace_tuple] += count
        else:
            self.log[trace_tuple] = count

    def remove_trace(self, trace, count=1):
        """
        Removes a trace from the log or decrements its count if the count is greater than 1.

        :param trace: A Trace instance to remove.
        """
        trace_tuple = tuple(trace.nodes)
        if trace_tuple in self.log:
            if self.log[trace_tuple] > count:
                self.log[trace_tuple] -= count
            else:
                del self.log[trace_tuple]

    def __str__(self):
        """
        Returns a string representation of the event log.
        """
        return str(self.log)

    def __len__(self):
        """
        Returns the total number of trace occurrences in the log.
        """
        return sum(self.log.values())

    def __iter__(self):
        """
        Allows iteration over each trace occurrence in the log.
        """
        for trace_tuple, count in self.log.items():
            for _ in range(count):
                yield Trace(list(trace_tuple))


def determine_powerset(elements):
    """Determines the powerset of a list of elements
    Args:
        elements (set): Set of elements
    Returns:
        list: Powerset of elements
    """
    lset = list(elements)
    ps_elements = chain.from_iterable(
        combinations(lset, option) for option in range(len(lset) + 1)
    )
    return [set(ps_element) for ps_element in ps_elements]


def get_sublists(lst):
    """
    Generates all possible non-empty sublists of a list.

    :param lst: The input list.
    :return: A list of all non-empty sublists.
    """
    sublists = []
    for r in range(2, len(lst) + 1):  # Generate combinations of length 2 to n
        sublists.extend(combinations(lst, r))
    return sublists


def get_iterative_subtrace(trace):
    """
    Generates all possible non-empty contiguous sublists of a list, maintaining order.

    :param lst: The input list.
            n: the minmum length of sublists
    :return: A list of all non-empty contiguous sublists.
    """
    sublists = []
    for i in range(0, len(trace)):
        sublists.append(trace.nodes[0 : i + 1])

    return sublists


def levenshtein_distance(seq1, seq2):
    """
    Calculates the Levenshtein distance between two sequences.

    Args:
        seq1 (str): The first sequence.
        seq2 (str): The second sequence.

    Returns:
        int: The Levenshtein distance between the two sequences.
    """
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = [[0] * size_y for _ in range(size_x)]
    for x in range(size_x):
        matrix[x][0] = x
    for y in range(size_y):
        matrix[0][y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x][y] = matrix[x - 1][y - 1]
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1, matrix[x][y - 1] + 1, matrix[x - 1][y - 1] + 1
                )
    return matrix[size_x - 1][size_y - 1]
