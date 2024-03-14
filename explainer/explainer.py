import itertools
import math
import re
from itertools import combinations, permutations, product,combinations_with_replacement, chain

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
class EventLog:
    def __init__(self, traces=None):
        """
        Initializes an EventLog instance.

        :param traces: A list of Trace instances.
        """
        self.log = {}
        if traces:
            for trace in traces:
                self.add_trace(trace)

    def add_trace(self, trace, count = 1):
        """
        Adds a trace to the log or increments its count if it already exists.

        :param trace: A Trace instance to add.
        """
        trace_tuple = tuple(trace.nodes)
        if trace_tuple in self.log:
            self.log[trace_tuple] += count
        else:
            self.log[trace_tuple] = count

    def remove_trace(self, trace, count = 1):
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
        con_activation = [0] * len(self.constraints)
        activated = False
        for idx, con in enumerate(self.constraints):
            if activated:
                activated = False
                continue
            target = self.identify_existance_constraints(con)
            if target:
                con_activation[idx] = 1
                continue
            for event in con:
                    if event in con:
                        con_activation[idx] = 1
                        activated = True
                        break
        return con_activation

    def identify_existance_constraints(self, pattern):

        # Check for AtLeastOne constraint
        for match in re.finditer(r'(?<!^)(.)\.\*', pattern):
            return ('ALO, 'f'{match.group(1)}')

        # Check for End constraint
        end_match = re.search(r'(.)\$(?=\Z|\))', pattern)
        if end_match:
            return ('E', f'{end_match.group(1)}')
        # Check for Init constraint
        init_match = re.match(r'(?:\A\^|\((?:\?[^)]+\))?\^)(.)', pattern)
        if init_match:
            return ('I', f'{init_match.group(1)}')
        return None
        
         
    def conformant(self, trace, constraints = None):
        """
        Checks if the trace is conformant according to all the constraints.
        
        :param trace: A Trace instance.
        :return: Boolean indicating if the trace is conformant with all constraints.
        """
        activation = self.activation(trace)
        if any(value == 0 for value in activation):
            new_explainer = Explainer()
            for idx, value in enumerate(activation):
                if value == 1:
                    new_explainer.add_constraint(self.constraints[idx])
            return new_explainer.conformant(trace)
        trace_str = ''.join(trace)
        if constraints:
            return all(re.search(constraint, trace_str) for constraint in constraints)
        return all(re.search(constraint, trace_str) for constraint in self.constraints)
    
    def contradiction(self):
        nodes = self.get_nodes_from_constraint()
        max_length = 10  # Set a reasonable max length to avoid infinite loops
        nodes = nodes + nodes
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
        
        # Because constraints that are not activated should not be considered we create a new explainer with the relevant constraints in this case
        activation = self.activation(trace)
        if any(value == 0 for value in activation):
            new_explainer = Explainer()
            for idx, value in enumerate(activation):
                if value == 1:
                    new_explainer.add_constraint(self.constraints[idx])
            return new_explainer.minimal_expl(trace)
        
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
        
        activation = self.activation(trace)
        if any(value == 0 for value in activation):
            new_explainer = Explainer()
            for idx, value in enumerate(activation):
                if value == 1:
                    new_explainer.add_constraint(self.constraints[idx])
            return new_explainer.counterfactual_expl(trace)
        
        if self.conformant(trace):
            return "The trace is already conformant, no changes needed."
        score = self.evaluate_similarity(trace)
        # Perform operation based on the lowest scoring heuristic
        return self.operate_on_trace(trace, score, '')

        
    def counter_factual_helper(self, working_trace, explanation, depth = 0):
        if self.conformant(working_trace):
            return f'{explanation}'
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

    def determine_shapley_value(self, log, constraints, index):
        """Determines the Shapley value-based contribution of a constraint to a the
        overall conformance rate.
        Args:
            log (dictionary): The event log, where keys are strings and values are
            ints
            constraints (list): A list of constraints (regexp strings)
            index (int): The
        Returns:
            float: The contribution of the constraint to the overall conformance
            rate
        """
        if len(constraints) < index:
            raise Exception (
                'Constraint not in constraint list.')
        contributor = constraints[index]
        sub_ctrbs = []
        reduced_constraints = [c for c in constraints if not c == contributor]
        subsets = determine_powerset(reduced_constraints)
        for subset in subsets:
            lsubset = list(subset)
            constraints_without = [c for c in constraints if c in lsubset]
            constraints_with = [c for c in constraints if c in lsubset + [contributor]]
            weight = (math.factorial(len(lsubset)) * math.factorial(len(constraints)-1-len(lsubset)))/math.factorial(len(constraints))
            sub_ctrb = weight * (self.determine_conformance_rate(log, constraints_without) - self.determine_conformance_rate(log, constraints_with))
            sub_ctrbs.append(sub_ctrb)
        return sum(sub_ctrbs)

    def evaluate_similarity(self, trace):
        length = len(self.adherent_trace)
        trace_len = len("".join(trace))
        lev_distance = levenshtein_distance(self.adherent_trace, "".join(trace))
        max_distance = max(length, trace_len)
        normalized_score = 1 - lev_distance / max_distance
        return normalized_score
    
    def determine_conformance_rate(self, event_log, constraints = None):
        if not self.constraints and not constraints:
            return "The explainer have no constraints"
        conformant = 0
        for trace in event_log:
            if self.conformant(trace, constraints):
                conformant += 1
        return round(conformant / len(event_log), 2)
    
    
def determine_powerset(elements):
    """Determines the powerset of a list of elements
    Args:
        elements (set): Set of elements
    Returns:
        list: Powerset of elements
    """
    lset = list(elements)
    ps_elements = chain.from_iterable(combinations(lset, option) for option in range(len(lset) + 1))
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

#event_log = EventLog()
exp = Explainer()
exp.add_constraint('^A')
exp.add_constraint('C$')
print(exp.conformant(Trace(['AXC'])))
#trace1 = Trace(['A','B','C'])
#trace2 = Trace(['B', 'C'])
#trace3 = Trace(['A', 'B'])
#trace4 = Trace(['B'])
#
## Adding traces
#event_log.add_trace(trace1, 5)
#event_log.add_trace(trace2, 10)
#event_log.add_trace(trace3, 5)
#event_log.add_trace(trace4, 5)
#for con in exp.constraints:
#    print(f"existance constraints: {exp.identify_existance_constraints(con)}")
##print(event_log)
##print(exp.determine_conformance_rate(event_log))
#print("False: " + str(exp.conformant(trace2))+ " activated: " + str(exp.activation(trace2)))
#print("False: " + str(exp.conformant(trace3))+ " activated: " + str(exp.activation(trace3)))
#print("False: " + str(exp.conformant(trace4))+ " activated: " + str(exp.activation(trace4)))
#print("True:  " +  str(exp.conformant(trace1))+ " activated: " + str(exp.activation(trace1)))
#
#
#print('Contribution ^a:', exp.determine_shapley_value(event_log, exp.constraints, 0))
#print('Contribution c$:', exp.determine_shapley_value(event_log, exp.constraints, 1))