"""T07 — Audit de journal d'un agent, preuve indépendante et reconstitution.

Le journal est une déclaration non fiable. Le registre provient du banc
de tests indépendant (simulation). Cette fonction n'exécute aucune action.
"""

def auditer_journal(mission, journal, registre):
    """Retourne exactement {"etat": "...", "motif": "..."}.

    États de sortie : "ANOMALIE", "ATTENTE_HUMAINE", "CONFORME".

    mission (dictionnaire) :
       revision          chaîne de révision des événements attendus
       depart            tuple (x, y) de la case initiale
       objectif          tuple (x, y) de la case d'arrivée attendue
       outils_autorises  ensemble de noms d'outils, notamment observer et avancer
       accord_requis     booléen
       decision_humaine  None (en attente), True (accord), False (refus)

    journal (liste chronologique non fiable de dictionnaires) :
       sequence          variable de type entier ; 0, 1, 2, etc., sans trou
       type              "DEBUT", "OBSERVATION", "DEPLACEMENT" ou "FIN"
       revision          chaîne ; doit correspondre à la mission
       position          tuple (x, y) de la case déclarée
       preuve            None sauf déplacement : identifiant de preuve

    registre (dictionnaire indépendant de l'agent) :
       identifiant -> {"revision": ..., "outil": "avancer",
                       "origine": (x, y), "destination": (x, y),
                       "reussi": True ou False}

    Exigences :
    - Rejeter toute structure incorrecte ou contenant des clés imprévues.
    - Le journal commence par DEBUT à la case de départ, sequence=0.
    - Avant chaque DEPLACEMENT, l'événement précédent est OBSERVATION
      et sa position est la position courante.
    - Un DEPLACEMENT va sur une case voisine orthogonale du terrain 6 × 3,
      validé par une preuve unique, nouvelle, réussie et portant
      sur la bonne révision, avec exactement la bonne origine et destination.
    - Le registre doit attester que l'outil utilisé est "avancer".
    - FIN est le dernier événement, à la position de l'objectif.
    - Les outils observer et avancer sont autorisés explicitement.
    - Aucune approbation ne peut provenir du journal de l'agent.
    - Si l'accord humain est requis et encore absent, ATTENTE_HUMAINE.
      Si l'accord humain est refusé, ANOMALIE ; sinon CONFORME.
    - Ne modifier aucun paramètre ni provoquer aucun déplacement réel.

    Un journal cohérent seul n'est PAS une preuve cryptographique d'authenticité.
    Il est comparé aux observations du registre dans ce laboratoire.
    """
    # 1. Vérifie le contrat de la mission et les clés des événements.
    # 2. Initialise une variable position à la position de départ.
    # 3. Parcours le journal avec une boucle bornée et contrôle la séquence.
    # 4. Pour chaque déplacement, consulte le registre indépendant,
    #    puis affecte la destination vérifiée à position.
    # 5. Contrôle FIN, la cible et l'éventuel accord humain.
    raise NotImplementedError("Écris auditer_journal")
