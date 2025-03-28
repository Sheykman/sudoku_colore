import random
from sage.all import Graph
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

def est_valide(graphe, sommet, couleur, sommets_colories):
    for voisin in graphe.neighbors(sommet):
        if voisin in sommets_colories and sommets_colories[voisin] == couleur:
            return False
    return True 

def generer_sudoku_initial(graphe, nombre_cases_remplies=20):
    sommets = list(graphe.vertices())
    sommets_colories = {}
    
    # Mélanger les sommets pour les remplir de manière aléatoire
    random.shuffle(sommets)
    
    for sommet in sommets[:nombre_cases_remplies]:
        couleurs_possibles = list(range(1, 10))  # Valeurs de 1 à 9
        random.shuffle(couleurs_possibles)
        
        for couleur in couleurs_possibles:
            # Vérifier si la couleur est valide
            if est_valide(graphe, sommet, couleur, sommets_colories):
                sommets_colories[sommet] = couleur
                break
    
    return sommets_colories

def backtracking(graphe, sommets_restants, sommets_colories):
    if not sommets_restants:
        return sommets_colories
    
    sommet = sommets_restants[0]
    
    # Si le sommet est déjà colorié (case préremplie), on le saute
    if sommet in sommets_colories:
        return backtracking(graphe, sommets_restants[1:], sommets_colories)
    
    # Essayer toutes les couleurs possibles
    for couleur in range(1, 10):
        if est_valide(graphe, sommet, couleur, sommets_colories):
            nouvelle_coloration = sommets_colories.copy()
            nouvelle_coloration[sommet] = couleur
            
            resultat = backtracking(graphe, sommets_restants[1:], nouvelle_coloration)
            
            if resultat is not None:
                return resultat
    
    return None

def creer_sudoku(nombre_cases_remplies=20):
    # Créer le graphe du Sudoku
    graphe = creer_graphe_sudoku()
    
    # Générer les cases préremplies
    sudoku_initial = generer_sudoku_initial(graphe, nombre_cases_remplies)
    print("Cases préremplies")
    afficher_sudoku(sudoku_initial)
    
    # Compléter le Sudoku avec backtracking
    sommets = list(graphe.vertices())
    sudoku_complet = backtracking(graphe, sommets, sudoku_initial)
    
    if sudoku_complet is None:
        raise ValueError("Impossible de générer un Sudoku valide")
    
    return sudoku_complet

def afficher_sudoku(sudoku):
    # Créer une grille 9x9
    grille = [[0 for _ in range(9)] for _ in range(9)]
    
    # Remplir la grille
    for sommet, valeur in sudoku.items():
        # Extraire les coordonnées à partir du nom du sommet
        colonne = int(sommet[0]) - 1
        bloc = sommet[1]
        ligne = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'].index(bloc)
        
        grille[ligne][colonne] = valeur
    
    # Affichage
    print("Sudoku généré :")
    for i, ligne in enumerate(grille):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        
        ligne_formatee = []
        for j, val in enumerate(ligne):
            if j % 3 == 0 and j != 0:
                ligne_formatee.append("|")
            
            # Si cases_premplies_uniquement est True, n'afficher que les cases non nulles
            if val != 0:
                ligne_formatee.append(str(val) if val != 0 else '.')
            else:
                ligne_formatee.append('.')
        
        print(" ".join(ligne_formatee))

def main():
    # Générer un Sudoku avec 20 cases préremplies
    sudoku_complet = creer_sudoku(nombre_cases_remplies=20)
    print("\nSudoku complet :")
    afficher_sudoku(sudoku_complet)

if __name__ == "__main__":
    main()