from data.excel_loader import load_project_data
from engine.project_graph import build_project_graph, get_buildable_components, critical_path, project_duration
from engine.finance import allocate_budget
import matplotlib.pyplot as plt 
import networkx as nx 
import time


def formater_entier(nombre):
    # On utilise l'astuce du formatage avec une virgule, 
    # puis on remplace la virgule par un espace.
    return f"{nombre:,}".replace(",", " ")


# Variables globales...
data = load_project_data("Project.xlsx")
components = data["components"]
graph = build_project_graph(components)
built_components: set = set()


def show_project_settings():
    global data
    print("PARAMETRES DU PROJET")
    print(f"Nom du projet: ") # on affiche le nom du projet
    print(f"budget intial du projet {data["parameters"].budget}")
    print(f"Nombre d'unités fonctionnelles: {len(data["components"])}") # On affiche le nombre d'unités fonctionnelles
    print("------------------------------------------------------------------------------")
    print(" ")
    print("retour au menu")
    time.sleep(3)
    start_program()
    

def show_nodes():
    global graph, components, data
    print("Tous les noeuds du projet".upper())
    print(graph.nodes)
    print("                                                                    ")
    print("Informations sur les unités fonctionnelles (noeuds) et leur dépendances")
    for i, item in enumerate(data["components"]):
        print(f"{i} - {item.name}")
        print(f"Coût de l'unité: {formater_entier(item.cost)} FCFA")
        print(f"Dépendance de l'unité: {item.dependency_id}")    
        print(f"Valeur stratégique: {item.strategic_value}")
        print("------------------------------------------------------------------------")
    
    print(" ")
    print("retour au menu")
    time.sleep(3)
    start_program()
        

def show_dependencies():
    global graph, components, data  
    print("ARETES DU PROJET")
    print(graph.edges)   
    
    for edge in graph.edges:
        print(f"{edge[1]} - {graph.nodes[edge[1]]['name']} dépend de {edge[0]} - {graph.nodes[edge[0]]['name']}")  

    unit = int(input("Veuillez entrer l'id d'une unité fonctionnelle: "))
    if graph.predecessors(unit):
        print(f"{unit} {graph.nodes[unit]['name']} a pour dépendance")
        for dep in graph.predecessors(unit):
            print(f"Nom de l'unité {graph.nodes[dep]["name"]}")
            print(f"Coût de l'unité {formater_entier(graph.nodes[dep]["cost"])} FCFA")
            print(f"Valeur stratégique {graph.nodes[dep]["value"]}")
    else:
        print("pas de dépendance pour cette unité")
        
    print("------------------------------------------------------------------------------")
    print(" ")
    print("retour au menu")
    time.sleep(3)
    start_program()
    

def show_project_graph():
    print("pas encore disponible".upper())
    print("------------------------------------------------------------------------------")
    print(" ")
    print("retour au menu")
    time.sleep(3)
    start_program()


def show_critical_path():
    print("le chemin critique".upper())
    global graph
    cp = critical_path(graph)
    
    print("Chemin critique:", cp)
    print("détail chemin critique")
    
    for node in cp:
        print("Noeud: ", node)
        print(f"Nom: {graph.nodes[node]["name"]}")
        print(f"Coût: {formater_entier(graph.nodes[node]["cost"])} FCFA")
        print(f"Valeur stratégique: {graph.nodes[node]["value"]}")
        print('*************************************************')
    
    print("------------------------------------------------------------------------------")
    print(" ")
    print("retour au menu")
    time.sleep(3)
    start_program()
    return cp


def show_buildables():
    print("unités réalisables à l'état initial du projet".upper())
    global built_components, graph
    buildable = get_buildable_components(graph, built_components) 
    
    for unit in buildable:
        print(f"{unit} - {graph.nodes[unit]['name']}")
    
    print("------------------------------------------------------------------------------")
    print(" ")
    print("retour au menu")
    time.sleep(3)
    start_program()
    

def simulate_decision():
    global built_components, graph
    print("SIMULATION")
    print("Vous allez entrer les unités déja construites en les séparant d'une virgule")
    units = input("entrez les id des unités déja construites...: ")
    
    # 2. On découpe la chaîne à chaque virgule -> devient ["10", " 20", " 30"]
    liste_chaines = units.split(",")

    # 3. On convertit chaque morceau en entier (int) et on nettoie les espaces
    liste_nombres = [int(n.strip()) for n in liste_chaines]
    print(liste_nombres)
    
    for nb in liste_nombres:
        built_components.add(nb)
        
    print("composants construits :", built_components)
    
    entree_budget = int(input('Entrez le budget disponible en (millions de FCFA)...: '))
    budget = 1000000 * entree_budget
    print(f"Bien. notre budget disponible est de : {formater_entier(budget)} FCFA")
    
    buildable = get_buildable_components(graph, built_components)
    selected, spent = allocate_budget(graph, buildable, built_components, budget)
    
    print("selected: ", selected)
    
    print("unités finançables avec le budget et les containtes")
    for dep in selected:
        print(f"{dep} - {graph.nodes[dep]['name']}")
        
    print("Budget spent:", spent)
    print("------------------------------------------------------------------------------")
    print(" ")
    print("retour au menu")
    time.sleep(3)
    start_program()
    
    
def start_program():
    """Fonction de lancement du programme"""
    # initailisation de certaines variables globales...
    built_components: set = set()
    
    print("programme de tets d'algorythme prédictif BTP...")
    print("à ce stade, le programme a lu le fichier project.xlsx qui contient toutes les données: \nque voulez vous faire?")
    print(" ")
    print("Menu______________________________")
    print("1- paramètres du projet")
    print("2- Afficher les noeuds du projet avec les détails pour chaque noeud")
    print("3- Afficher les relations de dépendance entre les différents noeuds")
    print("4- Graphe du projet")
    print("5- Chemin critique du projet")
    print("6- Afficher les unités constructibles")
    print("7- Simulation de décision")
    print("")

    choice = int(input("Entre le numéro du menu que vous voulez explorer: "))
    while choice not in list(range(1, 8)):
        choice = int(input("Entre le numéro du menu que vous voulez explorer: "))
    
    if choice == 1:
        show_project_settings()
    elif choice == 2:
        show_nodes()
    elif choice == 3:
        show_dependencies()
    elif choice == 4:
        show_project_graph()
    elif choice == 5:
        show_critical_path()
    elif choice == 6:
        show_buildables()
    else:
        simulate_decision()
        
    # options = {
    #     1: show_project_settings(),
    #     2: show_nodes(),
    #     3: show_dependencies(),
    #     4: show_project_graph(),
    #     5: show_critical_path(),
    #     6: show_buildables(),
    #     7: simulate_decision()
    # }
    
    # options[choice]
    print("")
    print("---------------------------------------------------------")
    print("")

start_program()

# _____________________________________________________________________________________________
# I-4. On lance la fonction qui va ressortir toutes les unités potentiellement réalisables    




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