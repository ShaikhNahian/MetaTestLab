"""
Author: Shaikh Nahian
Since: Dec 2025
"""
import random
from fuzzing.mutators import mutate_float_vector, clip_vector


class BoundarySeekingFuzzer:
    """
    Bug-directed fuzzer that tries to find inputs near the decision boundary.

    Boundary score idea:
      - If proba ~ 0.5 => close to boundary => more likely robustness failures
    """

    def __init__(
        self,
        seed_input,
        proba_fn,
        step=0.5,
        max_iters=500,
        candidates_per_iter=20,
        clip=(-10.0, 10.0),
        restart_prob=0.1,
        target=0.5
    ):
        self.seed_input = list(seed_input)
        self.proba_fn = proba_fn
        self.step = step
        self.max_iters = max_iters
        self.candidates_per_iter = candidates_per_iter
        self.clip = clip
        self.restart_prob = restart_prob
        self.target = target

    def boundary_score(self, x):
        """
        Higher score = closer to decision boundary.
        """
        p = self.proba_fn(x)
        # closeness to 0.5 => maximize score
        return 1.0 - abs(p - self.target)

    def find_counterexample(self, executor, mr):
        """
        Search for an MR violation using boundary seeking.
        """
        current = list(self.seed_input)
        best_result = executor.run_test(current, mr)

        # If already fails, done
        if (not best_result["passed"]) or best_result.get("input_mutated", False):
            return True, best_result

        best_score = self.boundary_score(current)

        for _ in range(self.max_iters):
            # occasional restart
            if random.random() < self.restart_prob:
                current = list(self.seed_input)
                best_score = self.boundary_score(current)

            best_candidate = None
            best_candidate_score = -1

            # Generate multiple candidates and pick best boundary one
            for _ in range(self.candidates_per_iter):
                candidate = mutate_float_vector(current, step=self.step)
                candidate = clip_vector(candidate, self.clip[0], self.clip[1])

                score = self.boundary_score(candidate)
                if score > best_candidate_score:
                    best_candidate_score = score
                    best_candidate = candidate

            # Evaluate the best candidate
            result = executor.run_test(best_candidate, mr)

            if (not result["passed"]) or result.get("input_mutated", False):
                return True, result

            # Move towards boundary if improved
            if best_candidate_score >= best_score:
                current = best_candidate
                best_score = best_candidate_score

        return False, best_result
