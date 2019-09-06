import netomaton as ntm
from .rule_test import *


class TestAnalysis(RuleTest):

    def test_shannon_entropy(self):
        entropy = ntm.shannon_entropy('1111111')
        self.assertEqual(entropy, 0)
        entropy = ntm.shannon_entropy('0000000')
        self.assertEqual(entropy, 0)
        entropy = ntm.shannon_entropy('01010101')
        self.assertEqual(entropy, 1.0)
        entropy = ntm.shannon_entropy('00010001')
        np.testing.assert_almost_equal(entropy, 0.8113, decimal=4)
        entropy = ntm.shannon_entropy('1234')
        self.assertEqual(entropy, 2.0)

    def test_average_cell_entropy_simple(self):
        activities = [[1, 0, 1],
                      [1, 1, 1],
                      [0, 0, 0],
                      [1, 0, 0]]
        # 0.81128 + 0.81128 + 1.0 = 2.62256; 2.62256/3 = 0.874186666666667
        avg_cell_entropy = ntm.average_cell_entropy(activities)
        np.testing.assert_almost_equal(avg_cell_entropy, 0.8742, decimal=4)

    def test_average_cell_entropy(self):
        activities = self._convert_to_matrix("rule30_random_init.ca")
        avg_cell_entropy = ntm.average_cell_entropy(activities.tolist())
        np.testing.assert_almost_equal(avg_cell_entropy, 0.9946, decimal=4)

    def test_joint_shannon_entropy(self):
        joint_entropy = ntm.joint_shannon_entropy('0010101', '3232223')
        np.testing.assert_almost_equal(joint_entropy, 1.842, decimal=3)

    def test_mutual_information(self):
        mutual_information = ntm.mutual_information('0010101', '3232223')
        np.testing.assert_almost_equal(mutual_information, 0.1281, decimal=4)
        mutual_information = ntm.mutual_information('0010101', '1101010')
        np.testing.assert_almost_equal(mutual_information, 0.9852, decimal=4)
        mutual_information = ntm.mutual_information('0010101', '0010101')
        np.testing.assert_almost_equal(mutual_information, 0.9852, decimal=4)
        mutual_information = ntm.mutual_information('0010101', '0001001')
        np.testing.assert_almost_equal(mutual_information, 0.0060, decimal=4)

    def test_average_mutual_information(self):
        cellular_automaton = self._convert_to_matrix("rule30_random_init.ca").tolist()
        avg_mutual_information = ntm.average_mutual_information(cellular_automaton)
        np.testing.assert_almost_equal(avg_mutual_information, 0.0047, decimal=4)
        avg_mutual_information = ntm.average_mutual_information(cellular_automaton, temporal_distance=2)
        np.testing.assert_almost_equal(avg_mutual_information, 0.0050, decimal=4)
        avg_mutual_information = ntm.average_mutual_information(cellular_automaton, temporal_distance=3)
        np.testing.assert_almost_equal(avg_mutual_information, 0.0051, decimal=4)
