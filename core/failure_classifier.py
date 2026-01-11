"""
Author: Shaikh Nahian
Since: Dec 2025
"""
def classify_failure(result):
    """
    Classify the type of failure based on MT execution result.
    """

    if result.get("input_mutated"):
        return "PURITY_FAILURE"

    # Change-sensitive MR failed
    if result["mr"] in {
        "ValuePerturbationMR",
        "FeaturePerturbationMR"
    } and not result["passed"]:
        return "SENSITIVITY_FAILURE"

    # Invariance MR failed
    if result["mr"] in {
        "PermutationMR",
        "IdempotenceMR",
        "AddConstantMR",
        "NoiseRobustnessMR",
        "FeatureScalingMR"
    } and not result["passed"]:
        return "ROBUSTNESS_FAILURE"

    return "NO_FAILURE"
