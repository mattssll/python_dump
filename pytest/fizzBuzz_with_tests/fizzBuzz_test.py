import unittest
from fizzBuzz import fizzbuzz


class TestFizzBuzz(unittest.TestCase):
    def test_fizz(self: unittest.TestCase) -> None:
        for i in [3, 6, 9, 18]:
            print('testing', i)
            assert fizzbuzz(i) == 'Fizz'

    def test_buzz(self: unittest.TestCase) -> None:
        for i in [5, 10, 50]:
            print('testing', i)
            assert fizzbuzz(i) == 'Buzz'

    def test_fizzbuzz(self: unittest.TestCase) -> None:
        for i in [15, 30, 75]:
            print('testing', i)
            assert fizzbuzz(i) == 'FizzBuzz'

    def test_number(self: unittest.TestCase) -> None:
        for i in [2, 4, 88]:
            print('testing', i)
            assert fizzbuzz(i) == i