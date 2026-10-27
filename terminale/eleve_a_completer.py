"""Terminale NSI - séance T01 : BFS avec une file FIFO.

La classe File suit la règle FIFO : le premier sommet ajouté est le premier retiré.
Tu dois écrire toi-même la recherche en largeur et la replanification.
"""

class File:
    """File : le premier élément ajouté est le premier retiré (FIFO)."""
    def __init__(self):
        self.elements = []

    def enfiler(self, valeur):
        self.elements.append(valeur)

    def defiler(self):
        return self.elements.pop(0)

    def est_vide(self):
        return len(self.elements) == 0


class AgentPlanificateur:
    def __init__(self, position):
        self.position = position
        self.plan = []

    def planifier(self, monde, objectif):
        """Renvoie le plus court chemin [départ, ..., arrivée] ou [].

        À faire : utiliser File, monde.voisins et les prédécesseurs.
        """
        raise NotImplementedError("Programme le parcours en largeur")

    def pas_suivant(self, monde, objectif):
        """Renvoie la prochaine case après vérification du plan.

        Si un obstacle apparaît, calcule un nouveau chemin.
        Renvoie None si l'agent doit s'arrêter.
        """
        raise NotImplementedError("Programme la décision et la replanification")
