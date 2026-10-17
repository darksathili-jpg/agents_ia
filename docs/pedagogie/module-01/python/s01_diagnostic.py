"""Diagnostic S01.1 : prédire avant Exécuter Python, aucune animation de grille."""


def choisir_x(x, cible_x):
    if x < cible_x:
        return "droite"
    if x > cible_x:
        return "gauche"
    return "arrêt"


def annoncer():
    print("haut")


if __name__ == "__main__":
    print("D1", choisir_x(1, 4))
    print("D2", choisir_x(4, 1))
    print("D3", choisir_x(2, 2))
    resultat = annoncer()
    print("D4 retour", resultat)
    print("D5 coordonnées", (3, 1)[0], (3, 1)[1])
    print("DIAGNOSTIC_S01_OK")
