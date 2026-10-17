# S02 — Protocoles, exercices, tests et indices

À distribuer avec la fiche élève. Les corrections sont dans le fichier enseignant distinct `CORRIGES.md`, pas dans ce sujet. Tous les scripts indiqués ci-dessous s’exécutent **en console**, dans une seule exécution par expérience. Aucun ne remplace le moteur de la grille.

## Activité 1 — TP02, programmer et contrôler une transition (30 min)

| Élément | Spécification |
|---|---|
| Objectifs / question | O2/O4/O8 ; distinguer commande admissible, déplacement possible et résultat. |
| Hypothèse | Un obstacle ou un bord provoque un refus sans mouvement. |
| Paramètres contrôlés | Grille 7 × 5, conventions x/y, dictionnaire de commandes ; même position/commande pour comparer libre et mur. |
| Variable modifiée | Présence d’un obstacle devant le robot ; autres essais isolant bord ou arrêt. |
| Données recueillies | Position avant, candidate, commande, résultat, position après. |
| Protocole | Prédire quatre essais ; compléter `appliquer` dans `s02_obstacle_depart.py` ; lancer ; ajouter un test libre et un bord ; comparer éventuellement aux deux pas du labo. |
| Attendu / réussite | Libre : `(0,2)` + droite donne `(1,2)` ; mur : `(1,2)` + droite conserve `(1,2)` ; bord haut conserve `(0,0)` ; arrêt conserve sa position. Chaque résultat est justifié. |
| Limites | La transition n’est pas une politique ; aucun détour ni changement du moteur de grille. Entrées initiales supposées cohérentes avec les bornes ; le corrigé signale aussi une position initiale invalide. |

Rythme conseillé : prédictions 5 min, code 15 min, tests 5 min, analyse 5 min. Le programme initial signale volontairement la partie à compléter. Après correction, aucun marqueur `A_COMPLETER` ne doit être nécessaire pour valider les quatre essais.

Indices gradués : I1, utiliser le déplacement `(dx,dy)` du dictionnaire ; I2, calculer `(x+dx,y+dy)` avant le test ; I3, ne retourner la candidate que si `libre(candidate, obstacles)` est vrai. Pour une commande inconnue, signaler une exception plutôt que choisir silencieusement une direction.

Tests supplémentaires : gauche en `(0,0)`, droite en `(6,4)`, bas en `(6,4)`, action inconnue « voler ». Le corrigé ajoute une position hors carte et une position dans un mur. Les deux premiers essais relient bien commande/effet ; un message d’erreur de syntaxe doit être traité avant d’interpréter la stratégie.

## Activité 2 — Comparer deux modèles de transition (15 min)

| Élément | Spécification |
|---|---|
| Objectif / question | O8 ; mêmes état et commande impliquent-ils toujours le même effet dans le modèle étudié ? |
| Hypothèse | Le modèle déterministe donne une seule issue ; le modèle avec glissement autorise deux issues sur une case libre. |
| Paramètres contrôlés | Position `(0,2)`, commande droite, carte sans mur ; remise au même état avant chaque essai, politique identique. |
| Variable modifiée | Modèle de transition puis tirage 0 ou 1. La politique ne varie pas. |
| Données recueillies | Position après et résultat accepté/patine ; série de huit essais. |
| Protocole | Après restitution TP02, lancer la démonstration `s02_corrige.py` ; lire d’abord les deux tirages forcés, puis la série de graine 7 ; refaire avec la même graine. |
| Attendu / réussite | Deux issues explicitement contrôlées : rester/patine ou avancer/accepté. Même graine reproduit une série dans le même runtime. L’élève identifie le composant modifié. |
| Limites | Huit essais ne valident pas une fréquence précise. Reproductibilité pseudo-aléatoire et modèle stochastique sont compatibles. Pas de bruit ni glissement ajouté à la grille réelle. |

