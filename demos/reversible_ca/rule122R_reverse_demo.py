import matplotlib.pyplot as plt
import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    # NKS page 443 - Rule 122R
    adjacencies = ntm.network.cellular_automaton(n=100)

    # carefully chosen initial conditions
    previous_state = [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1,
                      0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0,
                      1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1,
                      0, 0, 1, 1]
    initial_conditions = [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                          1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                          1, 1, 1, 0, 1, 1, 1]

    r = ntm.ReversibleRule(previous_state, lambda n, c, t: ntm.rules.nks_ca_rule(n, c, 122))
    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=1002, activity_rule=r.activity_rule)

    timestep = []
    average_cell_entropies = []

    for i, c in enumerate(activities):
        timestep.append(i)
        bit_string = ''.join([str(x) for x in c])
        average_cell_entropies.append(ntm.average_cell_entropy(activities[:i+1]))
        print("%s, %s" % (i, average_cell_entropies[-1]))

    plt.subplot(3, 1, (1, 2))
    plt.title("Avg. Cell (Shannon) Entropy")
    plt.gca().set_xlim(0, 1002)
    plt.gca().axes.xaxis.set_ticks([])
    plt.plot(timestep, average_cell_entropies)

    plt.subplot(3, 1, 3)
    plt.gca().axes.yaxis.set_ticks([])
    ntm.plot_grid(np.array(activities).T.tolist())


