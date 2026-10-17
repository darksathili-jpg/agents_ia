def decider(position, objectif, obstacles):
    x, y = position
    gx, gy = objectif
    if x < gx:
        return "droite"
    if x > gx:
        return "gauche"
    if y < gy:
        return "bas"
    if y > gy:
        return "haut"
    return "arrêt"

assert decider((0, 2), (2, 2), []) == "droite"
assert decider((4, 2), (2, 2), []) == "gauche"
assert decider((2, 2), (2, 2), []) == "arrêt"
assert decider((2, 2), (2, 1), []) == "haut"
print("S01_CORRECTION_OK")
