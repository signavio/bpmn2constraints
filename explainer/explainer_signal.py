from abc import ABC, abstractmethod
from explainer import Explainer, Trace, EventLog, get_sublists, levenshtein_distance
import re
import math
import SignavioAuthenticator
import json
from itertools import combinations, chain
import requests
from conf import system_instance, workspace_id, user_name, pw

KEYWORDS = [
    "ABS",
    "ALL",
    "ANALYZE",
    "AND",
    "ANY",
    "AS",
    "ASC",
    "AVG",
    "BARRIER",
    "BEHAVIOUR",
    "BETWEEN",
    "BOOL_AND",
    "BOOL_OR",
    "BUCKET",
    "BY",
    "CASE",
    "CASE_ID",
    "CATEGORY",
    "CEIL",
    "CHAR_INDEX",
    "CHAR_LENGTH",
    "COALESCE",
    "CONCAT",
    "COUNT",
    "CREATE",
    "CURRENT",
    "DATE_ADD",
    "DATE_DIFF",
    "DATE_PART",
    "DATE_TRUNC",
    "DEFAULT",
    "DENSE_RANK",
    "DESC",
    "DESCRIBE",
    "DISTINCT",
    "DROP",
    "DURATION",
    "DURATION_BETWEEN",
    "DURATION_FROM_DAYS",
    "DURATION_FROM_MILLISECONDS",
    "DURATION_TO_DAYS",
    "DURATION_TO_MILLISECONDS",
    "ELSE",
    "END",
    "END_TIME",
    "EVENT_ID",
    "EVENT_NAME",
    "EVENTS",
    "EXACT",
    "EXPLAIN",
    "EXTERNAL",
    "FALSE",
    "FILL",
    "FILTER",
    "FIRST",
    "FLATTEN",
    "FLOOR",
    "FOLLOWING",
    "FORMAT",
    "FROM",
    "GRANT",
    "GROUP",
    "HAVING",
    "IF",
    "ILIKE",
    "IN",
    "INVOKER",
    "IS",
    "JOIN",
    "JSON",
    "LAG",
    "LAST",
    "LEAD",
    "LEFT",
    "LIKE",
    "LIMIT",
    "LOCATION",
    "LOG",
    "MATCHES",
    "MAX",
    "MEDIAN",
    "MIN",
    "NOT",
    "NOW",
    "NULL",
    "NULLS",
    "OCCURRENCE",
    "ODATA",
    "OFFSET",
    "ON",
    "ONLY",
    "OR",
    "ORDER",
    "OUTER",
    "OVER",
    "PARQUET",
    "PARTITION",
    "PERCENT",
    "PERCENTILE_CONT",
    "PERCENTILE_DESC",
    "PERMISSIONS",
    "POW",
    "PRECEDING",
    "PRIVATE",
    "PUBLIC",
    "RANGE",
    "RANK",
    "REGR_INTERCEPT",
    "REGR_SLOPE",
    "REPEATABLE",
    "REPLACE",
    "RIGHT",
    "ROUND",
    "ROW",
    "ROW_NUMBER",
    "ROWS",
    "SECURITY",
    "SELECT",
    "SIGN",
    "SQRT",
    "START_TIME",
    "STDDEV",
    "SUBSTRING",
    "SUBSTRING_AFTER",
    "SUBSTRING_BEFORE",
    "SUM",
    "TABLE",
    "TABULAR",
    "TEXT",
    "THEN",
    "TIMESERIES",
    "TIMESTAMP",
    "TO",
    "TO_NUMBER",
    "TO_STRING",
    "TO_TIMESTAMP",
    "TRUE",
    "TRUNC",
    "UNBOUNDED",
    "UNION",
    "USING",
    "VIEW",
    "WHEN",
    "WHERE",
    "WITH",
    "WITHIN",
    "",
]


