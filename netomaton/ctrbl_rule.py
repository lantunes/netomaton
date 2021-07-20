from .topology import cellular_automaton2d


class CTRBLRule:
    """
    A particular kind of rule that operates on von Neumann neighbourhoods, taking into account the states of a cell's
    neighbours at the top, bottom, left and right positions explicitly. Only 2D automata with periodic boundaries and a
    radius of 1 are supported.
    """
    def __init__(self, dim, rule_table, rotations=False):
        """
        Creates a CTRBLRule instance.

        :param dim: a 2-tuple, representing the rows and columns in the 2D Cellular Automata

        :param rule_table:

        :param rotations: whether rotations in the rule table are implied (default is False)
        """
        self._network = cellular_automaton2d(dim[0], dim[1], r=1, neighbourhood="von Neumann")
        self._neighbourhood_map = self._init_neighbourhood_map(dim)

    def activity_rule(self, ctx):
        pass # TODO

    @property
    def network(self):
        return self._network

    @property
    def neighbourhood_map(self):
        return self._neighbourhood_map

    def _init_neighbourhood_map(self, dim):
        """
        Returns a map of the cell label to a dictionary of the labels of the top, bottom, left, and right neighbours.
        e.g. {61: VonNeumannNeighbourhood(top=1, bottom=121, left=60, right=62, center=61)}

        :param dim: a 2-tuple, representing the rows and columns in the 2D Cellular Automata

        :return: the neighbourhood map
        """
        rows, cols = dim
        neighbourhood_map = {}
        idx = 0
        for row in range(rows):
            for _ in range(cols):
                center = idx
                left = (((center-row*cols) - 1) % cols) + (row*cols)
                right = (((center-row*cols) + 1) % cols) + (row*cols)
                top = (center - cols) % (rows*cols)
                bottom = (center + cols) % (rows*cols)
                neighbourhood_map[idx] = VonNeumannNeighbourhood(center=center, top=top, bottom=bottom,
                                                                 left=left, right=right)
                idx += 1
        return neighbourhood_map


class VonNeumannNeighbourhood:
    """
    A container for the labels of a von Neumann neighbourhood.
    """
    def __init__(self, center, top, bottom, left, right):
        self._center = center
        self._top = top
        self._bottom = bottom
        self._left = left
        self._right = right

    @property
    def center(self):
        return self._center

    @property
    def bottom(self):
        return self._bottom

    @property
    def top(self):
        return self._top

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __eq__(self, other):
        return self.center == other.center and self.top == other.top and self.bottom == other.bottom and \
               self.left == other.left and self.right == other.right

    def __repr__(self):
        return "VonNeumannNeighbourhood(center=%s, top=%s, bottom=%s, left=%s, right=%s)" % \
               (self.center, self.top, self.bottom, self.left, self.right)
