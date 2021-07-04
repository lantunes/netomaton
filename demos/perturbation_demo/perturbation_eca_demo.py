import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    network = ntm.topology.cellular_automaton(n=200)
    initial_conditions = [0] * 100 + [1] + [0] * 99

    def perturb(pctx):
        """
        Mutates the value of the node with index 100 at each timestep, making it either 0 or 1 randomly.
        """
        if pctx.node_label == 100:
            return np.random.randint(2)
        return pctx.node_activity

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100,
                            activity_rule=ntm.rules.nks_ca_rule(30), perturbation=perturb)

    ntm.plot_activities(trajectory)
