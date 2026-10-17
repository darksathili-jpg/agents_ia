"""Support initial volontairement incomplet. Fonctions auxiliaires fournies.
Le message A_COMPLETER est attendu avant le travail, pas une validation du TP.
"""
from collections import deque

LARGEUR, HAUTEUR = 7, 5
MURS = [(2, 1), (2, 2), (2, 3), (4, 0), (4, 1), (4, 3), (4, 4)]
DIRECTIONS = [("droite", (1, 0)), ("bas", (0, 1)), ("haut", (0, -1)), ("gauche", (-1, 0))]

def libre(position, obstacles):
    x, y = position
    return 0 <= x < LARGEUR and 0 <= y < HAUTEUR and position not in obstacles

def chemin_bfs(depart, objectif, obstacles):
    raise NotImplementedError("Construire le chemin ou retourner None")

if __name__ == "__main__":
    try:
        print(chemin_bfs((0, 2), (6, 2), MURS))
    except NotImplementedError as erreur:
        print("A_COMPLETER_TP04", erreur)
