# Corrigés — document de préparation enseignant

À distribuer après recherche. Les sujets élève n’intègrent pas ce texte dans leur déroulé ; la séparation des fichiers n’est pas une protection d’accès d’un dépôt public. Les variantes de code correctes sont acceptées lorsqu’elles respectent les contrats et sont justifiées.

> **Jalon S01.1/S02 :** les corrections du diagnostic, des activités S02 et du bilan figurent à la fin de ce document. Pour ces activités, employer les fichiers `s01_*` et `s02_*` ; les corrigés TP03–05 du premier dossier restent des supports de référence, sans autorisation de rédiger les cours S03–S05.

## Séance pilote : observations et classification

Première tentative : `(0,2)`, cible à droite, commande droite, arrivée `(1,2)`, déplacement accepté. Deuxième : candidate `(2,2)` occupée, commande droite mais position conservée `(1,2)`, épisode bloqué. Il y a deux commandes et un seul déplacement. La carte est transmise, mais la règle horizontale n’en tire pas un chemin. Un retour constant et une comparaison ne sont pas distinguables par un seul appel favorable : tester une cible à gauche.

Porte automatique : automate possible comme modèle de contrôle ; agent possible avec frontière capteur-contrôleur-actionneur. Ce classement ne prouve pas une compétence complexe. Fonction de grille : composant de décision ; couplée au moteur dans une boucle, contrôleur d’un agent déterministe. FAQ : chatbot par interaction, pas forcément LLM ; une sortie textuelle peut compter comme action si l’environnement inclut l’utilisateur. Assistant à outils : le modèle propose, le système valide/exécute, le retour devient observation ; une autorisation humaine peut borner l’autonomie.

Transfert du personnage à clé : des actions possibles sont prendre, avancer, ouvrir. Observation courante et possession d’une clé doivent être distinguées. Si l’information utile disparaît de la scène, demander ce qui est mémorisé. Ne pas imposer une conception unique tant que frontière et contrat sont cohérents.

## TP01 — Correction expliquée

Le [support complet](python/corriges.py), fonction `decider`, compare d’abord les abscisses, puis les ordonnées, puis renvoie arrêt si aucune différence ne reste. Une vérification explicite de l’arrivée en tête est également correcte. Chaque branche renvoie une chaîne ; remplacer un `return` par `print` produit un affichage mais change le contrat.

Les cinq appels donnent droite, gauche, bas, haut, arrêt respectivement dans l’ordre des cas du sujet. Ils vérifient des branches, pas une capacité de navigation générale. La règle ignore les obstacles, donc sa collision initiale n’est ni un dysfonctionnement du runtime ni la preuve qu’un LLM serait requis. Une réparation locale qui s’arrête évite un refus mais ne résout pas le problème de trouver un détour.

## TP02 — Correction expliquée

`appliquer` cherche le déplacement associé au mot, calcule une candidate, vérifie bornes et obstacle. Si refus : ancienne position et résultat `refuse`. Arrêt : pas de mouvement. Mot inconnu : exception explicite, pas action inventée. Le conducteur borne l’épisode, enregistre la commande et termine au refus. La trace et les compteurs du support sont vérifiés par les tests.

Réponse critique : la transition peut refuser une commande à juste titre ; la politique et l’environnement ont des responsabilités différentes. Remplacer l’arrêt par un droit de réessai changerait la tâche ; cela doit être annoncé avant de comparer les stratégies.

## TP03 — Correction expliquée

`observer_case` laisse voir l’indice seulement en `(0,0)`. `decider_memoire` ne met à jour sa mémoire que si l’indice est présent. Les actions sont droite, bas, puis gauche si mémoire bleue ou droite si orange. Deux épisodes réussissent en trois mouvements. À la bifurcation, la position et l’indice masqué sont identiques ; seule la mémoire diffère.

Preuve attendue : une fonction de la même observation retourne la même action dans les deux mondes. Si une sortie différente est nécessaire immédiatement, elle ne garantit pas les deux réussites. Un seul indice mémorisé suffit ici parce que le problème a été construit ainsi. Une politique qui accède directement à la couleur cachée ne résout pas la tâche d’observation partielle ; elle en change les entrées.

## TP04 — Correction expliquée

`chemin_bfs` emploie une file et inscrit le prédécesseur à la découverte. Chaque sommet est découvert au plus une fois. En atteignant la cible, il remonte les actions et inverse la liste. Départ égal cible donne une liste vide ; file épuisée donne `None`. Les oracles de longueur sont C0=6, C1=10, C2=0, C3 sans chemin, C4=10, C5=4. Les tests rejouent chaque chemin et vérifient ses mouvements.

