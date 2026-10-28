# G0 — Assainissement du dépôt ORCHESTRA (branche de revue)

**Base contrôlée :** `main` au commit `35158f326976c33635a17430300c437c8aa93711` (28 octobre 2026).

## Changements proposés

- Retirer du suivi Git les **193 fichiers** de `node_modules/` (18,7 Mo), les **8 fichiers** de `test-results/` (6,4 Mo), les **4 fichiers** `.pyc` et `debug.log`.
- Ajouter `.gitignore` pour éviter de réintroduire ces artefacts.
- Ajouter un test `tests/test_repository_hygiene.py`, automatiquement découvert par la CI existante.
- **Ne pas modifier** le moteur, les exercices, les graphismes, la branche `main` ni le workflow de déploiement à ce stade.

## Points bloquants non résolus par ce nettoyage

1. Le dépôt est **public** : `premiere/tests/reference_solution.py` et plusieurs guides enseignants sont consultables sur GitHub. Leur suppression dans une future PR ne les effacerait **pas de l'historique Git**. Décider d'une séparation privée avant de promettre un corrigé inaccessible aux élèves.
2. `pyodide/` ne contient que `README.txt` à ce commit ; la construction stricte doit refuser la publication. Ne pas annoncer de fonctionnement hors ligne avant récupération des binaires et vérification de leurs empreintes.
3. La CI exécute les tests Python et une construction non stricte `--allow-cdn` sur les PR ; cela ne prouve ni Pyodide dans Edge ni le fonctionnement hors connexion au lycée.
4. Les tests de l'utilisation de la file et du BFS ne prouvent pas l'apprentissage : une justification de l'élève et une recette pédagogique restent nécessaires.

## Vérification locale

```bash
python -m pytest -q premiere/tests tests qa_enseignant/test_redressement.py qa_enseignant/test_variantes.py qa_enseignant/test_visualiseur_bfs.py
node premiere/tests/editor_indent.test.cjs
python scripts/build_site.py --allow-cdn
python -m pytest -q tests/test_publication.py
```

**Interdit à cette étape :** fusion, mise en ligne, modification forcée des permissions, publication de données d'élèves.
