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

    def test_substitution_demo7(self):
        expected = self._convert_to_list_of_lists("substitution_system7.ca")
        actual = self._evolve_substitution_system(expected, rules={
            "111": "22",
            "112": "121",
            "121": "11",
            "122": "",
            "211": "212",
            "212": "1",
            "221": "22",
            "222": "211",
        })
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_substitution_system(expected, rules):
        rows = len(expected)
        initial_conditions = np.array(expected[0]).flatten()
        subn_system = ntm.SubstitutionSystem(rules, len(initial_conditions))
        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=subn_system.network,
                                activity_rule=subn_system.activity_rule, timesteps=rows)
        activities = {t: state.activities for t, state in enumerate(trajectory)}
        activities = [[v for e, v in sorted(activities[k].items())] for k in sorted(activities)]
        return activities

