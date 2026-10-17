"""TP03 autonome : copier tout ce fichier dans la console du laboratoire.

Le conducteur conserve explicitement la mémoire dans UNE exécution.
Les fonctions du contrôleur ne reçoivent jamais la couleur cachée du monde.
"""
from random import Random

POSITIONS = ((0, 0), (1, 0), (1, 1), (0, 1), (2, 1))
MEMOIRES = (None, "bleu", "orange")
DIRECTIONS = {"droite": (1, 0), "bas": (0, 1),
              "gauche": (-1, 0), "haut": (0, -1), "arrêt": (0, 0)}


def mouvement(position, action):
    if position not in POSITIONS or action not in DIRECTIONS:
        raise ValueError("Position ou action invalide")
    dx, dy = DIRECTIONS[action]
    candidate = (position[0] + dx, position[1] + dy)
    return candidate if candidate in POSITIONS else position


def commander(observation, memoire):
    """Décision avec une mémoire déjà actualisée ; arrêt si indice inconnu."""
    position = observation["position"]
    if position == (0, 0):
        return "droite"
    if position == (1, 0):
        return "bas"
    if position == (1, 1):
        if memoire == "bleu":
            return "gauche"
        if memoire == "orange":
            return "droite"
    return "arrêt"


def oublier(observation, memoire):
    # Une règle réflexe : la même entrée courante donne la même action.
    if observation["position"] == (1, 1):
        return "gauche", None
    return commander(observation, None), None


def ecraser(observation, memoire):
    # Erreur volontaire : None signifie non visible, pas « effacer ».
    memoire = observation["indice"]
    return commander(observation, memoire), memoire


def retenir(observation, memoire):
    if memoire not in MEMOIRES or observation["indice"] not in MEMOIRES:
        raise ValueError("Couleur inconnue")
    # Mettre à jour seulement quand le capteur fournit une couleur.
    if observation["indice"] is not None:
        memoire = observation["indice"]
    return commander(observation, memoire), memoire


def a_completer(observation, memoire):
    """Remplacer ce corps, sans changer le contrat (action, mémoire)."""
    return "arrêt", memoire


def episode(controleur, couleur, visible=True, initiale=None, budget=3):
    if couleur not in ("bleu", "orange") or initiale not in MEMOIRES:
        raise ValueError("Monde ou mémoire invalide")
    if type(budget) is not int or not 0 <= budget <= 3:
        raise ValueError("Budget entier entre 0 et 3 requis")
    position, memoire, trace = (0, 0), initiale, []
    cible = (0, 1) if couleur == "bleu" else (2, 1)
    for pas in range(budget):
        observation = {"position": position,
                       "indice": couleur if visible and position == (0, 0) else None}
        avant = memoire
        action, suivante = controleur(dict(observation), memoire)
        if suivante not in MEMOIRES:
            raise ValueError("Mémoire retournée invalide")
        apres = mouvement(position, action)
        trace.append((pas, observation, avant, action, suivante, apres))
        memoire, position = suivante, apres
        if position == cible:
            return "réussite", trace
        if position in ((0, 1), (2, 1)):
            return "mauvaise sortie", trace
        if action == "arrêt":
            return "arrêt", trace
        if position == observation["position"]:
            return "refus", trace
    return "budget épuisé", trace


def choix_stochastique(tirage):
    """Politique à la bifurcation, sans couleur : deux commandes possibles."""
    if tirage not in (0, 1):
        raise ValueError("Tirage 0 ou 1 requis")
    return "gauche" if tirage == 0 else "droite"


def serie_actions(graine, nombre=8):
    if type(nombre) is not int or nombre < 0:
        raise ValueError("Nombre entier positif ou nul requis")
    generateur = Random(graine)
    return [choix_stochastique(generateur.randrange(2)) for _ in range(nombre)]


if __name__ == "__main__":
    for controleur in (oublier, ecraser, retenir):
        for couleur in ("bleu", "orange"):
            resultat, trace = episode(controleur, couleur)
            print(controleur.__name__, couleur, resultat)
            for ligne in trace:
                print(ligne)
    print("Indice absent", episode(retenir, "bleu", visible=False)[0])
    print("Mémoire erronée non corrigée", episode(retenir, "orange", False, "bleu")[0])
    print("Politique stochastique", serie_actions(7))
    print("TP03_S03_OK")
