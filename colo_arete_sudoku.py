import string

def get_bloc(bloc_index):
    bloc_names = [l for l in string.ascii_uppercase[:9]]
    return bloc_names[bloc_index]

def creer_graphe_sudoku():
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

def trouver_couleurs_dispo(graphe, arete, aretes_colories):
    # Liste des couleurs disponibles
    lst_couleurs = list(range(25))

    # On cherche les voisins de l'arête donnée
    u, v, _ = arete

    # Arêtes incidentes aux deux extrémités
    aretes_incidentes = graphe.edges_incident(u) + graphe.edges_incident(v)

    for a in aretes_incidentes:
        if a in aretes_colories:
            couleur = aretes_colories[a]
            if couleur in lst_couleurs:
                lst_couleurs.remove(couleur)

    return lst_couleurs

def backtrack(graphe, aretes_colories, arete_restantes):
    # Controle si toutes les arêtes sont colorées
    if not arete_restantes:
        return aretes_colories
    
    arete = arete_restantes[0]

    # On cherche les couleurs disponibles pour l'arête donnée
    couleurs_dispo = trouver_couleurs_dispo(graphe, arete, aretes_colories)
    # On essaye chaque couleur disponible
    for couleur in couleurs_dispo:
        # On colorie l'arête avec la couleur choisie
        aretes_colories[arete] = couleur
        # On enlève l'arête de la liste des arêtes restantes
        nouvelles_arete_restantes = arete_restantes[1:]
        # On appelle la fonction récursive pour le reste des arêtes
        result = backtrack(graphe, aretes_colories, nouvelles_arete_restantes)
        if result is not None:
            return result
    return None

def main():
    # Création du graphe
    graphe = creer_graphe_sudoku()

    # Dictionnaire pour stocker les arêtes coloriées
    aretes_colories = {}
    
    # Liste des arêtes restantes à colorier
    arete_restantes = list(graphe.edges())
    
    # Appel de la fonction de backtracking
    result = backtrack(graphe, aretes_colories, arete_restantes)
    
    if result is not None:
        print("Coloration trouvée :")
        for arete, couleur in result.items():
            print(f"{arete} : {couleur}")
    else:
        print("Aucune coloration trouvée.")
    
    
            
        






















if __name__ == "__main__":
    main()
