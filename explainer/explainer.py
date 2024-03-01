import itertools
import re
from itertools import combinations, permutations, product

class Trace:
    def __init__(self, nodes):
        """
        Initializes a Trace instance.
        
        :param nodes: A list of nodes where each node is represented as a string label.
        """
        self.nodes = nodes
    def __len__(self):
        return len(self.nodes)
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.nodes):
            result = self.nodes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
    def __split__(self):
        spl = []
        for node in self.nodes:
            spl.append(node)
        return spl

class Explainer:
    def __init__(self):
        """
        Initializes an Explainer instance.
        """
        self.constraints = []  # List to store constraints (regex patterns)
        self.adherent_trace = None
    
    def add_constraint(self, regex):
        """
        Adds a new constraint and updates the nodes list.
        
        :param regex: A regular expression representing the constraint.
        """
        self.constraints.append(regex)
        if self.contradiction():
            self.constraints.remove(regex)
            print(f"Constraint {regex} contradicts the other constraints.")

    def remove_constraint(self, idx):
        """
        Removes a constraint by index and updates the nodes list if necessary.
        
        :param idx: Index of the constraint to be removed.
        """
        if 0 <= idx < len(self.constraints):
            removed_regex = self.constraints.pop(idx)
            removed_nodes = set(filter(str.isalpha, removed_regex))
            
            # Re-evaluate nodes to keep based on remaining constraints
            remaining_nodes = set(filter(str.isalpha, ''.join(self.constraints)))
            self.nodes = remaining_nodes

            # Optionally, remove nodes that are no longer in any constraint
            for node in removed_nodes:
                if node not in remaining_nodes:
                    self.nodes.discard(node)

    def activation(self, trace):
        """
        Checks if any of the nodes in the trace activates any constraint.
        
        :param trace: A Trace instance.
        :return: Boolean indicating if any constraint is activated.
        """
        trace_str = ''.join(trace.nodes)
        return any(re.search(constraint, trace_str) for constraint in self.constraints)

    def conformant(self, trace):
        """
        Checks if the trace is conformant according to all the constraints.
        
        :param trace: A Trace instance.
        :return: Boolean indicating if the trace is conformant with all constraints.
        """
        trace_str = ''.join(trace)
        return all(re.search(constraint, trace_str) for constraint in self.constraints)

    def contradiction(self):
        nodes = self.get_nodes_from_constraint()
        max_length = 10  # Set a reasonable max length to avoid infinite loops

        for length in range(1, max_length + 1):
            for combination in product(nodes, repeat=length):
                test_str = ''.join(combination)
                if all(re.search(con, test_str) for con in self.constraints):
                    self.adherent_trace = test_str
                    return False  # Found a match
        return True  # No combination satisfied all constraints


    def minimal_expl(self, trace):
        """
        Provides a minimal explanation for non-conformance, given the trace and constraints.
        
        :param trace: A Trace instance.
        :return: Explanation of why the trace is non-conformant.
        """
        if self.conformant(trace):
            return "The trace is already conformant, no changes needed."
        
        explanations = None
        
        for constraint in self.constraints:
            for subtrace in get_sublists(trace):
                trace_str = ''.join(subtrace)
                if not re.search(constraint, trace_str):
                    explanations = f"Constraint ({constraint}) is violated by subtrace: {subtrace}"
                    break

        if explanations:
            return "Non-conformance due to: " + explanations
        else:
            return "Trace is non-conformant, but the specific constraint violation could not be determined."

    def counterfactual_expl(self, trace):
        if self.conformant(trace):
            return "The trace is already conformant, no changes needed."
        score = self.evaluate_similarity(trace)
        # Perform operation based on the lowest scoring heuristic
        return self.operate_on_trace(trace, score, f'{trace.nodes}')

        
    def counter_factual_helper(self, working_trace, explanation, depth = 0):
        if self.conformant(working_trace):
            return f'{explanation}\n{working_trace.nodes}'
        if depth > 100:
            return f'{explanation}\n Maximum depth of {depth -1} reached'
        score = self.evaluate_similarity(working_trace)
        return self.operate_on_trace(working_trace, score, explanation, depth)


    def operate_on_trace(self, trace, score, explanation_path, depth = 0):
        explanation = None
        counter_factuals = self.modify_subtrace(trace)
        best_subtrace = None
        best_score = -float('inf')
        for subtrace in counter_factuals:
            current_score = self.evaluate_similarity(subtrace[0])
            if current_score > best_score and current_score > score:
                best_score = current_score
                best_subtrace = subtrace[0]
                explanation = subtrace[1]
        if best_subtrace == None:
            for subtrace in counter_factuals:
                print(subtrace[0].nodes)
                self.operate_on_trace(subtrace[0], score, explanation_path, depth + 1)
        explanation_string = explanation_path + '\n' + str(explanation)
        return self.counter_factual_helper(best_subtrace, explanation_string, depth + 1)

    def get_nodes_from_constraint(self, constraint = None):
        """
        Extracts unique nodes from a constraint pattern.
        
        :param constraint: The constraint pattern as a string.
        :return: A list of unique nodes found within the constraint.
        """
        if constraint is None:
            all_nodes = set()
            for constr in self.constraints:
                all_nodes.update(re.findall(r'[A-Za-z]', constr))
            return list(set(all_nodes))
        else:
            return list(set(re.findall(r'[A-Za-z]', constraint)))
        
    def modify_subtrace(self, trace):
        """
        Modifies the given trace to meet constraints by adding nodes where the pattern fails.

        Parameters:
        - trace: A list of node identifiers 

        Returns:
        - A list of potential subtraces each modified to meet constraints.
        """
        potential_subtraces = []
        possible_additions = self.get_nodes_from_constraint()  
        for i, s_trace in enumerate(get_iterative_subtrace(trace)):
            for con in self.constraints:
                new_trace_str = "".join(s_trace)
                match = re.match(new_trace_str, con)
                if not match:
                    for add in possible_additions:
                
                        potential_subtraces.append([Trace(s_trace + [add] + trace.nodes[i+1:]),
                                                    f"Addition (Added {add} at position {i+1}): " + "->"
                                                    .join(s_trace + [add] + trace.nodes[i+1:])])
                        potential_subtraces.append([Trace(s_trace[:-1] + [add] + trace.nodes[i:]),
                                                    f"Addition (Added {add} at position {i}): " + "->"
                                                    .join(s_trace[:-1] + [add] + trace.nodes[i:])])
                    
                    potential_subtraces.append([Trace(s_trace[:-1] + trace.nodes[i+1:]),
                                                 f"Subtraction (Removed {s_trace[i]} from position {i}): " + "->".
                                                 join(s_trace[:-1] + trace.nodes[i+1:])])

        return potential_subtraces

    def evaluate_similarity(self, trace):
        length = len(self.adherent_trace)
        trace_len = len("".join(trace))
        lev_distance = levenshtein_distance(self.adherent_trace, "".join(trace))
        max_distance = max(length, trace_len)
        normalized_score = 1 - lev_distance / max_distance
        return normalized_score

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
        sublists.append(trace.nodes[0:i+1])
       
    return sublists
def levenshtein_distance(seq1, seq2):
    """
    Calculates the Levenshtein distance between two sequences.
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
            if seq1[x-1] == seq2[y-1]:
                matrix[x][y] = matrix[x-1][y-1]
            else:
                matrix[x][y] = min(
                    matrix[x-1][y] + 1, 
                    matrix[x][y-1] + 1,  
                    matrix[x-1][y-1] + 1  
                )
    return matrix[size_x-1][size_y-1]

