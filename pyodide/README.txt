ORCHESTRA NSI — Pyodide 0.27.7 (exécution Python dans le navigateur)

Distribution restaurée depuis le commit Git historique
1ecfac610d6d62d8b6656c9ff05b269b6263cd1a.

Les fichiers requis sont :
- pyodide.js, pyodide.asm.js, pyodide.asm.wasm
- python_stdlib.zip, pyodide-lock.json
- MANIFEST_INSTALLATION.json (tailles et empreintes SHA-256)

Validation du dossier public :
    python scripts/build_site.py --require-local-pyodide

Le script vérifie les empreintes et refuse la publication si un des fichiers
est manquant ou altéré. Dans cette publication, le CDN est désactivé.

L'identifiant du commit publié sera consultable dans :
    /agents_ia/orchestra-build.json

Cette vérification statique ne remplace PAS une recette Pyodide/Edge sur poste
élève, ni une vérification indépendante de la provenance officielle des fichiers.
