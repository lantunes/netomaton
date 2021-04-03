import netomaton as ntm
import numpy as np

if __name__ == '__main__':

    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    activities, adjacencies = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                           activity_rule=ntm.ReversibleRule_2(ntm.rules.nks_ca_rule_2(90)),
                                           past_conditions=[initial_conditions], timesteps=100)

    ntm.plot_grid(activities)
