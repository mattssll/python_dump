""" An example of a Python Module. """
from typing import List

def total(xs: List[float]) -> float:
    """ Total returns the sum of 'xs'"""
    result: float = 0.0
    for x in xs:
        result += x
    return result

