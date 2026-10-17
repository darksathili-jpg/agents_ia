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

def decider(position, objectif, obstacles):
    """TP01 : réagir à une position, sans rechercher un chemin."""
    x, y = position
    cible_x, cible_y = objectif
    if x < cible_x:
        return "droite"
    if x > cible_x:
        return "gauche"
    if y < cible_y:
        return "bas"
    if y > cible_y:
        return "haut"
    return "arrêt"

def executer(politique, depart, objectif, obstacles, limite=35):
    """Conducteur borné fourni : les élèves n'ont pas à le reconstruire en S1.

    Trace : (position avant, commande, position après, résultat).
    Tentatives compte les commandes, déplacements seulement les effets acceptés.
    Contrairement à un retour arrêt demandé trop tôt, départ=cible est un succès.
    """
    if limite < 0 or not libre(depart, obstacles) or not libre(objectif, obstacles):
        raise ValueError("Tâche invalide")
    position, trace, deplacements = depart, [], 0
    etat = "limite"
    for _ in range(limite):
        if position == objectif:
            etat = "reussite"
            break
        action = politique(position, objectif, obstacles)
        suivante, effet = appliquer(position, action, obstacles)
        trace.append((position, action, suivante, effet))
        position = suivante
        if effet != "accepte":
            etat = "bloque" if effet == "refuse" else "arret"
            break
        deplacements += 1
    if position == objectif:
        etat = "reussite"
    return {"etat": etat, "position": position, "trace": trace,
            "tentatives": len(trace), "deplacements": deplacements}

def chemin_bfs(depart, objectif, obstacles):
    """TP04 : file FIFO, sommets visités et prédécesseurs, coûts unitaires."""
    if not libre(depart, obstacles) or not libre(objectif, obstacles):
        raise ValueError("Tâche invalide")
    file = deque([depart])
    precedent = {depart: None}
    while file:
        position = file.popleft()
        if position == objectif:
            chemin = []
            while precedent[position] is not None:
                avant, action = precedent[position]
                chemin.append(action)
                position = avant
            return list(reversed(chemin))
        for action, (dx, dy) in DIRECTIONS:
            suivante = (position[0] + dx, position[1] + dy)
            if libre(suivante, obstacles) and suivante not in precedent:
                precedent[suivante] = (position, action)
                file.append(suivante)
    return None

def politique_bfs(position, objectif, obstacles):
    chemin = chemin_bfs(position, objectif, obstacles)
    return chemin[0] if chemin else "arrêt"

def comparer():
    raise NotImplementedError("Evaluer les politiques sur tous les cas")

CAS = [
    ("C0", (0, 2), (6, 2), [], 6),
    ("C1", (0, 2), (6, 2), MURS, 10),
    ("C2", (0, 2), (0, 2), [], 0),
    ("C3", (0, 2), (6, 2), [(5, 2), (6, 1), (6, 3)], None),
    ("C4", (0, 0), (6, 4), [], 10),
    ("C5", (0, 2), (2, 2), [(1, 2)], 4),
]

if __name__ == "__main__":
    try:
        print(comparer())
    except NotImplementedError as erreur:
        print("A_COMPLETER_TP05", erreur)