Indices : I1, regarder où le tirage entre dans la fonction ; I2, aucune sélection aléatoire de commande n’y est faite ; I3, vérifier séparément ce qui se passe devant un mur. Tests : les tirages 0/1 vers une case libre donnent les deux effets annoncés ; les deux tirages devant `(2,2)` restent refusés ; une série vide est possible si on demande zéro essai. Pour les élèves, la série peut être simplement lue ; l’interprétation ne nécessite pas de loi conditionnelle.

## Activité 3 — Deux états, une observation (25 min)

| Élément | Spécification |
|---|---|
| Objectifs / question | O2/O8 et préparation O6 ; une observation identique suffit-elle à garantir une sortie immédiate correcte ? |
| Hypothèse | Une couleur initiale utile disparaît ; sans information passée la dernière décision ne peut distinguer les deux mondes. |
| Paramètres contrôlés | Grille 3 × 2 décrite dans le script, parcours imposé droite/bas, position visible, budget trois commandes au total. |
| Variable modifiée | Couleur réelle bleu/orange, visible seulement au départ. |
| Données recueillies | Trois états et trois observations par monde ; commandes imposées puis décision finale proposée sur papier. |
| Protocole | Prédire deux colonnes ; lancer `s02_observation_masquee.py` ; comparer d’abord la première observation, puis les deux dernières ; choisir la sortie dans chacun des mondes. |
| Attendu / réussite | Historique initial différent, observation finale identique ; gauche et droite respectivement nécessaires avec une commande restante. Un contre-exemple est formulé avec sa contrainte de tâche. |
| Limites | Pas d’agent autonome ni contrôleur à mémoire programmé. Sans budget ou avec une commande d’interrogation, une autre analyse serait nécessaire. Aucune interface de masque intégrée au labo. |

Indices : I1, conserver dans le tableau la couleur réelle même si elle n’est plus reçue ; I2, `None` n’est pas une couleur ; I3, distinguer la dernière observation des trois observations reçues. Tests : les observations au départ diffèrent ; en `(1,1)` elles sont égales et ne contiennent plus la couleur ; droite/bas mènent effectivement à `(1,1)` ; les sorties requises diffèrent.

Modification de code possible dans les mêmes 25 min pour un groupe rapide : faire transmettre la couleur dans toutes les observations et noter pourquoi le contre-exemple change. Ce n’est pas une « correction de l’agent » : cela change le capteur. Ne pas programmer la mémoire à ce jalon.

## Exercices intégrés et preuves à rendre

| ID / créneau | Travail | Objectif et hypothèse mise à l’épreuve | Preuve attendue, indice et limite |
|---|---|---|---|
| S02-A / état-observation | Classer une donnée du monde et son accès au code | O2 ; affiché ne signifie pas seul connu | Nom de champ transmis ; inspecter la signature ; pas de vrai capteur. |
| S02-B / état-observation | Caméra coupée : proposer deux mondes | O2/O8 ; absence de signal ≠ monde vide | Deux états plausibles pour même signal ; ne pas inventer le monde réellement présent. |
| S02-C / TP02 | Prédire le mur | O4 ; candidate peut différer de l’après | Trace complète ; calculer avant de tester ; règle d’arrêt du labo explicitée. |
| S02-D / TP02 | Modifier la fonction et vérifier bord/libre | O4 ; la transition doit traiter deux branches | Code, appels et résultats ; utiliser `libre` ; cas choisis non preuve de tous les programmes. |
| S02-E / TP02 | Expliquer l’absence de détour | O8 ; transition ≠ choix de chemin | Deux responsabilités séparées ; chercher qui choisit l’action ; aucune recherche cachée. |
| S02-F / glissement | Interpréter une série | O8 ; l’effet varie à commande fixe | Variable modifiée/contrôles/limite ; lire le paramètre tirage ; aucun résultat universel sur huit essais. |
| S02-G / masque | Construire un contre-exemple | O2/O8 ; entrée identique, besoins différents | Deux états et une observation commune ; rappeler budget et sorties ; pas de généralisation à toutes les tâches. |

Bilan individuel B1–B5 dans la fiche : seuil proposé quatre réponses sur cinq avec état/observation et refus indispensables. Les corrigés explicitent les réponses et les remédiations ; un programme qui tourne ne valide pas seul le raisonnement.
