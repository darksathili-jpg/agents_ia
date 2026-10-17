"""TP01 élève : code initial complet à copier dans l'éditeur Python.

Pré-requis : fonction, condition, return, tuple et comparaison d'entiers.
Le retour constant est volontaire : prévoir son effet avant de le modifier.
"""


def decider(position, objectif, obstacles):
    # À modifier : choisir une action à partir de position et objectif.
    return "arrêt"


cas = [((0, 2), (2, 2)), ((4, 2), (2, 2)), ((2, 2), (2, 2))]
for position, objectif in cas:
    print(position, objectif, decider(position, objectif, []))

assert decider((2, 2), (2, 2), []) == "arrêt"
print("DEPART_TP01_OK : retour constant, à améliorer")
