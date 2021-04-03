import netomaton as ntm
from netomaton.vis import show_network, configuration_to_nx


if __name__ == '__main__':

    # wm1167
    rules = {
        "in": [(1, 1, 2), (3, 4, 1)], "out": [(1, 1, 4), (5, 4, 3), (2, 5, 1)]
    }
    config = [(1, 1, 1),(1, 1, 1)]

    model = ntm.WolframPhysicsModel(config, rules)

    _, connectivities = ntm.evolve(topology=model.connectivity_map, connectivity_rule=model.connectivity_rule,
                                   timesteps=198)

    configurations = model.to_configurations(connectivities)

    show_network(configuration_to_nx(configurations[-1]))
