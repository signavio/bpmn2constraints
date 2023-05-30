from bpmnsignal.templates.declare_templates import Declare
from bpmnsignal.templates.matching_templates import Signal
from bpmnsignal.utils.constants import *

class Compiler():

    def __init__(self, sequence, transitivity) -> None:
        self.sequence = sequence
        self.transitivity = transitivity
        self.declare = Declare()
        self.signal = Signal()
        self.concurrent = False

    def run(self):
        for cfo in self.sequence:
            self.compile(cfo)

    def compile(self, cfo):
        pass

    def create_succession_constraint(self, cfo):
        pass

    def create_precedence_constraint(self, cfo):
        pass

    def create_response_constraint(self, cfo):
        pass

    def create_init_constraint(self, cfo):
        pass

    def create_end_constraint(self, cfo):
        pass
        
    def get_cfo_name(self, cfo):
        name = cfo.get("name")
        if not name or name == " ":
            name = cfo.get("type")
        return name
    
    def is_activity(self, cfo):
        cfo_type = cfo.get("type")
        if cfo_type:
            return cfo_type in ALLOWED_ACTIVITIES
        return False
    
    def is_gateway(self, cfo):
        cfo_type = cfo.get("type")
        if cfo_type:
            return cfo_type in ALLOWED_GATEWAYS
        return False




