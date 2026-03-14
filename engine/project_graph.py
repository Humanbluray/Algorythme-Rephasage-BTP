import networkx as nx
import pandas as pd


def build_project_graph(components):

    G = nx.DiGraph()

    for comp in components:

        G.add_node(
            comp.id,
            name=comp.name,
            cost=comp.cost,
            value=comp.strategic_value,
            duration=comp.duration
        )

        if pd.notna(comp.dependency_id):

            G.add_edge(int(comp.dependency_id), comp.id, duration=comp.duration)

    return G


def get_buildable_components(graph, built_components):
    """La fonction permet d'afficher l'ensemble des unités fonctionnelles déja réalisées

    Args:
        graph graphique networkx: représente l'ensemble des relations de dépendance dans notre réseau
        built_components: set comprenant les unités fonctionnelles déja réalisées

    Returns:
        retourne une liste d'unités potentiellement réalisablmes avec le financement à l'instant T
    """
    buildable: list = []

    for node in graph.nodes:

        # ignorer ce qui est déjà construit
        if node in built_components:
            continue

        # récupérer les dépendances
        dependencies = list(graph.predecessors(node))

        # vérifier si toutes les dépendances sont construites
        if all(dep in built_components for dep in dependencies):

            buildable.append(node)

    return buildable


def critical_path(graph):
    """Calcul du chemin critique du projet"""
    # calcul du chemin le plus long basé sur la durée
    path = nx.dag_longest_path(graph, weight="duration")

    return path


def project_duration(graph):
    """durée totale du projet"""
    return nx.dag_longest_path_length(graph, weight="duration")

