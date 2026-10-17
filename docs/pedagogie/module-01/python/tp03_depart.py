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

def appliquer(position, action, obstacles):
    """TP02 : commande et effet distincts ; un refus ne traverse pas le mur."""
    if action == "arrêt":
        return position, "arret"
    for nom, (dx, dy) in DIRECTIONS:
        if action == nom:
            suivante = (position[0] + dx, position[1] + dy)
            if libre(suivante, obstacles):
                return suivante, "accepte"
            return position, "refuse"
    raise ValueError("Action inconnue : " + str(action))

def observer_case(position, indice):
    """TP03 : grille 3x2 ; en dehors du départ, la couleur-indice est masquée.

    Départ (0,0), couloir (1,0), bifurcation (1,1).
    Sortie gauche (0,1) si indice=bleu, droite (2,1) si indice=orange.
    La position reste observable ; la couleur ne l'est plus.
    """
    if indice not in ("bleu", "orange"):
        raise ValueError("Indice inconnu")
    if position not in ((0, 0), (1, 0), (1, 1), (0, 1), (2, 1)):
        raise ValueError("Case inconnue")
    return {"position": position, "indice": indice if position == (0, 0) else None}

def decider_memoire(observation, memoire):
    raise NotImplementedError("Retourner action et nouvelle memoire")

if __name__ == "__main__":
    try:
        print(decider_memoire(observer_case((0, 0), "bleu"), None))
    except NotImplementedError as erreur:
        print("A_COMPLETER_TP03", erreur)
