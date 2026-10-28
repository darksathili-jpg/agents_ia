# Publication contrôlée — Procédure administrateur

Cette archive est une **proposition de correctif**, pas une modification automatique de ton dépôt GitHub.

1. Conserver une branche de travail ; comparer les fichiers avec ceux du dépôt actuel. Ne jamais écraser les fichiers Pyodide locaux existants ni le manifeste SHA-256 sans vérification.
2. **Désactiver l'ancien workflow** dont `actions/upload-pages-artifact` publie `path: '.'` ; tant qu'il existe, la liste blanche du nouveau workflow ne protège pas la publication.
3. Copier le script `scripts/build_site.py` et adapter/remplacer le workflow existant avec `.github/workflows/pages.yml`. La publication passe par le dossier `_site` uniquement.
4. Lancer les tests ; corriger tout échec avant la publication. Depuis la racine du projet : `python -m pytest -q premiere/tests tests qa_enseignant/test_redressement.py qa_enseignant/test_variantes.py qa_enseignant/test_visualiseur_bfs.py` puis `node premiere/tests/editor_indent.test.cjs`.
5. Vérifier Pyodide local (fichiers et empreintes dans `MANIFEST_INSTALLATION.json`). Si le manifeste actuel a un autre format, ne pas l'écraser : adapter le script de vérification après examen du format réel.
6. Construire `python scripts/build_site.py --require-local-pyodide` : aucune publication si la distribution est absente/incomplète/corrompue. Inspecter `_site` ; il ne doit pas contenir `tests/`, `qa_enseignant/`, `.github/`, `*.md`, fichiers de référence ni `*.cmd`.
7. Sur un poste élève Edge, vérifier les deux parcours, le démarrage Pyodide en **mode hors ligne**, les scénarios et les traces, puis le zoom 200 % et le vidéoprojecteur.
8. Seulement après approbation humaine, déclencher manuellement l'action GitHub avec `confirmation=PUBLIER`. Une éventuelle protection d'environnement GitHub Pages est recommandée.

**Pas de diffusion à ce stade.** Le script ne supprime pas les fichiers déjà présents sur GitHub Pages ni ne révoque une ancienne publication : les fichiers publiés antérieurement peuvent demeurer accessibles tant que le site n'a pas été reconstruit et republié proprement.
