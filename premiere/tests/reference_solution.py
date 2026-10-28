"""Référence exclusivement destinée aux tests enseignants ; ne pas publier."""
REFERENCE_SOLUTION = '''def decider(observation):
    if observation["arrive"]:
        return "STOP"
    if not observation["devant_libre"]:
        return "TOURNER_DROITE"
    if observation["orientation"] == observation["balise"]:
        return "AVANCER"
    return "TOURNER_DROITE"
'''
