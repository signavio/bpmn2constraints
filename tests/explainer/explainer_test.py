from explainer.explainer import *


# Test 1: Adding and checking constraints
def test_add_constraint():
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    assert "A.*B.*C" in explainer.constraints, "Constraint 'A.*B.*C' should be added."


# Test 2: Removing constraints
def test_remove_constraint():
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    explainer.add_constraint("B.*C")
    explainer.remove_constraint(0)
    assert (
        "A.*B.*C" not in explainer.constraints,
    ),"Constraint 'A.*B.*C' should be removed."


# Test 3: Activation of constraints
def test_activation():
    trace = Trace(["A", "B", "C"])
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    assert explainer.activation(trace), "The trace should activate the constraint."


# Test 4: Checking conformance of traces
def test_conformance():
    trace = Trace(["A", "B", "C"])
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    assert explainer.conformant(trace), "The trace should be conformant."


# Test 5: Non-conformance explanation
def test_non_conformance_explanation():
    trace = Trace(["C", "A", "B"])
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    explanation = explainer.minimal_expl(trace)
    assert "violated" in explanation, "The explanation should indicate a violation."


# Test 6: Overlapping constraints
def test_overlapping_constraints():
    trace = Trace(["A", "B", "A", "C"])
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    explainer.add_constraint("A.*A.*C")
    assert explainer.conformant(
        trace
    ), "The trace should be conformant with overlapping constraints."

# Test 7: Partially meeting constraints
def test_partial_conformance():
    trace = Trace(["A", "C", "B"])
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    assert not explainer.conformant(trace), "The trace should not be fully conformant."


# Test 8: Constraints with repeated nodes
def test_constraints_with_repeated_nodes():
    trace = Trace(["A", "A", "B", "A"])
    explainer = Explainer()
    explainer.add_constraint("A.*A.*B.*A")
    assert explainer.conformant(
        trace
    ), "The trace should conform to the constraint with repeated nodes."

# Test 9: Removing constraints and checking nodes list
def test_remove_constraint_and_check_nodes():
    explainer = Explainer()
    explainer.add_constraint("A.*B")
    explainer.add_constraint("B.*C")
    explainer.remove_constraint(0)
    assert (
        "A" not in explainer.nodes and "B" in explainer.nodes and "C" in explainer.nodes
    ), "Node 'A' should be removed, while 'B' and 'C' remain."

# Test 10: Complex regex constraint
def test_complex_regex_constraint():
    trace = Trace(["A", "X", "B", "Y", "C"])
    explainer = Explainer()
    explainer.add_constraint(
         "A.*X.*B.*Y.*C"
    )  # Specifically expects certain nodes in order
    assert explainer.conformant(
        trace
    ), "The trace should conform to the complex regex constraint."


# Test 11: Constraint not covered by any trace node
def test_constraint_not_covered():
    trace = Trace(["A", "B", "C"])
    explainer = Explainer()
    explainer.add_constraint("D*")  # This node "D" does not exist in the trace
    assert explainer.activation(trace) == [
        0
    ], "The constraint should not be activated by the trace."

# Test 12: Empty trace and constraints
def test_empty_trace_and_constraints():
    trace = Trace([])
    explainer = Explainer()
    explainer.add_constraint("")  # Adding an empty constraint
    assert explainer.conformant(
        trace
    ), "An empty trace should be conformant with an empty constraint."


# Test 13: Removing non-existent constraint index
def test_remove_nonexistent_constraint():
    explainer = Explainer()
    explainer.add_constraint("A.*B")
    explainer.remove_constraint(10)  # Non-existent index
    assert (
        len(explainer.constraints) == 1
    ), "Removing a non-existent constraint should not change the constraints list."

# Test 14: Activation with no constraints
def test_activation_with_no_constraints():
    trace = Trace(["A", "B", "C"])
    explainer = Explainer()
    assert not explainer.activation(trace), "No constraints should mean no activation."


