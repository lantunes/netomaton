import unittest
import pytest
import netomaton as ntm


class TestCTRBLRule(unittest.TestCase):

    def test_neighbourhood_map_60x60(self):
        rule = ntm.CTRBLRule((60, 60), {})
        n_map = rule.neighbourhood_map

        self.assertEqual(3600, len(n_map))
        self.assertEqual(n_map[0], ntm.VonNeumannNeighbourhood(center=0, left=59, right=1, top=3540, bottom=60))
        self.assertEqual(n_map[3599], ntm.VonNeumannNeighbourhood(center=3599, left=3598, right=3540, top=3539, bottom=59))
        self.assertEqual(n_map[59], ntm.VonNeumannNeighbourhood(center=59, left=58, right=0, top=3599, bottom=119))
        self.assertEqual(n_map[61], ntm.VonNeumannNeighbourhood(center=61, left=60, right=62, top=1, bottom=121))
        self.assertEqual(n_map[60], ntm.VonNeumannNeighbourhood(center=60, left=119, right=61, top=0, bottom=120))
        self.assertEqual(n_map[119], ntm.VonNeumannNeighbourhood(center=119, left=118, right=60, top=59, bottom=179))

    def test_neighbourhood_map_3x60(self):
        rule = ntm.CTRBLRule((3, 60), {})
        n_map = rule.neighbourhood_map

        self.assertEqual(180, len(n_map))
        self.assertEqual(n_map[0], ntm.VonNeumannNeighbourhood(center=0, left=59, right=1, top=120, bottom=60))
        self.assertEqual(n_map[59], ntm.VonNeumannNeighbourhood(center=59, left=58, right=0, top=179, bottom=119))
        self.assertEqual(n_map[61], ntm.VonNeumannNeighbourhood(center=61, left=60, right=62, top=1, bottom=121))
        self.assertEqual(n_map[60], ntm.VonNeumannNeighbourhood(center=60, left=119, right=61, top=0, bottom=120))
        self.assertEqual(n_map[119], ntm.VonNeumannNeighbourhood(center=119, left=118, right=60, top=59, bottom=179))

    def test_neighbourhood_map_60x3(self):
        rule = ntm.CTRBLRule((60, 3), {})
        n_map = rule.neighbourhood_map

        self.assertEqual(180, len(n_map))
        self.assertEqual(n_map[0], ntm.VonNeumannNeighbourhood(center=0, left=2, right=1, top=177, bottom=3))
        self.assertEqual(n_map[2], ntm.VonNeumannNeighbourhood(center=2, left=1, right=0, top=179, bottom=5))
        self.assertEqual(n_map[3], ntm.VonNeumannNeighbourhood(center=3, left=5, right=4, top=0, bottom=6))
        self.assertEqual(n_map[4], ntm.VonNeumannNeighbourhood(center=4, left=3, right=5, top=1, bottom=7))
        self.assertEqual(n_map[179], ntm.VonNeumannNeighbourhood(center=179, left=178, right=177, top=176, bottom=2))

    def test_rotations(self):
        rule = ntm.CTRBLRule((3, 3), {
            (0, 1, 2, 3, 4): "a",
            (5, 6, 7, 8, 9): "b"
        })
        self.assertEqual(rule.rule_table, {
            (0, 1, 2, 3, 4): "a",
            (5, 6, 7, 8, 9): "b"
        })

        rule = ntm.CTRBLRule((3, 3), {
            (0, 1, 2, 3, 4): "a",
            (5, 6, 7, 8, 9): "b"
        }, add_rotations=True)
        self.assertEqual(rule.rule_table, {
            (0, 1, 2, 3, 4): "a",
            (0, 4, 1, 2, 3): "a",
            (0, 3, 4, 1, 2): "a",
            (0, 2, 3, 4, 1): "a",
            (5, 6, 7, 8, 9): "b",
            (5, 9, 6, 7, 8): "b",
            (5, 8, 9, 6, 7): "b",
            (5, 7, 8, 9, 6): "b"
        })

    def test_activity_rule(self):
        rule = ntm.CTRBLRule((3, 3), {
            (0, 1, 2, 3, 4): "a",
            (5, 6, 7, 8, 9): "b"
        })

        activity = rule.activity_rule(ntm.NodeContext(node_label=4, timestep=1,
                                                      activities={
                                                          0: 0, 1: 1, 2: 0, 3: 4, 4: 0, 5: 2, 6: 0, 7: 3, 8: 0
                                                      }, neighbour_labels=[4, 1, 5, 7, 3],
                                                      neighbourhood_activities=[0, 1, 2, 3, 4],
                                                      connection_states={}, current_activity=0,
                                                      past_activities=None, input=None))
        self.assertEqual("a", activity)

    def test_activity_rule_does_not_exist(self):
        rule = ntm.CTRBLRule((3, 3), {
            (5, 6, 7, 8, 9): "b"
        })

        with pytest.raises(Exception) as e:
            rule.activity_rule(ntm.NodeContext(node_label=4, timestep=1,
                                               activities={
                                                   0: 0, 1: 1, 2: 0, 3: 4, 4: 0, 5: 2, 6: 0, 7: 3, 8: 0
                                               }, neighbour_labels=[4, 1, 5, 7, 3],
                                               neighbourhood_activities=[0, 1, 2, 3, 4],
                                               connection_states={}, current_activity=0,
                                               past_activities=None, input=None))
        self.assertEqual(e.value.args, ("neighbourhood state (0, 1, 2, 3, 4) not in rule table",))