Sur un graphe fini à coûts unitaires, l’exploration par niveaux atteint une distance minimale ; un autre ordre des voisins peut fournir un autre chemin minimal. Avec une file efficace et les prédécesseurs, le coût conventionnel est `O(|V|+|E|)` en temps, `O(|V|)` en mémoire, sur une représentation adaptée. Cette borne ne gomme pas les coûts particuliers d’autres programmes. Chercher un chemin n’est pas apprendre à partir d’expériences.

## TP05 — Résultats et interprétation

| Cas | Politique locale : état / déplacements | BFS : état / déplacements |
|---|---|---|
| C0 | réussite / 6 | réussite / 6 |
| C1 | bloqué / 1 (2 tentatives) | réussite / 10 |
| C2 | réussite / 0 | réussite / 0 |
| C3 | bloqué / 4 (5 tentatives) | arrêt / 0, aucune solution trouvable |
| C4 | réussite / 10 | réussite / 10 |
| C5 | bloqué / 0 (1 tentative) | réussite / 4 |

Taux sur les six cas : 3/6 et 5/6. Sur les cinq cas accessibles : 3/5 et 5/5. Les deux présentations sont recevables si le dénominateur et l’exclusion du cas impossible sont explicites. Le taux global n’est pas une preuve de supériorité universelle. Surcoût `L−L*` défini seulement sur réussite accessible : zéro dans ces cas ; les échecs restent non définis, même si zéro mouvement a eu lieu. Ajouter des coûts variables ou des cartes inconnues est un autre protocole.

## Réponses des quinze exercices

| Exercice | Réponse attendue / marge d’acceptation |
|---|---|
| E01 | Le programme reçoit une observation et choisit ; l’environnement applique/refuse. La première trace ci-dessus est une réponse complète. |
| E02 | Automate et agent peuvent décrire la porte ; chatbot décrit l’interface, non l’algorithme. Accepter une autre frontière si elle est expliquée. |
| E03 | Le modèle génère une proposition ; validateur et outil réalisent ou refusent l’effet. Un humain peut autoriser avant exécution. |
| E04 | Code initial : trois arrêts. Horizontal corrigé : droite, gauche, arrêt. Les sorties doivent être prédites avant le lancement. |
| E05 | `decider` du support ; tests haut/bas distincts avec y croissant vers le bas. |
| E06 | L’état conserve l’indice ; la fonction d’observation ne le retourne plus. Inconnu n’est pas faux. |
| E07 | `observer_case` du support. Les dictionnaires en `(1,1)` sont identiques malgré les indices initiaux différents. |
| E08 | Mise à jour conditionnelle sur indice non nul ; ne pas remplacer mémoire par `None` quand l’indice disparaît. |
| E09 | Trace `episode_memoire` ; pour le refus, la position après reste égale à la précédente. |
| E10 | C5 ou mur `(2,2)` de la carte labo ; fournir commande et effet, pas seulement un dessin. |
| E11 | Deux instances recréées avec graine 7 reproduisent leur trace dans le même environnement ; changer la graine ne garantit pas un succès ni même une différence sur un tout petit échantillon. Aucune génération de langage n’intervient. |
| E12 | LIFO change l’ordre et ne donne pas la garantie de distance minimale du BFS ; trouver un chemin reste différent de trouver le plus court. |
| E13 | Conserver 5/6 avec effectif ; ne pas moyenner des échecs comme des longueurs nulles. Indicateur de longueur conditionné aux réussites. |
| E14 | Deux trajets construits de 2 pas à coût 5 chacun et 4 pas à coût 1 chacun : 10 contre 4. L’exemple est un dossier de coût, pas la carte actuelle à coût unitaire. |
| E15 | Proposition `supprimer_fichier` hors alphabet d’un outil de recherche ; validation rejette et test vérifie absence d’appel. Aucun effet externe réellement produit dans cet exercice. |

## Correction analytique des évaluations finales

### Variante NSI, sur 20