# Test 15: Trace conformance against multiple constraints
def test_trace_conformance_against_multiple_constraints():
    trace1 = Trace(
        ["A", "B", "D"]
    )  # This trace should not be fully conformant as it only matches one constraint
    trace2 = Trace(
        ["A", "B", "C", "D"]
    )  # This trace should be conformant as it matches both constraints

    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")  # Both traces attempt to conform to this
    explainer.add_constraint("B.*D")  # And to this

    # Checking conformance
    assert not explainer.conformant(
        trace1
    ), "Trace1 should not be conformant as it does not satisfy all constraints."
    assert explainer.conformant(
        trace2
    ), "Trace2 should be conformant as it satisfies all constraints."


# Test 16: Conformant trace does not generate minimal explaination 
def test_conformant_trace_handled_correctly():
    trace = Trace(["A", "B"])
    explainer = Explainer()
    explainer.add_constraint("AB")

    assert explainer.minimal_expl(trace) == "The trace is already conformant, no changes needed."


# Test 17: Conformant trace
def test_explainer_methods():
    trace = Trace(["A", "B", "C"])
    explainer = Explainer()
    explainer.add_constraint("A.*B.*C")
    explainer.add_constraint("B.*C")

    assert (
        explainer.conformant(trace) == True
    ), "Test 1 Failed: Trace should be conformant."
    assert (
        explainer.minimal_expl(trace)
        == "The trace is already conformant, no changes needed."
    ), "Test 1 Failed: Incorrect minimal explanation for a conformant trace."
    assert (
        explainer.counterfactual_expl(trace)
        == "The trace is already conformant, no changes needed."
    ), "Test 1 Failed: Incorrect counterfactual explanation for a conformant trace."


# Test 18: Some explaination test
def test_explaination():
    explainer = Explainer()
    
    conformant_trace = Trace(["A","B","C"])
    non_conformant_trace = Trace(["A","C"])
    
    explainer.add_constraint("A.*B.*C")

    assert explainer.conformant(non_conformant_trace) == False
    assert explainer.conformant(conformant_trace) == True
    assert (
        explainer.minimal_expl(non_conformant_trace)
        == "Non-conformance due to: Constraint (A.*B.*C) is violated by subtrace: ('A', 'C')"
    )
    assert (
        explainer.counterfactual_expl(non_conformant_trace)
        == "\nAddition (Added B at position 1): A->B->C"
    )


# Test 19: Complex explaination test.
"""
This part is not very complex as of now and is very much up for change, the complexity of counterfactuals 
proved to be slightly larger than expected
"""
def test_complex_counterfactual_explanation():
    explainer = Explainer()

    explainer.add_constraint("ABB*C")

    non_conformant_trace = Trace(["A", "C", "E", "D"])

    counterfactual_explanation = explainer.counterfactual_expl(non_conformant_trace)
    
    assert (
            counterfactual_explanation
            == "\nAddition (Added B at position 1): A->B->C->E->D"
    )

# Test 20: Event logs
def test_event_log():
    event_log = EventLog()
    assert event_log != None
    trace = Trace(["A", "B", "C"])
    event_log.add_trace(trace)
    assert event_log.log == {
        ("A", "B", "C"): 1
    }  # There should be one instance of the trace in the log
    event_log.add_trace(trace, 5)
    assert event_log.log == {
        ("A", "B", "C"): 6
    }  # There should be 6 instances of the trace in the log
    event_log.remove_trace(trace)
    assert event_log.log == {
        ("A", "B", "C"): 5
    }  # There should be 5 instances of the trace
    event_log.remove_trace(trace, 5)
    assert event_log.log == {}  # The log should be emptied
    event_log.add_trace(trace, 5)
    event_log.remove_trace(trace, 10)
    assert event_log.log == {}  # The log should be emptied
    trace2 = Trace(["X", "Y", "Z"])
    event_log.add_trace(trace, 5)
    event_log.add_trace(trace2, 7)
    assert event_log.log == {
        ("A", "B", "C"): 5,
        ("X", "Y", "Z"): 7,
    }  # There should be several traces in the log

