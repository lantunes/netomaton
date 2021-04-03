import netomaton as ntm
import numpy as np


if __name__ == '__main__':
    """
    This demo is inspired by "Collective dynamics of ‘small-world’ networks", by Duncan J. Watts and 
    Steven H. Strogatz (Nature 393, no. 6684 (1998): 440). Towards the end of the paper, they state: 
    "For cellular automata charged with the computational task of density classification, we find that a simple 
    ‘majority-rule’ running on a small-world graph can outperform all known human and genetic algorithm-generated rules 
    running on a ring lattice." The code below attempts to reproduce the experiment they are referring to.
    """

    adjacency_matrix = ntm.topology.adjacency.watts_strogatz_graph(n=149, k=8, p=0.5)

    initial_conditions = np.random.randint(0, 2, 149)

    print("density of 1s: %s" % (np.count_nonzero(initial_conditions) / 149))

    activities, adjacencies = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=149,
                                         activity_rule=ntm.rules.majority_rule)

    ntm.plot_grid(activities)
