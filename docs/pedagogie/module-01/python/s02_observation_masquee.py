"""Grille textuelle 3x2 : parcours imposé, pas un agent autonome ni une UI.

    (0,0) départ -> (1,0) couloir ; (2,0) mur
    (0,1) sortie <- (1,1) bifurcation -> (2,1) sortie
L'indice visible au départ autorise gauche si bleu, droite si orange.
Chaque parcours est entièrement exécuté en une fois dans la console.
"""
POSITIONS = [(0, 0), (1, 0), (1, 1), (0, 1), (2, 1)]


def observer(position, indice):
    if position not in POSITIONS or indice not in ("bleu", "orange"):
        raise ValueError("Situation invalide")
    return {"position": position, "indice": indice if position == (0, 0) else None}


def avancer(position, action):
    if position not in POSITIONS:
        raise ValueError("Case inconnue")
    if action == "arrêt":
        return position
    directions = {"droite": (1, 0), "bas": (0, 1), "gauche": (-1, 0), "haut": (0, -1)}
    if action not in directions:
        raise ValueError("Commande inconnue")
    dx, dy = directions[action]
    candidate = (position[0] + dx, position[1] + dy)
    return candidate if candidate in POSITIONS else position


def historique(indice):
    position = (0, 0)
    observations = [observer(position, indice)]
    for commande in ("droite", "bas"):
        position = avancer(position, commande)
        observations.append(observer(position, indice))
    return observations


if __name__ == "__main__":
    for indice in ("bleu", "orange"):
        print("Monde", indice)
        for observation in historique(indice):
            print(observation)
    print("OBSERVATION_MASQUEE_S02_OK")
