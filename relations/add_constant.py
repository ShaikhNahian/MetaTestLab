"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from core.metamorphic_relation import MetamorphicRelation

class AddConstantMR(MetamorphicRelation):
    """
    Adding a constant to all elements should preserve ordering.
    """

    def __init__(self, constant):
        self.constant = constant

    def transform(self, source_input):
        return [x + self.constant for x in source_input]

    def check(self, source_output, follow_up_output):
        adjusted_source = [x + self.constant for x in source_output]
        return adjusted_source == follow_up_output
