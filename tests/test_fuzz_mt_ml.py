from hypothesis import given, settings, strategies as st

from core.test_executor import MetamorphicTestExecutor
from systems_under_test.ml_model import predict, predict_buggy

from relations.noise_robustness import NoiseRobustnessMR
from relations.feature_scaling import FeatureScalingMR
from relations.input_purity import InputPurityMR


# ----------------------------
# Hypothesis strategies
# ----------------------------

# ML model expects exactly 3 features
ml_vectors_general = st.lists(
    st.floats(min_value=-5, max_value=5, allow_nan=False, allow_infinity=False),
    min_size=3,
    max_size=3
)

# For purity detection we avoid degenerate vectors like [0,0,0]
# because buggy in-place normalization may write the same values back,
# making mutation invisible in a value-based comparison.
ml_vectors_for_purity = ml_vectors_general.filter(lambda xs: len(set(xs)) > 1)


# ----------------------------
# Statistical MT for ML Robustness
# ----------------------------

# In ML, "noise robustness" is often statistical:
# some points near the decision boundary may flip under small noise.
noise_total = 0
noise_pass = 0


@given(source_input=ml_vectors_general)
@settings(max_examples=200)
def test_ml_noise_robustness_fuzz_statistical(source_input):
    global noise_total, noise_pass

    executor = MetamorphicTestExecutor(predict)
    mr = NoiseRobustnessMR(std=0.01, seed=42)

    result = executor.run_test(source_input, mr)

    noise_total += 1
    if result["passed"]:
        noise_pass += 1

    # predict() should never mutate the input
    assert not result["input_mutated"], f"Input mutated unexpectedly: {result}"

    # After enough examples, enforce a pass-rate threshold
    if noise_total >= 200:
        pass_rate = noise_pass / noise_total
        assert pass_rate >= 0.95, f"Noise robustness pass rate too low: {pass_rate}"


# ----------------------------
# Scaling stability (can be strict)
# ----------------------------

@given(source_input=ml_vectors_general)
@settings(max_examples=100)
def test_ml_scaling_stability_fuzz(source_input):
    executor = MetamorphicTestExecutor(predict)

    mr = FeatureScalingMR(scale=2.0)
    result = executor.run_test(source_input, mr)

    assert result["passed"], f"Scaling stability failed: {result}"
    assert not result["input_mutated"], f"Input mutated unexpectedly: {result}"


# ----------------------------
# Buggy pipeline purity detection (should always detect mutation)
# ----------------------------

@given(source_input=ml_vectors_for_purity)
@settings(max_examples=50)
def test_ml_buggy_pipeline_mutation_detected_fuzz(source_input):
    executor = MetamorphicTestExecutor(predict_buggy)

    mr = InputPurityMR()
    result = executor.run_test(source_input, mr)

    assert result["input_mutated"], f"Expected mutation not detected: {result}"
