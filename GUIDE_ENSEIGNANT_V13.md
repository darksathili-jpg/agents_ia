# Guide enseignant — Terminale NSI T01, version corrective v1.3

**Sujet réel :** programmer un agent déterministe qui planifie dans un graphe de grille, conserve un chemin, et le réexamine si un obstacle apparaît. Il ne s'agit pas encore d'agents fondés sur un LLM.

## Prérequis

Variables, listes, dictionnaires, fonctions Python ; définition d'une classe, attributs et méthodes ; tuples `(x, y)` ; conditions et boucles. Présenter le vocabulaire de graphe, sommet, arête et file avant l'activité.

## Objectifs observables et preuves

| Objectif | Travail demandé | Preuve à recueillir |
|---|---|---|
| Interpréter un graphe de grille | Relever les voisins des sommets | Croquis / réponse expliquée |
| Comprendre FIFO | Simuler ajouter puis retirer A, B et C | Ordre `A, B, C` justifié |
| Programmer un BFS | Écrire `planifier` avec `File`, prédécesseurs, reconstruction | Tests de plus court chemin + trace observée des retraits ; expliquer pourquoi BFS découvre par couches |
| Programmer l'agent | Écrire `pas_suivant`, mettre à jour `self.position` et `self.plan` | Trajectoire + état du plan après chaque pas |
| Réagir à l'obstacle | Recalculer uniquement si le chemin en cours est devenu inutilisable | Nombre de planifications sur terrain stable puis obstacle dynamique |
| Évaluer les limites des tests | Discuter une stratégie alternative | Bilan écrit / oral, **non inféré d'un score** |

## Progression recommandée — quatre étapes

**Étape A, 20–30 min — le graphe.** Montrer la grille. Demander les voisins du départ, lister les cases bloquées, dessiner un graphe de petite taille. Avant d'utiliser `monde.voisins`, demander ce que cette fonction doit retourner.

**Étape B, 35–50 min — FIFO et BFS.** Donner une file de trois éléments à manipuler sur papier. Écrire `planifier` d'abord. Explorer, stocker les prédécesseurs et reconstituer la liste de cases. Faire formuler la condition d'arrêt et le cas inaccessible.

**Étape C, 30–45 min — POO et plan.** Construire `pas_suivant` avec `self.position` et `self.plan`. Définir le contrat : `self.plan` est un itinéraire restant valide, commençant par la position actuelle ou par la prochaine case, et se terminant à la cible. L'élève doit le réutiliser entre les déplacements ; ne pas recalculer systématiquement.

**Étape D, 30–45 min — événement imprévu, validation et justification.** Montrer la démonstration avant/après en (2,2), puis exécuter le code. Comparer les traces d'un cas stable et d'un cas dynamique, noter quand le BFS est relancé. Exiger un court bilan : pourquoi le chemin initial n'était plus utilisable ? quels tests seraient nécessaires pour garantir davantage de sûreté ?

Ces durées sont indicatives, à adapter aux prérequis réels. Les quatre étapes sont un accompagnement d'une même application, **pas quatre applications autonomes déjà développées**.

## Évaluation : trois registres distincts

1. **Fonctionnalité (automatique)** : chemin minimal, absence de collision et arrivée.
2. **Méthode (indices automatiques)** : retraits/enfilages cohérents et réutilisation d'un plan, avec critères documentés. Ce contrôle détecte les mutations étudiées mais n'est pas inviolable.
3. **Compréhension (enseignant)** : explication des prédécesseurs, de la file, de l'invariant de parcours et de la nécessité de replanifier ; aucun badge automatique ne peut valider ce point seul.

## Risques et limites

- `File` utilise `list.pop(0)`, coût linéaire au retrait : choix d'enseignement sur de petits graphes, pas une recommandation de performance.
- Les objets Python fournis au code élève ne constituent pas une isolation sécurisée contre un adversaire déterminé.
- Pyodide hors connexion, Edge, zoom à 200 %, lecteur d'écran, interruptions réelles et réseau du lycée : **non validés ici**.
- Le parcours Première v5.1 et son moteur sont conservés, mais une expérimentation en classe ne doit commencer qu'après la recette informatique.
