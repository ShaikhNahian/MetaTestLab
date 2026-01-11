"""
Author: Shaikh Nahian
Since: Dec 2025
"""
import numpy as np
from core.metamorphic_relation import MetamorphicRelation

class NoiseRobustnessMR(MetamorphicRelation):
    """
    Small, controlled noise should not change prediction.
    """

    def __init__(self, std=0.01, seed=42):
        self.std = std
        self.seed = seed

    def transform(self, source_input):
        rng = np.random.default_rng(self.seed)
        noise = rng.normal(0, self.std, size=len(source_input))
        return [x + n for x, n in zip(source_input, noise)]

    def check(self, source_output, follow_up_output):
        return source_output == follow_up_output
