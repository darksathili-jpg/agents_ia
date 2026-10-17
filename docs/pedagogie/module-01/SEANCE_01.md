# Séance 01 — Qu’est-ce qu’un agent intelligent ?

**Fiche élève — 120 minutes.** Objectifs O1, O3, O4, O5. Prérequis : appeler une fonction, lire `if` et `return`, comprendre deux coordonnées. La séance ne demande ni graphes, ni classe Python, ni réseau neuronal. Matériel : navigateur, laboratoire ouvert, feuille de trace et code de départ fourni. L’enseignant utilise en parallèle le parcours de préparation distinct.

## A. Situation-problème — 0 à 10 min

Microduck doit atteindre la case verte. Il reçoit la position de départ `(0,2)` et la destination `(6,2)`. Une règle lui fait choisir « droite » lorsque la cible est à droite. Devant un mur, il se bloque.

**Question à résoudre : comment un programme peut-il choisir une action pertinente, sans comprendre la scène comme une personne ?** Sur votre feuille, dessinez le programme entouré des informations qui entrent et des commandes qui sortent. Ne cherchez pas encore à construire un meilleur trajet : il faut d’abord expliquer ce qui se passe.

Individuellement, écrivez une prédiction de la première action et une raison. En binôme, comparez deux raisons différentes. Une hypothèse doit pouvoir être confrontée à une observation : « il est intelligent » ne permet pas à elle seule de prédire où il ira.

## B. Observer — 10 à 18 min

Dans le laboratoire, choisir la politique gloutonne, puis **Réinitialiser**. Cliquer deux fois sur **Exécuter une étape**, en lisant le journal après chaque clic. Si le deuxième pas est refusé, noter la position conservée ; ne pas confondre le bouton actionné avec un déplacement accompli.

| Tentative | Position avant | Information utilisée par la règle | Action choisie | Position après / effet |
|---|---|---|---|---|
| 1 | À relever | À expliquer | À relever | À relever |
| 2 | À relever | À expliquer | À relever | À relever |

Relever aussi un élément que le programme reçoit mais que la règle locale ne consulte pas utilement. Un humain peut regarder toute l’illustration ; le programme de décision, lui, ne reçoit pas une image de classe ni les intentions de ses personnages.

## C. Formuler et départager des hypothèses — 18 à 25 min

Examiner ces trois propositions : H1, le programme choisit toujours une direction fixe ; H2, il compare des coordonnées ; H3, un modèle de langage interprète une phrase à chaque pas. Pour chacune, proposer une vérification : changer les coordonnées dans un appel direct, lire la fonction ou examiner les données transmises.

Deux pas identiques ne suffisent pas à distinguer H1 de H2. Il faut un autre cas, par exemple une cible à gauche. H3 ne se déduit ni de l’apparence du robot ni de la présence du mot « IA ». On cherchera une preuve dans le code réellement exécuté.

## D. Formaliser et classifier — 25 à 50 min

### Le système que nous allons étudier

Nous appelons **agent**, dans cette séance, le système qui reçoit des observations d’un environnement et choisit des actions qui peuvent agir sur lui. On l’étudie relativement à une tâche et à un critère de performance. Cette définition est un cadre de travail classique ; les communautés scientifiques ne posent pas toutes les mêmes exigences sur le mot. [R1, R2, bibliographie du dossier]

Une **observation** est une information accessible au programme : ici une position, la cible et une carte. Une **politique** est la règle de choix de l’action à partir des informations retenues. Une **action** est une commande : l’environnement détermine ensuite son effet. L’**environnement** inclut ce qui évolue ou impose des contraintes autour de ce contrôleur. La tâche impose une cible ; la politique ne l’invente pas.

Dans notre exemple original, le même programme peut servir à deux tâches. Tâche A : atteindre la cible en peu de déplacements. Tâche B : atteindre la cible sans tenter d’entrer dans un mur. Une stratégie peut avoir un bon résultat selon un critère et un mauvais selon un autre. Avant de dire « bon agent », préciser ce qui est évalué.

**Autonomie**, **rationalité**, **intelligence** ne sont pas des synonymes. Nous parlerons ici d’autonomie opérationnelle quand le programme choisit ses prochaines commandes sans recevoir chacune d’un humain, dans des limites définies. La rationalité concerne l’adéquation des choix à l’information et au critère retenu ; elle ne promet pas de toujours réussir. L’intelligence est une appréciation de capacités, qu’il faut soutenir par des tâches et des résultats. Aucun de ces mots ne prouve une conscience. Le mot « décide » désigne ici un calcul.

### Les catégories ne sont pas des boîtes étanches

En groupes, traiter les quatre dossiers ci-dessous. Pour chacun : délimiter le système, nommer ce qu’il observe, ce qu’il produit et ce qui peut être modifié ; justifier ensuite les termes applicables. Une justification vaut plus qu’une étiquette.

