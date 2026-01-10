from core.test_executor import MetamorphicTestExecutor
from systems_under_test.ml_model import predict
from relations.noise_robustness import NoiseRobustnessMR

def test_ml_noise_robustness():
    executor = MetamorphicTestExecutor(predict)

    source_input = [0.5, -1.2, 0.3]
    mr = NoiseRobustnessMR(std=0.01)

    result = executor.run_test(source_input, mr)

    print("\n[ML NOISE ROBUSTNESS]")
    print("MR:", result["mr"])
    print("Source input:", result["source_input"])
    print("Follow-up input:", result["follow_up_input"])
    print("Prediction (source):", result["source_output"])
    print("Prediction (follow-up):", result["follow_up_output"])

    assert result["passed"] is True
