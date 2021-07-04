import netomaton as ntm
import numpy as np

if __name__ == '__main__':

    network = ntm.topology.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=ntm.ReversibleRule(ntm.rules.nks_ca_rule(90)),
                            past_conditions=[initial_conditions], timesteps=100)

    ntm.plot_activities(trajectory)
