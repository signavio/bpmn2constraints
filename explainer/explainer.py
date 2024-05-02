from abc import ABC, abstractmethod
from itertools import combinations


class Explainer(ABC):
    def __init__(self):
        """
        Initializes an Explainer instance.
        """
        self.constraints = []  # List to store constraints (constraint patterns)
        self.adherent_trace = None
        self.adherent_traces = []
        self.minimal_solution = False

    def set_minimal_solution(self, minimal_solution):
        """
        Tells the explainer to generate minimal solutions
        Note: This will increase computations significantly

        Args:
            minimal_solution (bool): True to generate minimal solutions, False if it should be the first possible
        """
        self.minimal_solution = minimal_solution

    @abstractmethod
    def add_constraint(self, constr):
        """
        Adds a new constraint and updates the nodes list.

        :param constr: A regular expression or Signal constrain representing the constraint.
        """
        pass
    
    # Marking remove_constraint as abstract as an example
    @abstractmethod
    def remove_constraint(self, idx):
        """
        Removes a constraint by index and updates the nodes list if necessary.

        :param idx: Index of the constraint to be removed.
        """
        pass

    # Marking activation as abstract as an example
    @abstractmethod
    def activation(self, trace, constraints=None):
        """
        Checks if any of the nodes in the trace activates any constraint.

        :param trace: A Trace instance.
        :return: Boolean indicating if any constraint is activated.
        """
        pass

    @abstractmethod
    def conformant(self, trace, constraints=None):
        # Implementation remains the same
        pass

    @abstractmethod
    def minimal_expl(self, trace):
        # Implementation remains the same
        pass

    @abstractmethod
    def counterfactual_expl(self, trace):
        # Implementation remains the same
        pass

    @abstractmethod
    def determine_conformance_rate(self, event_log, constraints=None):
        # Implementation remains the same
        pass

    @abstractmethod
    def determine_fitness_rate(self, event_log, constraints=None):
        pass

    @abstractmethod
    def variant_ctrb_to_conformance_loss(self, event_log, trace, constraints=None):
        # Implementation remains the same
        pass

    @abstractmethod
    def variant_ctrb_to_fitness(self, event_log, trace, constraints=None):
        # Implementation remains the same
        pass

    @abstractmethod
    def constraint_ctrb_to_conformance(self, log, constraints, index):
        pass

    @abstractmethod
    def constraint_ctrb_to_fitness(self, log, constraints, index):
        # Implementation remains the same
        pass


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

    def get_variant_count(self, trace):
        """
        Returns the count of the specified trace in the log.

        :param trace: A Trace instance to check.
        """
        trace_tuple = tuple(trace.nodes)
        return self.log.get(trace_tuple, 0)

    def get_most_frequent_variant(self):
        """
        Returns the trace variant with the highest occurrence along with its count.

        :return: A tuple containing the most frequent trace as a Trace instance and its count.
        """
        if not self.log:
            return None, 0  # Return None and 0 if the log is empty

        # Find the trace with the maximum count
        max_trace_tuple = max(self.log, key=self.log.get)
        return Trace(list(max_trace_tuple))

    def get_traces(self):
        """
        Extracts and returns a list of all unique trace variants in the event log.

        :return: A list of Trace instances, each representing a unique trace.
        """
        # Generate a Trace instance for each unique trace tuple in the log
        return [Trace(list(trace_tuple)) for trace_tuple in self.log.keys()]

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
        Allows iteration over each trace occurrence in the log, sorted by count in descending order.
        """
        sorted_log = sorted(self.log.items(), key=lambda item: item[1], reverse=True)
        for trace_tuple, count in sorted_log:
            for _ in range(count):
                yield Trace(list(trace_tuple))


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
