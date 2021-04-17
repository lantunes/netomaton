import netomaton as ntm
from netomaton.vis import show_network


if __name__ == '__main__':

    # wm1167
    rules = {
        "in": [(1, 1, 2), (3, 4, 1)], "out": [(1, 1, 4), (5, 4, 3), (2, 5, 1)]
    }
    config = [(1, 1, 1), (1, 1, 1)]

    model = ntm.WolframPhysicsModel_N2(config, rules)

    trajectory = ntm.evolve_n2(network=model.network, topology_rule=model.topology_rule, timesteps=198)

    show_network(trajectory[-1].network)
