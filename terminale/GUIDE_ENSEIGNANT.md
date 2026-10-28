# Terminale NSI · T01 — Programmer un agent planificateur

**Séquence conseillée : deux séances de 55 minutes**, suivies éventuellement d'une évaluation de code. Ne pas présenter cette activité comme un parcours complet de formation à l'IA.

## Problème posé à l'élève

Un robot virtuel parcourt un quadrillage. Les cases libres sont les sommets d'un graphe non orienté ; les déplacements orthogonaux représentent ses arêtes. Un obstacle peut apparaître après la préparation du trajet. La classe Python `AgentPlanificateur` doit programmer :

1. `planifier(monde, objectif)` : produire le chemin le plus court par parcours en largeur (BFS), en utilisant une **file FIFO** (classe `File` avec `enfiler`, `defiler`, `est_vide`, fondée sur une liste Python) et la mémorisation des prédécesseurs. Renvoie `[]` si aucun chemin n'existe.
2. `pas_suivant(monde, objectif)` : consulter l'état du monde avant d'agir, mémoriser un plan dans `self.plan`, détecter un obstacle apparu et recalculer si nécessaire ; ne pas entrer dans une case bloquée.

La méthode `monde.voisins(case)` est **fournie**. Cela signifie que la traduction complète du terrain en liste d'adjacence **n'est pas réalisée par l'élève** dans T01 : la représentation d'un graphe devra faire l'objet d'un autre atelier.

## Déroulement recommandé

**Séance A : comprendre et programmer BFS.** 10 min d'observation : sommets, voisins, cible, obstacle. 10 min pour expliciter la file et les couches de BFS sur papier. 25 min de codage de `planifier`, découverte des indices gradués si nécessaire. 10 min de justification du chemin, du cas inaccessible et de la notion de longueur minimale.

**Séance B : conserver et contrôler le plan.** 10 min d'anticipation et de lecture de la trace de l'exploration. 30 min pour programmer `pas_suivant` et contrôler le monde avant chaque action, puis replanifier après un obstacle. 15 min pour comparer les réussites et échecs, inspecter les traces et exporter le bilan.

## Ce que l'évaluation vérifie réellement

- Neuf situations distinctes (direct, détour, inaccessible, obstacle dynamique, départ=arrivée, deux variantes déterministes à graines fixes, départ bloqué et cible bloquée).
- Le résultat de `planifier` est testé **séparément** des décisions de `pas_suivant` et les deux verdicts sont affichés.
- Le monde de référence est indépendant des objets consultables par l'élève : modifier sa vue ne change pas la géométrie qui valide ses déplacements.
- La présence d’une classe `File` et de ses opérations `enfiler`/`defiler` est repérée statiquement. **Cela ne prouve pas à soi seul l'algorithme** : faire expliciter la logique du BFS, la structure FIFO et l'invariant des distances.
- La visualisation des points bleus est issue des appels à `monde.voisins`, **pas d'une lecture de la file privée de l'élève**.

## Critères d'évaluation suggérés

| Dimension | Indices observables |
|---|---|
| Représentation du problème | Repère sommets, arêtes et sommets bloqués |
| Structure FIFO et BFS | Explique pourquoi les couches sont explorées dans l'ordre |
| Reconstruction | Le chemin est adjacent, minimal ou absent selon le cas |
| Replanification | N'agit jamais sur la base d'une information périmée |
| Argumentation | Sait distinguer cas testés, garantie et limites |

## Limites

Pas de DFS ni de cycle, de récursivité, ni de programmation par liste d'adjacence construite par l'élève dans T01. Pas de LLM. Tests navigateur réalisés sur rendu HTML avec Worker simulé ; Pyodide réel et réseau du lycée à valider sur place.


**v1.2.** On n’impose plus `collections.deque` : la classe `File` fournie illustre les opérations FIFO avec des listes, et l’élève programme réellement l’exploration, les prédécesseurs et la replanification. La marche de Microduck dans le héros est décorative.

Pour cette grille 7×5, l’implémentation pédagogique de `File` utilise `list.pop(0)` : elle reste simple mais retire les éléments en coût linéaire. Ce compromis n’est pas à privilégier pour de très grandes files.


## Ajustements v1.5 — vérification du scénario dynamique

Le panneau « Obstacle » montre d'abord un aperçu guidé et fixe. Le Worker de
l'élève tire une graine pour choisir la ligne du parcours (0 à 4) : l'obstacle
apparaît devant le robot après son premier pas. Le bilan exporté contient la
graine afin que l'enseignant puisse reproduire la situation. Il ne s'agit pas
d'un secret cryptographique ni d'une preuve de compréhension du BFS.

**Publication :** utiliser exclusivement `scripts/build_site.py` et la liste
blanche documentée dans `README_SECURITE_DEPLOIEMENT.md`. Ne pas publier ce
guide ni les fichiers de tests.
