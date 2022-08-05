""" An example of a test module in pytest """
from joinConcat import joinConcat

def test_join_use_case() -> None:
    assert joinConcat([1,2,3], '-') == '1-2-3'

def test_join_edge_single_item() -> None:
    assert joinConcat([1], '-') == '1'

def test_join_edge_empty_delimiter() -> None:
    """ Total of a list with many items is their sum"""
    assert joinConcat([1,2,3], '') == '123'
    