# Recette manuelle dans Edge — v1.4

Ne publiez pas le projet au lycée avant les contrôles ci-dessous.

1. Démarrer `LANCER_ORCHESTRA.cmd` et ouvrir la page Terminale dans Edge.
2. Trouver l'encart **Un obstacle apparaît. Que fait vraiment le BFS ?**. Vérifier que les **35 cases** du terrain apparaissent intégralement.
3. Cliquer sur **Explorer et planifier** : la grille doit être sans obstacle, et le BFS doit ajouter/retirer de la file pendant la lecture.
4. Cliquer sur **Obstacle imprévu** : un obstacle rouge apparaît en `(2,2)` sur le trajet précédemment envisagé, Microduck est à `(1,2)`.
5. Cliquer sur **Replanifier et avancer** : le second calcul démarre ; la file contient de nouveaux sommets et les cases explorées se colorent au fil des appels à `voisins()`.
6. Tester **▶ Lire / Ⅱ Pause**, flèches, curseur de lecture et **Recommencer**.
7. Vérifier les modes **Clair**, **Sombre**, **Projection** ainsi que le zoom Edge à **200 %** et une largeur proche de **390 px**.
8. Avant d'exécuter Python, le bouton **Mon exécution Python** doit être inactif.
9. Exécuter une réponse correcte, puis une réponse erronée : après chaque test, **Mon exécution Python** doit montrer uniquement les événements de la réponse courante (ou l'absence de trace).
10. Vérifier qu'une boucle infinie entraîne le redémarrage du Worker et conserve le code.
11. Tester Edge et le réseau filtré du lycée, d'abord avec Pyodide local puis sans accès CDN. Noter les messages d'erreur.
12. Faire expliquer à un élève la différence entre **sommet ajouté**, **sommet retiré**, **sommet exploré** et **déplacement du robot** ; recueillir sa justification du plus court chemin.

**Non-validés par le présent paquet :** Pyodide réel, filtrage du réseau lycée, lecteur d'écran, projection physique.


## Complément v1.5 — confidentialité et variabilité

1. Dans Edge, tester la Première et la Terminale hors ligne une fois
   l'installation locale Pyodide terminée, en utilisant `_site/` produit par
   `python scripts/build_site.py --require-local-pyodide`.
2. Dans l'onglet Réseau, vérifier qu'aucune requête vers Google Fonts ni
   vers un CDN n'est effectuée. Les polices doivent utiliser les familles
   système disponibles sur le poste.
3. Sur la Terminale, exécuter plusieurs fois le scénario « Obstacle » avec
   une vraie solution BFS ; vérifier les variantes de ligne et le bilan JSON,
   sans faux échec sur un programme correct.
4. À chaque exécution, vérifier que l'éditeur, le journal et la visualisation
   gardent des résultats cohérents après le redémarrage du Worker.
5. **Ne pas publier** si un test échoue, si l'ancien workflow GitHub publie
   `path: '.'` ou si le manifest Pyodide manque.
