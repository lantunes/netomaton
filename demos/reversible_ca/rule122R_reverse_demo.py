import matplotlib.pyplot as plt
import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    # NKS page 443 - Rule 122R
    adjacency_matrix = ntm.network.cellular_automaton(n=100)

    # carefully chosen initial conditions
    previous_state = [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1,
                      0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0,
                      1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1,
                      0, 0, 1, 1]
    initial_conditions = [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                          1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                          1, 1, 1, 0, 1, 1, 1]

    r = ntm.ReversibleRule(lambda ctx: ntm.rules.nks_ca_rule(ctx, 122))
    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=1002, activity_rule=r.activity_rule,
                               past_conditions=[previous_state])

    timestep = []
    average_node_entropies = []

    for i, c in enumerate(activities):
        timestep.append(i)
        bit_string = ''.join([str(x) for x in c])
        average_node_entropies.append(ntm.average_node_entropy(activities[:i+1]))
        print("%s, %s" % (i, average_node_entropies[-1]))

    plt.subplot(3, 1, (1, 2))
    plt.title("Avg. Node (Shannon) Entropy")
    plt.gca().set_xlim(0, 1002)
    plt.gca().axes.xaxis.set_ticks([])
    plt.plot(timestep, average_node_entropies)

    plt.subplot(3, 1, 3)
    plt.gca().axes.yaxis.set_ticks([])
    ntm.plot_grid(np.array(activities).T.tolist())


