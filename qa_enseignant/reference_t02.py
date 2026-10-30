"""Solution de référence T02 — réservée à la vérification, jamais au site élève."""
from pathlib import Path

STARTER = (Path(__file__).resolve().parents[1] / "terminale" / "t02" / "eleve.py").read_text(encoding="utf-8")
REFERENCE = STARTER[:STARTER.index("def chercher_largeur(")] + '''
def chercher_largeur(graphe, depart, objectif):
    if depart not in graphe or objectif not in graphe:
        return []
    file = File()
    file.enfiler(depart)
    parents = {depart: None}
    while not file.est_vide():
        actuel = file.defiler()
        if actuel == objectif:
            chemin = []
            while actuel is not None:
                chemin.append(actuel)
                actuel = parents[actuel]
            return list(reversed(chemin))
        for voisin in graphe[actuel]:
            if voisin not in parents:
                parents[voisin] = actuel
                file.enfiler(voisin)
    return []


def chercher_profondeur(graphe, depart, objectif):
    if depart not in graphe or objectif not in graphe:
        return []
    pile = Pile()
    pile.empiler(depart)
    parents = {depart: None}
    while not pile.est_vide():
        actuel = pile.depiler()
        if actuel == objectif:
            chemin = []
            while actuel is not None:
                chemin.append(actuel)
                actuel = parents[actuel]
            return list(reversed(chemin))
        for voisin in reversed(graphe[actuel]):
            if voisin not in parents:
                parents[voisin] = actuel
                pile.empiler(voisin)
    return []
'''
