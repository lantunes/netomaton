import unittest

from netomaton import *


class TestActivityRule(unittest.TestCase):

    def test_majority_rule(self):
        actual = ActivityRule.majority_rule([1, 2, 1, 3, 4])
        expected = 1
        self.assertEqual(expected, actual)

        actual = ActivityRule.majority_rule([2, 2, 2, 2, 2])
        expected = 2
        self.assertEqual(expected, actual)

        actual = ActivityRule.majority_rule([3])
        expected = 3
        self.assertEqual(expected, actual)

        actual = ActivityRule.majority_rule([0., 0., 5423.])
        expected = 0.
        self.assertEqual(expected, actual)


