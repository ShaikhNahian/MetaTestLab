from fuzzing.boundary_fuzzer import BoundarySeekingFuzzer
from core.campaign_runner import run_directed_campaign

from systems_under_test.ml_model import predict, predict_proba_clean
from relations.noise_robustness import NoiseRobustnessMR


def test_boundary_seeking_fuzzer_finds_noise_counterexample():
    mr = NoiseRobustnessMR(std=0.01, seed=42)

    fuzzer = BoundarySeekingFuzzer(
        seed_input=[0.5, -1.2, 0.3],
        proba_fn=predict_proba_clean,
        step=0.7,
        max_iters=400,
        candidates_per_iter=25
    )

    found, result, failure_type, saved_path = run_directed_campaign(
        sut=predict,
        mr=mr,
        fuzzer=fuzzer,
        label="BOUNDARY SEEKING FUZZ (Noise Robustness)",
        sut_name="predict",
        save_on_found=True
    )

    assert found in [True, False]

    if found:
        assert saved_path is not None
        assert failure_type == "ROBUSTNESS_FAILURE"
