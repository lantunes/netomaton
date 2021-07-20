import unittest
import netomaton as ntm


class TestCTRBLRule(unittest.TestCase):

    def test_neighbourhood_map_60x60(self):
        rule = ntm.CTRBLRule((60, 60), None)
        neighbourhood_map = rule.neighbourhood_map

        self.assertEqual(3600, len(neighbourhood_map))
        self.assertEqual(neighbourhood_map[0],
                         ntm.VonNeumannNeighbourhood(center=0, left=59, right=1, top=3540, bottom=60))
        self.assertEqual(neighbourhood_map[3599],
                         ntm.VonNeumannNeighbourhood(center=3599, left=3598, right=3540, top=3539, bottom=59))
        self.assertEqual(neighbourhood_map[59],
                         ntm.VonNeumannNeighbourhood(center=59, left=58, right=0, top=3599, bottom=119))
        self.assertEqual(neighbourhood_map[61],
                         ntm.VonNeumannNeighbourhood(center=61, left=60, right=62, top=1, bottom=121))
        self.assertEqual(neighbourhood_map[60],
                         ntm.VonNeumannNeighbourhood(center=60, left=119, right=61, top=0, bottom=120))
        self.assertEqual(neighbourhood_map[119],
                         ntm.VonNeumannNeighbourhood(center=119, left=118, right=60, top=59, bottom=179))

    def test_neighbourhood_map_3x60(self):
        rule = ntm.CTRBLRule((3, 60), None)
        neighbourhood_map = rule.neighbourhood_map

        self.assertEqual(180, len(neighbourhood_map))
        self.assertEqual(neighbourhood_map[0],
                         ntm.VonNeumannNeighbourhood(center=0, left=59, right=1, top=120, bottom=60))
        self.assertEqual(neighbourhood_map[59],
                         ntm.VonNeumannNeighbourhood(center=59, left=58, right=0, top=179, bottom=119))
        self.assertEqual(neighbourhood_map[61],
                         ntm.VonNeumannNeighbourhood(center=61, left=60, right=62, top=1, bottom=121))
        self.assertEqual(neighbourhood_map[60],
                         ntm.VonNeumannNeighbourhood(center=60, left=119, right=61, top=0, bottom=120))
        self.assertEqual(neighbourhood_map[119],
                         ntm.VonNeumannNeighbourhood(center=119, left=118, right=60, top=59, bottom=179))

    def test_neighbourhood_map_60x3(self):
        rule = ntm.CTRBLRule((60, 3), None)
        neighbourhood_map = rule.neighbourhood_map

        self.assertEqual(180, len(neighbourhood_map))
        self.assertEqual(neighbourhood_map[0],
                         ntm.VonNeumannNeighbourhood(center=0, left=2, right=1, top=177, bottom=3))
        self.assertEqual(neighbourhood_map[2],
                         ntm.VonNeumannNeighbourhood(center=2, left=1, right=0, top=179, bottom=5))
        self.assertEqual(neighbourhood_map[3],
                         ntm.VonNeumannNeighbourhood(center=3, left=5, right=4, top=0, bottom=6))
        self.assertEqual(neighbourhood_map[4],
                         ntm.VonNeumannNeighbourhood(center=4, left=3, right=5, top=1, bottom=7))
        self.assertEqual(neighbourhood_map[179],
                         ntm.VonNeumannNeighbourhood(center=179, left=178, right=177, top=176, bottom=2))

