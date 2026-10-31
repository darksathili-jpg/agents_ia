"""T05 — Contrôler un rapport d'agent avec un registre de preuves indépendant.

Aucune instruction ne déplace directement Microduck : le monde agit seulement
après la validation de l'orchestrateur.
"""

def controler_mission(mission, rapport, registre):
    """Retourne exactement {"etat": "...", "motif": "..."}.

    États de sortie possibles :
        BLOQUÉE         : anomalie, violation de permission, mensonge, échec.
        ATTENTE_HUMAINE : preuves conformes mais approbation manquante.
        VALIDÉE         : vérification indépendante réussie.

    mission (dictionnaire) :
        revision               chaîne de caractères de la révision attendue
        fichiers_autorises     ensemble des chemins autorisés
        tests_requis           ensemble des tests obligatoires
        approbation_requise    booléen
        decision_humaine       None, True (accord), False (refus)

    rapport (dictionnaire NON FIABLE venant de l'agent) :
        revision               révision déclarée
        fichiers_modifies      liste des fichiers effectivement déclarés
        preuves                liste des identifiants des preuves annoncées
        succes_annonce         booléen

    registre (dictionnaire FIABLE fourni par le banc de tests) :
        pour chaque identifiant de preuve :
        {"test": nom_du_test, "revision": revision_verifiee, "reussi": True/False}

    Contrat :
      - rejeter un dictionnaire mal formé ou avec des clés supplémentaires ;
      - rejeter toute modification hors périmètre et tout fichier dupliqué ;
      - vérifier chaque preuve auprès du REGISTRE, pas du rapport ;
      - rejeter toute preuve inconnue, dupliquée, échouée, portant sur
        une autre révision ou sur un test qui n'est pas requis ;
      - vérifier qu'il existe exactement une preuve valide pour CHAQUE
        test obligatoire ;
      - si l'agent annonce un échec, bloquer ;
      - après seulement, vérifier l'approbation humaine éventuelle ;
      - ne pas modifier les trois paramètres.
    Les raisons de refus sont de vraies situations du laboratoire.

    Attention : un rapport indiquant "succes_annonce": True ne prouve rien.
    Un accord écrit par l'agent lui-même dans le rapport est interdit.
    Le registre est indépendant de l'agent dans cette simulation.
    """
    # Étape 1 : valider la structure des dictionnaires.
    # Étape 2 : valider la révision et les fichiers modifiés.
    # Étape 3 : récupérer les preuves par identifiant dans le registre.
    # Étape 4 : confronter les tests réellement réussis aux tests requis.
    # Étape 5 : attendre une décision humaine si nécessaire.
    raise NotImplementedError("Écris la fonction controler_mission")
