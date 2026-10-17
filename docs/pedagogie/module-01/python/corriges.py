"""Supports enseignants autonomes, sans import tiers ni interface ajoutée.

Copier tout ce fichier dans l'éditeur et Exécuter Python pour les démonstrations.
Les TP03-05 utilisent leur propre modèle textuel, pas la grille de l'application.
"""
from collections import deque
from random import Random

LARGEUR, HAUTEUR = 7, 5
MURS = [(2, 1), (2, 2), (2, 3), (4, 0), (4, 1), (4, 3), (4, 4)]
DIRECTIONS = [("droite", (1, 0)), ("bas", (0, 1)),
              ("haut", (0, -1)), ("gauche", (-1, 0))]


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


def decider_prudent(position, objectif, obstacles):
    """Évaluation NSI : prévenir un refus local, sans promettre un détour."""
    action = decider(position, objectif, obstacles)
    _, effet = appliquer(position, action, obstacles)
    return "arrêt" if effet == "refuse" else action


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
    """TP03 : mémoire explicite entrée/sortie, valable dans une seule exécution."""
    indice = observation["indice"]
    if indice is not None:
        memoire = indice
    position = observation["position"]
    if position == (0, 0):
        action = "droite"
    elif position == (1, 0):
        action = "bas"
    elif position == (1, 1):
        if memoire not in ("bleu", "orange"):
            raise ValueError("Indice non mémorisé")
        action = "gauche" if memoire == "bleu" else "droite"
    else:
        action = "arrêt"
    return action, memoire


def episode_memoire(indice):
    position, memoire, trace = (0, 0), None, []
    objectif = (0, 1) if indice == "bleu" else (2, 1)
    for _ in range(3):
        observation = observer_case(position, indice)
        action, memoire = decider_memoire(observation, memoire)
        suivante, effet = appliquer(position, action, [])
        trace.append((observation, memoire, action, suivante))
        if effet != "accepte":
            raise AssertionError("Commande incorrecte dans ce scénario")
        position = suivante
    return position == objectif, trace


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


CAS = [
    ("C0", (0, 2), (6, 2), [], 6),
    ("C1", (0, 2), (6, 2), MURS, 10),
    ("C2", (0, 2), (0, 2), [], 0),
    ("C3", (0, 2), (6, 2), [(5, 2), (6, 1), (6, 3)], None),
    ("C4", (0, 0), (6, 4), [], 10),
    ("C5", (0, 2), (2, 2), [(1, 2)], 4),
]


def comparer():
    """TP05 : mêmes cas, même borne, aucune moyenne masquant les échecs."""
    lignes = []
    for nom, politique in (("locale", decider), ("bfs", politique_bfs)):
        for identifiant, depart, objectif, obstacles, longueur_min in CAS:
            resultat = executer(politique, depart, objectif, obstacles)
            reussite = resultat["etat"] == "reussite"
            surcout = resultat["deplacements"] - longueur_min if reussite else None
            lignes.append((nom, identifiant, resultat["etat"],
                           resultat["tentatives"], resultat["deplacements"], surcout))
    return lignes


def politique_aleatoire(graine):
    """Extension : générateur local réinitialisable, sans apprentissage ni LLM."""
    generateur = Random(graine)

    def choisir(position, objectif, obstacles):
        if position == objectif:
            return "arrêt"
        possibles = []
        for action, (dx, dy) in DIRECTIONS:
            if libre((position[0] + dx, position[1] + dy), obstacles):
                possibles.append(action)
        return generateur.choice(possibles) if possibles else "arrêt"

    return choisir


if __name__ == "__main__":
    print("TP01", [decider(p, (2, 2), []) for p in [(0, 2), (4, 2), (2, 2)]])
    print("TP02", executer(decider, (0, 2), (6, 2), MURS))
    print("TP03", episode_memoire("bleu"), episode_memoire("orange"))
    print("TP04", chemin_bfs((0, 2), (6, 2), MURS))
    for ligne in comparer():
        print("TP05", ligne)
