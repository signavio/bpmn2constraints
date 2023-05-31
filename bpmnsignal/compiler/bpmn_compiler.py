
from itertools import combinations
from bpmnsignal.templates.declare_templates import Declare
from bpmnsignal.templates.matching_templates import Signal
from bpmnsignal.compiler.ltl.declare2ltl import Declare2ltl
from bpmnsignal.utils.constants import *

class Compiler():

    def __init__(self, sequence, transitivity) -> None:
        self.sequence = sequence
        self.transitivity = transitivity
        self.declare = Declare()
        self.signal = Signal()
        self.ltlf = Declare2ltl()
        self.concurrent = True
        self.compiled_sequence = []

    def run(self):
        for cfo in self.sequence:
            self.compile(cfo)
        return self.compiled_sequence

    def compile(self, cfo):
        
        if cfo.get("is start"):
            self.create_init_constraint(cfo)
        if cfo.get("is end"):
            self.create_end_constraint(cfo)
        
        if self.is_activity(cfo):
            self.create_succession_constraint(cfo)

        if self.is_gateway(cfo):
            if cfo.get("splitting"):
                self.create_gateway_constraints(cfo)
                self.create_precedence_constraint(cfo)


            if cfo.get("joining"):
                self.create_response_constraint(cfo)
        
    def create_gateway_constraints(self, cfo):

        if cfo.get("name") == "XOR":
            self.create_exclusive_choice_constraint(cfo)

        if cfo.get("name") == "AND":
            self.create_parallel_gateway_constraint(cfo)
            self.concurrent = True

        if cfo.get("name") == "OR":
            self.create_inclusive_choice_constraint(cfo)

    def create_succession_constraint(self, cfo):
        name = self.get_cfo_name(cfo)
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                if successor.get("gateway successors"):
                    successors.extend(successor.get("gateway successors"))
        if self.transitivity:
            successors.extend(cfo.get("transitivity"))

        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                continue
            if successor.get("type") in ALLOWED_END_EVENTS:
                continue
            successor_name = self.get_cfo_name(successor)

            self.compiled_sequence.append(
                self.create_constraint_object(
                    description = f"{name} leads to {successor_name}",
                    signal = self.signal.succession(name, successor_name),
                    declare = self.declare.succession(name, successor_name),
                    ltlf = self.ltlf.to_ltl_str(self.declare.succession(name, successor_name)),
                )
            )

            self.compiled_sequence.append(
                self.create_constraint_object(
                    description= f"{name} and {successor_name}",
                    signal= self.signal.co_existence(name, successor_name),
                    declare= self.declare.co_existence(name, successor_name),
                    ltlf= self.ltlf.to_ltl_str(self.declare.co_existence(name, successor_name)),
                )
            )

            if self.concurrent:
                self.compiled_sequence.append(
                    self.create_constraint_object(
                        description= f"{name} leads to {successor_name}",
                        signal = self.signal.alternate_succession(name, successor_name),
                        declare = self.declare.alternate_succession(name, successor_name),
                        ltlf = self.ltlf.to_ltl_str(self.declare.alternate_succession(name, successor_name)),
                    )
                )
            
    def create_precedence_constraint(self, cfo):
        successors = cfo.get("successor")
        predecessors = cfo.get("predecessor")

        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))

        if self.transitivity:
            successors.extend(cfo.get("transitivity"))

        for successor in successors:
            successor_name = self.get_cfo_name(successor)
            if successor.get("type") in ALLOWED_GATEWAYS:
                continue
            for predecessor in predecessors:
                predecessor_name = self.get_cfo_name(predecessor)
                if predecessor.get("type") in ALLOWED_GATEWAYS:
                    continue
                self.compiled_sequence.append(
                    self.create_constraint_object(
                        description = f"{predecessor_name} precedes {successor_name}",
                        signal = self.signal.precedence(predecessor_name, successor_name),
                        declare = self.declare.precedence(predecessor_name, successor_name),
                        ltlf = self.ltlf.to_ltl_str(self.declare.precedence(predecessor_name, successor_name)),
                    )
                )

                if self.concurrent:
                    self.compiled_sequence.append(
                        self.create_constraint_object(
                            description = f"{predecessor_name} precedes {successor_name}",
                            signal = self.signal.alternate_precedence(predecessor_name, successor_name),
                            declare = self.declare.alternate_precedence(predecessor_name, successor_name),
                            ltlf = self.ltlf.to_ltl_str(self.declare.alternate_precedence(predecessor_name, successor_name)),
                        )
                    )

    def create_response_constraint(self, cfo):
        successors = cfo.get("successor")
        predecessors = cfo.get("predecessor")

        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))

        if self.transitivity:
            successors.extend(cfo.get("transitivity"))

        for predecessor in predecessors:
            predecessor_name = self.get_cfo_name(predecessor)
            for successor in successors:
                successor_name = self.get_cfo_name(successor)
                self.create_constraint_object(
                    description = f"{predecessor_name} responds to {successor_name}",
                    signal = self.signal.response(predecessor_name, successor_name),
                    declare = self.declare.response(predecessor_name, successor_name),
                    ltlf = self.ltlf.to_ltl_str(self.declare.response(predecessor_name, successor_name)),
                )

                if self.concurrent:
                    self.create_constraint_object(
                        description = f"{predecessor_name} responds to {successor_name}",
                        signal = self.signal.alternate_response(predecessor_name, successor_name),
                        declare = self.declare.alternate_response(predecessor_name, successor_name),
                        ltlf = self.ltlf.to_ltl_str(self.declare.alternate_response(predecessor_name, successor_name)),
                    )

    def create_init_constraint(self, cfo):
        name = self.get_cfo_name(cfo)
        self.compiled_sequence.append(
            self.create_constraint_object(
                description = f"starts with {name}",
                signal = self.signal.init(name),
                declare = self.declare.init(name),
                ltlf = self.ltlf.to_ltl_str(self.declare.init(name)),
            )
        )

    def create_end_constraint(self, cfo):
        name = self.get_cfo_name(cfo)
        self.compiled_sequence.append(
            self.create_constraint_object(
                description = f"ends with {name}",
                signal = self.signal.end(name),
                declare = self.declare.end(name),
                ltlf = self.ltlf.to_ltl_str(self.declare.end(name)),
            )
        )
        
    def create_exclusive_choice_constraint(self, cfo):
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))

        if successors:
            successors = [self.get_cfo_name(successor) for successor in successors if successor.get("type") not in ALLOWED_GATEWAYS]
            for split in combinations(successors, 2):
                self.compiled_sequence.append(
                    self.create_constraint_object(
                        description = f"{split[0]} xor {split[1]}",
                        signal = self.signal.exclusive_choice(split[0], split[1]),
                        declare = self.declare.exclusive_choice(split[0], split[1]),
                        ltlf = self.ltlf.to_ltl_str(self.declare.exclusive_choice(split[0], split[1])),
                    )
                )

    def create_parallel_gateway_constraint(self, cfo):
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))
        if successors:
            successors = [self.get_cfo_name(successor) for successor in successors if successor.get("type") not in ALLOWED_GATEWAYS]
            for split in combinations(successors, 2):
                self.compiled_sequence.append(
                    self.create_constraint_object(
                        description = f"{split[0]} and {split[1]}",
                        signal = self.signal.co_existence(split[0], split[1]),
                        declare = self.declare.co_existence(split[0], split[1]),
                        ltlf = self.ltlf.to_ltl_str(self.declare.co_existence(split[0], split[1])),
                    )
                )
                
    def create_inclusive_choice_constraint(self, cfo):
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))
        if successors:
            successors = [self.get_cfo_name(successor) for successor in successors if successor.get("type") not in ALLOWED_GATEWAYS]
            for split in combinations(successors, 2):
                self.compiled_sequence.append(
                    self.create_constraint_object(
                        description = f"{split[0]} or {split[1]}",
                        signal = self.signal.choice(split[0], split[1]),
                        declare = self.declare.choice(split[0], split[1]),
                        ltlf = self.ltlf.to_ltl_str(self.declare.choice(split[0], split[1])),
                    )
                )

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

    def create_constraint_object(self, description, signal, declare, ltlf):
        return {
            "description" : description,
            "SIGNAL" : signal,
            "DECLARE" : declare,
            "LTLf" : ltlf
        }



