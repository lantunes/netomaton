
class WolframPhysicsModel:
    def __init__(self, configuration, rules):
        self.connectivity_map, self.last_node = self._init_connectivity_and_conditions(configuration)
        self.rules = rules

    @staticmethod
    def _init_connectivity_and_conditions(config):
        """
        The Connectivity Map for the Wolfram Physics Model is comprised of connection states that are 2-tuples:
        (m, h), where "m" is the connection multiplicity (i.e. how copies of this edge are present) and "h" is the
        hyperedge label for the hyperedge this connection belongs to.
        """
        conn_map = {}
        last_node = 0
        for c, relation in enumerate(config):
            prev = None
            edge_label = str(c+1)
            is_hyperedge = len(relation) > 2
            next_edge_num = 0
            for node in relation:
                if node not in conn_map:
                    conn_map[node] = {}
                if prev is not None:
                    if prev not in conn_map[node]:
                        conn_map[node][prev] = []
                    prev_state = {"label": edge_label}
                    if is_hyperedge:
                        prev_state["hyperedge"] = {"index": next_edge_num}
                    conn_map[node][prev].append(prev_state)
                    next_edge_num += 1
                prev = node
                if node > last_node:
                    last_node = node
            if len(relation) == 1:
                n = relation[0]
                if n not in conn_map[n]:
                    conn_map[n][n] = []
                conn_map[n][n].append({"label": edge_label, "unary": True})
        return conn_map, last_node

    @staticmethod
    def connectivity_map_to_config(conn_map):
        edges = {}
        hyperedges = {}
        for to_node in conn_map:
            for from_node, connections in conn_map[to_node].items():
                for connection in connections:
                    edge_label = connection["label"]
                    if "unary" in connection:
                        edges[edge_label] = (from_node,)
                    elif "hyperedge" in connection:
                        if edge_label not in hyperedges:
                            hyperedges[edge_label] = []
                        hyperedges[edge_label].append(((from_node, to_node), connection["hyperedge"]["index"]))
                    else:
                        edges[edge_label] = (from_node, to_node)

        # merge hyperedges
        merged_hyperedges = {}
        if hyperedges:
            for edge_label in hyperedges:
                parts = hyperedges[edge_label]
                merged = [0] * (len(parts) + 1)
                for part in parts:
                    edge = part[0]
                    index = part[1]
                    merged[index] = edge[0]
                    if (index + 2) == len(merged):
                        merged[-1] = edge[1]
                merged_hyperedges[edge_label] = tuple(merged)

        edges.update(merged_hyperedges)
        config = [edges[label] for label in sorted(edges)]  # sort so that we can preserve the order of the relations

        return config

    def connectivity_rule(self, cctx):
        relations = self.connectivity_map_to_config(cctx.connectivity_map)

        matched_relations = []
        unmatched_relations = []
        partially_matched = []

        # keep scanning until there is an iteration where no matches are produced
        #  reset the symbol bindings during each scan
        scanning = True
        while scanning:

            # bind nodes to symbols
            symbol_bindings = {}

            for rule in self.rules["in"]:

                match_found = False

                for relation in list(relations):  # iterate over a copy of the list so that we can remove from the original
                    if self._matches(rule, relation, symbol_bindings):
                       partially_matched.append(relation)
                       relations.remove(relation)
                       match_found = True
                       break

                if len(partially_matched) == len(self.rules["in"]):
                    matched_relations.append((partially_matched, symbol_bindings))
                    partially_matched = []

                scanning = match_found

            # move all partially matched to unmatched
            unmatched_relations.extend(partially_matched)
            partially_matched = []

        new_config = []
        # add the relations that did not match the rules
        new_config.extend(relations)
        new_config.extend(unmatched_relations)
        # add the new relations
        for matched, bindings in matched_relations:
            for rule_out in self.rules["out"]:
                new_edge = []
                for symbol in rule_out:
                    if symbol not in bindings:
                        self.last_node += 1
                        bindings[symbol] = self.last_node
                    new_edge.append(bindings[symbol])
                new_config.append(tuple(new_edge))

        self.connectivity_map, self.last_node = self._init_connectivity_and_conditions(new_config)

        return self.connectivity_map

    def _matches(self, rule, relation, symbol_bindings):
        if len(rule) != len(relation):
            #  rule does not match this relation
            return False

        added_symbols = []
        for i, symbol in enumerate(rule):
            if symbol in symbol_bindings:
                if relation[i] != symbol_bindings[symbol]:
                    #  rule does not match this relation
                    for added in added_symbols:
                        del symbol_bindings[added]
                    return False
                else:
                    continue

            symbol_bindings[symbol] = relation[i]
            added_symbols.append(symbol)

        return True

    def to_configurations(self, connectivities_over_time):
        configs = []
        for timestep in connectivities_over_time:
            configs.append(self.connectivity_map_to_config(connectivities_over_time[timestep]))
        return configs