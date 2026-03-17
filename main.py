from data.excel_loader import load_project_data
from engine.project_graph import build_project_graph, get_buildable_components, critical_path, project_duration
import matplotlib.pyplot as plt 
import networkx as nx 
import time


# Module CPM
# __________________________________________________________________________________________________________________________________

# I-1. On lit le fichier excel avce noptre fonction de lecture
print("Lecture des données du fichier excel")
data = load_project_data("Project.xlsx")
print("1- lecture du fichier excel du projet et de ses composants")
print("------------------------------------------------------------------------")
print("                                                                        ")
time.sleep(3)

#________________________________________________________________________________________
# I-2. Affichage des donées extraites de notre fichier
print("2- Affichage des données de notre fichier")
print(f"Nom du projet: {data["parameters"].name}") # on affiche le nom du projet
print(f"Nombre d'unités fonctionnelles: {len(data["components"])}") # On affiche le nombre d'unités fonctionnelles

# on lit les informations sur les composants (unités fonctionnelles)
print("Informations sur les unités fonctionnelles et leur dépendances")
for i, item in enumerate(data["components"]):
    print(f"{i} - {item.name} - {item.cost} - {item.dependency_id} - {item.strategic_value}")
    
print("------------------------------------------------------------------------")
print("                                                                        ")
time.sleep(3)


#________________________________________________________________________________________
# I-3. On crée le graphe mettant en exergue le réseau de dépendances
print("3- Créatin du graphe en mettant en exergue les dépendances")
components = data["components"]
graph = build_project_graph(components)

# exemple pour vérifier les dépendances
# print("nodes", graph.nodes)
print("On affiche tous les Noeuds")
print("nodes", graph.nodes(data=True))

#les dépendances de chaque étape
print("On affiche toutes les arêtes")
print("edges", graph.edges)


# Affiche la liste des dépendance de l'unité 2
unit = int(input("Veuillez entrer l'id d'une unité fonctionnelle: "))
print(f"dépendance de l'unité {unit}", list(graph.predecessors(unit)))

if graph.predecessors(unit):
    for dep in graph.predecessors(unit):
        print(f"Nom de l'unité {graph.nodes[dep]["name"]}")
        print(f"Coût de l'unité {graph.nodes[dep]["cost"]} FCFA")
        print(f"Valeur stratégique {graph.nodes[dep]["value"]}")
else:
    print("pas de dépendance pour cette unité")


print("------------------------------------------------------------------------")
print("                                                                        ")
time.sleep(3)

# _____________________________________________________________________________________________
# I-4. On lance la fonction qui va ressortir toutes les unités potentiellement réalisables    

print("4- unités réalisables")
built_components: set = set()  # Set qui va contenir les id des unités déja construites...

buildable = get_buildable_components(graph, built_components) # Notre fonction qui détermine qui es tréalisable ou pas
print(f"Unités réalisables {buildable}")
for unit in buildable:
    print(f"{unit} - {graph.nodes[unit]['name']}")


# print("buildbales ", buildable)

# on simule la construction de l'unité numéro 1
built_components = {1}
buildable = get_buildable_components(graph, built_components) # Notre fonction qui détermine qui es tréalisable ou pas
print(f"Si l'unité 1 est construite: {buildable}")
# print("buildbales ", buildable)

print("les unités finançables")
for unit in buildable:
    print(f"{unit} - {graph.nodes[unit]['name']}")


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

print("------------------------------------------------------------------------")
print("                                                                        ")

time.sleep(3)


# I-6. calcul du chemin critique, quels unités construire en priorité en fonction de la durée
cp = critical_path(graph)
print("Chemin critique:", cp)
print("chemin critique")
for node in cp:
    print("Noeud: ", node)
    print('_______________________________________________')
    print(f"Nom: {graph.nodes[node]["name"]}")
    print('_______________________________________________')
    print(f"Coût: {graph.nodes[node]["cost"]} FCFA")
    print('_______________________________________________')
    print(f"Valeur stratégique: {graph.nodes[node]["value"]}")
    

# Durée du projet...
# print("Durée totale du projet: ", project_duration(graph))

print("------------------------------------------------------------------------")
print("                                                                        ")


# II - Module Finances
# __________________________________________________________________________________________________________________________________
# cette étape va calculer le budget disponible, le stress financier et la capacité d'investissement
# c'est elle qui décidera quelle unité du projet foinancer avec les fonds disponibles

from engine.finance import allocate_budget
budget = 600000000

# on reinitialise les unités construites à 0
built_components.remove(1)
buildable = get_buildable_components(graph, built_components)

selected, spent = allocate_budget(graph, buildable, built_components, budget)

print(f"budget : {budget} FCFA")
for dep in selected:
    print(f"{dep} - {graph.nodes[dep]['name']}")
    
print("Budget spent:", spent)
 
 
