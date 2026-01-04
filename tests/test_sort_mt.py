from core.test_executor import MetamorphicTestExecutor
from systems_under_test.sorting import sort_numbers, buggy_sort
from relations.permutation import PermutationMR
from relations.idempotence import IdempotenceMR
from relations.add_constant import AddConstantMR
from relations.value_perturbation import ValuePerturbationMR


def test_correct_sort_with_logging():
    executor = MetamorphicTestExecutor(sort_numbers)

    relations = [
        PermutationMR(),
        IdempotenceMR(),
        AddConstantMR(constant=10),
        ValuePerturbationMR(index=0, delta=1000)
    ]

    for mr in relations:
        result = executor.run_test([3, 1, 4, 2], mr)

        print("\n[CORRECT SORT]")
        print("MR:", result["mr"])
        print("Source input:", result["source_input"])
        print("Follow-up input:", result["follow_up_input"])
        print("Source output:", result["source_output"])
        print("Follow-up output:", result["follow_up_output"])

        assert result["passed"] is True


def test_buggy_sort_with_logging():
    executor = MetamorphicTestExecutor(buggy_sort)

    relations = [
        PermutationMR(),
        IdempotenceMR(),
        AddConstantMR(constant=10),
        ValuePerturbationMR(index=0, delta=1000)
    ]

    failures = 0

    for mr in relations:
        result = executor.run_test([3, 1, 4, 2], mr)

        print("\n[BUGGY SORT]")
        print("MR:", result["mr"])
        print("Source input:", result["source_input"])
        print("Follow-up input:", result["follow_up_input"])
        print("Source output:", result["source_output"])
        print("Follow-up output:", result["follow_up_output"])
        print("PASSED:", result["passed"])

        if not result["passed"]:
            failures += 1

    # At least one MR should detect the fault
    assert failures >= 1
