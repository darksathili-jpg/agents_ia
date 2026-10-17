"""TP02 élève : compléter seulement appliquer, puis relancer les quatre essais.
Usage console autonome ; il n'y a pas de fonction decider pour piloter la grille.
Le marqueur A_COMPLETER est attendu avant modification, pas après réussite.
"""
LARGEUR, HAUTEUR = 7, 5
MURS = [(2, 1), (2, 2), (2, 3), (4, 0), (4, 1), (4, 3), (4, 4)]
DIRECTIONS = {"droite": (1, 0), "gauche": (-1, 0),
              "haut": (0, -1), "bas": (0, 1)}


def libre(position, obstacles):
    x, y = position
    return 0 <= x < LARGEUR and 0 <= y < HAUTEUR and position not in obstacles


def appliquer(position, action, obstacles):
    # Retour attendu : (position apres, resultat).
    # Resultats : accepte, refuse ou arret. Mot inconnu : ValueError.
    raise NotImplementedError("Completer la fonction appliquer")


if __name__ == "__main__":
    essais = [((0, 2), "droite", []), ((1, 2), "droite", MURS),
              ((0, 0), "haut", []), ((0, 2), "arrêt", [])]
    try:
        for position, action, murs in essais:
            print(position, action, appliquer(position, action, murs))
    except NotImplementedError as erreur:
        print("A_COMPLETER_S02", erreur)
