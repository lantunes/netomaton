import unittest

import netomaton as ntm


class TestFunctions(unittest.TestCase):

    def test_copy_connectivity_map(self):
        conn_map = {
            1: {
                3: [{
                        "hyperedge": {
                            "label": "1",
                            "index": 2
                        }
                    }]
            },
            2: {
                1: [{
                        "weight": 1.0,
                        "unary": False,
                        "hyperedge": {
                            "label": "1",
                            "index": 0
                        }
                    },
                    {
                        "weight": 1.0,
                    },
                    {
                        "hyperedge": {
                            "label": "1",
                            "index": 3
                        }
                    }]
            },
            3: {
                2: [{
                        "hyperedge": {
                            "label": "1",
                            "index": 1
                        }
                    }],
                4: [{}, {}]
            },
            4: {
                5: [{}]
            },
            5: {}
        }

        conn_map_copy = ntm.copy_connectivity_map(conn_map)

        self.assertEqual(conn_map, conn_map_copy)

        conn_map[3][4][0]["weight"] = 1.0
        self.assertNotEqual(conn_map, conn_map_copy)