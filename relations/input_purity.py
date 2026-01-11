"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from core.metamorphic_relation import MetamorphicRelation

class InputPurityMR(MetamorphicRelation):
    """
    Metamorphic Relation that checks input purity:
    the SUT must not modify its input.
    """

    def transform(self, source_input):
        # No transformation needed
        return source_input

    def check(self, source_output, follow_up_output):
        # Output is irrelevant for this MR
        return True
