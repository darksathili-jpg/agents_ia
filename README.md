# ORCHESTRA NSI — Première / Terminale · v1.6 (restauration Pyodide et contrôles de publication)

**Statut : candidate de recette, non approuvée pour diffusion définitive.**

**G2 — Publication :** les binaires Pyodide 0.27.7 ont été restaurés depuis le commit historique `1ecfac6`. Le site strict inclut `orchestra-build.json` avec l'identifiant Git du build et le contrôle SHA-256 de l'accueil. La recette réelle Edge sur un poste du lycée reste à effectuer. Voir `docs/stabilisation/G2_RESTAURATION_PUBLICATION.md`.

**Important v1.5 :** `README_SECURITE_DEPLOIEMENT.md` décrit le déploiement par liste blanche et la désactivation nécessaire de tout ancien workflow publiant `path: '.'`. `RAPPORT_CORRECTIONS_V15.md` détaille les écarts avec le dépôt et les limites vérifiées. Un nouveau workflow ne désactive pas automatiquement l’ancien.

## Ce que contient cette livraison

- **Première NSI** : atelier introductif sur un agent réflexe, conservé depuis v5.1.
- **Terminale NSI** : atelier Python sur la classe `AgentPlanificateur`, la file FIFO, le parcours en largeur (BFS), le plan mémorisé et la replanification.
- **Nouveau visualiseur Terminale** : remplace les deux dessins « Avant / Après ». Grille 7 × 5 entièrement cadrée, personnage Microduck, défilement des opérations `enfiler`, `defiler`, `monde.voisins`, indication de la file, cases explorées, obstacle et chemin.
- Modes **clair**, **sombre** et **vidéoprojecteur**.

## Exemple guidé vs résultats de l'élève

Avant une exécution, le visualiseur propose un **exemple guidé** de 197 instantanés produits à partir de la sortie de la solution de référence exécutée sous CPython. Cette démonstration ne prouve **rien** sur le code de l'élève. La solution de référence Première est désormais conservée dans les tests enseignants, exclus du site public. Le bouton de l’élève fournit une aide méthodologique, pas le corrigé intégral.

Après l'exécution des tests, le bouton **Mon exécution Python** permet de voir les opérations réellement enregistrées par `runner.py` lors du scénario « Obstacle imprévu ». Si aucune recherche n'a eu lieu, aucune exploration n'est fabriquée. La démonstration peut être réaffichée explicitement.

La représentation de la file est reconstruite à partir des opérations instrumentées sur la classe `File` de l'élève. Il ne s'agit pas d'une preuve formelle de correction d'un BFS : les tests et les traces ont des limites, et une justification écrite reste nécessaire.

## Démarrage Windows

1. Décompresser l'archive **dans un nouveau dossier** (ne pas écraser la version précédente).
2. Lancer `LANCER_ORCHESTRA.cmd`.
3. Ouvrir dans Edge l'adresse affichée par le lanceur, normalement `http://127.0.0.1:8000/`.
4. Cliquer sur **Terminale**, puis descendre à **Un obstacle apparaît. Que fait vraiment le BFS ?**.
5. Cliquer sur les trois phases, puis sur **▶ Lire**, les flèches ou le curseur.
6. Programmer les deux méthodes Python, lancer les tests, puis cliquer sur **Mon exécution Python**.

En développement, Pyodide 0.27.7 est disponible localement, avec CDN de secours. **En publication stricte v1.5**, Pyodide local et les empreintes sont requis et le CDN est désactivé. L'exécution Pyodide **n'a pas été validée dans Edge sur le réseau du lycée**.

## Vérifications

- 52 tests Première réussis ; 21 tests d'intégration réussis.
- 15 tests contradictoires/structurels enseignants réussis ; un test Node vérifie les trois phases, l'obstacle réel et l'absence de fausse trace.
- Rendu HTML/CSS/JS dans Chromium, Worker **simulé avec des résultats CPython authentiques**, sans erreurs JavaScript ni débordement horizontal sur trois formats (390, 900 et 1440 px).
- Cette recette ne démontre **pas** que le téléchargement et l'exécution de Pyodide dans Edge fonctionneront.

Voir `RAPPORT_VALIDATION_V14.md` et `RECETTE_EDGE.md`.

## Séparation élève / enseignant

Seul le dossier `_site/` construit par `scripts/build_site.py` exclut les corrigés et les scripts de vérification enseignants ; l’archive source de développement contient les tests. Une seconde archive destinée à l'enseignant fournit des audits reproductibles ; son contenu doit rester hors de la publication GitHub Pages destinée aux élèves.
