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
            for r, row in enumerate(adjacency_matrix):
                for c, _ in enumerate(row):
                    if r == c:
                        adjacency_matrix[r][c] = 1.
                        adjacency_matrix[r][c - 1] = 1.
                        adjacency_matrix[r][(c + 1) % len(adjacency_matrix[r])] = 1.
        return adjacency_matrix

    @staticmethod
    def watts_strogatz_graph(n, k, p):
        G = nx.watts_strogatz_graph(n, k, p)
        return nx.adjacency_matrix(G).todense().tolist()