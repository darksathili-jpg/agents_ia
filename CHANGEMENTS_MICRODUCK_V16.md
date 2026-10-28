# ORCHESTRA v1.6 — Animation Microduck unifiée

**Objectif :** homogénéiser le personnage dans tous les espaces sans retoucher la logique de l'agent.

- Planche originale découpée en 12 poses avec **ancrage 256×256 strictement constant**.
- Héros Première (face) et Terminale (profil droit) animés par 3 poses en CSS ; pause/reprise et visibilité conservées.
- Terrain Première : orientation N/E/S/O fournie par la trace, pas alterné uniquement pour l'instruction `AVANCER`.
- Plateau Terminale : direction déduite du dernier déplacement observé, pose neutre lors d'un événement immobile.
- Visualiseur BFS : orientation conservée d'un mouvement au suivant, événements de recherche/obstacle sans marche artificielle.
- Illustration de présentation Première harmonisée avec le même personnage.
- `shared/microduck-sprite.js` expose `frame()` et `facing()` ; ne participe jamais aux décisions de Python.
- `scripts/build_site.py` inclut l'adaptateur graphique, mais jamais le matériel d'audit.

## Recette effectuée
- Tests Python, contrôles d'images, tests JS syntaxiques et logique d'orientation sous Node.
- Construction publique avec `--allow-cdn` (usage **local de test uniquement**).
- Non vérifié : chargement réel de Pyodide dans Edge, animation de l'application complète dans un navigateur (navigation locale bloquée ici).

## Distribution
- La version publique **stricte** nécessite les binaires locaux Pyodide 0.27.7, leur manifeste SHA-256 et le bon dossier `pyodide/` ; ne pas publier la version de démonstration qui autorise le CDN.
- Les fichiers enseignants et les tests sont séparés de `_site`.
