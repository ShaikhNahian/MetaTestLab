"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from core.test_executor import MetamorphicTestExecutor
from systems_under_test.ml_model import predict
from relations.noise_robustness import NoiseRobustnessMR
from relations.feature_perturbation import FeaturePerturbationMR
from relations.feature_scaling import FeatureScalingMR
from systems_under_test.ml_model import predict_clean, predict_with_buggy_preprocessing
from relations.input_purity import InputPurityMR
from core.failure_classifier import classify_failure



def test_ml_noise_robustness():
    executor = MetamorphicTestExecutor(predict)

    source_input = [0.5, -1.2, 0.3]
    mr = NoiseRobustnessMR(std=0.01, seed=42)

    result = executor.run_test(source_input, mr)

    print("\n[ML NOISE ROBUSTNESS]")
    print("MR:", result["mr"])
    print("Source input:", result["source_input"])
    print("Follow-up input:", result["follow_up_input"])
    print("Prediction (source):", result["source_output"])
    print("Prediction (follow-up):", result["follow_up_output"])

    # Small noise → prediction should remain stable
    assert result["passed"]
    assert not result["input_mutated"]

def test_ml_feature_perturbation_sensitivity():
    executor = MetamorphicTestExecutor(predict)
    mr = FeaturePerturbationMR(feature_index=0, delta=5.0)

    result = executor.run_test([0.5, -1.2, 0.3], mr)
    failure_type = classify_failure(result)

    print("\n[ML FEATURE SENSITIVITY]")
    print("MR:", result["mr"])
    print("Failure type:", failure_type)

    if not result["passed"]:
        assert failure_type == "SENSITIVITY_FAILURE"
    else:
        assert failure_type == "NO_FAILURE"


def test_ml_feature_scaling_stability():
    executor = MetamorphicTestExecutor(predict)

    source_input = [0.5, -1.2, 0.3]
    mr = FeatureScalingMR(scale=2.0)

    result = executor.run_test(source_input, mr)

    print("\n[ML FEATURE SCALING]")
    print("MR:", result["mr"])
    print("Source input:", result["source_input"])
    print("Follow-up input:", result["follow_up_input"])
    print("Prediction (source):", result["source_output"])
    print("Prediction (follow-up):", result["follow_up_output"])

    assert result["passed"]
    assert not result["input_mutated"]

def test_ml_clean_pipeline_purity():
    executor = MetamorphicTestExecutor(predict_clean)

    source_input = [0.5, -1.2, 0.3]
    mr = InputPurityMR()

    result = executor.run_test(source_input, mr)

    print("\n[ML CLEAN PIPELINE]")
    print("MR:", result["mr"])
    print("Source input:", result["source_input"])
    print("Follow-up input:", result["follow_up_input"])
    print("Prediction:", result["source_output"])
    print("INPUT MUTATED:", result["input_mutated"])

    assert result["passed"]
    assert not result["input_mutated"]

def test_ml_buggy_pipeline_purity():
    executor = MetamorphicTestExecutor(predict_with_buggy_preprocessing)
    mr = InputPurityMR()

    result = executor.run_test([0.5, -1.2, 0.3], mr)
    failure_type = classify_failure(result)

    print("\n[ML BUGGY PIPELINE]")
    print("MR:", result["mr"])
    print("Failure type:", failure_type)
    print("INPUT MUTATED:", result["input_mutated"])

    assert failure_type == "PURITY_FAILURE"






