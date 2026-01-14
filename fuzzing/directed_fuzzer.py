"""
Author: Shaikh Nahian
Since: Dec 2025
"""
import random
from fuzzing.mutators import mutate_float_vector, clip_vector


class DirectedFuzzer:
    """
    Bug-directed fuzzer:
    - Starts from a seed input
    - Mutates input iteratively
    - Stops when it finds an MR violation or purity violation
    """

    def __init__(self, seed_input, step=0.5, max_iters=300, clip=(-10.0, 10.0), restart_prob=0.15):
        self.seed_input = list(seed_input)
        self.step = step
        self.max_iters = max_iters
        self.clip = clip
        self.restart_prob = restart_prob

    def find_counterexample(self, executor, mr):
        """
        Search for an input that causes:
        - MR failure (passed == False)
        OR
        - input mutation (input_mutated == True)

        Returns:
            (found: bool, result: dict)
        """
        current = list(self.seed_input)

        # Evaluate the starting point
        best_result = executor.run_test(current, mr)

        if (not best_result["passed"]) or best_result.get("input_mutated", False):
            return True, best_result

        for _ in range(self.max_iters):
            # Occasionally restart from the seed to avoid local traps
            if random.random() < self.restart_prob:
                current = list(self.seed_input)

            candidate = mutate_float_vector(current, step=self.step)
            candidate = clip_vector(candidate, self.clip[0], self.clip[1])

            result = executor.run_test(candidate, mr)

            # Success condition: MR violation OR purity violation
            if (not result["passed"]) or result.get("input_mutated", False):
                return True, result

            # Keep exploring by moving the search point sometimes
            if random.random() < 0.5:
                current = candidate

            best_result = result

        return False, best_result