class ExplainerSignal(Explainer):
    def __init__(self):
        super().__init__()
        self.authenticator = SignavioAuthenticator.SignavioAuthenticator(
            system_instance, workspace_id, user_name, pw
        )
        self.auth_data = self.authenticator.authenticate()
        self.cookies = {
            "JSESSIONID": self.auth_data["jsesssion_ID"],
            "LBROUTEID": self.auth_data["lb_route_ID"],
        }
        self.headers = {
            "Accept": "application/json",
            "x-signavio-id": self.auth_data["auth_token"],
        }
        self.event_log = EventLog()
        self.signal_endpoint = None
        self.cache = {}

    def set_endpoint(self, endpoint="/g/api/pi-graphql/signal"):
        self.signal_endpoint = system_instance + endpoint
        self.load_variants()

    def remove_constraint(self, idx):
        """
        Removes a constraint by index and updates the nodes list if necessary.

        :param idx: Index of the constraint to be removed.
        """
        if idx < len(self.constraints):
            del self.constraints[idx]

    def activation(self, trace, constraints=None):
        """
        Checks if any of the nodes in the trace activates any constraint.

        :param trace: A Trace instance.
        :return: Boolean indicating if any constraint is activated.
        """
        if constraints is None:
            constraints = self.constraints

        for node in trace:
            for constraint in constraints:
                if re.search(constraint, node):
                    return True
        return False

    def add_constraint(self, constr):
        """
        Adds a new constraint and updates the nodes list.

        :param constr: A regular expression or Signal constrain representing the constraint.
        """
        self.constraints.append(constr)

    def conformant(self, trace, constraints=None):
        if not constraints:
            constraints = self.constraints
        if len(constraints) > 1:
            constraints = " AND ".join(
                [f"event_name MATCHES {constraint}" for constraint in constraints]
            )
        else:
            constraints = "".join(f"event_name MATCHES {constraints[0]}")
        query = (
            f'SELECT ACTIVITY, COUNT(CASE_ID) FROM "defaultview-4" WHERE {constraints}'
        )
        conformant = False
        cache_key = hash(query)
        if cache_key in self.cache:
            for res in self.cache[cache_key]:
                if trace.nodes == res[0]:
                    conformant = True
                    break
            return conformant

        query_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={"query": query},
        )
        result = query_request.json()["data"]
        self.cache[cache_key] = result  # Store the result in cache

        for res in result:
            if trace.nodes == res[0]:
                conformant = True
                break
        return conformant

    def minimal_expl(self, trace):

        if self.conformant(trace):
            return "The trace is already conformant, no changes needed."
        explanations = None

        for constraint in self.constraints:
            for subtrace in get_sublists(trace):
                trace_str = "".join(subtrace)
                if not re.search(constraint, trace_str):
                    explanations = (
                        f"Constraint ({constraint}) is violated by subtrace: {subtrace}"
                    )
                    break

        if explanations:
            return "Non-conformance due to: " + explanations
        else:
            return "Trace is non-conformant, but the specific constraint violation could not be determined."

    def counterfactual_expl(self, trace):
        constraints = self.constraints
        if len(constraints) > 1:
            constraints = " AND ".join(
                [f"event_name MATCHES {constraint}" for constraint in constraints]
            )
        else:
            constraints = "".join(f"event_name MATCHES {constraints[0]}")
        query = (
            f'SELECT ACTIVITY, COUNT(CASE_ID) FROM "defaultview-4" WHERE {constraints}'
        )
        query_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={"query": query},
        )
        result = query_request.json()["data"]

        best_score = -float("inf")
        for res in result:
            current_score = self.evaluate_similarity(trace, "".join(res[0]))
            if current_score > best_score:
                best_score = current_score
                self.adherent_trace = Trace(res[0])

        return self.operate_on_trace(trace, 0, "")

    def counter_factual_helper(self, working_trace, explanation, depth=0):
        if self.conformant(working_trace):
            return f"{explanation}"
        if depth > 100:
            return f"{explanation}\n Maximum depth of {depth -1} reached"
        return self.operate_on_trace(working_trace, 0, explanation, depth)

    def operate_on_trace(self, trace, score, explanation_path, depth=0):
        explanation = None
        counter_factuals = self.modify_subtrace(trace)
        best_subtrace = None
        best_score = -float("inf")
        for subtrace in counter_factuals:
            current_score = self.evaluate_similarity(subtrace[0])
            if current_score > best_score:
                best_score = current_score
                best_subtrace = subtrace[0]
                explanation = subtrace[1]
        if best_subtrace == None:
            for subtrace in counter_factuals:
                self.operate_on_trace(subtrace[0], score, explanation_path, depth + 1)
        explanation_string = explanation_path + "\n" + str(explanation)
        return self.counter_factual_helper(best_subtrace, explanation_string, depth + 1)

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
                match = re.search(con, new_trace_str)
                if not match:
                    for add in possible_additions:
                        potential_subtraces.append(
                            [
                                Trace(s_trace + [add] + trace.nodes[i + 1 :]),
                                f"Addition (Added {add} at position {i+1}): "
                                + "->".join(s_trace + [add] + trace.nodes[i + 1 :]),
                            ]
                        )
                        potential_subtraces.append(
                            [
                                Trace(s_trace[:-1] + [add] + trace.nodes[i:]),
                                f"Addition (Added {add} at position {i}): "
                                + "->".join(s_trace[:-1] + [add] + trace.nodes[i:]),
                            ]
                        )

                    potential_subtraces.append(
                        [
                            Trace(s_trace[:-1] + trace.nodes[i + 1 :]),
                            f"Subtraction (Removed {s_trace[i]} from position {i}): "
                            + "->".join(s_trace[:-1] + trace.nodes[i + 1 :]),
                        ]
                    )
        return potential_subtraces

    def get_nodes_from_constraint(self, constraint=None):
        """
        Extracts unique nodes from a constraint pattern.

        :param constraint: The constraint pattern as a string.
        :return: A list of unique nodes found within the constraint.
        """
        if constraint is None:
            all_nodes = set()
            for con in self.constraints:
                all_nodes.update(self.filter_keywords(con))
            return list(set(all_nodes))
        else:
            return list(set(self.filter_keywords(constraint)))

    def filter_keywords(self, text):
        text = re.sub(r"\s+", "_", text.strip())
        words = re.findall(r"\b[A-Z_a-z]+\b", text)
        modified_words = [word.replace("_", " ") for word in words]
        filtered_words = [
            word for word in modified_words if word.strip() not in KEYWORDS
        ]

        return filtered_words

    def evaluate_similarity(self, trace, cmp_trace=None):
        """
        Calculates the similarity between the adherent trace and the given trace using the Levenshtein distance.

        :param trace: The trace to compare with the adherent trace.
        :return: A normalized score indicating the similarity between the adherent trace and the given trace.
        """
        if cmp_trace == None:
            cmp_trace = "".join(self.adherent_trace)
        trace_len = len("".join(trace))
        length = len(cmp_trace)
        lev_distance = levenshtein_distance(cmp_trace, "".join(trace))
        max_distance = max(length, trace_len)
        normalized_score = 1 - lev_distance / max_distance
        return normalized_score

    def determine_conformance_rate(self, event_log=None, constraints=None):
        if constraints == None:
            constraints = self.constraints
        if constraints == []:
            return 1
        non_conformant = 0
        non_conformant = self.check_violations(constraints)

        len_log = self.get_total_cases()

        return (len_log - non_conformant) / len_log

    def determine_fitness_rate(self, event_log=None, constraints=None):
        if not constraints:
            constraints = self.constraints
        len_log = self.get_total_cases()
        total_conformance = 0
        for con in constraints:
            total_conformance += self.check_conformance(con)
        return total_conformance / (len_log * len(constraints))

    def variant_ctrb_to_conformance_loss(self, event_log, trace, constraints=None):
        if not self.constraints and not constraints:
            return "The explainer have no constraints"
        if not constraints:
            constraints = self.constraints
        total_traces = len(event_log)
        contribution_of_trace = 0
        if not self.conformant(trace, constraints=constraints):
            contribution_of_trace = event_log.get_variant_count(trace)

        return contribution_of_trace / total_traces

    def variant_ctrb_to_fitness(self, event_log, trace, constraints=None):
        if not self.constraints and not constraints:
            return "The explainer have no constraints"
        if not constraints:
            constraints = self.constraints
        total_traces = len(event_log)
        contribution_of_trace = 0
        for con in constraints:
            if self.conformant(trace, constraints=[con]):
                contribution_of_trace += 1
        nr = event_log.get_variant_count(trace)
        contribution_of_trace = contribution_of_trace / len(constraints)
        contribution_of_trace = nr * contribution_of_trace
        return contribution_of_trace / total_traces

    def constraint_ctrb_to_conformance(self, log=None, constraints=None, index=-1):
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
        if not constraints:
            constraints = self.constraints
        if len(constraints) < index:
            raise Exception("Constraint not in constraint list.")
        if index == -1:
            return f"Add an index for the constraint:\n {constraints}"
        contributor = constraints[index]
        sub_ctrbs = []
        reduced_constraints = [c for c in constraints if not c == contributor]
        subsets = determine_powerset(reduced_constraints)
        for subset in subsets:
            lsubset = list(subset)
            constraints_without = [c for c in constraints if c in lsubset]
            constraints_with = [c for c in constraints if c in lsubset + [contributor]]
            weight = (
                math.factorial(len(lsubset))
                * math.factorial(len(constraints) - 1 - len(lsubset))
            ) / math.factorial(len(constraints))
            sub_ctrb = weight * (
                self.determine_conformance_rate(constraints=constraints_without)
                - self.determine_conformance_rate(constraints=constraints_with)
            )
            sub_ctrbs.append(sub_ctrb)
        return sum(sub_ctrbs)

    def constraint_ctrb_to_fitness(self, log=None, constraints=None, index=-1):
        # Implementation remains the same
        if len(constraints) < index:
            raise Exception("Constraint not in constraint list.")
        if not constraints:
            constraints = self.constraints
        if index == -1:
            return f"Add an index for the constraint:\n {constraints}"
        contributor = constraints[index]
        ctrb_count = self.check_conformance(contributor)
        len_log = self.get_total_cases()
        return ctrb_count / (len_log * len(constraints))

    def check_conformance(self, constraint):
        query = f'SELECT COUNT(CASE_ID) FROM "defaultview-4" WHERE event_name MATCHES{constraint}'
        cache_key = hash(query)
        if cache_key in self.cache:
            return self.cache[cache_key]
        query_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={"query": query},
        )
        result = query_request.json()["data"][0][0]
        self.cache[cache_key] = result
        return result

    def check_violations(self, constraints):
        combined_constraints = " OR ".join(
            [f"NOT event_name MATCHES {constraint}" for constraint in constraints]
        )
        query = (
            f'SELECT COUNT(CASE_ID) FROM "defaultview-4" WHERE {combined_constraints}'
        )
        cache_key = hash(query)
        if cache_key in self.cache:
            return self.cache[cache_key]
        query_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={"query": query},
        )
        result = query_request.json()["data"][0][0]
        self.cache[cache_key] = result
        return result

    def get_total_cases(self):
        query = 'SELECT COUNT(CASE_ID) FROM "defaultview-4"'
        cache_key = hash(query)
        if cache_key in self.cache:
            return self.cache[cache_key]
        count_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={"query": query},
        )
        case_count = count_request.json()["data"][0][0]
        self.cache[cache_key] = case_count
        return case_count

    def load_variants(self):
        query = 'SELECT Activity From "defaultview-4"'

        query_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={"query": query},
        )
        data = query_request.json()["data"]
        for activity in data:
            self.event_log.add_trace(Trace(activity[0]))


def get_event_log():
    return f'Select * FROM "defaultview-4"'


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
