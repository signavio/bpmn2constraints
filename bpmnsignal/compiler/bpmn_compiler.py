
from itertools import combinations
from bpmnsignal.templates.declare_templates import Declare
from bpmnsignal.templates.matching_templates import Signal
from bpmnsignal.compiler.ltl.declare2ltl import Declare2ltl
from bpmnsignal.utils.constants import *

# TODO: Check the order of constraints..

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
            self._compile(cfo)
        return self.compiled_sequence

    def _compile(self, cfo):
        
        if cfo.get("is start"):
            self._create_init_constraint(cfo)
        if cfo.get("is end"):
            self._create_end_constraint(cfo)
        
        if self._is_activity(cfo):
            self._create_succession_constraint(cfo)

        elif self._is_gateway(cfo):
            if cfo.get("splitting"):
                self._create_gateway_constraints(cfo)
                self._create_precedence_constraint(cfo)


            if cfo.get("joining"):
                self._create_response_constraint(cfo)
        
    def _create_gateway_constraints(self, cfo):
        gateway_type = cfo.get("type")
        if gateway_type == "Exclusive_Databased_Gateway":
            self._create_exclusive_choice_constraint(cfo)

        if gateway_type == "ParallelGateway":
            self._create_parallel_gateway_constraint(cfo)
            self.concurrent = True

        if gateway_type == "InclusiveGateway":
            self._create_inclusive_choice_constraint(cfo)

    def _create_succession_constraint(self, cfo):
        name = self._get_cfo_name(cfo)
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                if successor.get("gateway successors"):
                    successors.extend(successor.get("gateway successors"))
        if self.transitivity:
            try:
                transitivity = cfo.get("transitivity")
                transitivity = [x for x in transitivity if not self._is_gateway(x)]
                successors.extend(transitivity)
            except Exception:
                pass

        for successor in successors:
            if successor.get("type") in ALLOWED_END_EVENTS:
                continue
            successor_name = self._get_cfo_name(successor)

            if successor_name in ALLOWED_GATEWAYS:
                continue

            if not successor.get("gateway successor"):
                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description = f"{name} leads to {successor_name}",
                        signal = self.signal.succession(name, successor_name),
                        declare = self.declare.succession(name, successor_name),
                        ltlf = self.ltlf.to_ltl_str(self.declare.succession(name, successor_name)),
                    )
                )

                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description= f"{name} and {successor_name}",
                        signal= self.signal.co_existence(name, successor_name),
                        declare= self.declare.co_existence(name, successor_name),
                        ltlf= self.ltlf.to_ltl_str(self.declare.co_existence(name, successor_name)),
                    )
                )

                if self.concurrent:
                    self.compiled_sequence.append(
                        self._create_constraint_object(
                            description = f"{name} leads to {successor_name}",
                            signal = self.signal.alternate_succession(name, successor_name),
                            declare = self.declare.alternate_succession(name, successor_name),
                            ltlf = self.ltlf.to_ltl_str(self.declare.alternate_succession(name, successor_name)),
                        )
                    )
            else:
                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description = f"{name} responds to {successor_name}",
                        signal = self.signal.alternate_response(name, successor_name),
                        declare = self.declare.alternate_response(name, successor_name),
                        ltlf= self.ltlf.to_ltl_str(self.declare.alternate_response(name, successor_name))
                    )
                )

                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description = f"{successor_name} precedes {name}",
                        signal = self.signal.alternate_precedence(successor_name, name),
                        declare = self.declare.alternate_precedence(successor_name, name),
                        ltlf= self.ltlf.to_ltl_str(self.declare.alternate_response(successor_name, name))
                    )
                )
            
    def _create_precedence_constraint(self, cfo):
        successors = cfo.get("successor")
        predecessors = cfo.get("predecessor")

        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))

        # if self.transitivity:
        #     successors.extend(cfo.get("transitivity"))

        for successor in successors:
            successor_name = self._get_cfo_name(successor)
            if successor.get("type") in ALLOWED_GATEWAYS:
                continue

            if not self._is_valid_name(successor_name):
                continue

            for predecessor in predecessors:
                predecessor_name = self._get_cfo_name(predecessor)
                if predecessor.get("type") in ALLOWED_GATEWAYS:
                    continue

                if not self._is_valid_name(predecessor_name):
                    continue

                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description = f"{predecessor_name} precedes {successor_name}",
                        signal = self.signal.precedence(predecessor_name, successor_name),
                        declare = self.declare.precedence(predecessor_name, successor_name),
                        ltlf = self.ltlf.to_ltl_str(self.declare.precedence(predecessor_name, successor_name)),
                    )
                )

                if self.concurrent:
                    self.compiled_sequence.append(
                        self._create_constraint_object(
                            description = f"{predecessor_name} precedes {successor_name}",
                            signal = self.signal.alternate_precedence(predecessor_name, successor_name),
                            declare = self.declare.alternate_precedence(predecessor_name, successor_name),
                            ltlf = self.ltlf.to_ltl_str(self.declare.alternate_precedence(predecessor_name, successor_name)),
                        )
                    )

    def _is_valid_name(self, name):
        if name in ALLOWED_START_EVENTS:
            return False
        if name in ALLOWED_END_EVENTS:
            return False
        if name in ALLOWED_GATEWAYS:
            return False
        return True

    def _create_response_constraint(self, cfo):
        successors = cfo.get("successor")
        predecessors = cfo.get("predecessor")

        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))

        # if self.transitivity:
        #     successors.extend(cfo.get("transitivity"))

        for predecessor in predecessors:
            predecessor_name = self._get_cfo_name(predecessor)
            if not self._is_valid_name(predecessor_name):
                continue

            if predecessor.get("type") in ALLOWED_GATEWAYS:
                    continue

            for successor in successors:
                successor_name = self._get_cfo_name(successor)
                if not self._is_valid_name(successor_name):
                    continue

                if successor.get("type") in ALLOWED_GATEWAYS:
                    continue

                self._create_constraint_object(
                    description = f"{predecessor_name} responds to {successor_name}",
                    signal = self.signal.response(predecessor_name, successor_name),
                    declare = self.declare.response(predecessor_name, successor_name),
                    ltlf = self.ltlf.to_ltl_str(self.declare.response(predecessor_name, successor_name)),
                )

                if self.concurrent:
                    self._create_constraint_object(
                        description = f"{predecessor_name} responds to {successor_name}",
                        signal = self.signal.alternate_response(predecessor_name, successor_name),
                        declare = self.declare.alternate_response(predecessor_name, successor_name),
                        ltlf = self.ltlf.to_ltl_str(self.declare.alternate_response(predecessor_name, successor_name)),
                    )

    def _create_init_constraint(self, cfo):
        name = self._get_cfo_name(cfo)

        self.compiled_sequence.append(
            self._create_constraint_object(
                description = f"starts with {name}",
                signal = self.signal.init(name),
                declare = self.declare.init(name),
                ltlf = self.ltlf.to_ltl_str(self.declare.init(name)),
            )
        )

    def _create_end_constraint(self, cfo):
        name = self._get_cfo_name(cfo)

        if not self._is_valid_name(name):
            return
        
        self.compiled_sequence.append(
            self._create_constraint_object(
                description = f"ends with {name}",
                signal = self.signal.end(name),
                declare = self.declare.end(name),
                ltlf = self.ltlf.to_ltl_str(self.declare.end(name)),
            )
        )

    def _create_exclusive_choice_constraint(self, cfo):
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))

        if successors:
            successors = [self._get_cfo_name(successor) for successor in successors]
            for split in combinations(successors, 2):
                if not self._is_valid_name(split[0]) and not self._is_valid_name(split[1]):
                    continue
                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description = f"{split[0]} xor {split[1]}",
                        signal = self.signal.exclusive_choice(split[0], split[1]),
                        declare = self.declare.exclusive_choice(split[0], split[1]),
                        ltlf = self.ltlf.to_ltl_str(self.declare.exclusive_choice(split[0], split[1])),
                    )
                )

    def _create_parallel_gateway_constraint(self, cfo):
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))
        if successors:
            successors = [self._get_cfo_name(successor) for successor in successors]
            for split in combinations(successors, 2):
                if not self._is_valid_name(split[0]) and not self._is_valid_name(split[1]):
                    continue
                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description = f"{split[0]} and {split[1]}",
                        signal = self.signal.co_existence(split[0], split[1]),
                        declare = self.declare.co_existence(split[0], split[1]),
                        ltlf = self.ltlf.to_ltl_str(self.declare.co_existence(split[0], split[1])),
                    )
                )
                
    def _create_inclusive_choice_constraint(self, cfo):
        successors = cfo.get("successor")
        for successor in successors:
            if successor.get("type") in ALLOWED_GATEWAYS:
                successors.extend(successor.get("gateway successors"))
        if successors:
            successors = [self._get_cfo_name(successor) for successor in successors]
            for split in combinations(successors, 2):
                if not self._is_valid_name(split[0]) and not self._is_valid_name(split[1]):
                    continue
                self.compiled_sequence.append(
                    self._create_constraint_object(
                        description = f"{split[0]} or {split[1]}",
                        signal = self.signal.choice(split[0], split[1]),
                        declare = self.declare.choice(split[0], split[1]),
                        ltlf = self.ltlf.to_ltl_str(self.declare.choice(split[0], split[1])),
                    )
                )

    def _get_cfo_name(self, cfo):
        name = cfo.get("name")
        if not name or name == " ":
            name = cfo.get("type")
        return name
    
    def _is_activity(self, cfo):
        cfo_type = cfo.get("type")
        if cfo_type:
            return cfo_type in ALLOWED_ACTIVITIES
        return False
    
    def _is_gateway(self, cfo):
        cfo_type = cfo.get("type")
        if cfo_type:
            return cfo_type in ALLOWED_GATEWAYS
        return False

    def _create_constraint_object(self, description, signal, declare, ltlf):
        return {
            "description" : description,
            "SIGNAL" : signal,
            "DECLARE" : declare,
            "LTLf" : ltlf
        }



