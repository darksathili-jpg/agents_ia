# Séance 02 — Environnement, observations et actions

**Parcours NSI, 120 min estimées.** Question centrale : **« Pourquoi un agent ne peut-il pas toujours prendre la bonne décision avec les informations qu’il reçoit ? »**

Objectifs : distinguer état et observation (O2), prédire une commande et son effet (O4), expliquer une limite expérimentale (O8), préparer la mémoire (O6, sans programmer encore un contrôleur à mémoire). Acquis mobilisés : S01, fonction/retour, condition, coordonnées et lecture d’un dictionnaire fourni. Aucune probabilité conditionnelle ni connaissance de réseau neuronal exigée. Utiliser la [fiche élève S02](SUPPORT_ELEVE_S02.md). Le [parcours enseignant S02](ENSEIGNANT_S02.md) est distinct.

## Plan de travail

| Temps | Activité | Preuve recueillie |
|---|---|---|
| 0–10 | Rappel, problème et hypothèses | Commande distincte du mouvement ; question d’information formulée. |
| 10–25 | État réel et observation | Deux descriptions clairement séparées. |
| 25–55 | TP02, transition et refus | Fonction modifiée, tests et trace avant/commande/après. |
| 55–70 | Même commande, plusieurs effets | Comparaison déterministe/glissement, sans changer la politique. |
| 70–95 | Observation masquée, préparation TP03 | Deux historiques, même observation finale, décisions différentes. |
| 95–110 | Formalisation accessible et transfert | Schéma causal et contre-exemple expliqué. |
| 110–120 | Bilan formatif individuel | Cinq réponses, remédiation ciblée. |

Les activités sont intégrées à ces 120 min ; les exercices S02-A à G ne s’ajoutent pas en devoir complet au même créneau. Le temps de lecture enseignant remplace une partie du guidage, il n’allonge pas la séance.

## A. Problème et hypothèses — 0 à 10 min

Reprendre la seconde tentative refusée en S01. Le programme a-t-il choisi de ne pas avancer, le moteur a-t-il refusé, ou la carte a-t-elle changé ? Écrire une hypothèse et une observation qui la départagerait. **Choisir une commande, l’envoyer, l’appliquer et observer son résultat sont quatre opérations distinctes.** Dans notre code, la chaîne retournée représente la commande ; on ne suppose pas qu’elle a déjà modifié le monde.

La question s’élargit : si deux mondes ont la même apparence pour le programme, peut-il toujours choisir ce qui convient ? Ne pas répondre par « oui, s’il est plus intelligent » : il faudra préciser ce qu’il reçoit.

## B. Ce qui existe et ce qui est reçu — 10 à 25 min

L’**état réel** décrit les informations nécessaires pour représenter le monde du modèle. Dans une carte fixe, on peut décrire la position et conserver murs/cible comme paramètres connus. Une **observation** est ce que la fonction d’observation rend accessible au contrôleur. Un dictionnaire ne devient pas une observation complète par sa seule forme ; il peut omettre une information essentielle.

Exemple original : une carte porte une couleur de sortie autorisée. Le monde conserve cette couleur même quand le capteur ne la transmet plus. Deux faits sont donc différents : « la couleur n’existe pas » et « je ne la reçois pas ». Dans nos données, `None` indiquera un indice non visible. Ce n’est ni « bleu » ni « aucune sortie ».

Dans le laboratoire habituel, la politique Python reçoit position, cible et obstacles : masquer une partie de l’image sur l’écran ne cache rien à cette fonction. **L’expérience masquée de cette séance utilise un autre script, en console**, avec une fonction d’observation qui omet réellement un champ. La grille interactive ne change pas.

Exercice S02-A : donner pour le robot une information du monde et dire si elle est accessible à sa politique actuelle. S02-B : une caméra coupée permet-elle de conclure que le couloir est vide ? Justifier par deux états possibles.

## C. TP02 — Une transition n’est pas la politique — 25 à 55 min

**Mode console uniquement pour ce TP de programmation.** Copier [s02_obstacle_depart.py](python/s02_obstacle_depart.py), pas un ancien fichier du TP. Il fournit les bornes, les directions et `libre` ; compléter seulement `appliquer(position, action, obstacles)`. Le programme initial affiche `A_COMPLETER_S02` : il fonctionne comme support incomplet, pas comme solution.

Question : que devient une commande devant un mur ? Hypothèse : le déplacement est refusé et la position conservée. Garder dimensions et commande fixes ; comparer carte libre puis obstacle. Relever candidate, position après et résultat. Le protocole détaillé et les indices sont dans l’[annexe des activités S02](ACTIVITES_S02.md).

Ordre de travail : (1) prédire les quatre essais avant exécution ; (2) traiter arrêt ; (3) retrouver le déplacement du mot ; (4) calculer la candidate ; (5) accepter seulement si elle est libre ; (6) signaler un mot inconnu. Exécuter les essais et distinguer erreur Python, refus correct et effet attendu.

S02-C : écrire la transition de `(1,2)` avec « droite » devant le mur `(2,2)`. S02-D : modifier la fonction puis tester un bord et une action libre. S02-E : expliquer pourquoi ce code ne choisit pas à lui seul une meilleure direction. Nous programmons l’environnement textuel fourni, pas une nouvelle politique de recherche.

