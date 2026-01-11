"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from core.metamorphic_relation import MetamorphicRelation

class ValuePerturbationMR(MetamorphicRelation):
    """
    Changing one element significantly should change the output.
    This is a change-sensitive metamorphic relation.
    """

    def __init__(self, index=0, delta=1000):
        self.index = index
        self.delta = delta

    def transform(self, source_input):
        source_input[self.index] += self.delta
        return source_input

    def check(self, source_output, follow_up_output):
        # Output MUST change
        return source_output != follow_up_output
