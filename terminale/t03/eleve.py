"""ORCHESTRA NSI — T03 : architecture d'un agent Microduck.
Le capteur n'indique que les obstacles adjacents : pas de carte complète.
Une décision n'est pas encore un déplacement : le monde valide l'action.
"""


class AgentMicroduck:
    def __init__(self, position):
        """Initialiser deux attributs d'instance : position et memoire."""
        self.position = position
        self.memoire = set()

    def percevoir(self, observation):
        """Actualiser l'état interne à partir d'une observation.

        observation est un dictionnaire :
            {"position": (x, y), "obstacles": ((x1, y1), ...)}
        Les obstacles déjà observés doivent rester mémorisés.
        """
        # 1. Affecte la position observée à self.position.
        # 2. Ajoute chaque obstacle observé à self.memoire.
        raise NotImplementedError("Écris la méthode percevoir")

    def decider(self, objectif):
        """Choisir une case voisine, sans modifier les attributs.

        Le terrain mesure 6 colonnes (0 à 5) et 3 lignes (0 à 2).
        Déplacements possibles : Est, Nord, Sud, Ouest, dans cet ordre.
        Exclure les obstacles mémorisés et les cases hors du terrain.
        Choisir la case dont la distance de Manhattan à l'objectif
        est la plus faible ; en cas d'égalité, conserver l'ordre ci-dessus.
        Renvoyer None si l'agent est déjà arrivé ou si aucune case
        voisine n'est accessible.
        """
        raise NotImplementedError("Écris la méthode decider")
