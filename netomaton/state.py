import msgpack
import gc
import networkx as nx


class Network:
    __slots__ = ("_network", "_rotation_system")

    def __init__(self, n=0):
        """
        Constructs a fully disconnected Network with n nodes.

        :param n: the number of nodes
        """
        self._network = {i: self._new_node() for i in range(n)}
        self._rotation_system = None

    def add_edge(self, i, j, **attr):
        """
        Add an edge from i to j. If i and j do not exist, create them.
        An additional edge will be added if an edge from i to j already exists.

        :param i:

        :param j:

        :param attr:

        :return:
        """
        self._init_node(i)
        self._init_node(j)
        if i not in self._network[j]["incoming"]:
            self._network[j]["incoming"][i] = []
        self._network[j]["incoming"][i].append(attr)
        self._increment_in_degree(j)
        self._increment_out_degree(i)
        self._add_outgoing(i, j)

    def add_edge_bidir(self, i, j, **attr):
        """
        Adds two edges: one from i to j, and one from j to i. The edge attributes (if any
        are provided) will be identical for both edges.

        :param i:

        :param j:

        :param attr:

        :return:
        """
        self.add_edge(i, j, **attr)
        self.add_edge(j, i, **attr)

    def add_node(self, node_label, **attr):
        """
        Add a node. If the node already exists

        :param node_label:

        :param attr:

        :return:
        """
        self._init_node(node_label)
        self._network[node_label].update(attr)

    def update_edge(self, i, j, indices=None, **attr):
        if j not in self._network or i not in self._network[j]["incoming"]:
            raise Exception("edge does not exist")
        if indices is None:
            # update all edges in this connection
            for edge in self._network[j]["incoming"][i]:
                edge.update(attr)
        else:
            for k in indices:
                self._network[j]["incoming"][i][k].update(attr)

    def remove_node(self, node_label):
        for i, v in self._network[node_label]["incoming"].items():
            self._decrement_out_degree(i, n=len(v))
            self._remove_outgoing(i, node_label)
        for j in self._network[node_label]["outgoing"]:
            self._decrement_in_degree(j)
            self._remove_incoming(node_label, j)
        del self._network[node_label]

    def remove_edge(self, i, j):
        """
        Removes all instances of an edge from i to j.

        :param i: the originating node of the edge

        :param j: the target destination node of the edge
        """
        n = len(self._network[j]["incoming"][i])
        self._remove_outgoing(i, j)
        self._decrement_out_degree(i, n=n)
        self._decrement_in_degree(j, n=n)
        self._remove_incoming(i, j)

    @property
    def rotation_system(self):
        return self._rotation_system

    @rotation_system.setter
    def rotation_system(self, rotation_system):
        """
        A rotation system specifies an ordering of the nodes connected to any given node. For example, consider the
        network A<->B<->C, where node A is connected to node B, and node B is connected to node C, and each node is
        connected to itself. A rotation system for this network could be: {A: (A, B), B: (A, B, C), C: (B, C)}. Another
        valid rotation system for this network would be: {A: (B, A), B: (C, B, A), C: (C, B)}.

        :param rotation_system: a dictionary mapping each node (as its label) to a sequence of its incident nodes (the
                                labels of the nodes that are connected to it) and the node itself
        """
        # validate that the rotation system is comprised of nodes in the network
        network_nodes = self.nodes
        for node_label in rotation_system:
            assert node_label in network_nodes, "the node '%s' is not in the network" % node_label
            incoming_nodes = rotation_system[node_label]
            for incoming_node in incoming_nodes:
                assert incoming_node in network_nodes, "the incoming node '%s' is not in the network" % incoming_node
        self._rotation_system = rotation_system

    def in_edges(self, node_label):
        return self._network[node_label]["incoming"]

    def edge(self, i, j):
        return self._network[j]["incoming"][i]

    def to_dict(self):
        return self._network

    @property
    def nodes(self):
        return self._network.keys()

    @property
    def edges(self):
        for j, v in self._network.items():
            for i in v["incoming"]:
                for k in v["incoming"][i]:
                    yield i, j, k

    def has_edge(self, i, j):
        return j in self._network and i in self._network[j]["incoming"]

    def degree(self, node_label):
        return self._network[node_label]["out"] + self._network[node_label]["in"]

    def in_degree(self, node_label):
        return self._network[node_label]["in"]

    def out_degree(self, node_label):
        return self._network[node_label]["out"]

    def copy(self):
        return self.decompress(self.compress())

    def compress(self):
        """
        Compresses the Network into a binary format.

        :return: packed bytes
        """
        return _Compressor.compress(self._network)

    @staticmethod
    def decompress(packed):
        """
        Decompresses a compressed Network.

        :param packed: packed bytes

        :return: a Network
        """
        n = Network()
        n._network = _Compressor.decompress(packed)
        return n

    @staticmethod
    def from_networkx(G):
        """
        Creates a Network from the given NetworkX graph.

        :param G: a NetworkX graph

        :return: a Network
        """
        network = Network()
        for node in G.nodes(data=True):
            network.add_node(node[0], **node[1])
        for edge in G.edges(data=True):
            network.add_edge(edge[0], edge[1], **edge[2])
        return network

    def to_networkx(self):
        """
        Returns this Network as a NetworkX MultiDiGraph.

        :return: a NetworkX MultiDiGraph
        """
        G = nx.MultiDiGraph()
        for node in self.nodes:
            atts = {}
            for key in self._network[node]:
                if key not in self._new_node():
                    atts[key] = self._network[node][key]
            G.add_node(node, **atts)
        for i, j, data in self.edges:
            G.add_edge(i, j, **data)
        return G

    def to_adjacency_matrix(self, nodelist=None, sum_multiedges=True, weight="weight"):
        """
        Returns this Network as an adjacency matrix. A connection is represented by a int greater than zero, and zero
        means no connection is present.

        :param nodelist: defines the node order in the adjacency matrix; if no nodelist is provided, then the order
                         is determined by Network.nodes. (default is None)

        :param sum_multiedges : whether the presence of a connection should be indicated by summing the number of
                                edges in the connection (default is True)

        :param weight : a string or None indicating which edge attribute contains the edge weight. If an edge does
                        not contain the attribute, then 1 is used. (default is 'weight')

        :return: an adjacency matrix representing this Network
        """
        num_nodes = len(self._network)
        M = [[0]*num_nodes for _ in range(num_nodes)]
        if not nodelist:
            nodelist = list(self.nodes)
        for n1, n2, atts in self.edges:
            w = atts[weight] if weight in atts else 1
            i = nodelist.index(n1)
            j = nodelist.index(n2)
            if sum_multiedges:
                M[i][j] += w
            else:
                M[i][j] = w
        return M

    def _init_node(self, node_label):
        if node_label not in self._network:
            self._network[node_label] = self._new_node()

    def _new_node(self):
        return {"in": 0, "out": 0, "incoming": {}, "outgoing": []}

    def _increment_out_degree(self, node_label, n=1):
        self._network[node_label]["out"] += n

    def _decrement_out_degree(self, node_label, n=1):
        self._network[node_label]["out"] -= n

    def _increment_in_degree(self, node_label, n=1):
        self._network[node_label]["in"] += n

    def _decrement_in_degree(self, node_label, n=1):
        self._network[node_label]["in"] -= n

    def _add_outgoing(self, i, j):
        self._network[i]["outgoing"].append(j)

    def _remove_outgoing(self, i, j):
        self._network[i]["outgoing"] = [x for x in self._network[i]["outgoing"] if x != j]

    def _remove_incoming(self, i, j):
        if i in self._network[j]["incoming"]:
            del self._network[j]["incoming"][i]

    def __getitem__(self, item):
        return self._network[item]

    def __delitem__(self, key):
        self.remove_node(key)

    def __len__(self):
        return len(self._network)

    def __eq__(self, other):
        return self._network == other._network


class State:
    __slots__ = ("_activities", "_network", "_compression")

    def __init__(self, activities=None, network=None, compression=False):
        """

        :param activities: a dict from node label to activity

        :param network: a Network
        """
        self._compression = compression
        self._activities = None
        self.activities = activities
        self._network = None
        self.network = network

    @property
    def activities(self):
        if self._activities:
            return _Compressor.decompress(self._activities) if self._compression else self._activities

    @activities.setter
    def activities(self, a):
        if a:
            self._activities = _Compressor.compress(a) if self._compression else a

    @property
    def network(self):
        if self._network:
            return Network.decompress(self._network) if self._compression else self._network

    @network.setter
    def network(self, n):
        if n:
            self._network = n.compress() if self._compression else n


class _Compressor:
    def __init__(self):
        pass

    @staticmethod
    def compress(obj):
        """
        Compresses the given object into a binary format.

        :param network: an object

        :return: packed bytes
        """
        return msgpack.packb(obj)

    @staticmethod
    def decompress(packed):
        """
        Decompresses a compressed object.

        :param packed: packed bytes

        :return: a decompressed object
        """
        gc.disable()
        d = msgpack.unpackb(packed, strict_map_key=False)
        gc.enable()
        return d