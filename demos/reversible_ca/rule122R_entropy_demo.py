import matplotlib.pyplot as plt
import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    # NKS page 442 - Rule 122R
    adjacencies = ntm.AdjacencyMatrix.cellular_automaton(n=100)
    initial_conditions = [0]*40 + [1]*20 + [0]*40
    r = ntm.ReversibleRule(initial_conditions, lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 122))
    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=1000, activity_rule=r.activity_rule)

    timestep = []
    average_cell_entropies = []

    for i, c in enumerate(activities):
        timestep.append(i)
        bit_string = ''.join([str(x) for x in c])
        average_cell_entropies.append(ntm.average_cell_entropy(activities[:i+1]))
        print("%s, %s" % (i, average_cell_entropies[-1]))

    plt.subplot(3, 1, (1, 2))
    plt.title("Avg. Cell (Shannon) Entropy")
    plt.gca().set_xlim(0, 1000)
    plt.gca().axes.xaxis.set_ticks([])
    plt.plot(timestep, average_cell_entropies)

    plt.subplot(3, 1, 3)
    plt.gca().axes.yaxis.set_ticks([])
    ntm.plot_grid(np.array(activities).T.tolist())


