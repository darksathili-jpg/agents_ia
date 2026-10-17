# Objectifs observables, prérequis et correspondances NSI

Références P0–P2 : [bibliographie](REFERENCES_SCIENTIFIQUES.md). Les correspondances ci-dessous résultent de la lecture des annexes actuellement référencées par éduscol, pas d’une assimilation de la NSI à un cours d’IA.

## Cartographie réglementaire et transposition

**D** : contenu directement inscrit ; **A** : application de ce contenu ; **F** : approfondissement facultatif, sans prétention réglementaire.

| Appui vérifié, rubrique officielle | Classe / statut | Application proposée et limite |
|---|---|---|
| Langages et programmation : constructions élémentaires, spécification, mise au point | Première, D [P1] | A : contrat de décision, assertions et code à compléter ; le succès de tests n’établit pas une preuve universelle. |
| Types construits : p-uplets, tableaux, dictionnaires | Première, D [P1] | A : coordonnées et enregistrement d’une observation ; les ensembles Python sont expliqués et non exigés d’emblée. |
| Architectures : capteurs et actionneurs dans l’interface d’un système embarqué | Première, D [P1] | A : capteurs simulés ; la grille ne représente pas la perception physique réelle du robot illustré. |
| Algorithmique : algorithmes gloutons | Première, D [P1] | A : choix local ; notre règle horizontale est un témoin volontairement limité, pas tout l’algorithme best-first. |
| Structures de données : listes, piles, files ; graphes et représentations | Terminale, D [P2] | A : choix de FIFO et graphe de cases accessibles. Aucun formalisme d’agent exigé par cette rubrique. |
| Algorithmique : parcours en profondeur/largeur, recherche d’un chemin | Terminale, D [P2] | A : BFS dans un labyrinthe ; preuve d’optimalité conditionnelle approfondie pour enseignants. |
| Programmation objet, modularité | Terminale, D [P2] | A possible : encapsuler la mémoire ; une classe n’est pas requise pour le pilote. |
| Agent, autonomie, rationalité, observation partielle, utilité, agent LLM | Première/Terminale, F | Cadres scientifiques du module ; ne pas les annoncer comme rubriques explicitement prescrites dans ces annexes. |

Les renvois portent sur les rubriques, non sur des citations textuelles. Rôle des structures, lecture de programmes et raisonnement sont réinvestis ; le nombre de notions nouvelles doit rester maîtrisé.

## Prérequis et diagnostic

Élève : lire une condition et un `return`, appeler une fonction, parcourir une petite liste et repérer `(x,y)`. Diagnostic : prédire `decider((0,2),(2,2),[])`, repérer un retour manquant et écrire une assertion. Une difficulté conduit à 10 min de code guidé dans le temps prévu du TP01, pas à une exclusion.

Première : tableaux et fonctions fournis, explications sans calcul probabiliste ; TP04 observé ou squelette guidé si les graphes n’ont pas été étudiés. Terminale : mobiliser files/graphes lorsque déjà enseignés ; ne pas supposer que tout élève de Terminale les connaît au premier cours. Enseignant : même socle Python, puis notation ensembliste et probabilité conditionnelle introduites progressivement ; aucun appel API requis. Aucune connaissance de réseau neuronal n’est nécessaire.

## Dix objectifs et preuves attendues

| ID | Compétence observable | Séance / activité | Preuve et seuil pédagogique proposé |
|---|---|---|---|
| O1 | Définir et délimiter un agent | S1, E01–02 | Nommer observation, décision, action et environnement pour deux cas. |
| O2 | Identifier les informations accessibles | S2, E06–07, TP03 | Distinguer deux états donnant une même observation. |
| O3 | Distinguer modèle de langage et système agent | S1/S5, E03/E15 | Séparer génération et exécution d’une action ; justifier un cas ambigu. |
| O4 | Décrire une politique | S1/S3, E04/E09 | Prédire trois retours d’une fonction et citer son domaine. |
| O5 | Programmer un agent réactif | S1/S4, TP01 | Fonction conforme sur les cas droit, gauche, arrivée et conflit. |
| O6 | Expliquer un état interne | S3, TP03/E08 | Même observation, mémoire différente, action différente ; pas de mémoire magique du Worker. |
| O7 | Comparer des politiques à conditions fixes | S4/S5, TP04–05 | Tableau de plusieurs cas, avec échecs et conditions d’arrêt. |
| O8 | Borner une conclusion expérimentale | S2/S5, E10/E14 | Identifier au moins deux hypothèses invalidant une généralisation. |
| O9 | Distinguer déterminisme, hasard et LLM | S3/S5, E11/E15 | Un tirage aléatoire ne transforme pas le script en LLM. |
| O10 | Justifier une évaluation | S5, E13 et épreuve | Métrique définie, effectif, traitement des échecs et interprétation. |

Ces seuils sont des choix de conception à éprouver avec apprenants. Pour l’enseignant, on ajoute une justification formelle, une critique de source et une transposition didactique, plutôt qu’un simple allongement du vocabulaire.

## Difficultés structurantes à surveiller

« Décider » ne signifie pas penser consciemment ; un objectif est fixé dans la tâche, pas forcément représenté explicitement dans le code. Une action admissible peut échouer dans l’environnement. Mémoire ne signifie pas modèle complet du monde. Une politique déterministe peut comporter une recherche complexe ; une politique stochastique peut être très simple. Une réussite isolée n’établit ni robustesse ni intelligence générale.
