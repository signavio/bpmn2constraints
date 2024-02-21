import itertools
import re
from itertools import combinations

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

class Explainer:
    def __init__(self):
        """
        Initializes an Explainer instance.
        """
        self.constraints = []  # List to store constraints (regex patterns)
        self.nodes = set()     # Set to store unique nodes involved in constraints

    def add_constraint(self, regex):
        """
        Adds a new constraint and updates the nodes list.
        
        :param regex: A regular expression representing the constraint.
        """
        self.constraints.append(regex)
        # Extract unique characters (nodes) from the regex and update the nodes set
        unique_nodes = set(filter(str.isalpha, regex))
        self.nodes.update(unique_nodes)

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
        """
        Provides a counterfactual explanation for a non-conformant trace, suggesting changes to adhere to the constraints.
        
        :param trace: A Trace instance.
        :return: Suggestion to make the trace conformant.
        """
        if self.conformant(trace):
            return "The trace is already conformant, no changes needed."

        violated_constraints = self.identify_violated_constraints(trace)
        if not violated_constraints:
            return "Unable to identify specific violated constraints."

        counterfactuals = []
        for constraint in violated_constraints:
            counterfactuals.extend(self.generate_potential_counterfactuals(trace, constraint))

        conformant_counterfactuals = [cf for cf in counterfactuals if self.conformant(cf[0])]
        if conformant_counterfactuals:
            selected_counterfactual = min(conformant_counterfactuals, key=lambda x: len(x[0].nodes))  # Example selection criteria
            return f"Suggested change to make the trace ({trace.nodes}) conformant: {selected_counterfactual[1]}"
        else:
            return "Unable to generate potential counterfactuals."


    def identify_violated_constraints(self, trace):
        """
        Identifies which constraints are violated by the given trace.
        
        :param trace: A Trace instance to check against the constraints.
        :return: A list of constraints that the trace violates.
        """
        violated = []
        trace_str = ''.join(trace.nodes)
        for constraint in self.constraints:
            if not re.search(constraint, trace_str):
                violated.append(constraint)
        return violated
    
    def introduces_new_violations(self, counterfactual, violated_constraints):
        """
        Checks if a counterfactual trace introduces new violations.
        
        :param counterfactual: A modified Trace instance to check.
        :param violated_constraints: Constraints that were initially violated.
        :return: True if new violations are introduced, False otherwise.
        """
        for constraint in self.constraints:
            if constraint not in violated_constraints and not re.search(constraint, ''.join(counterfactual.nodes)):
                return True
        return False
    
    def generate_potential_counterfactuals(self, trace, violated_constraint):
        """
        Generates potential counterfactual modifications for a trace based on a violated constraint.
        
        :param trace: The original Trace instance.
        :param violated_constraint: The specific constraint that is violated.
        :return: A list of counterfactuals suggesting how to modify the trace.
        """
        trace_str = "".join(trace)
        if re.search(violated_constraint, trace_str):
           return f"Trace: {trace_str} is conformant for the constraint: {violated_constraint}"     
        # Extrace all the nodes in the constraint
        used_nodes = self.get_nodes_from_constraint(violated_constraint)
        # Extract which part of the trace that violates the constraint
        violating_subtraces = self.get_violating_subtrace(trace, violated_constraint)
        # Generate counterfactuals
        addition_counterfactuals = self.addition_modification(trace, used_nodes, violating_subtraces)
        subtraction_counterfactuals = self.subtraction_modification(trace)
        reordering_counterfactuals = self.reordering_modification(trace)
        substitution_counterfactuals = self.substitution_modification(trace, used_nodes)

        return addition_counterfactuals + subtraction_counterfactuals + reordering_counterfactuals + substitution_counterfactuals

    
    def get_nodes_from_constraint(self, constraint):
        """
        Extracts unique nodes from a constraint pattern.
        
        :param constraint: The constraint pattern as a string.
        :return: A list of unique nodes found within the constraint.
        """
        return list(set(re.findall(r'[A-Za-z]', constraint)))

    def select_best_counterfactual(self, counter_factuals):
        """
        Selects the best counterfactual modification from a list.
        
        :param counter_factuals: A list of counterfactual modifications.
        :return: The selected best counterfactual modification.
        TODO: Implement this based on a heuristic 
        """
        return counter_factuals[0]
    
    def get_violating_subtrace(self, trace, constraint):
        """
        Finds subtraces of a given trace that violate a specific constraint.
        
        :param trace: The Trace instance to analyze.
        :param constraint: The constraint to check against the trace.
        :return: A list of subtraces that violate the given constraint.
        """
        violating_subtrace = []
        for subtrace in get_sublists(trace):
            trace_str = ''.join(subtrace)
            if not re.search(constraint, trace_str):
                violating_subtrace.append(subtrace)
        return violating_subtrace
    
    def addition_modification(self, trace, used_nodes, violating_subtraces):
        """
        Suggests additions to the trace to meet constraints.
        """
        counterfactuals = []
        for subtrace in violating_subtraces:
            for i in range(len(subtrace) - 1):
                for node in used_nodes:
                    new_trace = list(trace.nodes)  # Ensure we're working with a full trace copy
                    new_trace.insert(i + 1, node)  # Insert a node between each node in the subtrace
                    new_trace_str = "Addition: " + "->".join(new_trace)  
                    counterfactuals.append((Trace(new_trace), new_trace_str))
        return counterfactuals


    def subtraction_modification(self, trace):
        """
        Suggests node removals from the trace for conformance.
        """
        counterfactuals = []
        
        for r in range(1, len(trace.nodes)):
            for indices_to_remove in combinations(range(len(trace.nodes)), r):
                modified_trace_nodes = [node for index, node in enumerate(trace.nodes) if index not in indices_to_remove]
                
                removed_nodes_str = "->".join([trace.nodes[index] for index in indices_to_remove])
                new_trace_str = f"Subtraction (Removed {removed_nodes_str}): " + "->".join(modified_trace_nodes)
                
                counterfactuals.append((Trace(modified_trace_nodes), new_trace_str))
        return counterfactuals



    def reordering_modification(self, trace):
        """
        Suggests reordering of nodes in the trace for conformance.
        """
        counterfactuals = []
        permutations = itertools.permutations(trace.nodes)
        for perm in permutations:
            if perm not in [cf[0].nodes for cf in counterfactuals]:
                new_trace_str = "Reordering: " + "->".join(perm)  # Descriptive string
                counterfactuals.append((Trace(list(perm)), new_trace_str))
        return counterfactuals


    def substitution_modification(self, trace, used_nodes):
        """
        Suggests substitutions within the trace to meet constraints.
        """
        counterfactuals = []
        for i, node in enumerate(trace.nodes):
            if node in used_nodes:
                for replacement_node in (self.nodes - set([node])):  # Ensure it's a set operation
                    new_trace_nodes = trace.nodes[:]  # Copy the list of nodes
                    new_trace_nodes[i] = replacement_node
                    new_trace_str = f"Substitution: Replace {node} with {replacement_node} at position {i+1}"
                    new_trace = Trace(new_trace_nodes)
                    if new_trace not in [cf[0] for cf in counterfactuals]:
                        counterfactuals.append((new_trace, new_trace_str))
        return counterfactuals

        
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
