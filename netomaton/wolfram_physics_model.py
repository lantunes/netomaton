

class WolframPhysicsModel:
    def __init__(self, configuration, rules):
        self.connectivity_map, self.initial_conditions, self.last_vertex = self._init_connectivity_and_conditions(configuration)
        self.rules = rules

    def _init_connectivity_and_conditions(self, config):
        conn_map = {}
        initial_conditions = {}
        last_vertex = 0
        for i, edge in enumerate(config):
            conn_map[i] = {i: 1.0}
            initial_conditions[i] = edge
            for vertex in edge:
                if vertex > last_vertex:
                    last_vertex = vertex
        return conn_map, initial_conditions, last_vertex

    def activity_rule(self, ctx):
        # TODO this currently only supports single, binary relation rules

        relation = ctx.current_activity

        for rule_in in self.rules["in"]:

            # bind nodes to symbols
            symbol_bindings = {}

            if len(rule_in) == 1 and len(relation) > 1:
                #  rule does not match this relation
                return relation

            for i, symbol in enumerate(rule_in):
                if symbol in symbol_bindings:
                    if relation[i] != symbol_bindings[symbol]:
                        #  rule does not match this relation
                        return relation
                    else:
                        continue

                symbol_bindings[symbol] = relation[i]

            ctx.remove_node(ctx.node_label)

            for rule_out in self.rules["out"]:
                new_edge = []
                for symbol in rule_out:
                    if symbol not in symbol_bindings:
                        self.last_vertex += 1
                        symbol_bindings[symbol] = self.last_vertex
                    new_edge.append(symbol_bindings[symbol])

                ctx.add_node(tuple(new_edge), {})

        return None

    def to_configurations(self, activities):
        configs = []
        for timestep in activities:
            config = []
            for relation in activities[timestep].values():
                config.append(relation)
            configs.append(config)
        return configs
