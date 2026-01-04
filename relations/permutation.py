import random
from core.metamorphic_relation import MetamorphicRelation

class PermutationMR(MetamorphicRelation):
    """
    Permuting the input list should not change sorted output.
    """

    def transform(self, source_input):
        random.shuffle(source_input)
        return source_input

    def check(self, source_output, follow_up_output):
        return source_output == follow_up_output
