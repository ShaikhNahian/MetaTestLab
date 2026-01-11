"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from core.test_executor import MetamorphicTestExecutor
from systems_under_test.sorting import sort_numbers, buggy_sort
from relations.permutation import PermutationMR
from relations.idempotence import IdempotenceMR
from relations.add_constant import AddConstantMR
from relations.value_perturbation import ValuePerturbationMR
from relations.input_purity import InputPurityMR



def test_correct_sort_with_logging():
    executor = MetamorphicTestExecutor(sort_numbers)

    relations = [
        PermutationMR(),
        IdempotenceMR(),
        AddConstantMR(constant=10),
        ValuePerturbationMR(index=0, delta=1000),
        InputPurityMR()
    ]

    for mr in relations:
        result = executor.run_test([3, 1, 4, 2], mr)

        print("\n[CORRECT SORT]")
        print("MR:", result["mr"])
        print("Source input:", result["source_input"])
        print("Follow-up input:", result["follow_up_input"])
        print("Source output:", result["source_output"])
        print("Follow-up output:", result["follow_up_output"])
        print("PASSED:", result["passed"])
        print("INPUT MUTATED:", result["input_mutated"])

        assert bool(result["passed"]) is True
        assert bool(result["input_mutated"]) is False


def test_buggy_sort_with_logging():
    executor = MetamorphicTestExecutor(buggy_sort)

    relations = [
        PermutationMR(),
        IdempotenceMR(),
        AddConstantMR(constant=10),
        ValuePerturbationMR(index=0, delta=1000),
        InputPurityMR()
    ]

    failures = 0

    for mr in relations:
        result = executor.run_test([2, 1, 4, 3], mr)

        print("\n[BUGGY SORT]")
        print("MR:", result["mr"])
        print("Source input:", result["source_input"])
        print("Follow-up input:", result["follow_up_input"])
        print("Source output:", result["source_output"])
        print("Follow-up output:", result["follow_up_output"])
        print("PASSED:", result["passed"])
        print("INPUT MUTATED:", result["input_mutated"])

        # Failure if MR fails OR input purity broke
        if not result["passed"] or result["input_mutated"]:
            failures += 1

    # buggy system should give failure, so getting failure means test passed
    assert failures >= 1

