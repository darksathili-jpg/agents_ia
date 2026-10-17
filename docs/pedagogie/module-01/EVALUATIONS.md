# Évaluations — sujets et barèmes

**Propositions pour S5 : 60 min**, sans accès au corrigé. Deux variantes sur 20, répondant à la même répartition **4 + 5 + 7 + 4**. Les contrôles formatifs du pilote ne sont pas une certification du module. Ces épreuves anticipent l’alignement de la progression ; leur passation attend la rédaction/validation des séances suivantes.

## Retour formatif du pilote S1

**Mise à jour S01.1/S02 :** S01 commence désormais par un diagnostic de huit minutes, sans note, corrigé dans `CORRIGES.md`. Le bilan S02 B1–B5 et ses critères sont dans `SEANCE_02.md` et `SUPPORT_ELEVE_S02.md` ; correction séparée. Ces deux contrôles formatifs s’ajoutent à l’alignement du dossier sans rédiger S03–S05 ni modifier les épreuves finales proposées ci-dessous.

Billet de sortie (10 min inclus dans S1) : schéma observation/politique/action/environnement, exemple de recouvrement automate-agent, différence entre notre Python et un agent LLM, test manquant de sa fonction. Réussite proposée : trois éléments corrects sur quatre, dont la distinction commande/effet ; remédiation courte avant la séance suivante si celle-ci manque. Ne pas noter uniquement les définitions récitées.

## Variante A — NSI

Matériel autorisé : dictionnaire des noms d’actions, aide Python du langage, auxiliaire `appliquer` fourni et testé par l’enseignant. Première : coordonnées et schéma de la grille fournis ; aucune implémentation de BFS exigée. Terminale : la question de transfert peut demander le rôle de FIFO, sans changer le barème.

**Partie 1 — Définir et distinguer (10 min, 4 points).** Sur le cas d’un personnage de jeu qui reçoit position et murs, renvoie une commande puis observe son résultat : définir observation, politique et action (2 points). Expliquer pourquoi un automate et un agent ne sont pas nécessairement exclusifs (1 point). Dire pourquoi l’interface textuelle ne suffit pas à conclure à un LLM (1 point).

**Partie 2 — Analyser une trace (15 min, 5 points).** Départ `(0,2)`, cible `(6,2)`, mur `(2,2)`, politique horizontale. Prédire et justifier les deux tentatives (2 points), expliquer la position finale et le refus (1 point), distinguer nombre de tentatives et nombre de déplacements acceptés (1 point), proposer un cas discriminant pour départager retour constant et comparaison de coordonnées (1 point).

**Partie 3 — Programmer (25 min, 7 points).** À partir du squelette TP01, écrire `prudente(position, objectif, obstacles)` : renvoyer arrêt à l’arrivée ; sinon proposer une direction qui rapproche horizontalement puis verticalement ; si cette commande serait refusée par `appliquer`, renvoyer arrêt. Le programme n’a pas à inventer de détour. Fournir au moins trois tests, dont arrivée et mur. Le code s’exécute réellement dans la console du laboratoire, pas dans un faux moteur de notation.

Barème analytique : arrivée 1 ; sélection horizontale/verticale 2 ; vérification de l’effet de la candidate 2 ; contrat et retours 1 ; tests discriminants 1. Une solution différente correctement spécifiée et répondant aux exigences est recevable. Une simple suite d’actions écrites pour la carte connue ne remplit pas la demande.

**Partie 4 — Interpréter (10 min, 4 points).** Un rapport indique « BFS réussit 5 cartes sur 6 ; le trajet moyen des échecs vaut zéro ; cela prouve sa robustesse sur tout environnement ». Corriger métrique et conclusion (2 points), expliquer le rôle d’un cas impossible (1 point), distinguer outil de planification et modèle de langage dans un futur système (1 point).

## Variante B — Approfondissement enseignant

**Partie 1 — Cadres scientifiques (10 min, 4 points).** Définir une politique à historique et ses symboles (2 points) ; distinguer autonomie opérationnelle et rationalité relative à un critère (1 point) ; donner une limite d’une classification agent/chatbot/automate (1 point).

**Partie 2 — Argumenter sur l’information (15 min, 5 points).** Reprendre la grille TP03. Deux indices initiaux différents mènent à une même observation de bifurcation, mais exigent deux sorties différentes. Démontrer l’insuffisance d’une politique déterministe de l’observation seule (2 points), proposer une mémoire suffisante pour ce cas (1 point), expliquer pourquoi cela ne constitue pas un modèle complet du monde (1 point), distinguer hasard de politique et hasard de transition (1 point).

**Partie 3 — Programmer un contrôleur à mémoire (25 min, 7 points).** Avec la fonction d’observation et le conducteur du TP03 fournis, reconstruire `decider_memoire(observation, memoire)` sans lire l’indice caché de l’environnement. Retourner action et nouvelle mémoire. Traiter les deux couleurs, la bifurcation, l’arrivée et l’absence de mémoire. Écrire un test de non-effacement et un test de discrimination. L’exécution se fait en une seule boucle console : aucune modification de Worker.

Barème : mise à jour seulement si indice présent 2 ; actions des étapes et bifurcation 2 ; retour et absence d’accès clandestin 1 ; absence d’information signalée 1 ; tests des deux histoires 1.

**Partie 4 — Critique et transposition (10 min, 4 points).** Concevoir un protocole distinguant l’apport de la mémoire du simple changement de carte (1 point), justifier les limites d’une réussite sur deux cas (1 point), préciser une condition de validité de l’optimalité de BFS (1 point), formuler une question NSI déconstruisant « une décision exige un LLM » (1 point).

## Critères communs, erreurs et remédiation

Seuil pédagogique proposé : **12/20, dont 4/7 en code**, et distinction commande/effet explicitée dans une reprise si nécessaire. Ce seuil doit être validé avec le commanditaire. La qualité de l’analyse peut être reconnue même après une erreur de syntaxe corrigée ; elle ne remplace pas l’exigence d’exécution du programme.

Erreurs fréquentes : sortie imprimée mais non retournée, absence de cas terminal, mémoire écrasée par `None`, accès direct à une variable cachée, échecs convertis en longueur zéro, succès empirique présenté comme preuve. Remédiations : appel isolé, table de vérité des branches, deux historiques écrits côte à côte, recalcul manuel d’un indicateur, contre-exemple demandé.

En cas d’incident réseau, conserver le code et proposer une reprise d’exécution ; ne pas substituer une animation simulée à du Python annoncé réel. Un lecteur d’écran ou une adaptation de temps peut être nécessaire : la durée de 60 min est une base de conception, pas une restriction d’aménagement. Corrections complètes et exemples de réponses sont dans le document enseignant séparé.