**Retour à la grille, observation seulement (si utile dans les 30 min).** Le professeur peut rejouer les deux pas gloutons pour comparer les traces. Coller une fonction `appliquer` dans l’éditeur ne remplace pas le moteur JavaScript. Le mode Mon agent Python appelle `decider`, il ne prend pas en charge cette nouvelle transition.

## D. Déterminisme et effets variables — 55 à 70 min

Dans le premier modèle, mêmes état, carte et commande donnent le même résultat. Un refus devant un mur est donc **déterministe**, même si l’utilisateur ne s’y attendait pas. Ne pas confondre « je ne savais pas » avec « le modèle tire au hasard ».

Le professeur lance ensuite le bloc « glissement » de [s02_corrige.py](python/s02_corrige.py), après le TP, ou en donne les sorties. La commande reste toujours droite sur une case libre. Une variable de tirage vaut 0 ou 1 : avec 0 le robot patine ; avec 1 il se déplace. On étudie ainsi une **transition modélisée comme stochastique**. La politique n’est pas devenue aléatoire ; c’est l’effet qui varie. La graine permet de rejouer une expérience informatique, pas de certifier la fiabilité d’un robot physique.

Comparer d’abord explicitement les deux tirages possibles, puis huit essais avec une graine. **Chaque essai repart du même état**, ce ne sont pas huit mouvements successifs. Une poignée d’essais ne mesure pas précisément une probabilité ; aucun calcul de fréquence n’est exigé ici. La transition de la grille de l’application reste déterministe.

S02-F : indiquer ce qui a été modifié, ce qui reste contrôlé et la limite de la conclusion. Un mur reste infranchissable dans les deux issues du modèle fourni.

## E. Deux mondes, la même observation — 70 à 95 min

**Mode console, parcours imposé, pas un agent à mémoire déjà construit.** Copier [s02_observation_masquee.py](python/s02_observation_masquee.py). La grille textuelle 3 × 2 comporte départ `(0,0)`, couloir `(1,0)`, mur `(2,0)`, sorties `(0,1)` et `(2,1)`, bifurcation `(1,1)`.

La tâche complète autorise la sortie gauche si l’indice initial est bleu, la droite s’il est orange. L’indice est visible seulement au départ ; le monde le conserve ensuite. Le parcours est imposé : droite puis bas ; il reste **une commande de sortie**, dans un budget total de trois. À la bifurcation, on ne peut pas retourner lire l’indice et prétendre respecter ce même budget.

Avant de lancer, remplir deux colonnes d’état/observation. Après exécution, comparer les deux historiques : au départ les observations diffèrent ; dans le couloir et à la bifurcation elles sont identiques. Pourtant la sortie requise diffère. Pour cette tâche immédiate, une règle déterministe qui ne reçoit **que l’observation finale** choisit pareil dans les deux cas : elle ne garantit pas les deux réussites.

Cette conclusion ne dit pas que toute politique réactive échoue dans tout environnement partiellement observable. Elle n’affirme pas non plus que toute mémoire suffit. Ici retenir la couleur serait utile ; la programmation du contrôleur à mémoire appartient à S03, non rédigée dans ce jalon.

S02-G : proposer les deux états, l’observation commune et les deux décisions requises. Que perd-on si l’on supprime l’histoire reçue au départ ? Donner une information supplémentaire qui rendrait ce cas plus facile.

## F. Mettre en mots, puis transférer — 95 à 110 min

Première : dessiner « monde → informations reçues → règle → commande → effet → nouvelle information ». Terminale préparée : noter `observation = observer(etat)` et `etat_suivant = transition(etat, commande)`, en expliquant d’abord ce que représentent les variables. La notation n’est pas une démonstration à elle seule.

Transfert : un logiciel de navigation n’a pas reçu une fermeture de route. Peut-il produire la même proposition qu’hier alors que le monde a changé ? Indiquer état réel, observation et vérification de l’effet. Il peut y avoir erreur d’information sans tirage aléatoire de l’environnement. Ce dossier est une étude de cas, pas un service de navigation implémenté.

## G. Bilan formatif — 110 à 120 min

Répondre seul : B1, une phrase état/observation avec exemple ; B2, une transition refusée complète ; B3, un contraste entre refus déterministe et glissement ; B4, les deux mondes indiscernables et la limite sans mémoire ; B5, nommer quel code pilote la grille et quel script reste en console.

Maîtrise proposée : au moins quatre réponses satisfaisantes sur cinq, avec B1 et B2 indispensables. Si B4 manque, reprendre les deux colonnes sans passer immédiatement au code de mémoire. Si B5 manque, refaire un appel console puis un pas de grille. Ce seuil est formatif et doit être éprouvé en classe ; il ne valide pas le module complet.

## Synthèse accessible

L’état décrit le monde du modèle ; l’observation ne transmet qu’une partie de ses informations. La politique choisit une commande, la transition détermine l’effet. Une transition peut être déterministe ou modélisée comme stochastique. Deux états différents peuvent être indistinguables pour une observation : certaines tâches demandent alors une information supplémentaire ou une mémoire, sous des hypothèses à préciser. Aucune de ces expériences n’emploie un LLM.
