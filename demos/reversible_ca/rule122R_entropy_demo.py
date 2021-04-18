import matplotlib.pyplot as plt
import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    # NKS page 442 - Rule 122R
    network = ntm.topology.cellular_automaton(n=100)
    initial_conditions = [0]*40 + [1]*20 + [0]*40
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=ntm.ReversibleRule(ntm.rules.nks_ca_rule(122)),
                            past_conditions=[initial_conditions], timesteps=1000)

    timestep = []
    average_node_entropies = []

    activities = ntm.get_activities_over_time_as_list(trajectory)
    for i, c in enumerate(activities):
        timestep.append(i)
        bit_string = ''.join([str(x) for x in c])
        average_node_entropies.append(ntm.average_node_entropy(activities[:i+1]))
        print("%s, %s" % (i, average_node_entropies[-1]))

    plt.subplot(3, 1, (1, 2))
    plt.title("Avg. Node (Shannon) Entropy")
    plt.gca().set_xlim(0, 1000)
    plt.gca().axes.xaxis.set_ticks([])
    plt.plot(timestep, average_node_entropies)

    plt.subplot(3, 1, 3)
    plt.gca().axes.yaxis.set_ticks([])
    ntm.plot_grid(np.array(activities).T.tolist())


