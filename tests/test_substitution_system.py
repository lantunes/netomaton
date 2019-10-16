import netomaton as ntm
from .rule_test import *


class TestSubstitutionSystem(RuleTest):

    def test_substitution_demo1(self):
        expected = self._convert_to_list_of_lists("substitution_system1.ca")
        actual = self._evolve_substitution_system(expected, rules={
            "2": "21",
            "1": "12"
        })
        np.testing.assert_equal(expected, actual)

    def test_substitution_demo2(self):
        expected = self._convert_to_list_of_lists("substitution_system2.ca")
        actual = self._evolve_substitution_system(expected, rules={
            "2": "1",
            "1": "12"
        })
        np.testing.assert_equal(expected, actual)

    def test_substitution_demo3(self):
        expected = self._convert_to_list_of_lists("substitution_system3.ca")
        actual = self._evolve_substitution_system(expected, rules={
            "22": "22",
            "21": "1",
            "12": "21",
            "11": ""
        })
        np.testing.assert_equal(expected, actual)

    def test_substitution_demo4(self):
        expected = self._convert_to_list_of_lists("substitution_system4.ca")
        actual = self._evolve_substitution_system(expected, rules={
            "33": "1",
            "32": "1",
            "31": "3",
            "23": "11",
            "22": "12",
            "21": "22",
            "13": "3",
            "12": "3",
            "11": "1"
        })
        np.testing.assert_equal(expected, actual)

    def test_substitution_demo5(self):
        expected = self._convert_to_list_of_lists("substitution_system5.ca")
        actual = self._evolve_substitution_system(expected, rules={
            "33": "3",
            "32": "12",
            "31": "1",
            "23": "",
            "22": "",
            "21": "3",
            "13": "1",
            "12": "12",
            "11": "3"
        })
        np.testing.assert_equal(expected, actual)


    def test_substitution_demo6(self):
        expected = self._convert_to_list_of_lists("substitution_system6.ca")
        actual = self._evolve_substitution_system(expected, rules={
            "2": "212",
            "1": "121"
        })
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_substitution_system(expected, rules):
        rows = len(expected)
        initial_conditions = np.array(expected[0]).flatten()
        subn_system = ntm.SubstitutionSystem(rules, len(initial_conditions))
        activities, _ = ntm.evolve(initial_conditions, subn_system.adjacency_matrix,
                                   connectivity_rule=subn_system.connectivity_rule,
                                   activity_rule=subn_system.activity_rule, timesteps=rows)
        return activities
