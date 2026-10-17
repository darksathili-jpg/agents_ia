# Séance 03 — Architectures d’agents, politiques de décision et mémoire

Parcours NSI ; **120 minutes estimées**, non mesurées en classe. Question : « Comment utiliser une information qui n’est plus visible ? » Prérequis : S01/S02, fonctions avec retour, `if`, tuples, lecture de dictionnaire et boucle `for` fournie. Aucun LLM, apprentissage automatique ou calcul de probabilités conditionnelles requis.

Objectifs observables : écrire un contrôleur `(observation, memoire) → (action, nouvelle_memoire)` ; expliquer sa mise à jour ; prévoir trois traces ; tester les deux mondes et un indice absent ; situer réflexe, état interne, objectif, utilité et hasard sans les confondre.

Utiliser le [support élève](SUPPORT_ELEVE_S03.md). Les [corrigés](CORRIGES_S03.md) et le [parcours enseignant](ENSEIGNANT_S03.md) sont distribués séparément.

| Temps | Travail intégré | Preuve attendue |
|---|---|---|
| 0–10 | Rappel S02, hypothèses | Observation commune et sorties différentes. |
| 10–25 | Traces prédictives, oubli et écrasement | Localisation précise de la perte de couleur. |
| 25–40 | Contrat et modèle de mémoire | Règle de mise à jour formulée. |
| 40–80 | TP03 : programmer, tester, corriger | Deux réussites et une trace commentée. |
| 80–95 | Limites, absence et erreur de mémoire | Cas qui invalide une garantie trop générale. |
| 95–110 | Architectures, objectif, utilité et hasard | Comparaison justifiée sur deux décisions. |
| 110–120 | Bilan individuel | Code, preuve et limite. |

Les exercices A à G sont intégrés aux plages indiquées, sans ajout de devoir obligatoire. Première : conducteur et table des positions fournis, travail en binôme puis bilan seul. Terminale : invariant et contre-exemple remplacent une partie de la saisie guidée. La lecture longue enseignante est préparatoire ; son activité courte remplace le guidage de 95–110 min, elle ne s’ajoute pas aux 120 min.

## Observer et faire une hypothèse — 0 à 25 min

Reconstituer le parcours S02 : départ `(0,0)`, droite vers `(1,0)`, bas vers `(1,1)`. Le bleu autorise la sortie gauche `(0,1)`, l’orange la droite `(2,1)`. Il reste une commande : retourner lire l’indice ne résout pas cette tâche. La couleur est stable dans un épisode, visible seulement au départ.

A : expliquer pourquoi la dernière observation ne distingue pas les mondes. B : prédire les résultats d’une règle qui choisit toujours gauche à la bifurcation. Elle réussit dans le monde bleu ; cela ne suffit pas à valider les deux mondes.

Comparer ensuite une règle qui remplace sa mémoire par `observation["indice"]` à chaque pas. Dans le couloir, cette valeur est `None`. C : prédire ce qui est perdu. `None` signifie « information non reçue », pas « couleur effacée dans le monde ». Écrire une hypothèse testable : conserver la dernière couleur effectivement observée devrait permettre les deux sorties, sous les hypothèses annoncées.

## Comprendre le mécanisme — 25 à 40 min

Une **politique réactive sans mémoire**, au sens retenu ici, dépend seulement de l’observation courante. Un **contrôleur à état interne** reçoit aussi une information conservée. Le mot réactif peut avoir un sens plus large dans d’autres travaux ; préciser toujours la définition utilisée.

La mémoire du TP vaut `None`, `"bleu"` ou `"orange"`. Elle ne lit pas directement la couleur cachée. On actualise d’abord la mémoire si une couleur est reçue, puis on calcule l’action avec cette mémoire actualisée. Le conducteur réinjecte explicitement le retour au pas suivant. Une variable locale perdue entre deux appels ne suffit pas.

D : écrire en français la règle complète : « si un indice est reçu, le retenir ; sinon conserver la mémoire antérieure ». Tester mentalement `(indice=None, mémoire=orange)` et `(indice=bleu, mémoire=None)`. Un dictionnaire riche ou une grande mémoire ne garantissent ni exactitude ni utilité.

## TP03 — 40 à 80 min

Copier entièrement [s03_depart.py](python/s03_depart.py) dans l’éditeur du laboratoire et utiliser **Exécuter Python**, mode console. Il conserve la boucle dans une seule exécution Pyodide. **Le laboratoire actuel ne conserve pas de mémoire Python persistante entre les décisions de la grille.** Le script ne fournit pas `decider` et ne pilote pas la grille ; ne pas choisir Mon agent Python pour ce TP. Aucun Worker n’est modifié.