1. **Porte automatique** : un capteur détecte une présence, un contrôleur commande l’ouverture, un dispositif mécanique peut rencontrer un obstacle. Peut-elle être décrite par un automate ? Par un agent ? Que n’avons-nous pas évalué ?
2. **Programme de grille** : une fonction compare des coordonnées, renvoie un mot d’action et le moteur vérifie le déplacement. Le fait qu’elle soit déterministe l’empêche-t-il d’agir comme contrôleur d’agent ?
3. **Chatbot de FAQ** : il choisit une réponse dans une table à partir d’un mot-clé. L’action est une sortie de texte, pas une opération sur un dossier client. Une interface de dialogue implique-t-elle un LLM ?
4. **Assistant à outils** : un modèle propose une requête, du code vérifie son format, un outil renvoie un résultat, un humain autorise l’opération finale. Où placer le modèle ? Où placer le système complet ?

Un automate est un modèle de contrôle ; un chatbot caractérise une interaction ; un LLM est un modèle de langage ; un agent décrit un système en interaction. Un même système peut relever de plusieurs descriptions. Inversement, il n’est pas utile de qualifier tout `if` d’agent intelligent : il faut expliquer la frontière, la boucle et la tâche.

### Trois repères pour situer cette évolution

Le contrôle robotique par couches de Brooks, publié comme rapport en 1985 puis article en 1986, montre que l’action située précède largement les agents LLM [R8]. Wooldridge organise un cadre pour agents autonomes et interactions dans son manuel de 2009 [R2]. ReAct, prépublié en 2022 puis publié en 2023, étudie une manière d’articuler générations de langage et actions [R4]. Ce sont des repères de lecture, pas les dates d’invention d’une notion unique ni une histoire exhaustive.

## E. Expérimenter et programmer — 50 à 90 min

**TP01 — Mon premier agent réactif**, sujet complet dans `TP_ET_EXPERIENCES.md`. Copier le fichier de départ fourni dans l’éditeur. Le premier lancement renvoie volontairement toujours `arrêt` : il permet de comprendre la différence entre code qui s’exécute et politique qui accomplit la tâche.

Travail : prédire, exécuter, puis remplacer ce retour constant par une décision horizontale : droite si la cible est à droite, gauche si elle est à gauche, arrêt si la position est la cible. Ajouter ensuite le mouvement vertical pour le second axe. Pour chaque modification, écrire au moins un appel dont le résultat était prédit avant l’exécution.

Les exemples sont des coordonnées et des chaînes Python ; ils n’appellent aucun modèle de langage. Dans le panneau, **Exécuter Python** vérifie les appels et affiche la console. Pour animer la grille, choisir ensuite **Mon agent Python** et utiliser les pas. Les deux usages ne sont pas identiques.

On attend une trace pour cible à droite, une pour cible à gauche et une à la cible. Si un nom d’action est mal orthographié, expliquer le message réel au lieu de conclure que la politique « a changé d’avis ». Si une boucle accidentelle bloque l’exécution, utiliser Stop puis relancer un code borné. Demander un indice seulement après avoir formulé ce qui ne fonctionne pas.

## F. Analyser les résultats — 90 à 100 min

Reprendre le mur initial : votre fonction connaît-elle la liste d’obstacles ? L’utilise-t-elle ? Pourquoi une action qu’elle renvoie peut-elle être refusée ? Une fonction qui respecte son contrat de retour peut-elle être inadéquate pour la tâche ?

L’expérience ne démontre pas qu’aucun raisonnement ne peut être programmé sans LLM. Elle montre qu’une sélection d’action précise peut être obtenue par une règle déterministe et que son succès dépend de l’environnement. Il reste à étudier mémoire et recherche : nous ne les avons pas rendues présentes par le seul changement de vocabulaire.

## G. Réinvestir — 100 à 110 min

Un personnage de jeu observe `porte_ouverte` et `cle_presente`. Sa tâche est de quitter une pièce. Décrire trois actions possibles, deux observations distinctes et un test de décision. La clé n’est visible qu’avant de quitter le point de départ : quelle question poseriez-vous avant d’écrire une politique qui n’observe que la scène courante ?

Le transfert attendu est de retrouver les responsabilités du système, pas de recopier les mots « droite/gauche ». Répondre en phrases et par un appel de fonction proposé ; la réalisation complète du contrôleur à mémoire appartient à une séance ultérieure.

## H. Synthèse et billet de sortie — 110 à 120 min

À retenir : le programme reçoit des informations, calcule une commande, puis observe son effet. Il faut distinguer la règle de décision, l’environnement et le critère qui permet d’évaluer les résultats. Une règle déterministe peut piloter un agent ; une interface de dialogue n’identifie pas à elle seule l’algorithme sous-jacent.

Billet individuel : définir un agent avec les quatre éléments du premier dessin ; donner un système qui soit à la fois automate et agent ; expliquer en une phrase pourquoi notre Python n’est pas un agent LLM. Ajouter un cas de test qui manque encore à votre fonction. L’enseignant utilise ces réponses pour décider de la remédiation, pas pour annoncer le module entier acquis.

## Adaptation et regard de l’enseignant

Les développements scientifiques et l’audit de cette séance sont séparés de cette fiche. Première : fournir lecture de tuple et conducteur ; Terminale : demander de spécifier les retours et comparer deux politiques, sans anticiper obligatoirement BFS. Pour un groupe enseignant, remplacer une partie des essais guidés par l’analyse de frontière et la contre-épreuve du contrat décrites dans le parcours approfondi. Aucune variation ne rend les corrections visibles par défaut dans le sujet distribué.
