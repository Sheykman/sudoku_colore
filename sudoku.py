from sage.all import Graph
import string

# Création du graphe
G = Graph()

# Génération des noms des blocs (A à I)
bloc_names = [l for l in string.ascii_uppercase[:9]]  # ['A', 'B', 'C', ..., 'I']

# Fonction pour identifier le bloc d'une case (i, j)
def get_bloc(bloc_index):
    return bloc_names[bloc_index]  # Retourner la lettre du bloc

# Dictionnaire pour stocker les sommets sous leur nom unique
sommets = {}

# Ajouter les sommets avec des noms personnalisés
for i in range(9):
    lst = []
    for j in range(9):
        sommet = f"{j+1}{get_bloc(i)}"
        G.add_vertex(sommet)
        # On range les sommets en carré dans le dictionnaire
        if i == 0 or i == 3 or i == 6:
            if j <= 2:
                sommets[(i, j)] = sommet
            elif 6 > j >= 3:
                sommets[(i+1, j-3)] = sommet
            elif j >= 6:
                sommets[(i+2, j-6)] = sommet
        elif i == 1 or i == 4 or i == 7:
            if j <= 2:
                sommets[(i-1, j+3)] = sommet
            elif 6 > j >= 3:
                sommets[(i, j)] = sommet
            elif j >= 6:
                sommets[(i+1, j-3)] = sommet
        elif i == 2 or i == 5 or i == 8:
            if j <= 2:
                sommets[(i-2, j+6)] = sommet
            elif 6 > j >= 3:
                sommets[(i-1, j+3)] = sommet
            elif j >= 6:
                sommets[(i, j)] = sommet
        # On créé déjà les arêtes entre les membres d'un même bloc
        if len(lst) != 0:
            for k in lst :
                G.add_edge(k, sommet)
        lst.append(sommet)

# Ajouter les arêtes selon les règles du Sudoku
for i in range(9):
    for j in range(9):
        sommet = sommets[(i, j)]

        # Relier aux autres cases de la même ligne
        for k in range(9):
            if k != j :
                voisin = sommets[(i, k)]
                if not G.has_edge(sommet, voisin):  # Vérifie qu'il n'y a pas déjà une arête
                    G.add_edge(sommet, voisin)

        # Relier aux autres cases de la même colonne
        for k in range(9):
            if k != i :
                voisin = sommets[(k, j)]
                if not G.has_edge(sommet, voisin):  # Vérifie qu'il n'y a pas déjà une arête
                    G.add_edge(sommet, voisin)


# Vérifications
print(f"Nombre de sommets créés : {G.num_verts()} (attendu : 81)")
print(f"Nombre d'arêtes créées : {G.num_edges()} (attendu : 810)")

def backtracking(sommet, graphe, couleurs):
    voisin_sommet_courant = graphe.neighbors(sommet)

def coloration(graphe, couleurs):

    # Initialisation de l'index de couleur
    index_couleur_courant = 0
    
    # Parcourir les sommets triés
    for sommet in graphe.vertices():
        # Vérifier les couleurs des voisins du sommet
        voisins_couleurs = set(couleurs.get(voisin) for voisin in graphe.neighbors(sommet))
        reset = 0
        
        # Trouver la première couleur disponible
        while couleurs_disponibles[index_couleur_courant] in voisins_couleurs:
            index_couleur_courant += 1
            if index_couleur_courant >= len(couleurs_disponibles):
                if reset == 1:
                    # Ajouter une nouvelle couleur à la liste si nécessaire
                    backtracking(sommet, graphe)
                index_couleur_courant = 0
                reset = 1
        
        # Attribuer la couleur au sommet
        couleurs[sommet] = couleurs_disponibles[index_couleur_courant]
        
    
    return couleurs

# Appliquer l'algorithme de Welsh-Powell
resultat_coloration = coloration(G)

# Afficher la coloration des sommets
for sommet, couleur in resultat_coloration.items():
    print(f"Le sommet {sommet} a été coloré en {couleur}")

def main():
    # Liste des couleurs disponibles
    couleurs_disponibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Dictionnaire pour stocker les couleurs des sommets
    couleurs = {}

