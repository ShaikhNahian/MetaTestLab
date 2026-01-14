from core.failure_classifier import classify_failure
from core.test_executor import MetamorphicTestExecutor
from core.reporting import save_counterexample


def run_directed_campaign(sut, mr, fuzzer, label="DIRECTED_CAMPAIGN", sut_name="sut", save_on_found=True):
    """
    Run a bug-directed search for a counterexample for one MR.
    """
    executor = MetamorphicTestExecutor(sut)

    found, result = fuzzer.find_counterexample(executor, mr)
    failure_type = classify_failure(result)

    print(f"\n[{label}]")
    print("MR:", result["mr"])
    print("Found counterexample:", found)
    print("Failure type:", failure_type)
    print("Source input:", result["source_input"])
    print("Follow-up input:", result["follow_up_input"])
    print("Source output:", result["source_output"])
    print("Follow-up output:", result["follow_up_output"])
    print("PASSED:", result["passed"])
    print("INPUT MUTATED:", result.get("input_mutated"))

    saved_path = None
    if found and save_on_found:
        saved_path = save_counterexample(
            result=result,
            failure_type=failure_type,
            sut_name=sut_name
        )
        print("Saved counterexample to:", saved_path)

    return found, result, failure_type, saved_path
