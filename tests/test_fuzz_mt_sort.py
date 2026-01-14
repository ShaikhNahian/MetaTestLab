from hypothesis import given, settings, strategies as st

from core.test_executor import MetamorphicTestExecutor
from systems_under_test.sorting import sort_numbers, buggy_sort

from relations.permutation import PermutationMR
from relations.idempotence import IdempotenceMR
from relations.add_constant import AddConstantMR
from relations.input_purity import InputPurityMR


# ----------------------------
# Hypothesis strategies
# ----------------------------

# For purity testing, we want lists where sorting *actually changes something*
# so we avoid:
# - size 1 lists
# - already-sorted lists
int_lists_for_purity = st.lists(
    st.integers(min_value=-1000, max_value=1000),
    min_size=2,
    max_size=30
).filter(lambda xs: xs != sorted(xs))


# For general MT relations, any non-empty list is okay
int_lists_general = st.lists(
    st.integers(min_value=-1000, max_value=1000),
    min_size=1,
    max_size=30
)


# ----------------------------
# Fuzzed MT Tests (Correct Sort)
# ----------------------------

@given(source_input=int_lists_general)
@settings(max_examples=100)
def test_sort_numbers_metamorphic_fuzz(source_input):
    executor = MetamorphicTestExecutor(sort_numbers)

    relations = [
        PermutationMR(),
        IdempotenceMR(),
        AddConstantMR(constant=10),
        InputPurityMR()
    ]

    for mr in relations:
        result = executor.run_test(source_input, mr)

        # All MRs should hold
        assert result["passed"], f"MR failed: {result}"

        # Correct sort should never mutate input
        assert not result["input_mutated"], f"Input mutated: {result}"


# ----------------------------
# Fuzzed MT Tests (Buggy Sort)
# ----------------------------

@given(source_input=int_lists_for_purity)
@settings(max_examples=50)
def test_buggy_sort_detects_purity_violation(source_input):
    executor = MetamorphicTestExecutor(buggy_sort)

    mr = InputPurityMR()
    result = executor.run_test(source_input, mr)

    # buggy_sort uses in-place sorting, so input purity should break
    assert result["input_mutated"], f"Expected mutation not detected: {result}"
