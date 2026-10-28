# G2 — Restaurer la distribution Pyodide et identifier le site publié

**Base** : `main`, commit `35158f326976c33635a17430300c437c8aa93711`.

## Source de restauration

Le commit ancien `1ecfac610d6d62d8b6656c9ff05b269b6263cd1a` contenait :
`pyodide.js`, `pyodide.asm.js`, `pyodide.asm.wasm`,
`python_stdlib.zip`, `pyodide-lock.json` et `MANIFEST_INSTALLATION.json`.

Ces six fichiers sont réintroduits à partir de leurs **blobs Git exacts** :
aucun téléchargement externe, aucune recompilation, aucune modification du moteur.

Les empreintes SHA-256 du manifeste sont vérifiées par `scripts/build_site.py --require-local-pyodide`
et le test `tests/test_release_g2.py`.

## Preuve d'identité de la publication

Chaque site construit inclut désormais le fichier public `orchestra-build.json` :
- `source_commit` : SHA du commit de construction ;
- `built_at_utc` : date du build UTC ;
- `mode` : `pyodide-local-verifie` pour la diffusion stricte ;
- `index_sha256` : empreinte de l'accueil effectivement copié.

Après publication, consulter :
`https://darksathili-jpg.github.io/agents_ia/orchestra-build.json`

Ce fichier permettra de vérifier **quel commit est réellement publié**.
Son absence signifie seulement qu'il n'a pas été créé par la nouvelle procédure.

## Vérification

```bash
python -m pytest -q premiere/tests tests qa_enseignant
python scripts/build_site.py --require-local-pyodide
```

Inspecter le répertoire `_site` : il ne doit contenir ni corrigé enseignant,
ni `tests/`, `qa_enseignant/`, `.github/` ou `node_modules/`.

## Réserves

- Réussir la CI CPython n'est pas une recette Pyodide/Edge.
- Les fichiers enseignants restent accessibles dans **l'historique public Git** :
  la publication contrôlée de Pages ne les efface pas.
- Ne pas fusionner les PR G0 et G1 implicitement. Elles sont indépendantes.
- **La publication de Pages reste manuelle** : GitHub Actions →
  `ORCHESTRA — tests et publication contrôlée` → `Run workflow` →
  branche `main`, confirmation `PUBLIER`.
- La synchronisation du commit en ligne doit être vérifiée après la publication.
