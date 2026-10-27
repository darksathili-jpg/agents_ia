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
