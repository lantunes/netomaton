import netomaton as ntm
from netomaton.vis import show_network, configuration_to_nx


if __name__ == '__main__':

    # rules = {
    #     "in": [("x", "y")], "out": [("x", "y"), ("y", "z")]
    # }
    # config = [(1, 2)]

    # rules = {
    #     "in": [("x", "y")], "out": [("z", "y"), ("y", "x")]
    # }
    # config = [(1, 2)]

    # rules = {
    #     "in": [("x", "y")], "out": [("x", "z"), ("x", "z"), ("y", "z")]
    # }
    # config = [(1, 1)]

    # rules = {
    #     "in": [("x", "x")], "out": [("y", "y"), ("y", "y"), ("x", "y")]
    # }
    # config = [(1, 1)]

    # rules = {
    #     "in": [("x", "y")], "out": [("x", "z"), ("z", "w"), ("y", "z")]
    # }
    # config = [(1, 1)]

    # rules = {
    #     "in": [("x", "x", "y")], "out": [("w", "w", "x"), ("y", "x", "x")]
    # }
    # config = [(1, 1, 1)]

    # rules = {
    #     "in": [("x", "x", "x")], "out": [("w", "w", "w"), ("w", "w", "x")]
    # }
    # config = [(1, 1, 1)]

    rules = {
        "in": [("x", "y", "x")], "out": [("w", "z", "w"), ("z", "y", "y"), ("x", "z", "y"), ("u", "z", "u")]
    }
    config = [(1, 1, 1)]

    model = ntm.WolframPhysicsModel(config, rules)

    activities, _ = ntm.evolve_2(model.initial_conditions, topology=model.connectivity_map,
                                 activity_rule=model.activity_rule, timesteps=4)

    configurations = model.to_configurations(activities)

    show_network(configuration_to_nx(configurations[-1]))
