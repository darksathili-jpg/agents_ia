# Vérifications techniques — U01.1

Exécutées le 18 octobre 2026 sur la branche d’intégration. Aucun apprenant n’a participé à ces contrôles.

## Résultats

| Vérification | Résultat constaté |
|---|---|
| `python scripts/construire-formation.py` | Ancien point d’entrée : génère maintenant U01.1 à partir des cinq sources approuvées. |
| `python scripts/verifier-u01.py` | Réussite : paragraphes, règles et questions conservés ; liens et ancres locaux valides ; sources conformes au commit de référence ; empreintes des archives ; moteur et Worker inchangés. |
| Python du guide sous CPython | Quatre assertions du code source exécutées sans erreur, avec les quatre sorties prévues. |
| `npx playwright test --workers=2 --reporter=dot` | **27 tests réussis**, aucun échec lors du dernier passage. Suite actuelle : parcours U01.1, accueil et régressions V2. |
| Microduck, commandes clavier | Départ `0,2`, compteur 0 ; droite vers `1,2` ; seconde droite refusée, position `1,2`, compteur 2 ; bouton étape désactivé à l’arrêt ; réinitialisation revient au départ et vide les tentatives. |
| Pyodide réel, sans faux Worker | Quatre lignes du modèle de la porte ; exception contrôlée ; interruption d’une boucle ; restauration et nouvelle exécution réussie. |
| Sauvegarde et export | Champs et tableaux retrouvés après rechargement ; JSON U01.1 fidèle ; anciennes réponses S01 non reprises ; aucun score ajouté. |
| Affichage et clavier | Clair, sombre, vidéoprojecteur ; thème transmis aux cadres ; focus visible ; navigation des étapes et des volets ; régions de tableau accessibles au clavier. |
| Responsive | Vérification à 390, 768 et 1440 px dans les tests actifs ; pas de débordement horizontal du document ; tableaux larges contenus dans leur propre région défilante. |
| Sous-dossier | Parcours, cadre et URL du Worker vérifiés sous `/agents_ia/` avec réacheminement local des requêtes ; aucun déploiement effectué. |
| Syntaxe JavaScript | `node --check` exécuté sans erreur sur `u01.js`, `u01-laboratoire.js`, `laboratoire-moteur.js`. |
| Préservation | Aucun changement dans `docs/pedagogie/`, `python-worker.js`, les CSS V2 existantes ou les ressources graphiques. Les pages historiques remplacées aux accès actifs sont conservées en archive. |

Le journal résumé du dernier passage est conservé dans [tests-navigateur.txt](tests-navigateur.txt). Les captures sont produites par les tests et présentées dans [la galerie](index.html). Elles montrent des états techniques construits pour le contrôle, pas des productions d’élèves.

## Revue visuelle et limites

Les captures ont été examinées, et pas seulement générées : entrée élève, laboratoire dans les trois thèmes, Nora, curseur mobile, préparation scientifique et Python réel. La collision de noms de variables de l’adaptateur et le débordement mobile des libellés masqués ont été corrigés puis retestés. Les champs restent libres : leur contenu ne fait pas l’objet d’une correction automatique.

Le passage historique initial comportait deux attentes mobiles en échec ; après correction, le test ciblé passe aux deux largeurs et la suite complète passe. Les suites S01 conservées dans `tests/historique/` ne sont pas présentées comme exécutées ou réussies : elles exigent précisément le parcours retiré et sont remplacées par les scénarios U01.1.

À examiner humainement : pertinence du parcours d’écran et de la place d’écriture, compréhension de toutes les consignes, temps réel, autonomie des transferts, lecture avec aides techniques et projection sur matériel réel. Ni les captures ni les 27 succès ne valident l’efficacité pédagogique. Les conditions de l’essai documentaire précédent restent distinctes de cette intégration applicative.

Arrêt pour inspection humaine. Aucune publication de branche, fusion ou mise en ligne.
