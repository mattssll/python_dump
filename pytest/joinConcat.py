""" An example of a Python Module. """
from typing import List

def joinConcat(xs: List[int], delimiter: str) -> float:
    """ Produce a string where subsequent items are separated by delimiter """
    result: str = ''
    for item in xs:
        if result == '':
            result = str(item)
        else:
            result += delimiter + str(item) 
    return result