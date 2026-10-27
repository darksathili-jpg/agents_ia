# ORCHESTRA Agent Lab v5.1 — Vérifications et limites

## Périmètre

Séance pilote **Première NSI**, un agent réflexe déterministe piloté par une fonction `decider(observation)`.
La recherche de chemin est fournie par le moteur, et l'élève ne programme pas de LLM, ni la POO, ni le BFS.

## Contrôles automatisés

Les résultats exécutés pour cette livraison figurent dans `PREUVES_V51.md` : moteur et cas adversariaux sous CPython, vérifications syntaxiques JavaScript, éditeur et tests navigateur à l'aide d'un Worker simulant Pyodide.

## Restrictions et risques résiduels

1. **Pyodide réel et Microsoft Edge non vérifiés ici.** Une recette sur les postes du lycée est indispensable.
2. L'essai avec une boucle infinie dans le vrai Worker doit être confirmé. La conservation du brouillon est prévue, mais `localStorage` peut être désactivé.
3. Le simulateur 2D et son avatar ne pilotent aucun robot Microduck réel et n'utilisent pas le SDK de Pollen Robotics.
4. Le contrôle de sécurité est une couverture de 16 sondes, pas une preuve exhaustive ni une protection face à un code élève intentionnellement hostile.
5. L'accès à la solution reste une aide pédagogique contournable par un utilisateur qui maîtrise les outils de développement du navigateur.
6. Un Web Worker n'est pas une isolation sécurisée pour du code malveillant. La distribution sur un site public nécessite une étude de sécurité supplémentaire.
7. Les travaux demeurent indépendants du dépôt historique ORCHESTRA NSI v2.1 : aucun commit, fusion ou déploiement n'a été effectué.
