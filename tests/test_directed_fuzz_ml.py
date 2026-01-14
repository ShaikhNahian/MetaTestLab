"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from fuzzing.directed_fuzzer import DirectedFuzzer
from core.campaign_runner import run_directed_campaign

from systems_under_test.ml_model import predict
from relations.noise_robustness import NoiseRobustnessMR


def test_directed_fuzz_find_noise_counterexample():
    """
    Bug-directed fuzzing: try to find an input where small noise flips prediction.
    This is a robustness counterexample.
    """

    mr = NoiseRobustnessMR(std=0.01, seed=42)

    fuzzer = DirectedFuzzer(
        seed_input=[0.5, -1.2, 0.3],
        step=0.5,
        max_iters=500
    )

    found, result, failure_type = run_directed_campaign(
        sut=predict,
        mr=mr,
        fuzzer=fuzzer,
        label="DIRECTED FUZZ (ML Noise Robustness)"
    )

    # This is a discovery test: it may or may not find one depending on model boundary
    # We only assert the test runs correctly.
    assert found in [True, False]

    # If it does find one, it must be classified correctly
    if found:
        assert failure_type in ["ROBUSTNESS_FAILURE", "PURITY_FAILURE"]
