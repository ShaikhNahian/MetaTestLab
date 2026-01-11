"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from core.metamorphic_relation import MetamorphicRelation

class FeatureScalingMR(MetamorphicRelation):
    """
    Scaling features consistently should preserve prediction.
    """

    def __init__(self, scale=2.0):
        self.scale = scale

    def transform(self, source_input):
        return [x * self.scale for x in source_input]

    def check(self, source_output, follow_up_output):
        # Scaling should not flip prediction arbitrarily
        return source_output == follow_up_output
