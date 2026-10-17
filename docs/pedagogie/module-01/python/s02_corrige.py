"""TP02 corrigé et contraste déterministe/stochastique. Console seulement.
La politique fixe la commande droite ; le tirage affecte uniquement son effet.
"""
from random import Random

LARGEUR, HAUTEUR = 7, 5
MURS = [(2, 1), (2, 2), (2, 3), (4, 0), (4, 1), (4, 3), (4, 4)]
DIRECTIONS = {"droite": (1, 0), "gauche": (-1, 0),
              "haut": (0, -1), "bas": (0, 1)}


def libre(position, obstacles):
    x, y = position
    return 0 <= x < LARGEUR and 0 <= y < HAUTEUR and position not in obstacles


def appliquer(position, action, obstacles):
    if not libre(position, obstacles):
        raise ValueError("Position initiale invalide")
    if action == "arrêt":
        return position, "arret"
    if action not in DIRECTIONS:
        raise ValueError("Commande inconnue")
    dx, dy = DIRECTIONS[action]
    candidate = (position[0] + dx, position[1] + dy)
    if libre(candidate, obstacles):
        return candidate, "accepte"
    return position, "refuse"


def appliquer_avec_glissement(position, action, obstacles, tirage):
    # 0 : le robot patine ; 1 : il exécute le déplacement demandé si libre.
    # Paramètre explicite pour tester tous les effets sans hasard fragile.
    if tirage not in (0, 1):
        raise ValueError("Tirage attendu : 0 ou 1")
    suivante, resultat = appliquer(position, action, obstacles)
    if resultat == "accepte" and tirage == 0:
        return position, "patine"
    return suivante, resultat


def essais_glissement(graine, nombre=8):
    if nombre < 0:
        raise ValueError("Nombre négatif")
    generateur = Random(graine)
    # Remise au même état avant CHAQUE essai : ce ne sont pas huit pas successifs.
    return [appliquer_avec_glissement((0, 2), "droite", [], generateur.randrange(2))
            for _ in range(nombre)]


if __name__ == "__main__":
    position = (0, 2)
    for _ in range(2):
        avant = position
        position, resultat = appliquer(position, "droite", MURS)
        print("obstacle", avant, "droite", position, resultat)
    print("deux effets possibles", appliquer_avec_glissement((0, 2), "droite", [], 0),
          appliquer_avec_glissement((0, 2), "droite", [], 1))
    print("tirages graine 7", essais_glissement(7))
    print("CORRIGE_S02_OK")
