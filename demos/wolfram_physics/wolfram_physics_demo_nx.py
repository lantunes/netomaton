import netomaton as ntm
from netomaton.vis import show_network


if __name__ == '__main__':

    # wm1167
    rules = {
        "in": [(1, 1, 2), (3, 4, 1)], "out": [(1, 1, 4), (5, 4, 3), (2, 5, 1)]
    }
    config = [(1, 1, 1), (1, 1, 1)]

    model = ntm.WolframPhysicsModel_NX(config, rules)

    trajectory = ntm.evolve_nx(network=model.network, topology_rule=model.topology_rule, timesteps=198)

    show_network(trajectory[197])  # TODO if trajectory were a list, we could use -1 instead of 197