# Rapport d'audit — ORCHESTRA NSI v1.4 · visualisation BFS

**Périmètre :** remplacement de la démonstration graphique Terminale par un visualiseur d'événements. Le parcours Première et les contrats de notation Terminale de v1.3 ne sont pas modifiés. La modification de `terminale/runner.py` ajoute exclusivement la collecte des événements pendant les appels effectifs à `planifier`, à `File.enfiler`, à `File.defiler` et à `monde.voisins` ; la structure `searches` est ajoutée aux résultats JSON.

## Preuves reproductibles

| Contrôle | Résultat |
|---|---|
| Première | 52 tests réussis (`python -m unittest discover -s premiere/tests`) |
| Tests d'intégration | 21 réussis (`python -m unittest discover -s tests`) |
| Audit enseignant | 15 réussis (`python -m unittest discover -s qa_enseignant -p 'test_*.py'`) |
| Timeline JavaScript | Test Node réussi (`node qa_enseignant/test_timeline.cjs`) |
| Référence Terminale | 9/9 contrats réussis sous CPython |
| Scénario dynamique | 2 calculs de chemins distincts, avant et après l'obstacle `(2,2)` |
| Événements dynamiques | 183 événements instrumentés, présentés en 197 étapes guidées |
| Chromium autonome | 390, 900, 1440 px : aucune erreur JS ni débordement horizontal |
| Modes visuels | Clair, sombre et vidéoprojecteur contrôlés dans Chromium |
| Mode « Mon exécution Python » | Activation après réponse simulée du Worker transportant des résultats CPython |
| Pyodide réel / Edge / réseau du lycée | **Non vérifié** |

## Contrats pédagogiques

1. L'exemple guidé est identifié comme provenant de la référence. Le corrigé Python est absent de l'archive élève.
2. La grille affiche toutes les cellules : aucune rangée tronquée, pas de représentation trompeuse du trajet.
3. Les ajouts, retraits et visites sont instrumentés pendant l'exécution de la méthode réellement fournie par l'élève.
4. Lors d'une évaluation ne générant aucune recherche, le visualiseur n'invente ni file, ni visite, ni chemin.
5. Un obstacle apparaît sur l'ancien plan après le premier déplacement, puis une seconde recherche reprend depuis la position réelle du robot.
6. Les mesures affichées sont les **événements observés**, pas une garantie de compréhension ni une preuve formelle de sûreté.

## Limitations résiduelles

- La démonstration est un enregistrement de référence réalisé sous **CPython**. Les traces de l'élève dépendront du démarrage réel de Pyodide, non testé ici.
- Les événements de file sont limités à 450 par recherche pour borner l'affichage. Un programme extrême peut produire un journal partiel. L'interface ne remplace pas un débogueur Python.
- Le vérificateur reste une **évaluation pédagogique, pas un environnement sécurisé pour du code Python hostile**. Le Worker limite le temps mais n'est pas une frontière de sécurité formelle.
- L'exactitude et la minimalité du parcours relèvent du vérificateur existant, non du dessin de la grille.
- La recette lecteur d'écran / zoom 200 % / projecteur physique reste à effectuer.

**Décision :** fonction visualiseur **candidate à recette Edge**, pas autorisée à être déclarée définitivement diffusable.
