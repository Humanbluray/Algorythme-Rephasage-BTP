def affordable_components(graph, buildable_nodes, budget):
    """Permet de déterminer quelles unités peut on financer avec le budget actuel"""
    affordable = []

    for node in buildable_nodes:

        cost = graph.nodes[node]["cost"]

        if cost <= budget:
            affordable.append(node)

    print("Unités finançables: ", affordable)
    return affordable


def prioritize_components(graph, nodes):
    """on fait un classement des unités par note stratégique"""
    nodes_sorted = sorted(
        nodes,
        key=lambda n: graph.nodes[n]["value"],
        reverse=True
    )

    print("Sorted nodes: ", nodes_sorted)
    return nodes_sorted



def select_components(graph, nodes, budget):
    """selectionner les investissements"""
    selected = []
    spent = 0

    for node in nodes:

        cost = graph.nodes[node]["cost"]

        if spent + cost <= budget:

            selected.append(node)
            spent += cost

    print("")
    return selected, spent


def allocate_budget(graph, buildable_nodes, built_components, budget):
    # enlever les unités déja construites
    candidates = []
    for node in buildable_nodes:
        if node not in built_components:
            candidates.append(node)
    
    print('builts components:', built_components)
    print("buildable nodes:", buildable_nodes)
    print("candidates", candidates)
    
    # 2 filtrer les unités finançables
    affordable = affordable_components(graph, candidates, budget)

    # 3 prioriser
    prioritized = prioritize_components(graph, affordable)

    # 3 sélectionner
    selected, spent = select_components(graph, prioritized, budget)

    return selected, spent

