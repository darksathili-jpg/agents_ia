"""T06 — Retour à un point sûr après une anomalie de Microduck.

Aucune action ne doit reprendre avant une validation indépendante.
Complète uniquement la fonction ci-dessous.
"""

def decider_reprise(mission, incident, correctif, registre):
    """Retourne exactement {"etat": "...", "motif": "..."}.

    États possibles :
      BLOQUÉE          : défaut, preuve absente, ancien test, droit refusé ;
      ATTENTE_HUMAINE  : tout est conforme mais l'accord humain manque ;
      REPRISE_AUTORISÉE : toutes les conditions sont validées.

    mission :
      revision_cible       chaîne représentant la nouvelle révision
      fichiers_autorises   ensemble des fichiers que l'on peut modifier
      tests_requis         ensemble des tests obligatoires à refaire
      approbation_requise  booléen
      decision_humaine     None, True (accord) ou False (refus)
      position_reprise     tuple (x, y), point sûr validé

    incident :
      etat                  doit être "BLOQUÉE"
      revision              révision dans laquelle l'incident est survenu
      position_sure         tuple (x, y), dernier point sûr observé
      cause                 chaîne non vide

    correctif NON FIABLE (rapport de l'agent) :
      revision              doit être la nouvelle révision attendue
      fichiers_modifies     liste de fichiers modifiés
      preuves               liste d'identifiants du registre
      succes_annonce        booléen (une annonce seule ne prouve rien)

    registre indépendant (simulation pédagogique) :
      chaque identifiant de preuve référence un dictionnaire :
      {"test": nom, "revision": revision, "reussi": True/False}

    Exigences :
      - refuser une structure invalide ou une clé supplémentaire ;
      - la révision cible doit différer de la révision de l'incident ;
      - les deux points sûrs doivent être identiques, sur une grille 6 × 3,
        avec des coordonnées de type entier (les booléens sont interdits) ;
      - aucun fichier déclaré ne sort du périmètre ;
      - chaque test requis doit avoir UNE preuve nouvelle et réussie,
        sur la révision cible, récupérée par identifiant dans le registre ;
      - rejeter preuves inventées, échouées, dupliquées et périmées ;
      - demander un accord humain si la mission le requiert, même si
        l'agent déclare lui-même être autorisé ;
      - ne modifier ni mission, ni incident, ni correctif, ni registre ;
      - ne provoquer aucun déplacement de Microduck.
    """
    # 1. Contrôler les clés, les types et l'état de l'incident.
    # 2. Vérifier le nouveau numéro de révision et le point de reprise sûr.
    # 3. Vérifier le périmètre des modifications.
    # 4. Consulter les preuves nouvelles dans le registre indépendant.
    # 5. Traiter le besoin éventuel de validation humaine.
    raise NotImplementedError("Complète la fonction decider_reprise")
