class MetamorphicTestExecutor:
    """
    Executes metamorphic tests on a system under test (SUT).
    """

    def __init__(self, system_under_test):
        self.sut = system_under_test

    def run_test(self, source_input, mr):
        source_output = self.sut(source_input)

        follow_up_input = mr.transform(source_input.copy())
        follow_up_output = self.sut(follow_up_input)

        passed = mr.check(source_output, follow_up_output)

        return {
            "mr": mr.__class__.__name__,
            "source_input": source_input,
            "follow_up_input": follow_up_input,
            "source_output": source_output,
            "follow_up_output": follow_up_output,
            "passed": passed
        }
