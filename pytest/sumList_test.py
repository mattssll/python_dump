""" An example of a test module in pytest """
from sumList import total

def test_total_empty() -> None:
    assert total([]) == 0.0

def test_total_single_item() -> None:
    assert total([110.0]) == 110.0

def test_total_many_items() -> None:
    """ Total of a list with many items is their sum"""
    assert total([25.0,25.0,25.0,25.0]) == 100.0
    