Compléter seulement `a_completer`, dont le retour initial `arrêt` est volontairement insuffisant. Les autres contrôleurs et le conducteur servent de comparaison. Le sujet contient des exemples de défauts, sans fournir la correction de la mise à jour.

Protocole : cinq minutes de prédictions ; vingt minutes de code guidé ; dix minutes de tests et traces ; cinq minutes d’interprétation. Garder carte, chemin et budget fixes. Variable étudiée : règle de mémoire. Mesurer issue et suite des observations/actions/mémoires, pas une impression d’intelligence. Remplacer dans le bloc final le contrôleur à essayer par `a_completer`, puis lancer successivement bleu et orange. Comparer à `oublier` et `ecraser`.

Résultats recherchés : droite, bas, gauche dans le monde bleu ; droite, bas, droite dans le monde orange ; couleur conservée dans les deux dernières décisions. Une réussite sans la bonne trace n’établit pas que le mécanisme attendu est utilisé.

Indices gradués : 1. séparer observation et mémoire ; 2. tester `is not None` ; 3. appeler `commander(observation, memoire)` après la mise à jour et retourner aussi `memoire`. Les erreurs Python sont corrigées à partir du message réel. Une exécution normale comporte au plus trois appels au contrôleur. Si du code ajouté boucle, utiliser Stop ; la borne du conducteur ne protège pas contre une boucle infinie à l’intérieur de la fonction élève.

## Interpréter et éprouver les limites — 80 à 95 min

E : lancer un épisode avec `visible=False`, mémoire initiale `None`. Le contrôleur corrigé s’arrête à la bifurcation : il ne retrouve pas une couleur jamais reçue. Le critère de réussite n’est pas atteint, même si cet arrêt évite une décision arbitraire.

F : initialiser la mémoire à bleu dans le monde orange et cacher l’indice. La mauvaise information persiste et mène à gauche. Refaire avec l’indice visible : la mise à jour corrige alors la mémoire initiale. Distinguer initialisation erronée corrigible et erreur non détectable dans les observations reçues. Dans un monde qui changerait de couleur après le départ, retenir l’ancienne couleur pourrait aussi échouer : c’est un contre-exemple au modèle, pas une expérience prétendument déjà intégrée.

Terminale : expliquer pourquoi après la première observation fiable, la mémoire reste égale à la couleur de cet épisode ; préciser les hypothèses de stabilité et de capteur. On n’en déduit aucune garantie universelle.

## Situer les architectures — 95 à 110 min

Un **réflexe simple** applique des règles à l’observation seule. Un **réflexe avec état interne** utilise des règles sur une information conservée. La couleur du TP est un résumé utile, pas un modèle complet du monde. Le contrôleur corrigé reste essentiellement une table de règles : réussir une tâche fixée ne suffit pas à prouver qu’il planifie.

Dans une architecture **orientée objectif**, des états satisfaisant un but sont représentés et les conséquences des actions peuvent être comparées à l’aide d’un modèle. Dans une architecture **orientée utilité**, une fonction représente des préférences entre résultats ; sous incertitude, on peut comparer les utilités espérées selon un modèle explicite. Une utilité n’est ni une émotion ni une morale automatique.

G : sur deux plans fournis atteignant le même but, l’un coûte deux unités et l’autre cinq. Le seul test de but accepte les deux ; `U=-coût` préfère le premier. Si une panne non modélisée survient, ce choix n’est plus garanti. Ceci est une analyse sur table, sans implémentation de recherche ni anticipation du cours S04. Une architecture hybride pourrait combiner mémoire, choix de plan et règle d’arrêt de sécurité ; elle exige de définir leurs priorités.

Comparer enfin `choix_stochastique(0)` et `(1)` dans [le support corrigé](python/s03_tp.py), puis une série à graine fixe. Ici les commandes varient et les déplacements restent déterministes, contrairement au glissement de S02. À observation finale identique sans mémoire, tirer au hasard une sortie ne garantit pas les deux mondes. Les huit tirages illustrent une politique, sans mesurer sa qualité statistique. Ces axes (mémoire, objectif, utilité, hasard) se combinent : **la liste n’est pas une taxonomie exhaustive**.

## Bilan individuel — 110 à 120 min

Sans consulter la correction : B1 écrire la mise à jour et le retour ; B2 compléter une trace avec indice invisible et mémoire orange ; B3 expliquer l’échec de l’écrasement ; B4 distinguer hasard de décision et hasard de transition ; B5 donner une limite du contrôleur correct. Critères et remédiations dans le support et les corrigés. Arrêt de conception après S03 : S04/S05 restent à autoriser.
