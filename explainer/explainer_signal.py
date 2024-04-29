from abc import ABC, abstractmethod
from explainer import Explainer, Trace, EventLog
import re
import math
import SignavioAuthenticator
import json
from itertools import combinations, chain
import requests
from conf import system_instance, workspace_id, user_name, pw
class ExplainerSignal(Explainer):
    def __init__(self):
        super().__init__()
        self.authenticator = SignavioAuthenticator.SignavioAuthenticator(system_instance, workspace_id, user_name, pw)
        self.auth_data = self.authenticator.authenticate()
        self.cookies = {'JSESSIONID': self.auth_data['jsesssion_ID'], 'LBROUTEID': self.auth_data['lb_route_ID']}
        self.headers = {'Accept': 'application/json', 'x-signavio-id':  self.auth_data['auth_token']}
        self.signal_endpoint = system_instance + '/g/api/pi-graphql/signal'
        self.event_log = EventLog()
        self.load_variants()
        self.minimal_expl(self.event_log.get_most_frequent_variant())

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

    def conformant(self, trace, constraints=None):
        if not constraints:
            constraints = self.constraints
        
        pass
    def contradiction(self, check_multiple=False, max_length=10):
        pass
    
    def minimal_expl(self, trace):
        print(trace)
    
    def counterfactual_expl(self, trace):
        pass
    
    def determine_shapley_value(self, log, constraints, index):
        pass
    
    def evaluate_similarity(self, trace):
        pass
    
    def determine_conformance_rate(self, event_log = None, constraints=None):
        if constraints == None:
            constraints = self.constraints
        if constraints == []:
            return 1
        non_conformant = 0
        non_conformant = self.check_violations(constraints)

        len_log = self.get_total_cases()
        
        return (len_log - non_conformant) / len_log
        
    
    def determine_fitness_rate(self, event_log = None, constraints = None):
        if not constraints:
            constraints = self.constraints
        len_log = self.get_total_cases()
        total_conformance = 0
        for con in constraints:
            total_conformance += self.check_conformance(con)
        
        return total_conformance / (len_log * len(constraints))
        
        
    def variant_ctrb_to_conformance_loss(self, event_log, trace, constraints=None):
        # Implementation remains the same
        pass
    
    def variant_ctrb_to_fitness(self, event_log, trace, constraints=None):
        # Implementation remains the same
        pass
    
    def constraint_ctrb_to_conformance(self, log = None, constraints = None, index = -1):
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
    
    def constraint_ctrb_to_fitness(self, log = None, constraints = None, index = -1):
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
        query_request = requests.post(
        self.signal_endpoint,
        cookies=self.cookies,
        headers=self.headers,
        json={'query': f'SELECT COUNT(CASE_ID) FROM "defaultview-4" WHERE event_name MATCHES{constraint}'})
        return query_request.json()['data'][0][0]
    
    def check_conformances(self, constraints):
        combined_constraints = " AND ".join([f"event_name MATCHES {constraint}" for constraint in constraints])
        query = f'SELECT COUNT(CASE_ID) FROM "defaultview-4" WHERE {combined_constraints}'

        query_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={'query': query}
        )
        return query_request.json()['data'][0][0]
    
    def check_violations(self, constraints):
        combined_constraints = " OR ".join([f"NOT event_name MATCHES {constraint}" for constraint in constraints])
        query = f'SELECT COUNT(CASE_ID) FROM "defaultview-4" WHERE {combined_constraints}'

        query_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={'query': query}
        )
        return query_request.json()['data'][0][0]

    def get_total_cases(self):
        count_request = requests.post(
            self.signal_endpoint,
            cookies=self.cookies,
            headers=self.headers,
            json={'query': 'SELECT COUNT(CASE_ID) FROM "defaultview-4"'})
        case_count = count_request.json()['data'][0][0]
        return case_count
    
    def load_variants(self):
        query_request = requests.post(
            exp.signal_endpoint,
            cookies=exp.cookies,
            headers=exp.headers,
            json={'query': 'SELECT Activity From "defaultview-4"'}
        )
        data = query_request.json()['data']
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


exp = ExplainerSignal()
exp.add_constraint("(^'review request')")
#exp.add_constraint("( ^ NOT('review request'|'prepare contract')* ('review request'NOT('review request'|'prepare contract')*'prepare contract'NOT('review request'|'prepare contract')*)*NOT('review request'|'prepare contract')* $)")
exp.add_constraint("(^NOT('prepare contract')* ('prepare contract' ANY*'send quote')* NOT('prepare contract')*$)")
exp.add_constraint("(^NOT('assess risks')* ('assess risks' ANY*'send quote')* NOT('assess risks')*$)")
print("Conf rate: " + str(exp.determine_conformance_rate()))
print("Fitness rate: " + str(exp.determine_fitness_rate()))

query_request1 = requests.post(
            exp.signal_endpoint,
            cookies=exp.cookies,
            headers=exp.headers,
            json={'query': 'SELECT "Activity" From "defaultview-4"'}
        )
query_request = requests.post(
            exp.signal_endpoint,
            cookies=exp.cookies,
            headers=exp.headers,
            json={'query': 'SELECT Activity From "defaultview-4" WHERE "VARIANT-INDEX" = 2'}
        )

data = query_request.json()['data']
event_log = EventLog()

first_ctrb = exp.constraint_ctrb_to_fitness(constraints=exp.constraints, index = 0)
snd_ctrb = exp.constraint_ctrb_to_fitness(constraints=exp.constraints, index = 1)
thr_ctrb = exp.constraint_ctrb_to_fitness(constraints=exp.constraints, index = 2)
print(f"First constraint contribution to fitness: {first_ctrb}")
print(f"Second constraint contribution to fitness: {snd_ctrb}")
print(f"third constraint contribution to fitness: {thr_ctrb}")
print(f"total distributon to fitness: {first_ctrb + snd_ctrb + thr_ctrb}")
first_ctrb = exp.constraint_ctrb_to_conformance(index = 0)
snd_ctrb = exp.constraint_ctrb_to_conformance(index = 1)
thr_ctrb = exp.constraint_ctrb_to_conformance(index = 2)


print(f"First constraint contribution to conf: {first_ctrb}")
print(f"Second constraint contribution to conf: {snd_ctrb}")
print(f"Third constraint contribution to conf: {thr_ctrb}")

print(f"total distributon to conf loss: {first_ctrb + snd_ctrb + thr_ctrb}")
