"""T04 — Outils, contrats et autorisations d'un agent Microduck.

L'agent propose un appel ; il ne peut pas s'attribuer une autorisation.
L'orchestrateur vérifie l'appel avant que le monde réalise éventuellement une action.

Complète verifier_appel sans utiliser d'import.
"""

def verifier_appel(appel, permissions):
    """Renvoyer un dictionnaire avec exactement deux clés :
        {"statut": "...", "motif": "justification"}

    Les statuts possibles sont :
      "AUTORISÉ" : requête valide sans approbation supplémentaire ;
      "ATTENTE_HUMAINE" : requête valide qui exige un accord humain ;
      "REFUSÉ" : outil interdit, droit absent ou contrat invalide.

    Contrat des outils (les dictionnaires ne contiennent AUCUNE clé supplémentaire) :
      appel = {"outil": nom, "arguments": dictionnaire}

      observer     : arguments == {}                         -> AUTORISÉ si droit
      avancer      : {"direction": "N" / "E" / "S" / "O"}      -> AUTORISÉ si droit
      ouvrir_porte : {"position": (x, y)}                    -> ATTENTE_HUMAINE si droit
                    x est un entier de 0 à 5 et y un entier de 0 à 2
      tout autre outil                                       -> REFUSÉ

    permissions est un ensemble de noms d'outils autorisables.
    Une permission pour ouvrir_porte NE remplace PAS la décision humaine.
    Même si "teleporter" figure dans permissions, l'outil est interdit.
    Un booléen n'est pas une coordonnée de type entier valide (type(v) is int).
    Rejeter tout appel mal formé ou contenant un champ imprévu, même "approuve".
    La fonction ne modifie ni appel ni permissions et ne déclenche aucun effet.
    Dans tous les cas, préciser un motif explicite et non vide.
    """
    # Étape 1 : vérifier les types et les clés de l'appel.
    # Étape 2 : appliquer la liste blanche et contrôler les permissions.
    # Étape 3 : vérifier exactement le contrat de l'outil.
    # Étape 4 : décider si l'accord humain est requis.
    raise NotImplementedError("Écris verifier_appel")
