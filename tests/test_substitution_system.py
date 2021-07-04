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

    def test_algae(self):
        system = ntm.SubstitutionSystem(rules={
            "A": "AB",
            "B": "A"
        }, axiom="A")

        trajectory = ntm.evolve(network=system.network,
                                initial_conditions=system.initial_conditions,
                                activity_rule=system.activity_rule, timesteps=8)

        expected = [
            "A",
            "AB",
            "ABA",
            "ABAAB",
            "ABAABABA",
            "ABAABABAABAAB",
            "ABAABABAABAABABAABABA",
            "ABAABABAABAABABAABABAABAABABAABAAB"
        ]
        self.assertEqual(expected, system.to_string(trajectory))

    def test_fractal_tree(self):
        system = ntm.SubstitutionSystem(rules={
            "1": "11",
            "0": "1[0]0"
        }, constants=["[", "]"], axiom="0")

        trajectory = ntm.evolve(network=system.network,
                                initial_conditions=system.initial_conditions,
                                activity_rule=system.activity_rule, timesteps=4)

        expected = [
            "0",
            "1[0]0",
            "11[1[0]0]1[0]0",
            "1111[11[1[0]0]1[0]0]11[1[0]0]1[0]0"
        ]
        self.assertEqual(expected, system.to_string(trajectory))

    def test_koch_curve(self):
        system = ntm.SubstitutionSystem(rules={
            "F": "F+F-F-F+F"
        }, constants=["+", "-"], axiom="F")

        trajectory = ntm.evolve(network=system.network,
                                initial_conditions=system.initial_conditions,
                                activity_rule=system.activity_rule, timesteps=4)

        expected = [
            "F",
            "F+F-F-F+F",
            "F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F",
            "F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F+F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F-F+F-F-"
            "F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F-F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F+F+F-F-F+F+F+"
            "F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F"
        ]
        self.assertEqual(expected, system.to_string(trajectory))

    @staticmethod
    def _evolve_substitution_system(expected, rules):
        rows = len(expected)
        initial_conditions = np.array(expected[0]).flatten()
        system = ntm.SubstitutionSystem(rules=rules, axiom=initial_conditions)
        trajectory = ntm.evolve(initial_conditions=system.initial_conditions, network=system.network,
                                activity_rule=system.activity_rule, timesteps=rows)
        activities = {t: state.activities for t, state in enumerate(trajectory)}
        activities = [[v for e, v in sorted(activities[k].items())] for k in sorted(activities)]
        return activities

