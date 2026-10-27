# ORCHESTRA NSI — Première / Terminale · v1.4 (visualiseur BFS)

**Statut : candidate de recette, non approuvée pour diffusion définitive.**

## Ce que contient cette livraison

- **Première NSI** : atelier introductif sur un agent réflexe, conservé depuis v5.1.
- **Terminale NSI** : atelier Python sur la classe `AgentPlanificateur`, la file FIFO, le parcours en largeur (BFS), le plan mémorisé et la replanification.
- **Nouveau visualiseur Terminale** : remplace les deux dessins « Avant / Après ». Grille 7 × 5 entièrement cadrée, personnage Microduck, défilement des opérations `enfiler`, `defiler`, `monde.voisins`, indication de la file, cases explorées, obstacle et chemin.
- Modes **clair**, **sombre** et **vidéoprojecteur**.

## Exemple guidé vs résultats de l'élève

Avant une exécution, le visualiseur propose un **exemple guidé** de 197 instantanés produits à partir de la sortie de la solution de référence exécutée sous CPython. Cette démonstration ne prouve **rien** sur le code de l'élève. Aucune solution Python de référence n'est intégrée au site.

Après l'exécution des tests, le bouton **Mon exécution Python** permet de voir les opérations réellement enregistrées par `runner.py` lors du scénario « Obstacle imprévu ». Si aucune recherche n'a eu lieu, aucune exploration n'est fabriquée. La démonstration peut être réaffichée explicitement.

La représentation de la file est reconstruite à partir des opérations instrumentées sur la classe `File` de l'élève. Il ne s'agit pas d'une preuve formelle de correction d'un BFS : les tests et les traces ont des limites, et une justification écrite reste nécessaire.

## Démarrage Windows

1. Décompresser l'archive **dans un nouveau dossier** (ne pas écraser la version précédente).
2. Lancer `LANCER_ORCHESTRA.cmd`.
3. Ouvrir dans Edge l'adresse affichée par le lanceur, normalement `http://127.0.0.1:8000/`.
4. Cliquer sur **Terminale**, puis descendre à **Un obstacle apparaît. Que fait vraiment le BFS ?**.
5. Cliquer sur les trois phases, puis sur **▶ Lire**, les flèches ou le curseur.
6. Programmer les deux méthodes Python, lancer les tests, puis cliquer sur **Mon exécution Python**.

Pyodide est chargé localement s'il a été installé avec `INSTALLER_PYODIDE.cmd`, sinon depuis un CDN. L'exécution Pyodide **n'a pas été validée dans Edge sur le réseau du lycée**.

## Vérifications

- 52 tests Première réussis ; 21 tests d'intégration réussis.
- 15 tests contradictoires/structurels enseignants réussis ; un test Node vérifie les trois phases, l'obstacle réel et l'absence de fausse trace.
- Rendu HTML/CSS/JS dans Chromium, Worker **simulé avec des résultats CPython authentiques**, sans erreurs JavaScript ni débordement horizontal sur trois formats (390, 900 et 1440 px).
- Cette recette ne démontre **pas** que le téléchargement et l'exécution de Pyodide dans Edge fonctionneront.

Voir `RAPPORT_VALIDATION_V14.md` et `RECETTE_EDGE.md`.

## Séparation élève / enseignant

L'archive de l'application **ne contient pas** les corrigés ni les scripts de vérification enseignants. Une seconde archive destinée à l'enseignant fournit des audits reproductibles ; son contenu doit rester hors de la publication GitHub Pages destinée aux élèves.
