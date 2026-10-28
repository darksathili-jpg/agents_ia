# ORCHESTRA NSI — intégration graphique Microduck 4×3

## Espaces et comportement

| Zone | Orientation | Animation | Origine des données |
| --- | --- | --- | --- |
| Héros Première | face (sud) | trois poses en boucle, bob léger, pause | décoratif |
| Héros Terminale | profil (est) | trois poses en boucle, pause | décoratif |
| Présentation Première | face (sud), neutre | fixe | introductif |
| Terrain Première | selon `orientation` N/E/S/O | pose fixe ou marche associée à un `AVANCER` observé | trace de `engine.py` |
| Terrain Terminale | calculée à partir du déplacement précédent | pose liée à la trace | trace de `runner.py` |
| Visualiseur BFS | direction conservée d’un déplacement observé au suivant | pas A / pas B uniquement pour événements `move` ; autres événements neutres | `trace` Python, jamais exploration inventée |

## Architecture

- `design/microduck-source-4x3.png` : source originale ; 4 bandes `microduck-walk-{direction}.webp`, 12 fichiers de frames, 4 poses neutres.
- `shared/microduck-sprite.js` : adaptation orientation/pose/nom de fichier pour la présentation ; ne communique pas avec Pyodide.
- `premiere/app.js`, `terminale/app.js` et `terminale/bfs-visualizer.js` sélectionnent la pose après lecture de la trace.
- Héros animés avec CSS local ; aucune police/image en provenance de CDN pour les sprites.
- `scripts/build_site.py` ajoute uniquement le helper public, sans publier les tests ni la documentation.

## Contrôles

1. Vérifier 12 frames RGBA et quatre bandes de trois frames ; centrage constant.
2. Vérifier N/E/S/O et la pose neutre lors d’un événement immobile.
3. Vérifier que la même trace Python donne la même orientation après relecture.
4. Vérifier pause, réduction du mouvement, mode vidéoprojecteur, zoom à 200 %, format mobile.
5. Exécuter les tests Python et le build à liste blanche ; confirmer Pyodide réel dans Edge avant diffusion.

**Aucune nouvelle compétence pédagogique n’est ajoutée par les sprites :** le renforcement reste visuel et doit être interprété comme tel.
