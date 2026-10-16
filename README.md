# Agent Academy — Laboratoire d'apprentissage des agents IA

Plateforme pédagogique interactive **en français** pour étudier les agents IA, leurs architectures, leur fonctionnement et leur évaluation.

## Prototype 01 — Observer, décider, agir

Le prototype initial contient :
- une leçon sur la définition d'un agent et la boucle observation/décision/action ;
- un environnement déterministe 7 × 5 avec des obstacles et un objectif ;
- deux stratégies comparables : une politique gloutonne volontairement limitée et un parcours en largeur (BFS) ;
- un journal transparent des décisions, un mode pas à pas et un mode automatique ;
- une mini-évaluation formative ;
- un éditeur Python avec exécution réelle grâce à Pyodide 0.27.7 dans un Web Worker (chargé à la demande) ;
- une politique Python personnalisable reliée à la grille (« Mon agent Python »), avec arrêt et limite d’exécution ;
- des modes sombre, clair et vidéoprojecteur, ainsi qu'une interface adaptable aux mobiles.

**Limites assumées de ce premier jalon :** le code Python de l'atelier n'est pas encore relié au moteur de la grille ; le simulateur est écrit en JavaScript. Il ne s'agit pas d'une simulation de LLM. Pyodide est chargé depuis un CDN et nécessite donc une connexion au premier lancement. L'exécution Python dans le fil principal n'offre pas de bouton d'arrêt robuste contre une boucle infinie : réserver les expériences à du code de confiance et prévoir un Web Worker dédié lors du prochain jalon.

## Tester

Ouvrir `index.html` dans un navigateur récent ou servir le dossier avec un serveur statique. GitHub Pages peut héberger le site sans étape de compilation.

1. Choisir « Gloutonne », cliquer sur « Exécuter une étape » : elle se bloque sur le mur en (2,2).
2. Réinitialiser, choisir « Recherche en largeur (BFS) », puis lancer l'exécution : l'agent contourne le mur et atteint (6,2).
3. Vérifier le journal et la mini-évaluation.
4. Exécuter le code Python proposé et vérifier l'affichage de `droite`.
7. Vérifier les modes visuels, le clavier et le format mobile.

## Références scientifiques et techniques

- [Hugging Face — Agents Course (français)](https://huggingface.co/learn/agents-course/fr/unit0/introduction)
- [Yao et al., ReAct](https://arxiv.org/abs/2210.03629)
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

## Suite proposée

Le jalon 02 intègre une première politique Python pilotant la simulation via un Web Worker avec limite de temps, interruption et traçabilité. Des tests navigateurs automatisés et une isolation renforcée restent à apporter. Les modules ultérieurs introduiront les appels d'outils, l'état et les agents fondés sur un LLM.

**Statut :** prototype de revue. Pas encore validé par des tests navigateur automatisés.
