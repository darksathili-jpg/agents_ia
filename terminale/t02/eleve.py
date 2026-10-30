"""T02 — Comparer deux parcours de graphe.

Le graphe est un dictionnaire : chaque sommet (x, y) est associé à ses voisins.
Les voisins sont fournis dans un ordre défini par le terrain.

Consigne :
- chercher_largeur : utiliser File, renvoyer un plus court chemin ou [].
- chercher_profondeur : utiliser Pile, renvoyer un chemin valide ou [].
- départ = objectif : renvoyer [depart].

Chaque chemin est une liste de tuples (x, y).
"""

class File:
    def __init__(self):
        self.elements = []

    def enfiler(self, sommet):
        self.elements.append(sommet)

    def defiler(self):
        return self.elements.pop(0)

    def est_vide(self):
        return len(self.elements) == 0


class Pile:
    def __init__(self):
        self.elements = []

    def empiler(self, sommet):
        self.elements.append(sommet)

    def depiler(self):
        return self.elements.pop()

    def est_vide(self):
        return len(self.elements) == 0


def chercher_largeur(graphe, depart, objectif):
    """Renvoie le plus court chemin de depart à objectif, ou []."""
    # Utilise une File et un dictionnaire des prédécesseurs.
    raise NotImplementedError("Écris le parcours en largeur")


def chercher_profondeur(graphe, depart, objectif):
    """Renvoie un chemin valide de depart à objectif, ou []."""
    # Utilise une Pile et un dictionnaire des prédécesseurs.
    raise NotImplementedError("Écris le parcours en profondeur")
