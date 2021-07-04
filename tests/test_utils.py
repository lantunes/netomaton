import netomaton as ntm
import numpy as np
from .rule_test import *


class TestUtils(RuleTest):

    def test_binarize_for_plotting(self):
        activities = [[2], [35], [12]]

        np.testing.assert_equal([[0, 0, 0, 0, 1, 0],
                                 [1, 0, 0, 0, 1, 1],
                                 [0, 0, 1, 1, 0, 0]], ntm.binarize_for_plotting(activities))
