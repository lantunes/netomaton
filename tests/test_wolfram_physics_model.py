from netomaton import evolve, WolframPhysicsModel
from .rule_test import *


class TestWolframPhysicsModel(RuleTest):

    def test_init_unary_relation(self):
        config = [(1,)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{"label": "1", "unary": True}]
            }
        }, model.connectivity_map)
        self.assertEqual(1, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_multi_unary_relation(self):
        config = [(1,), (1,)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{"label": "1", "unary": True}, {"label": "2", "unary": True}]
            }
        }, model.connectivity_map)
        self.assertEqual(1, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_binary_relation(self):
        config = [(1, 2)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {},
            2: {
                1: [{"label": "1"}]
            }
        }, model.connectivity_map)
        self.assertEqual(2, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_unary_and_binary_relation(self):
        config = [(1,), (1, 2)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{"label": "1", "unary": True}]
            },
            2: {
                1: [{"label": "2"}]
            }
        }, model.connectivity_map)
        self.assertEqual(2, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_ternary_self_looping_relation(self):
        config = [(1, 1, 1)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }, model.connectivity_map)
        self.assertEqual(1, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_multiple_relations(self):
        config = [(1, 1, 1), (1, 2), (1, 2), (1, 2), (2, 3), (3, 2)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            2: {
                1: [{"label": "2"}, {"label": "3"}, {"label": "4"}],
                3: [{"label": "6"}]
            },
            3: {
                2: [{"label": "5"}]
            }
        }, model.connectivity_map)
        self.assertEqual(3, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_ternary_relation(self):
        config = [(1, 2, 3)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {},
            2: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }]
            },
            3: {
                2: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }, model.connectivity_map)
        self.assertEqual(3, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_large_hyperedge(self):
        config = [(3, 1, 2, 1, 1, 4, 1, 1)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 3
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 6
                    }
                }],
                2: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 2
                    }
                }],
                3: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }],
                4: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 5
                    }
                }]
            },
            2: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            3: {},
            4: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 4
                    }
                }]
            }
        }, model.connectivity_map)
        self.assertEqual(4, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_multiple_ternary_relations(self):
        config = [(1, 1, 1), (1, 2, 3), (3, 4, 4)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            2: {
                1: [{
                    "label": "2",
                    "hyperedge": {
                        "index": 0
                    }
                }]
            },
            3: {
                2: [{
                    "label": "2",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            4: {
                3: [{
                    "label": "3",
                    "hyperedge": {
                        "index": 0
                    }
                }],
                4: [{
                    "label": "3",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }, model.connectivity_map)
        self.assertEqual(4, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_init_multiple_ternary_relations2(self):
        config = [(2, 3, 3), (1, 3, 3), (2, 1, 1)]
        rules = {"in": [("x", "y")], "out": [("x", "y"), ("y", "z")]}
        model = WolframPhysicsModel(config, rules)

        self.assertEqual({
            1: {
                1: [{
                    "label": "3",
                    "hyperedge": {
                        "index": 1
                    }
                }],
                2: [{
                    "label": "3",
                    "hyperedge": {
                        "index": 0
                    }
                }]
            },
            2: {},
            3: {
                1: [{
                    "label": "2",
                    "hyperedge": {
                        "index": 0
                    }
                }],
                2: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }],
                3: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }, {
                    "label": "2",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }, model.connectivity_map)
        self.assertEqual(3, model.last_node)
        self.assertEqual(rules, model.rules)

    def test_connectivity_map_to_config(self):
        config = [(1,)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                1: [{"label": "1", "unary": True}]
            }
        }))

    def test_connectivity_map_to_config2(self):
        config = [(1, 2)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {},
            2: {
                1: [{"label": "1"}]
            }
        }))

    def test_connectivity_map_to_config3(self):
        config = [(1,), (1, 2)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                1: [{"label": "1", "unary": True}]
            },
            2: {
                1: [{"label": "2"}]
            }
        }))

    def test_connectivity_map_to_config4(self):
        config = [(1,), (1,)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                1: [{"label": "1", "unary": True}, {"label": "2", "unary": True}]
            }
        }))

    def test_connectivity_map_to_config5(self):
        config = [(1, 1, 1)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }))

    def test_connectivity_map_to_config6(self):
        config = [(1, 1, 1), (1, 2), (1, 2), (1, 2), (3, 2), (2, 3)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            2: {
                1: [{"label": "2"}, {"label": "3"}, {"label": "4"}],
                3: [{"label": "5"}]
            },
            3: {
                2: [{"label": "6"}]
            }
        }))

    def test_connectivity_map_to_config7(self):
        config = [(1, 2, 3)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {},
            2: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }]
            },
            3: {
                2: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }))

    def test_connectivity_map_to_config8(self):
        config = [(3, 1, 4, 2)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                3: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }]
            },
            2: {
                4: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 2
                    }
                }]
            },
            3: {},
            4: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }))

    def test_connectivity_map_to_config9(self):
        config = [(3, 1, 2, 1, 1, 4, 1, 1)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 3
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 6
                    }
                }],
                2: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 2
                    }
                }],
                3: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }],
                4: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 5
                    }
                }]
            },
            2: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            3: {},
            4: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 4
                    }
                }]
            }
        }))

    def test_connectivity_map_to_config10(self):
        config = [(1, 1, 1), (1, 2, 3), (3, 4, 4)]
        self.assertEqual(config, WolframPhysicsModel.connectivity_map_to_config({
            1: {
                1: [{
                    "label": "1",
                    "hyperedge": {
                        "index": 0
                    }
                }, {
                    "label": "1",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            2: {
                1: [{
                    "label": "2",
                    "hyperedge": {
                        "index": 0
                    }
                }]
            },
            3: {
                2: [{
                    "label": "2",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            },
            4: {
                3: [{
                    "label": "3",
                    "hyperedge": {
                        "index": 0
                    }
                }],
                4: [{
                    "label": "3",
                    "hyperedge": {
                        "index": 1
                    }
                }]
            }
        }))

    def test_config_interconversion(self):
        expected = [(1, 1, 3), (1, 3, 2), (1, 2, 4), (2, 4, 1)]
        connectivity_map = WolframPhysicsModel(expected, {}).connectivity_map
        actual = WolframPhysicsModel.connectivity_map_to_config(connectivity_map)
        self.assertEqual(actual, expected)

    def test_config_interconversion2(self):
        expected = [(4, 2), (2, 3), (5, 1), (1, 2)]
        connectivity_map = WolframPhysicsModel(expected, {}).connectivity_map
        actual = WolframPhysicsModel.connectivity_map_to_config(connectivity_map)
        self.assertEqual(actual, expected)

    def test_config_interconversion3(self):
        expected = [(1, 1, 1), (1, 2), (1, 2), (1, 2), (2, 3), (3, 2)]
        connectivity_map = WolframPhysicsModel(expected, {}).connectivity_map
        actual = WolframPhysicsModel.connectivity_map_to_config(connectivity_map)
        self.assertEqual(actual, expected)

    def test_wm148(self):
        rules = {
            "in": [("x", "y")], "out": [("x", "y"), ("y", "z")]
        }
        config = [(1, 2)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 2)],
            [(1, 2), (2, 3)],
            [(1, 2), (2, 4), (2, 3), (3, 5)],
            [(1, 2), (2, 6), (2, 4), (4, 7), (2, 3), (3, 8), (3, 5), (5, 9)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm192(self):
        rules = {
            "in": [("x", "y")], "out": [("z", "y"), ("y", "x")]
        }
        config = [(1, 2)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 2)],
            [(3, 2), (2, 1)],
            [(4, 2), (2, 3), (5, 1), (1, 2)],
            [(6, 2), (2, 4), (7, 3), (3, 2), (8, 1), (1, 5), (9, 2), (2, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm686(self):
        rules = {
            "in": [("x", "y")], "out": [("y", "z"), ("z", "x")]
        }
        config = [(1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1)],
            [(1, 2), (2, 1)],
            [(2, 3), (3, 1), (1, 4), (4, 2)],
            [(3, 5), (5, 2), (1, 6), (6, 3), (4, 7), (7, 1), (2, 8), (8, 4)],
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm4768(self):
        rules = {
            "in": [("x", "x")], "out": [("y", "y"), ("y", "y"), ("x", "y")]
        }
        config = [(1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1)],
            [(2, 2), (2, 2), (1, 2)],
            [(1, 2), (3, 3), (3, 3), (2, 3), (4, 4), (4, 4), (2, 4)],
            [(1, 2), (2, 3), (2, 4), (5, 5), (5, 5), (3, 5), (6, 6), (6, 6),
             (3, 6), (7, 7), (7, 7), (4, 7), (8, 8), (8, 8), (4, 8)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm37684(self):
        rules = {
            "in": [("x", "y")], "out": [("x", "z"), ("x", "z"), ("y", "z")]
        }
        config = [(1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1)],
            [(1, 2), (1, 2), (1, 2)],
            [(1, 3), (1, 3), (2, 3), (1, 4), (1, 4), (2, 4), (1, 5), (1, 5), (2, 5)],
            [(1, 6), (1, 6), (3, 6),  (1, 7), (1, 7), (3, 7),  (2, 8), (2, 8), (3, 8),
             (1, 9), (1, 9), (4, 9),  (1, 10), (1, 10), (4, 10),  (2, 11), (2, 11), (4, 11),
             (1, 12), (1, 12), (5, 12),  (1, 13), (1, 13), (5, 13),  (2, 14), (2, 14), (5, 14)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm2736(self):
        rules = {
            "in": [("x", "y")], "out": [("x", "z"), ("z", "w"), ("y", "z")]
        }
        config = [(1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1)],
            [(1, 2), (2, 3), (1, 2)],
            [(1, 4), (4, 5), (2, 4), (2, 6), (6, 7), (3, 6), (1, 8), (8, 9), (2, 8)],
            [(1, 10), (10, 11), (4, 10), (4, 12), (12, 13), (5, 12), (2, 14), (14, 15), (4, 14),
             (2, 16), (16, 17), (6, 16), (6, 18), (18, 19), (7, 18), (3, 20), (20, 21), (6, 20),
             (1, 22), (22, 23), (8, 22), (8, 24), (24, 25), (9, 24), (2, 26), (26, 27), (8, 26)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1295(self):
        rules = {
            "in": [("x", "y", "z")], "out": [("x", "y", "w"), ("y", "w", "z")]
        }
        config = [(1, 1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1, 1)],
            [(1, 1, 2), (1, 2, 1)],
            [(1, 1, 3), (1, 3, 2), (1, 2, 4), (2, 4, 1)],
            [(1, 1, 5), (1, 5, 3), (1, 3, 6), (3, 6, 2), (1, 2, 7), (2, 7, 4), (2, 4, 8), (4, 8, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1137(self):
        rules = {
            "in": [("x", "x", "y")], "out": [("y", "y", "y"), ("y", "x", "y"), ("x", "y", "w"), ("w", "w", "x")]
        }
        config = [(1, 1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1, 1)],
            [(1, 1, 1), (1, 1, 1), (1, 1, 2), (2, 2, 1)],
            [(1, 1, 1), (1, 1, 1), (1, 1, 3), (3, 3, 1), (1, 1, 1), (1, 1, 1), (1, 1, 4), (4, 4, 1),
             (2, 2, 2), (2, 1, 2), (1, 2, 5), (5, 5, 1), (1, 1, 1), (1, 2, 1), (2, 1, 6), (6, 6, 2)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1194(self):
        rules = {
            "in": [("x", "x", "y")], "out": [("w", "w", "x"), ("y", "x", "x")]
        }
        config = [(1, 1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1, 1)],
            [(2, 2, 1), (1, 1, 1)],
            [(3, 3, 2), (1, 2, 2), (4, 4, 1), (1, 1, 1)],
            [(5, 5, 3), (2, 3, 3), (1, 2, 2), (6, 6, 4), (1, 4, 4), (7, 7, 1), (1, 1, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm2487(self):
        rules = {
            "in": [("x", "x", "x")], "out": [("w", "w", "w"), ("w", "w", "x")]
        }
        config = [(1, 1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1, 1)],
            [(2, 2, 2), (2, 2, 1)],
            [(3, 3, 3), (3, 3, 2), (2, 2, 1)],
            [(4, 4, 4), (4, 4, 3), (3, 3, 2), (2, 2, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1888(self):
        rules = {
            "in": [("x", "y", "y")], "out": [("w", "z", "z"), ("x", "z", "z"), ("w", "x", "y")]
        }
        config = [(1, 1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1, 1)],
            [(2, 3, 3), (1, 3, 3), (2, 1, 1)],
            [(4, 5, 5), (2, 5, 5), (4, 2, 3),  (6, 7, 7), (1, 7, 7,), (6, 1, 3),  (8, 9, 9), (2, 9, 9), (8, 2, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1527(self):
        rules = {
            "in": [("x", "y", "x")], "out": [("w", "z", "w"), ("z", "y", "y"), ("x", "z", "y"), ("u", "z", "u")]
        }
        config = [(1, 1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1, 1)],
            [(2, 3, 2), (3, 1, 1), (1, 3, 1), (4, 3, 4)],
            [(5, 6, 5), (6, 3, 3), (2, 6, 3), (7, 6, 7), (3, 1, 1), (8, 9, 8), (9, 3, 3), (1, 9, 3), (10, 9, 10),
             (11, 12, 11), (12, 3, 3), (4, 12, 3), (13, 12, 13)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm225(self):
        rules = {
            "in": [("x",)], "out": [("x", "y"), ("y",), ("y",)]
        }
        config = [(1,)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1,)],
            [(1, 2), (2,), (2,)],
            [(1, 2), (2, 3), (3,), (3,), (2, 4), (4,), (4,)],
            [(1, 2), (2, 3), (3, 5), (5,), (5,), (3, 6), (6,), (6,), (2, 4), (4, 7), (7,), (7,), (4, 8), (8,), (8,)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm6655(self):
        rules = {
            "in": [("x", "y"), ("x", "z")], "out": [("x", "y"), ("x", "w"), ("y", "w"), ("z", "w")]
        }
        config = [(1, 1), (1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1), (1, 1)],
            [(1, 1), (1, 2), (1, 2), (1, 2)],
            [(1, 1), (1, 3), (1, 3), (2, 3), (1, 2), (1, 4), (2, 4), (2, 4)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1483(self):
        rules = {
            "in": [(1, 1, 2), (3, 2, 4)], "out": [(4, 4, 1), (1, 5, 1), (5, 2, 3)]
        }
        config = [(1, 1, 1), (1, 1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1, 1), (1, 1, 1)],
            [(1, 1, 1), (1, 2, 1), (2, 1, 1)],
            [(1, 1, 1), (1, 3, 1), (3, 1, 2), (1, 2, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1157(self):
        rules = {
            "in": [(1, 2), (1, 3), (1, 4)], "out": [(1, 1), (5, 1), (5, 2), (3, 5), (4, 3)]
        }
        config = [(1, 1), (1, 1), (1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1), (1, 1), (1, 1)],
            [(1, 1), (2, 1), (2, 1), (1, 2), (1, 1)],
            [(1, 1), (3, 1), (3, 1), (2, 3), (1, 2), (2, 1), (2, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1743(self):
        rules = {
            "in": [(1, 2, 3), (4, 1)], "out": [(1, 4, 5), (6, 5, 3), (5, 2), (6, 1)]
        }
        config = [(1, 1, 1), (1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1, 1), (1, 1)],
            [(1, 1, 2), (3, 2, 1), (2, 1), (3, 1)],
            [(1, 2, 4), (5, 4, 2), (4, 1), (5, 1), (3, 2, 1), (3, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm1653(self):
        rules = {
            "in": [("x", "y")], "out": [("w", "y", "x"), ("x", "w"), ("w", "y")]
        }
        config = [(1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1, 1)],
            [(2, 1, 1), (1, 2), (2, 1)],
            [(2, 1, 1), (3, 2, 1), (1, 3), (3, 2), (4, 1, 2), (2, 4), (4, 1)],
            [(2, 1, 1), (3, 2, 1), (4, 1, 2), (5, 3, 1), (1, 5), (5, 3),  (6, 2, 3), (3, 6), (6, 2),  (7, 4, 2), (2, 7),
             (7, 4),  (8, 1, 4), (4, 8), (8, 1)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm161(self):
        rules = {
            "in": [("x",)], "out": [("x", "y"), ("x",)]
        }
        config = [(1,)]
        actual = self._evolve_wolfram_physics_model(config, rules, 4)
        expected = [
            [(1,)],
            [(1, 2), (1,)],
            [(1, 2), (1, 3), (1,)],
            [(1, 2), (1, 3), (1, 4), (1,)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    def test_wm17494(self):
        rules = {
            "in": [(1, 2, 3), (1, 4, 5), (3, 6)],
            "out": [(7, 8, 7), (7, 5, 6), (9, 5, 5), (1, 7, 4), (7, 5), (5, 10), (11, 6), (6, 9)]
        }
        config = [(1, 1, 1), (1, 1, 1), (1, 1)]
        actual = self._evolve_wolfram_physics_model(config, rules, 3)
        expected = [
            [(1, 1, 1), (1, 1, 1), (1, 1)],
            [(2, 3, 2), (2, 1, 1), (4, 1, 1), (1, 2, 1), (2, 1), (1, 5), (6, 1), (1, 4)],
            [(4, 1, 1), (1, 2, 1), (1, 5), (6, 1), (1, 4),
             (7, 8, 7), (7, 1, 1), (9, 1, 1), (2, 7, 1), (7, 1), (1, 10), (11, 1), (1, 9)]
        ]
        self._assert_configurations_over_time_equal(actual, expected)

    @staticmethod
    def _evolve_wolfram_physics_model(config, rules, timesteps):
        model = WolframPhysicsModel(config, rules)
        _, connectivities = evolve(topology=model.connectivity_map, connectivity_rule=model.connectivity_rule,
                                   timesteps=timesteps)
        return model.to_configurations(connectivities)

    @staticmethod
    def _assert_configurations_over_time_equal(actual, expected):
        assert len(actual) == len(expected), \
            "expected {%s} is not equal to actual {%s}: different number of timesteps" % (expected, actual)
        for expected_config, actual_config in zip(expected, actual):
            # check that the number of elements are the same
            assert len(actual_config) == len(expected_config), \
                "expected config {%s} is not equal to actual config {%s}: different number of elements" % (expected_config, actual_config)

            # create dictionaries of element counts for each config, and check that they are equal
            expected_counts = {}
            for relation in expected_config:
                if relation not in expected_counts:
                    expected_counts[relation] = 0
                expected_counts[relation] += 1

            actual_counts = {}
            for relation in actual_config:
                if relation not in actual_counts:
                    actual_counts[relation] = 0
                actual_counts[relation] += 1

            assert actual_counts == expected_counts, \
                "expected config {%s} is not equal to actual config {%s}: different elements" % (expected_config, actual_config)