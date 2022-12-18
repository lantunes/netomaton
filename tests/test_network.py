import netomaton as ntm
from .rule_test import *
import networkx as nx
import pytest


class TestNetwork(RuleTest):

    def test_init_empty(self):
        network = ntm.Network()
        self.assertEqual([], list(network.nodes))
        self.assertEqual([], list(network.edges))

    def test_init(self):
        network = ntm.Network(5)

        expected = [0, 1, 2, 3, 4]
        self.assertEqual(expected, list(network.nodes))
        self.assertEqual([], list(network.edges))

    def test_add_node(self):
        network = ntm.Network()
        network.add_node(1, activity=1.0)

        self.assertEqual(1.0, network[1]["activity"])

    def test_nodes(self):
        network = ntm.Network()
        network.add_node(1)
        network.add_node("2", foo="bar")
        network.add_edge(3, 1)
        network.add_edge("2", 4, weight=1.0)

        nodes = []
        for node in network.nodes:
            nodes.append(node)

        expected = [1, "2", 3, 4]
        self.assertEqual(expected, nodes)

    def test_edges(self):
        network = ntm.Network()
        network.add_edge(1, 2, weight=1.0)
        network.add_edge(2, 3, weight=2.0)
        network.add_edge(2, 3, weight=3.0)

        edges = []
        for edge in network.edges:
            edges.append(edge)

        expected = [(1, 2, {"weight": 1.0}), (2, 3, {"weight": 2.0}), (2, 3, {"weight": 3.0})]
        self.assertEqual(expected, edges)

    def test_remove_node(self):
        network = ntm.Network()
        network.add_node(1)
        network.add_edge(2, 1)

        network.remove_node(1)

        self.assertEqual([2], list(network.nodes))
        self.assertEqual([], list(network.edges))

    def test_remove_node_multi(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(1, 2)

        network.remove_node(1)

        self.assertEqual([2], list(network.nodes))
        self.assertEqual([], list(network.edges))
        self.assertEqual(0, network.degree(2))

    def test_remove_node_with_key(self):
        network = ntm.Network()
        network.add_node(1)
        network.add_edge(2, 1)

        del network[1]

        self.assertEqual([2], list(network.nodes))
        self.assertEqual([], list(network.edges))

    def test_remove_node_outgoing(self):
        network = ntm.Network()
        network.add_edge(0, 1)
        network.add_edge(1, 0)

        network.remove_node(0)
        network.remove_node(1)

        self.assertEqual([], list(network.nodes))
        self.assertEqual([], list(network.edges))

    def test_remove_edge(self):
        network = ntm.Network()
        network.add_node(1)
        network.add_edge(2, 1)

        network.remove_edge(2, 1)

        self.assertEqual([], list(network.edges))

    def test_get_node(self):
        network = ntm.Network()
        network.add_node(1, foo="bar")

        self.assertEqual("bar", network[1]["foo"])

    def test_len(self):
        network = ntm.Network()
        network.add_edge(1, 2, weight=1.0)
        network.add_edge(2, 3, weight=2.0)
        network.add_edge(2, 3, weight=3.0)

        self.assertEqual(3, len(network))

    def test_degree(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(2, 3)

        self.assertEqual(1, network.degree(1))
        self.assertEqual(3, network.degree(2))
        self.assertEqual(2, network.degree(3))
        self.assertEqual(1, network.out_degree(1))
        self.assertEqual(0, network.in_degree(1))
        self.assertEqual(2, network.out_degree(2))
        self.assertEqual(1, network.in_degree(2))
        self.assertEqual(0, network.out_degree(3))
        self.assertEqual(2, network.in_degree(3))

    def test_degree_after_removing_nodes(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(2, 3)

        network.remove_node(3)

        self.assertEqual(1, network.degree(1))
        self.assertEqual(1, network.degree(2))
        self.assertEqual(1, network.out_degree(1))
        self.assertEqual(0, network.in_degree(1))
        self.assertEqual(0, network.out_degree(2))
        self.assertEqual(1, network.in_degree(2))

        network.remove_node(1)

        self.assertEqual(0, network.degree(2))
        self.assertEqual(0, network.out_degree(2))
        self.assertEqual(0, network.in_degree(2))

    def test_degree_after_adding_edges(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(2, 3)

        self.assertEqual(1, network.degree(1))
        self.assertEqual(3, network.degree(2))
        self.assertEqual(2, network.degree(3))
        self.assertEqual(1, network.out_degree(1))
        self.assertEqual(0, network.in_degree(1))
        self.assertEqual(2, network.out_degree(2))
        self.assertEqual(1, network.in_degree(2))
        self.assertEqual(0, network.out_degree(3))
        self.assertEqual(2, network.in_degree(3))

        network.add_edge(3, 1)

        self.assertEqual(2, network.degree(1))
        self.assertEqual(3, network.degree(2))
        self.assertEqual(3, network.degree(3))
        self.assertEqual(1, network.out_degree(1))
        self.assertEqual(1, network.in_degree(1))
        self.assertEqual(2, network.out_degree(2))
        self.assertEqual(1, network.in_degree(2))
        self.assertEqual(1, network.out_degree(3))
        self.assertEqual(2, network.in_degree(3))

    def test_degree_after_removing_edges(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(2, 3)

        self.assertEqual(1, network.degree(1))
        self.assertEqual(3, network.degree(2))
        self.assertEqual(2, network.degree(3))
        self.assertEqual(1, network.out_degree(1))
        self.assertEqual(0, network.in_degree(1))
        self.assertEqual(2, network.out_degree(2))
        self.assertEqual(1, network.in_degree(2))
        self.assertEqual(0, network.out_degree(3))
        self.assertEqual(2, network.in_degree(3))

        network.remove_edge(2, 3)

        self.assertEqual(1, network.degree(1))
        self.assertEqual(1, network.degree(2))
        self.assertEqual(0, network.degree(3))
        self.assertEqual(1, network.out_degree(1))
        self.assertEqual(0, network.in_degree(1))
        self.assertEqual(0, network.out_degree(2))
        self.assertEqual(1, network.in_degree(2))
        self.assertEqual(0, network.out_degree(3))
        self.assertEqual(0, network.in_degree(3))

    def test_in_edges(self):
        network = ntm.Network()
        network.add_edge(1, 2, a="b")
        network.add_edge(2, 3)
        network.add_edge(2, 3, foo="bar")

        self.assertEqual({}, network.in_edges(1))
        self.assertEqual({1: [{"a": "b"}]}, network.in_edges(2))
        self.assertEqual({2: [{}, {"foo": "bar"}]}, network.in_edges(3))

    def test_update_edge(self):
        network = ntm.Network()
        network.add_edge(1, 2, a="b")
        network.add_edge(2, 3, val=1)

        network.update_edge(1, 2, weight=1.0)
        network.update_edge(2, 3, val=2)

        expected = [(1, 2, {"a": "b", "weight": 1.0}), (2, 3, {"val": 2})]
        self.assertEqual(expected, list(network.edges))

    def test_update_edge_with_indices(self):
        network = ntm.Network()
        network.add_edge(1, 2, a="b")
        network.add_edge(1, 2)
        network.add_edge(1, 2)

        network.update_edge(1, 2, indices=[1, 2], weight=1.0)

        expected = [(1, 2, {"a": "b"}), (1, 2, {"weight": 1.0}), (1, 2, {"weight": 1.0})]
        self.assertEqual(expected, list(network.edges))

    def test_has_edge(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(2, 3)

        self.assertTrue(network.has_edge(1, 2))
        self.assertTrue(network.has_edge(2, 3))
        self.assertFalse(network.has_edge(3, 2))

    def test_edge(self):
        network = ntm.Network()
        network.add_edge(1, 2, a="b")
        network.add_edge(2, 1)
        network.add_edge(2, 1, weight=1.0)

        self.assertEqual([{"a": "b"}], network.edge(1, 2))
        self.assertEqual([{}, {"weight": 1.0}], network.edge(2, 1))

    def test_equals(self):
        network1 = ntm.Network()
        network1.add_edge(1, 2, a="b")
        network1.add_edge(2, 1)
        network1.add_edge(2, 1, weight=1.0)

        network2 = ntm.Network()
        network2.add_edge(1, 2, a="b")
        network2.add_edge(2, 1)
        network2.add_edge(2, 1)

        self.assertEqual(network1, network1)
        self.assertEqual(network2, network2)
        self.assertNotEqual(network1, network2)

    def test_copy(self):
        network = ntm.Network()
        network.add_edge(1, 2, a="b")
        network.add_edge(2, 1)
        network.add_edge(2, 1, weight=1.0)

        network_copy = network.copy()

        self.assertEqual(network_copy, network)

    def test_to_dict(self):
        network = ntm.Network()
        network.add_edge(1, 2, a="b")
        network.add_edge(2, 1)
        network.add_edge(2, 1, weight=1.0)

        d = network.to_dict()

        expected = {
            1: {'in': 2, 'out': 1, 'incoming': {2: [{}, {'weight': 1.0}]}, 'outgoing': [2]},
            2: {'in': 1, 'out': 2, 'incoming': {1: [{'a': 'b'}]}, 'outgoing': [1, 1]}
        }
        self.assertEqual(expected, d)

    def test_from_networkx(self):
        G = nx.MultiDiGraph()
        G.add_node(1, foo="bar", a="b")
        G.add_node(2)
        G.add_edge(1, 2, weight=1.0)
        G.add_edge(2, 3, weight=2.0)
        G.add_edge(1, 2, weight=3.0)

        network = ntm.Network.from_networkx(G)

        expected = {
            1: {'foo': 'bar', 'a': 'b', 'in': 0, 'out': 2, 'incoming': {}, 'outgoing': [2, 2]},
            2: {'in': 2, 'out': 1, 'incoming': {1: [{'weight': 1.0}, {'weight': 3.0}]}, 'outgoing': [3]},
            3: {'in': 1, 'out': 0, 'incoming': {2: [{'weight': 2.0}]}, 'outgoing': []}
        }
        self.assertEqual(expected, network.to_dict())

    def test_to_networkx(self):
        network = ntm.Network()
        network.add_node(1, foo="bar", a="b")
        network.add_node(2)
        network.add_edge(1, 2, weight=1.0)
        network.add_edge(2, 3, weight=2.0)
        network.add_edge(1, 2, weight=3.0)

        G = network.to_networkx()

        expected = nx.MultiDiGraph()
        expected.add_node(1, foo="bar", a="b")
        expected.add_node(2)
        expected.add_edge(1, 2, weight=1.0)
        expected.add_edge(2, 3, weight=2.0)
        expected.add_edge(1, 2, weight=3.0)

        self._assert_networks_equal(expected, G)

    def test_to_adjacency_matrix(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(1, 2)
        network.add_edge(3, 2)
        network.add_edge(1, 1)

        M = network.to_adjacency_matrix()

        self.assertEqual([
            [1, 2, 0],
            [0, 0, 1],
            [0, 1, 0]
        ], M)

    def test_to_adjacency_matrix_nodelist(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(1, 2)
        network.add_edge(3, 2)
        network.add_edge(1, 1)

        M = network.to_adjacency_matrix(nodelist=[3, 2, 1])

        self.assertEqual([
            [0, 1, 0],
            [1, 0, 0],
            [0, 2, 1],
        ], M)

    def test_to_adjacency_matrix_sum_multiedges(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 3)
        network.add_edge(1, 2)
        network.add_edge(3, 2)
        network.add_edge(1, 1)
        network.add_edge(1, 1)

        M = network.to_adjacency_matrix(sum_multiedges=False)

        self.assertEqual([
            [1, 1, 0],
            [0, 0, 1],
            [0, 1, 0],
        ], M)

    def test_to_adjacency_matrix_weight(self):
        network = ntm.Network()
        network.add_edge(1, 2, weight=2.0)
        network.add_edge(2, 3, weight=2.0)
        network.add_edge(1, 2, weight=2.0)
        network.add_edge(3, 2, weight=2.0)
        network.add_edge(1, 1, weight=2.0)
        network.add_edge(1, 1, weight=2.0)

        M = network.to_adjacency_matrix(sum_multiedges=False)

        self.assertEqual([
            [2.0, 2.0, 0.0],
            [0.0, 0.0, 2.0],
            [0.0, 2.0, 0.0],
        ], M)

    def test_rotation_system(self):
        network = ntm.Network()
        network.add_edge("A", "B")
        network.add_edge("A", "A")
        network.add_edge("B", "A")
        network.add_edge("B", "B")
        network.add_edge("C", "B")
        network.add_edge("B", "C")
        network.add_edge("C", "C")

        try:
            network.rotation_system = {
                "A": ("B", "A"),
                "B": ("A", "B", "C"),
                "C": ("B", "C")
            }
        except Exception as e:
            self.fail("raised Exception unexpectedly: %s" % e.args)

    def test_rotation_system_no_self_connections(self):
        network = ntm.Network()
        network.add_edge("A", "B")
        network.add_edge("B", "A")
        network.add_edge("C", "B")
        network.add_edge("B", "C")

        try:
            network.rotation_system = {
                "A": ("B",),
                "B": ("A", "C"),
                "C": ("C",)
            }
        except Exception as e:
            self.fail("raised Exception unexpectedly: %s" % e.args)

    def test_rotation_system_illegal(self):
        network = ntm.Network()
        network.add_edge("A", "B")
        network.add_edge("B", "A")
        network.add_edge("C", "B")
        network.add_edge("B", "C")

        with pytest.raises(Exception) as e:
            network.rotation_system = {
                "A": ("B", "A"),
                "B": ("A", "B", "C"),
                "C": ("B", "C", "D")
            }
        self.assertEqual(e.value.args, ("the incoming node 'D' is not in the network",))

    def test_add_edge_bidirectional(self):
        network = ntm.Network()
        network.add_edge(1, 2)
        network.add_edge(2, 1)
        network.add_edge(3, 2)
        network.add_edge(2, 3)
        edges = list(network.edges)

        bidir_network = ntm.Network()
        bidir_network.add_edge_bidir(1, 2)
        bidir_network.add_edge_bidir(3, 2)
        bidir_edges = list(bidir_network.edges)

        self.assertEqual(edges, bidir_edges)

    def test_add_edge_bidirectional_with_attrs(self):
        network = ntm.Network()
        network.add_edge(1, 2, foo=1, bar=2)
        network.add_edge(2, 1, foo=1, bar=2)
        network.add_edge(3, 2, foo=3, bar=2)
        network.add_edge(2, 3, foo=3, bar=2)
        edges = list(network.edges)

        bidir_network = ntm.Network()
        bidir_network.add_edge_bidir(1, 2, foo=1, bar=2)
        bidir_network.add_edge_bidir(3, 2, foo=3, bar=2)
        bidir_edges = list(bidir_network.edges)

        self.assertEqual(edges, bidir_edges)
