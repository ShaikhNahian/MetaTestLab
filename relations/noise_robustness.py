import numpy as np
from core.metamorphic_relation import MetamorphicRelation

class NoiseRobustnessMR(MetamorphicRelation):
    """
    Small Gaussian noise should not change prediction.
    """

    def __init__(self, std=0.01):
        self.std = std

    def transform(self, source_input):
        noise = np.random.normal(0, self.std, size=len(source_input))
        return [x + n for x, n in zip(source_input, noise)]

    def check(self, source_output, follow_up_output):
        return source_output == follow_up_output
