from data.excel_loader import load_project_data
from engine.project_graph import build_project_graph, get_buildable_components, critical_path, project_duration
import matplotlib.pyplot as plt 
import networkx as nx 


# 1. On lit le fichier excel avce noptre fonction de lecture
data = load_project_data("Project.xlsx")

#________________________________________________________________________________________
# 2. Affichage des donées extraites de notre fichier
print(data["parameters"].name) # on affiche le nom du projet
print(len(data["components"])) # On affiche le nombre d'unités fonctionnelles

# on lit les onformations sur les composants (unités fonctionnelles)
for i, item in enumerate(data["components"]):
    print(f"{i} - {item.name} - {item.dependency_id}")
    

#________________________________________________________________________________________
# 3. On crée le graphe mettant en exergue le réseau de dépendances
components = data["components"]
graph = build_project_graph(components)

# exemple pour vérifier les dépendances
print("nodes", graph.nodes)
# print("nodes", graph.nodes(data=True))

#les dépendances de chaque étape
print("edges", graph.edges)


# Affiche la liste des dépendance de l'unité 2
print("dépendance de l'unité 2",list(graph.predecessors(2)))
for dep in graph.predecessors(2):
    print(f"Nom de l'unité {graph.nodes[dep]["name"]}")
    print(f"Coût de l'unité {graph.nodes[dep]["cost"]:.2f} $")
    print(f"Valeur stratégique {graph.nodes[dep]["value"]}")


# _____________________________________________________________________________________________
# 4. On lance la fonction qui va ressortir toutes les unités potentiellement réalisables    
built_components: set = set()  # Set qui va contenir les id des unités déja construites...

buildable = get_buildable_components(graph, built_components) # Notre fonction qui détermine qui es tréalisable ou pas
print(f"Unités réalisables {buildable}")


# on simule la construction de l'unité numéro 1
built_components = {1}
buildable = get_buildable_components(graph, built_components) # Notre fonction qui détermine qui es tréalisable ou pas
print(f"Unités réalisables après avoir construit l'unité 1 {buildable}")


# on va afficher le graphe du projet hospitalier pour visaaliser les dépendances
# plt.figure(figsize=(10,7))
# pos = nx.spring_layout(graph) # calcule une position naturelledu réseau
# labels = {}

# for node in graph.nodes:
#     labels[node] = graph.nodes[node]["name"]

# # dessin du graph
# # il affiche: nodes = unités hospitalières, flèches = dépendances
# nx.draw(
#     graph, 
#     pos,
#     labels=labels,
#     node_size=3000,
#     node_color="lightblue",
#     font_size=9
# ) 
# plt.title('Hôpital')
# plt.show()


# 6. calcul du chemin critique, quels unités construire en priorité en fonction de la durée
cp = critical_path(graph)
print("Critical path:", cp)
for node in cp:
    print(f"{graph.nodes[node]["name"]} - {graph.nodes[node]["cost"]:.0f} Euros -  durée {graph.nodes[node]["duration"]} Mois")
    

# Durée du projet...
print("Durée totale du projet: ", project_duration(graph))






# ______________________________________________________________________________________________
# 5. Finances
# cette étape va calculer le budget disponible, le stress financier et la capacité d'investissement
# c'est elle qui décidera quelle unité du projet foinancer avec les fonds disponibles
 
 
