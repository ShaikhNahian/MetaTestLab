"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from core.metamorphic_relation import MetamorphicRelation

class FeaturePerturbationMR(MetamorphicRelation):
    """
    Large change to one feature should change the model prediction.
    """

    def __init__(self, feature_index=0, delta=5.0):
        self.feature_index = feature_index
        self.delta = delta

    def transform(self, source_input):
        follow_up = list(source_input)
        follow_up[self.feature_index] += self.delta
        return follow_up

    def check(self, source_output, follow_up_output):
        # Change-sensitive: output MUST change
        return source_output != follow_up_output
