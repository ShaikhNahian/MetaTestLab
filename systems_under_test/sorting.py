"""
Author: Shaikh Nahian
Since: Dec 2025
"""
def sort_numbers(numbers):
    """
    Simple sorting function (SUT).
    """
    return sorted(numbers)

def buggy_sort(numbers):
    """
    BUGGY sorting implementation.
    """
    numbers.sort()   # in-place
    return numbers

