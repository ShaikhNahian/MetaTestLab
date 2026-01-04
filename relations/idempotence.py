from core.metamorphic_relation import MetamorphicRelation

class IdempotenceMR(MetamorphicRelation):
    """
    Sorting twice should give the same result as sorting once.
    """

    def transform(self, source_input):
        return sorted(source_input)

    def check(self, source_output, follow_up_output):
        return source_output == follow_up_output
