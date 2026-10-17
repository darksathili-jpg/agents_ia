# Agent Academy — Laboratoire d'apprentissage des agents IA

Plateforme de formation interactive **en français**, développée progressivement pour comprendre, programmer et évaluer des agents.

## Jalon 03 — Observer, décider, agir

Le prototype comprend :
- un cours introductif sur les agents, leurs observations, politiques de décision et actions ;
- un environnement 7 × 5 avec obstacles, une politique gloutonne et une recherche en largeur (BFS) ;
- une politique Python éditable qui prend directement des décisions dans la grille ;
- un journal et une explication structurée de chaque décision (observation → politique → action) ;
- une mini-évaluation, trois thèmes (clair, sombre, vidéoprojecteur) et une mise en page mobile ;
- un interpréteur **Pyodide 0.27.7** dans un **Web Worker** séparé, avec bouton Stop et délai limite.

L'application est entièrement statique et peut être hébergée sur GitHub Pages. Au premier lancement, Pyodide doit être téléchargé depuis un CDN. Aucune clé d'API n'est requise. Le laboratoire démontre d'abord les agents déterministes, **pas un LLM**.

### Utilisation

Ouvrir le site via un serveur web statique (et non directement en `file://`). Choisir la politique « Mon agent Python » pour relier votre fonction `decider(position, objectif, obstacles)` à la grille. Les actions admises sont `droite`, `gauche`, `haut`, `bas` et `arrêt`.

L'exemple Python emploie une recherche en largeur et contourne les obstacles. La politique gloutonne se bloque volontairement pour illustrer les limites d'un choix local.

### Tests

```bash
npm install
npx playwright install chromium
npm run test:browser
```

Les tests couvrent l'affichage, BFS, les modes, le mobile, l'intégration du Worker (simulée), l'arrêt, et **une exécution réelle de Pyodide** sans simulation. Le test Pyodide dépend de l'accès au CDN : un échec réseau ne doit pas être confondu avec une erreur de Python.

**Limites** : le code Python s'exécute dans le navigateur et le Web Worker peut être terminé, mais cela ne constitue pas une sandbox de sécurité pour du code non fiable. Les protections d'accès aux API et d'isolation sont à renforcer. Les tests ne prouvent pas encore la sécurité ou la fiabilité de tous les programmes.

## Références

- [Hugging Face — Agents Course, français](https://huggingface.co/learn/agents-course/fr/unit0/introduction)
- [Yao et al. — ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

## Développement

La PR #1 reste en brouillon. Ne pas fusionner avant validation du workflow et des essais utilisateur sur ordinateur et mobile.

## Accueil illustré — branche artistique

L’accueil est désormais `index.html` ; le laboratoire existant est accessible dans `laboratoire.html`. Les chemins sont relatifs. Voir `docs/art/bible-graphique.md`, `docs/art/architecture-et-verification.md` et `docs/art/captures/` pour la direction artistique, l’architecture et les preuves visuelles. Aucun mécanisme Python ou algorithme n’a été modifié.
