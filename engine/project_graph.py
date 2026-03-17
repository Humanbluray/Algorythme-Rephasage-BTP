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

    buildable = []

    for node in graph.nodes:
        
        # liste des dépendances pour chaque noeud
        predecessors = list(graph.predecessors(node))

        # ignorer déjà construits
        if node in built_components:
            pass
        
        # si pas encore construit, on vérifie les dépendances
        else:
            # si dépendances il y a 
            if predecessors:
                # on vérifie pour chaque dépendance si elle est réalisée
                for dep in predecessors:
                    # si elle est réalisée
                    if dep in built_components:
                        buildable.append(node)
                    # sinon
                    else:
                        pass
                    
            # si pas de dépendances
            else:
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

