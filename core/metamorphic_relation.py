"""
Author: Shaikh Nahian
Since: Dec 2025
"""
from abc import ABC, abstractmethod

class MetamorphicRelation(ABC):
    """
    Base class for all Metamorphic Relations (MRs).
    """

    @abstractmethod
    def transform(self, source_input):
        """
        Given a source input, produce a follow-up input.
        """
        pass

    @abstractmethod
    def check(self, source_output, follow_up_output) -> bool:
        """
        Check whether the MR holds between outputs.
        """
        pass
