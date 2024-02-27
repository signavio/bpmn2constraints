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
        self.nodes = set()     # Set to store unique nodes involved in constraints
        self.constraint_fulfillment_alpha = 1
        self.repetition_alpha = 1
        self.sub_trace_adherence_alpha = 1

    def set_heuristic_alpha(self, constraint_fulfillment_alpha = 1, repetition_alpha = 1, sub_trace_adherence_alpha = 1):
        self.constraint_fulfillment_alpha = constraint_fulfillment_alpha
        self.repetition_alpha = repetition_alpha
        self.sub_trace_adherence_alpha
        return
    
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
            3 Heuristics: 
                Constraint fulfillment - Prioritize modifications that maximize the number of constraints the trace fulfills.
                Minimal Deviation - Seek the least number of changes necessary to make the trace adhere to constraints.
                Sub-trace Adherence - Evaluate the proportion of the trace that adheres to constraints after each modification.
        """
        if self.conformant(trace):
            return "The trace is already conformant, no changes needed."
        # Evaluate heuristic for original trace
        constraint_fulfillment_score = 1
        if len(self.constraints) > 1:
            constraint_fulfillment_score = self.evaluate(trace, "constraint_fulfillment")
        sub_trace_adherence_score = self.evaluate(trace, "sub_trace_adherence")
        repetition_score = self.evaluate(trace, "repetition")
        # Identify the lowest score and the corresponding heuristic
        scores = {
            'constraint_fulfillment': constraint_fulfillment_score,
            'sub_trace_adherence': sub_trace_adherence_score,
            'repetition' : repetition_score
        }
        
        lowest_heuristic, lowest_score = min(scores.items(), key=lambda x: x[1])

        # Perform operation based on the lowest scoring heuristic
        if lowest_heuristic:
            return self.operate_on_trace(trace, lowest_heuristic, lowest_score, "")
        else:
            return "Error identifying the lowest scoring heuristic."
        
    def counter_factual_helper(self, working_trace, explanation, depth = 0):
        if self.conformant(working_trace):
            print(depth)
            return explanation
        if depth > 100:
            return f'{explanation}\n Maximum depth of {depth -1} reached'
        # Evaluate heuristic for original trace
        constraint_fulfillment_score = 1
        if len(self.constraints) > 1:
            constraint_fulfillment_score = self.evaluate(working_trace, "constraint_fulfillment")
        sub_trace_adherence_score = self.evaluate(working_trace, "sub_trace_adherence")
        repetition_score = self.evaluate(working_trace, "repetition")
        if constraint_fulfillment_score == 0 and sub_trace_adherence_score == 0:
            self.constraint_fulfillment_alpha = 1
            self.sub_trace_adherence_alpha = 1
            return self.counter_factual_helper(working_trace, explanation, depth + 1)
        # Identify the lowest score and the corresponding heuristic
        scores = {
            'sub_trace_adherence': sub_trace_adherence_score,
            'repetition' : repetition_score,
            'constraint_fulfillment': constraint_fulfillment_score,
        }
        
        lowest_heuristic, lowest_score = min(scores.items(), key=lambda x: x[1])
        # Perform operation based on the lowest scoring heuristic
        if lowest_heuristic:
            return self.operate_on_trace(working_trace, lowest_heuristic, lowest_score, explanation, depth)
        else:
            return "Error identifying the lowest scoring heuristic."

    def operate_on_trace(self, trace, heuristic, score, explanation_path, depth = 0):
        explanation = None
        counter_factuals = self.modify_subtrace(trace)
        best_subtrace = None
        best_score = -float('inf')
        for subtrace in counter_factuals:
            current_score = self.evaluate(subtrace[0], heuristic)
            if current_score > best_score and current_score > score:
                best_score = current_score
                best_subtrace = subtrace[0]
                explanation = subtrace[1]
        if best_subtrace == None:
            for subtrace in counter_factuals:
                print(subtrace[0].nodes)
                print(heuristic)
                self.operate_on_trace(subtrace[0], heuristic, score, explanation_path, depth + 1)
        explanation_string = explanation_path + '\n' + str(explanation) + f", based on heurstic {heuristic}"
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
                all_nodes.update(re.findall(r'[A-Za-z]+', constr))
            return list(set(all_nodes))
        else:
            return list(set(re.findall(r'[A-Za-z]', constraint)))
    
    def modify_subtrace(self, trace):
        
        add_mod = self.addition_modification(trace)
        sub_mod = self.subtraction_modification(trace)

        return sub_mod + add_mod
    
    from itertools import combinations, chain

    def addition_modification(self, trace):
        """
        Suggests additions to the trace to meet constraints, but only one node at a time.
        """
        counterfactuals = []
        possible_additions = self.get_nodes_from_constraint()

        # Only add one node at a time
        for added_node in possible_additions:
            for insertion_point in range(len(trace.nodes) + 1):
                # Create a new trace with the added node
                new_trace_nodes = trace.nodes[:insertion_point] + [added_node] + trace.nodes[insertion_point:]
                new_trace_str = f"Addition (Added {added_node} at position {insertion_point}): " + "->".join(new_trace_nodes)
                
                counterfactuals.append((Trace(new_trace_nodes), new_trace_str))
        
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

    def evaluate(self, trace, heurstic):
        if heurstic == "constraint_fulfillment":
            return self.evaluate_constraint_fulfillment(trace)
        elif heurstic == "sub_trace_adherence":
            return self.evaluate_sub_trace_adherence(trace)
        elif heurstic == "repetition":
            return self.evaluate_repetition(trace)
        else:
            return "No valid evaluation method"
    
    def evaluate_constraint_fulfillment(self, optional_trace):
        if self.constraint_fulfillment_alpha == 0:
            return 0
        fulfilled_constraints = sum(1 for constraint in self.constraints if re.search(constraint,"".join(optional_trace)))
        total_constraints = len(self.constraints)
        return (fulfilled_constraints / total_constraints) * self.constraint_fulfillment_alpha if total_constraints else 0

    def evaluate_repetition(self, trace):
        if self.repetition_alpha == 0:
            return 1

        node_counts = {}
        for node in trace.nodes:
            if node in node_counts:
                node_counts[node] += 1
            else:
                node_counts[node] = 1

        # Calculate the deviation of each node's occurrence from 1
        deviations = [count - 1 for count in node_counts.values()]

        # Normalize deviation: Here, we take the sum of deviations and divide by the total number of nodes
        # This gives an average deviation per node, which we normalize by dividing by the length of the trace
        # This assumes the worst case where every node in the trace is different and repeated once
        if trace.nodes:
            normalized_deviation = sum(deviations) / len(trace.nodes)
        else:
            normalized_deviation = 0

        # Ensure the score is between 0 and 1
        normalized_deviation = 1 - min(max(normalized_deviation, 0), 1)

        return normalized_deviation * self.repetition_alpha


    def evaluate_sub_trace_adherence(self, optional_trace):
        
        sub_lists = list(set([node for node in optional_trace]))
        adherence_scores = [[0 for _ in self.constraints] for _ in sub_lists]
        for i, sub_trace in enumerate(sub_lists):
            trace_string = "".join(sub_trace)
            for j, con in enumerate(self.constraints):
                match = re.search(trace_string, con)
                if match:
                    adherence_scores[i][j] = 1
        num_nodes = len(self.get_nodes_from_constraint())
        total_scores = sum(sum(row) for row in adherence_scores)
        
        average_score = total_scores / num_nodes if num_nodes else 0
        return average_score * self.sub_trace_adherence_alpha

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
def get_sublists1(lst, n):
    """
    Generates all possible non-empty contiguous sublists of a list, maintaining order.
    
    :param lst: The input list.
    :return: A list of all non-empty contiguous sublists.
    """
    sublists = []
    for i in range(len(lst)):
        
        for j in range(i + 2, min(i + n + 1, len(lst) + 1)):
            sub = lst[i:j]
            sublists.append(sub)
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
                    matrix[x-1][y] + 1,  # Deletion
                    matrix[x][y-1] + 1,  # Insertion
                    matrix[x-1][y-1] + 1  # Substitution
                )
    return matrix[size_x-1][size_y-1]

exp = Explainer()
exp.add_constraint('A.*B.*C.*D')
#exp.add_constraint('A.*B.*C')
#exp.add_constraint('A.*B')
#optional_trace = Trace(['A', 'B', 'C', 'E', 'E'])
optional_trace = Trace(['A', 'B', 'B'])
print(exp.evaluate_repetition(optional_trace))


#print(exp.counterfactual_expl(optional_trace))

