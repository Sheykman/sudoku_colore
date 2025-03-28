from sage.all import Graph
import string

# Fonction pour identifier le bloc d'une case (i, j)
def get_bloc(bloc_index):
    # Génération des noms des blocs (A à I)
    bloc_names = [l for l in string.ascii_uppercase[:9]]  # ['A', 'B', 'C', ..., 'I']

    return bloc_names[bloc_index]  # Retourner la lettre du bloc

def creer_sudoku():
    # Création du graphe
    Graphe = Graph()

    # Dictionnaire pour stocker les sommets sous leur nom unique
    sommets = {}

    # Ajouter les sommets avec des noms personnalisés
    for i in range(9):
        lst = []
        for j in range(9):
            sommet = f"{j+1}{get_bloc(i)}"
            Graphe.add_vertex(sommet)
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
                    Graphe.add_edge(k, sommet)
            lst.append(sommet)

    # Ajouter les arêtes selon les règles du Sudoku
    for i in range(9):
        for j in range(9):
            sommet = sommets[(i, j)]

            # Relier aux autres cases de la même ligne
            for k in range(9):
                if k != j :
                    voisin = sommets[(i, k)]
                    if not Graphe.has_edge(sommet, voisin):  # Vérifie qu'il n'y a pas déjà une arête
                        Graphe.add_edge(sommet, voisin)

            # Relier aux autres cases de la même colonne
            for k in range(9):
                if k != i :
                    voisin = sommets[(k, j)]
                    if not Graphe.has_edge(sommet, voisin):  # Vérifie qu'il n'y a pas déjà une arête
                        Graphe.add_edge(sommet, voisin)
    return Graphe

def trouver_coleurs_dispo(graphe, sommet, sommets_colories):
    # Liste des couleurs disponibles
    lst_couleurs = list(range(9))
    # On enlève de la liste les couleurs des voisins
    for voisin in graphe.neighbors(sommet):
        if voisin in sommets_colories:
            if sommets_colories[voisin] in lst_couleurs:
                lst_couleurs.remove(sommets_colories[voisin])
    
    # Si le sommet est déjà coloré, on enlève cette couleur de la liste
    if sommet in sommets_colories:
        lst_couleurs.remove(sommets_colories[sommet])

    return lst_couleurs


def backtracking(graphe, sommets_restants, sommets_colories):
    # Condition d'arrêt : tous les sommets sont coloriés
    if not sommets_restants:
        return sommets_colories

    sommet = sommets_restants[0]

    couleurs_dispo = trouver_coleurs_dispo(graphe, sommet, sommets_colories)
    
    # On essaye chaque couleur disponible
    for couleur in couleurs_dispo:
        # On créé une copie du dictionnaire de sommets coloriés
        nouvelle_coloration = sommets_colories.copy()
        nouvelle_coloration[sommet] = couleur
        
        # On créé une nouvelle liste de sommets restants sans le sommet actuel
        nouveaux_sommets_restants = sommets_restants[1:]
        
        # On essaye de colorier le reste du graphe
        resultat = backtracking(graphe, nouveaux_sommets_restants, nouvelle_coloration)
        
        # Si une solution est trouvée, la retourner
        if resultat is not None:
            return resultat
    
    # Si aucune solution n'a été trouvée on retourne None
    return None

def coloration(graphe):
    # On convertit la liste des sommets en liste
    sommets = list(graphe.vertices())
    
    resultat = backtracking(graphe, sommets, {})
    
    if resultat is None:
        raise ValueError("Impossible de colorier le graphe")
    
    return resultat


def main():
    Graphe = creer_sudoku()

    # Vérifications
    print(f"Nombre de sommets créés : {Graphe.num_verts()} (attendu : 81)")
    print(f"Nombre d'arêtes créées : {Graphe.num_edges()} (attendu : 810)")

    Graphe_colore = coloration(Graphe)

    # Afficher la coloration des sommets
    for sommet, couleur in Graphe_colore.items():
        print(f"Le sommet {sommet} a été coloré en {couleur}")
















if __name__ == "__main__":
    main()