1. Observation = données accessibles ; politique = fonction de sélection ; action = commande, pas effet : 2 points. Recouvrement automate-agent justifié : 1. Interface textuelle non probante quant au LLM : 1.
2. Trace `(0,2)→(1,2)` puis refus `(2,2)` : 2. Position maintenue et état bloqué : 1. Deux tentatives/un déplacement : 1. Cible à gauche ou arrivée comme contre-épreuve : 1.
3. `decider_prudent` dans le support est une correction exécutable, avec `decider` et `appliquer` comme auxiliaires. Arrivée : 1. Choix des deux axes : 2. Candidate validée par transition et refus remplacé par arrêt : 2. Contrat : 1. Tests arrivée, libre, mur : 1. Cette politique peut s’arrêter avant le but ; ne pas attribuer des points de recherche de détour non demandée.
4. Moyenne sur échecs invalide et généralisation excessive corrigées : 2. Cas impossible identifié : 1. BFS calcule une recherche dans un modèle connu, le LLM est un autre composant possible : 1.

### Variante enseignant, sur 20

1. Historique ordonné et domaines des symboles : 2. Autonomie opérationnelle distincte du critère rationnel : 1. Frontière/classification non exclusive : 1.
2. Argument de même observation/même action : 2. Mémoire de couleur : 1. Information partielle, pas carte complète : 1. Tirage de politique distinct de transition : 1.
3. `decider_memoire` et ses deux histoires dans les tests donnent le corrigé exécutable. Mise à jour conditionnelle : 2. Étapes et bifurcation : 2. Signature et aucune lecture cachée : 1. Information absente signalée : 1. Tests non-effacement/discrimination : 1.
4. Même carte et mêmes observations, seule mémoire modifiée : 1. Deux cas ne donnent pas une robustesse générale : 1. Coûts uniformes et carte statique pour la garantie annoncée : 1. Question NSI reliant règle réellement exécutée et retour observé : 1.

Remédiation ciblée : confusion observation/état → deux mondes côte à côte ; retour/effet → transition isolée ; mémoire → tableau entrée/sortie ; métrique → recompter les dénominateurs ; preuve → construire un contre-exemple. Un code non exécuté ne satisfait pas les points d’exécution, mais la correction argumentée et la reprise peuvent valider la compétence après travail.

## S01.1 — Diagnostic initial et guidage

D1 : droite. D2 : gauche. D3 : les deux conditions sont fausses, le dernier retour donne arrêt. D4 : `annoncer` affiche haut mais renvoie implicitement `None` ; le script imprime ensuite ce retour. D5 : 3 puis 1, abscisse puis ordonnée dans notre convention.

Interprétation formative : si les branches sont comprises mais les coordonnées inversées, distribuer le repère et demander un appel vertical ; si D4 manque, faire lire `resultat = annoncer()` puis `resultat = choisir_x(1,4)` côte à côte. Ne pas confondre erreur d’index et conception erronée d’un agent. Les huit minutes ne comprennent pas une remise à niveau générale : un besoin collectif demande un aménagement ultérieur plutôt que la suppression du TP.

La [production enseignant S01 complète](PRODUCTION_ENSEIGNANT_S01.md) donne un modèle de réponse avec choix de frontière, trace, argumentation et limites. Les fiches élève remplies peuvent varier, mais doivent identifier le retour et son effet, une preuve de code et un contre-test.

## S02 — Correction TP02 et résultats de référence

Le fichier [s02_corrige.py](python/s02_corrige.py) est autonome et contient `appliquer`, plus la démonstration de glissement. Pour restituer seulement TP02, expliquer d’abord la partie déterministe, puis lancer la démonstration suivante dans son créneau prévu. Ce script reste en console ; il ne remplace pas le moteur graphique et ne contient pas de politique `decider`.

| Essai | Candidate | Position après | Résultat |
|---|---|---|---|
| `(0,2)`, droite, libre | `(1,2)` | `(1,2)` | accepte |
| `(1,2)`, droite, murs du labo | `(2,2)` | `(1,2)` | refuse |
| `(0,0)`, haut, libre | `(0,-1)` | `(0,0)` | refuse |
| `(0,2)`, arrêt | Pas de déplacement | `(0,2)` | arret |

La fonction traite arrêt, vérifie le mot, calcule la candidate et teste `libre`. Elle refuse les entrées initiales invalides dans le corrigé. Les tests vérifient aussi les quatre bords, l’arrivée et une commande inconnue. Un élève qui retourne la candidate avant le test peut traverser un mur ; un élève qui retourne toujours la position initiale échoue sur le test libre. Ces tests sont discriminants sans exiger une recherche de chemin.

