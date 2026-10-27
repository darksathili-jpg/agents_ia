"""Grille (graphe non orienté) : composant fourni à l'élève de Terminale."""


class Monde:
    """Chaque case libre est un sommet ; chaque voisin orthogonal est une arête."""

    def __init__(self, largeur, hauteur, obstacles=()):
        if largeur < 1 or hauteur < 1:
            raise ValueError("Dimensions incorrectes")
        self.largeur, self.hauteur = largeur, hauteur
        self.obstacles = set(obstacles)
        if not all(self.dans_grille(case) for case in self.obstacles):
            raise ValueError("Obstacle hors grille")

    def dans_grille(self, case):
        x, y = case
        return 0 <= x < self.largeur and 0 <= y < self.hauteur

    def est_libre(self, case):
        return self.dans_grille(case) and case not in self.obstacles

    def voisins(self, case):
        x, y = case
        possibles = ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
        return [c for c in possibles if self.est_libre(c)]

    def ajouter_obstacle(self, case):
        if not self.dans_grille(case):
            raise ValueError("Obstacle hors grille")
        self.obstacles.add(case)
