"""
Author: Shaikh Nahian
Since: Dec 2025
"""
import copy

class MetamorphicTestExecutor:
    """
    Executes metamorphic tests on a system under test (SUT).
    """

    def __init__(self, system_under_test):
        self.sut = system_under_test

    def run_test(self, source_input, mr):
        # Deep copy -> detect mutation
        original_input = copy.deepcopy(source_input)

        # source test
        source_output = self.sut(source_input)

        # follow-up input
        follow_up_input = mr.transform(copy.deepcopy(source_input))
        follow_up_output = self.sut(follow_up_input)

        # MR Check
        passed = mr.check(source_output, follow_up_output)

        # Input Purity Check
        input_mutated = source_input != original_input

        return {
            "mr": mr.__class__.__name__,
            "source_input": original_input,
            "follow_up_input": follow_up_input,
            "source_output": source_output,
            "follow_up_output": follow_up_output,
            "passed": passed,
            "input_mutated": input_mutated
        }
