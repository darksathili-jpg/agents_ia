# ORCHESTRA NSI — Terminale T03 · Architecture d'un agent Microduck

## Positionnement NSI et statut

**Suite de T01/T02, sans fusion dans `main`.** Trois séances de 55 minutes.
Ce module illustre explicitement le vocabulaire du programme officiel :
**classe**, **objet**, **attribut**, **méthode**, **interface**, **implémentation**,
et **mise au point des programmes**. Le cycle perception–mémoire–décision–action
est ici une **modélisation pédagogique des agents**, non une compétence
officielle indépendante ajoutée au programme de Terminale.

Sources institutionnelles :
- https://eduscol.education.gouv.fr/5823/programmes-et-ressources-en-numerique-et-sciences-informatiques-voie-g
- https://www.education.gouv.fr/bo/2026/Special4/MENE2622643N

L'exercice ne présente pas un LLM comme moteur de Microduck : les décisions sont
**déterministes**. Cette distinction sera importante pour T04 (outils et contrats).

## Contrat de l'agent

`AgentMicroduck` est une classe Python.
Un objet de cette classe possède deux attributs d'instance :
- `position` : tuple de deux entiers, position observée ;
- `memoire` : ensemble de tuples de deux entiers, obstacles déjà observés.

`percevoir(observation)` actualise les attributs à partir du dictionnaire
`{"position": (x, y), "obstacles": ((x1, y1), ...)}`.
**L'observation est locale**, limitée aux cases adjacentes. Un obstacle qui
sort du champ d'observation doit rester dans `memoire`.

`decider(objectif)` ne déplace **jamais** directement l'agent.
La méthode calcule les cases voisines de la position courante, exclut les
cases hors du terrain (6 colonnes × 3 lignes) et les obstacles mémorisés,
puis renvoie la case minimisant la distance de Manhattan à l'objectif.
En cas d'égalité, l'ordre Est, Nord, Sud, Ouest prévaut.
La méthode renvoie `None` quand l'objet est déjà arrivé ou qu'aucun voisin
n'est admissible. Aucun attribut n'est modifié pendant la décision.

Le **monde**, et non la classe, vérifie ensuite l'action et actualise la position
physique. La perception suivante fournit cette nouvelle position à l'objet.

**Limite algorithmique :** cette règle est une politique locale, pas BFS/DFS.
Elle peut prendre de mauvaises décisions, tourner en rond ou ne pas atteindre
un objectif accessible. Une réponse de l'élève prétendant que cette méthode
garantit toujours un plus court chemin doit être rejetée.

## Séance 1 — Observer, distinguer, anticiper (55 min)

1. Faire découvrir une grille sans obstacle ; prédire l'action.
2. Faire apparaître l'obstacle en `(3,1)`. Distinguer information visible et
   mémoire persistante sur le cycle suivant.
3. Arrêter la chronologie et demander quelle partie appartient à l'objet,
   au capteur et au monde.
4. Faire formuler une hypothèse testable sur la sélection d'un voisin.

Question de diagnostic : « Après `decider`, `self.position` a-t-elle changé ? »
Réponse attendue : non ; seule l'action validée dans le monde déplace Microduck.

## Séance 2 — Programmer et tester (55 min)

1. Donner le squelette `terminale/t03/eleve.py` sans corrigé.
2. Compléter `percevoir` : affecter à `self.position` la position observée,
   puis ajouter à `self.memoire` les obstacles détectés.
3. Compléter `decider` ; parcourir les candidats avec une boucle bornée,
   exclure les cases invalides et comparer les distances.
4. Exécuter les **sept contrôles Python réels** (Pyodide en Worker).
5. Examiner une trace du programme élève validé ; ne jamais confondre avec
   la démonstration JavaScript.

Aides graduées :
- niveau 1 : identifier les deux attributs de l'objet ;
- niveau 2 : écrire les quatre tuples de voisins dans l'ordre imposé ;
- niveau 3 : comparer explicitement les distances de Manhattan ;
- niveau 4 : étudier le cas `None` (cible atteinte ou voisins bloqués).

## Séance 3 — Argumenter et transférer (55 min)

Faire expliquer la persistance de la mémoire sur le scénario « Mémoire ».
Demander un contre-exemple à la politique gloutonne.
Pour aller plus loin : remplacer la décision locale par une
**planification BFS** comme dans T02, mais conserver séparées la perception,
la mémoire, la décision et l'exécution d'action.

**Évaluation humaine recommandée** : exactitude du vocabulaire
(objet/attribut/méthode), compréhension du capteur incomplet, distinction
décision/action, limites d'une stratégie locale, justification du transfert.

## Vérification et sécurité

- `python -m pytest -q qa_enseignant/test_t03.py`
- `node tests/test_t03_visualizer.cjs`
- `python tests/browser_t03.py` (Chromium Playwright + Pyodide local)
- `python scripts/build_site.py --allow-cdn` en développement
- Pour publier : construction stricte Pyodide local vérifié, validation
  humaine explicite et **aucune fusion automatique**.

Les tests refusent les codes incomplets, l'oubli de mémoire, les collisions
et les décisions qui changent la position. Ils vérifient plusieurs scénarios
et les traces individuelles. Ils ne constituent **ni preuve formelle ni
isolation sûre de code hostile**. L'élève ne doit exécuter que du code
supervisé et ne doit pas importer de bibliothèques arbitraires.

La distribution élève exclut les fichiers `qa_enseignant`, les tests
et les solutions de référence. Le caractère **vrai** des résultats est
garanti par l'exécution de `runner_t03.py`, jamais par le simulateur de
démonstration.
