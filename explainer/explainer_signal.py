from abc import ABC, abstractmethod
from explainer import Explainer, Trace, EventLog
import re
from tutorial import SignavioAuthenticator
import json
from conf import system_instance, workspace_id, user_name, pw
class ExplainerSignal(Explainer):
    def __init__(self):
        super().__init__()
        authenticator = SignavioAuthenticator(system_instance, workspace_id, user_name, pw)
        auth_data = authenticator.authenticate()
        cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
        headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
        #diagram_url = system_instance + '/p/revision'
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
        pass
    
    def counterfactual_expl(self, trace):
        pass
    
    def determine_shapley_value(self, log, constraints, index):
        pass
    
    def evaluate_similarity(self, trace):
        pass
    
    def determine_conformance_rate(self, event_log, constraints=None):
        pass
    
    def trace_contribution_to_conformance_loss(self, event_log, trace, constraints=None):
        pass


exp = ExplainerSignal()
exp.add_constraint("(^'A')")
print(exp.constraints)