import networkx as nx


class AdjacencyMatrix:
    @staticmethod
    def cellular_automaton(n, r=1, boundary="periodic"):
        """
        Creates the adjacency matrix for a 1D cellular automaton, with the given number of cells and neighbourhood
        radius.
        :param n: the number of cells in this automaton
        :param r: the neighbourhood radius
        :param boundary: the boundary condition
        :return: an adjacency matrix describing this cellular automaton
        """
        if n < 3:
            raise Exception("There must be at least 3 cells")
        adjacency_matrix = [[0. for j in range(n)] for i in range(n)]
        if boundary == "periodic":
            for w, row in enumerate(adjacency_matrix):
                for c, _ in enumerate(row):
                    if w == c:
                        adjacency_matrix[w][c] = 1.
                        for i in range(r):
                            adjacency_matrix[w][c - (1 + i)] = 1.
                        for i in range(r):
                            adjacency_matrix[w][(c + (1 + i)) % len(adjacency_matrix[w])] = 1.
        return adjacency_matrix

    @staticmethod
    def watts_strogatz_graph(n, k, p):
        G = nx.watts_strogatz_graph(n, k, p)
        return nx.adjacency_matrix(G).todense().tolist()