S02-A : la position, la cible et la carte sont effectivement transmises à la politique du labo. S02-B : le couloir peut être libre ou occupé derrière un capteur coupé ; aucun de ces états ne peut être affirmé à partir de l’absence de signal seule. S02-C : candidate `(2,2)`, refus, position `(1,2)` conservée. S02-D : voir fonction et cas du tableau. S02-E : cette fonction applique une commande déjà choisie ; elle n’évalue pas des suites d’actions et ne choisit pas un détour.

## S02 — Correction du contraste déterministe/stochastique

Sans glissement, la transition de `(0,2)` avec droite donne toujours `(1,2)` sur carte libre. Dans le second modèle : tirage forcé 0 → `(0,2)`, patine ; tirage forcé 1 → `(1,2)`, accepte. Devant le mur, les deux donnent refus et position conservée. Le mot droite n’a pas varié : la différence ne vient pas d’une politique stochastique.

S02-F : variable expérimentale = modèle de transition puis tirage ; contrôlés = position de départ, commande et carte. Les huit essais sont réinitialisés séparément. La même graine permet un rejeu dans les mêmes conditions ; elle ne prouve ni une fréquence exacte à long terme ni un hasard physique. Le test exhaustif des deux valeurs du tirage vérifie le code du petit modèle, pas sa validité pour un vrai robot.

## S02 — Observation masquée et contre-exemple

| Position / étape | État bleu : couleur réelle | Observation bleue : indice | État orange : couleur réelle | Observation orange : indice |
|---|---|---|---|---|
| `(0,0)` départ | bleu | bleu | orange | orange |
| `(1,0)` après droite | bleu | `None` | orange | `None` |
| `(1,1)` après bas | bleu | `None` | orange | `None` |

La position demeure observable dans les deux mondes. À la bifurcation, le dictionnaire transmis est `{"position": (1,1), "indice": None}` dans les deux cas. La sortie autorisée est gauche pour bleu, droite pour orange. Sur une commande restante, ces réussites demandent des actions distinctes. Si la règle ne lit que ce dictionnaire, sa sortie déterministe est la même ; elle ne garantit donc pas les deux réussites. Une décision différente dans deux copies de cette même entrée impliquerait une autre information, une mémoire ou du hasard, et non une discrimination produite par cette entrée seule.

S02-G : donner ces deux états et ce dictionnaire, rappeler le budget et les deux sorties. La couleur reçue au départ rend les historiques différents ; la supprimer de la dernière observation n’efface pas rétroactivement ce qui avait été reçu. La mémoriser aiderait pour ce cas, sans fournir un modèle complet du monde. L’implémentation de cette mémoire reste à S03.

Variante de capteur pour groupe rapide : transmettre `indice` à toutes les positions. Les deux observations finales deviennent différentes ; le contre-exemple précédent ne s’applique plus à ce nouveau capteur. Retourner au départ demanderait plus de commandes que le budget fixé et changerait donc la tâche. Avec un autre budget ou une requête supplémentaire, il faut réexaminer la conclusion.

Transfert navigation : la fermeture existe dans le monde, l’observation du logiciel peut encore décrire une route ouverte, la proposition doit être confrontée à l’information et à l’effet. On ne peut pas inférer de ce décalage que les transitions physiques ont été modélisées comme aléatoires.

## S02 — Bilan formatif et critères observables

| Item | Réponse satisfaisante | Remédiation si confusion |
|---|---|---|
| B1 | Distingue donnée réelle et donnée reçue, avec exemple de couleur persistante mais masquée | Deux colonnes monde/capteur, refaire un appel d’observation. |
| B2 | Donne avant `(1,2)`, droite, après `(1,2)` et refus | Rejouer candidate et test d’obstacle, sans toute la politique. |
| B3 | Refus déterministe ; glissement = effet variable à commande fixe | Fixer la commande et forcer les deux tirages. |
| B4 | Même observation finale, sorties distinctes, limite d’une commande restante | Relire les deux historiques et leur dernière ligne ; ne pas programmer la mémoire trop tôt. |
| B5 | `decider` pilote la grille ; les nouveaux scripts de transition/masque/glissement restent en console | Comparer Exécuter Python et un pas de Mon agent Python ; rappeler que les appels ne changent pas la carte graphique. |

Proposition : quatre items satisfaisants sur cinq, B1 et B2 requis. Une réussite de code sans interprétation ne valide pas B1/B4 ; une définition récitée sans trace ne valide pas B2. Ce seuil et les temps doivent être confirmés avec des apprenants, sans transformer le bilan en certification du module.
