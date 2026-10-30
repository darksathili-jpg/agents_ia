# ORCHESTRA — Terminale T02 · BFS contre DFS

## Positionnement

Ce module prolonge T01. Les capacités travaillées relèvent du programme
de Terminale NSI : parcourir un graphe en profondeur et en largeur,
rechercher un chemin, utiliser les structures de données **file** et **pile**,
raisonner sur les coûts des opérations.

Référence officielle : https://eduscol.education.gouv.fr/5823/programmes-et-ressources-en-numerique-et-sciences-informatiques-voie-g

**Durée suggérée :** trois séances de 55 minutes.

### Séance 1 — Observer, formuler une hypothèse (55 min)
- Prédire le prochain sommet retiré d'une file et d'une pile.
- Manipuler le terrain « Un détour trompeur ».
- Identifier les sommets découverts, traités et le chemin reconstruit.
- Expliquer pourquoi BFS trouve ici un plus court chemin.
- Observer que DFS peut aussi trouver un plus court chemin dans certains cas,
  sans que ce résultat soit garanti.

### Séance 2 — Programmer les parcours (55 min)
- Compléter les fonctions Python \`chercher_largeur\` et \`chercher_profondeur\`.
- Utiliser respectivement une file FIFO et une pile LIFO.
- Construire les prédécesseurs pour reconstruire un chemin.
- Gérer les cas limites : départ = cible et cible inaccessible.
- Tester les programmes avec les contre-exemples fournis.

### Séance 3 — Justifier et transférer (55 min)
- Comparer une nouvelle grille et exposer les stratégies.
- Justifier le choix BFS/DFS selon l'objectif.
- Expliquer la différence entre complexité du parcours en \`O(V+E)\`
  avec des opérations de structure à temps constant, et la complexité réelle
  de \`list.pop(0)\` en \`O(n)\` sur les listes Python.
- Étudier une variante d'implémentation de file (indice de tête, etc.).

## Distinction indispensable

La **démonstration guidée** est calculée en JavaScript, à partir
du terrain choisi et de l'ordre des voisins.

Les **résultats Python** sont produits par \`runner_t02.py\` dans le Worker
Pyodide. Le journal des appels à \`File.enfiler / defiler\` et
\`Pile.empiler / depiler\` provient des appels réellement instrumentés.

Le dispositif n'affirme jamais que la visualisation guidée est une trace
du code de l'élève. La justification écrite est indispensable ; elle n'est
pas évaluée automatiquement.

## Fiabilité des comptes rendus

Une modification de code invalide immédiatement le score et les traces
de l'exécution précédente. Les résultats d'une exécution encore en cours
sont ignorés si le code a été modifié entre-temps. Chaque situation
affiche séparément : chemin BFS, utilisation FIFO, chemin DFS, utilisation LIFO.
Un score de deux parcours signifie que les deux méthodes passent leurs
contrats ; il ne constitue **pas** une note de compréhension.

## Critères et limites

- BFS : chemin valide **et minimal**.
- DFS : chemin valide, **sans imposer** qu'il soit minimal.
- Utilisation effective de File/Pile vérifiée par appels observables, mais
  ces contrôles ne prouvent pas formellement la méthode, ni la compréhension.
- 7 situations de test, dont des grilles variées avec graine.
- Fonctionnement local Pyodide 0.27.7 : requiert un serveur HTTP, et doit
  encore être éprouvé sur un poste Edge du lycée.
- Worker Pyodide **n'est pas une sandbox de sécurité** pour du code hostile.

## Recette

\`\`\`text
python -m pytest -q tests/test_t02.py
node tests/test_t02_visualizer.cjs
node --check terminale/t02/lab.js
node --check terminale/t02/python-worker.js
python scripts/build_site.py --require-local-pyodide
\`\`\`

Tester manuellement desktop 1440 px, 900 px et mobile 390 px, modes
clair/sombre/projection, navigation clavier, zoom 200 %, ralentissement,
dépassement du temps maximum et arrêt/recréation du Worker.

**Statut :** module candidat ; ne pas présenter comme validé en classe
sans ces recettes.
