# ORCHESTRA NSI — Corrections de publication et d'intégrité v1.5

**Statut : candidat de recette ; aucune publication GitHub et aucun commit effectués.**

## Périmètre

- Base : archive `ORCHESTRA_NSI_v1_4_VISUALISEUR_BFS.zip` remise dans la conversation.
- La copie reçue ne contenait **pas** `.github/workflows/` et ne contenait **pas** les binaires de Pyodide (seulement `pyodide/README.txt`). Les constats sur ton dépôt réel, notamment son workflow `path: '.'` et ses binaires, nécessitent une comparaison avec ce dépôt : ne pas écraser les fichiers existants sans inspection.
- Aucune refonte visuelle, aucune nouvelle séance, aucun changement de l'algorithme Première.

## Correctifs réalisés

1. **Build à liste blanche** : `scripts/build_site.py` copie les fichiers HTML, JS, CSS et Python nécessaires, les images et Prism, sans les tests, le corrigé, les guides, les rapports, les archives ni les scripts Windows. Il refuse les dossiers publics contenant ces familles de fichiers.
2. **Workflow de référence** : `.github/workflows/pages.yml` exécute les tests Python, l'indentation et `node --check` avant de permettre une publication. Elle n'est lancée pour déploiement que via `workflow_dispatch` avec saisie explicite `PUBLIER`, sur `main`, après les tests. Il faut **désactiver ou remplacer tout ancien workflow qui publie le dépôt entier** : ce nouveau fichier ne désactive pas automatiquement les anciens workflows.
3. **Contrôle Pyodide** : publication exigeant les cinq binaires locaux et `MANIFEST_INSTALLATION.json` (SHA-256, version 0.27.7). En sortie stricte, la connexion de secours vers le CDN est désactivée. L'archive source livrée n'inclut pas ces binaires ; un poste connecté doit installer la distribution ou fournir les fichiers déjà présents dans le dépôt.
4. **Données/extérieur** : suppression des liens Google Fonts, remplacement par des piles de polices système, sans redistribution de fichiers de police.
5. **Première** : le corrigé complet n'apparaît plus dans les fichiers publics d'exécution. Il est déplacé dans `premiere/tests/reference_solution.py` (enseignant seulement). Le bouton propose un retour méthodologique et non un corrigé. Le terrain fixe est nommé **terrain de contrôle**, pas « terrain caché ».
6. **Terminale** : contrôle AST bloquant l'accès explicite aux attributs internes (`_VueMonde__audit` notamment). Le scénario dynamique varie par graine la ligne de départ, la cible et la case bloquée, toujours sur le chemin initial et immédiatement devant le robot après un déplacement. La graine est créée dans le Worker, conservée dans le résultat et exportable dans le bilan. Les graines 0 (démonstration) et non nulles (évaluations) restent reproductibles.
7. **Tests robustes au format CSS** : remplacement de plusieurs recherches de fragments littéraux par des expressions régulières tolérantes aux espaces et aux retours à la ligne.

## Limites et décision de diffusion

- Un test de comportement ou un filtre AST ne garantit **ni la compréhension du BFS, ni la résistance à un adversaire exécutant du Python hostile**. Un Worker n'est pas une sandbox de sécurité.
- Les sources publiques restent consultables : un terrain fixe n'est pas secret. Les résultats et leur justification doivent être évalués autrement que par un obstacle présumé introuvable.
- Les binaires Pyodide de ton dépôt ne sont pas inclus dans l'archive de travail, donc **le test Edge avec vrai Pyodide est encore requis**.
- Les tests **5 en échec** annoncés dans ton dépôt n'ont pas été reproduits sur l'archive v1.4 source, qui passe ses 73 tests initiaux. Le correctif des tests CSS est préventif, pas la preuve que les cinq échecs de ton dépôt sont corrigés.
- **Aucune validation de publication** sans comparaison avec ton dépôt existant, retrait de l'ancien workflow et recette poste élève.

## Exécution locale

```bash
python -m pytest -q premiere/tests tests qa_enseignant/test_redressement.py qa_enseignant/test_variantes.py qa_enseignant/test_visualiseur_bfs.py
node premiere/tests/editor_indent.test.cjs
python scripts/build_site.py --allow-cdn
# Publication réelle, uniquement après installation et vérification Pyodide :
python scripts/build_site.py --require-local-pyodide
```

Le site public strict est alors dans `_site/`, seul répertoire à téléverser.
