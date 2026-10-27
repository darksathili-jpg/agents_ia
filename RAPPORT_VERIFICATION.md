# ORCHESTRA NSI — Rapport de redressement v1.3

**État : CANDIDAT DE RECETTE, NO-GO pour une publication immédiate.**

- Base : version intégrée v1.2, SHA-256 de l'archive source : `fd99c4917119ad77b0f246f835ca171a83d25f041a1cf0be8e553484d7e46556`.
- Première : moteur et exercices conservés ; 52 tests de la suite d'origine relancés sur l'arborescence finale.
- Terminale : correction du contrat d'évaluation, clarification éditoriale, meilleure progression guidée et métadonnées synchronisées.
- Les tests automatisés ne constituent pas une validation d'Edge ou de Pyodide, ni une preuve d'acquisition du BFS.

## Défauts reproduits puis corrigés

| Constat | Avant | Contrôle maintenant |
|---|---|---|
| Classe `File` employée seulement dans `if False` | 9/9 déclaré réussi | 9/9 trajets fonctionnels mais seulement 3/9 contrats complets : usage réel non observé |
| Replanifier à chaque pas | 9/9 déclaré réussi | Trajets conservés ; phase « plan réutilisé » en échec |
| Coordonnées décimales ou booléens | Valeurs acceptées | Type strict tuple `(int, int)` |
| Score global contradictoire | « BFS ✓ / Agent ✓ » et 0/9 | Quatre composantes visibles, résultat fonctionnel distinct de la méthode |
| File invisible | Affichage des seuls voisins consultés | Trace instrumentée des appels réels `enfiler` / `defiler` sur le calcul initial |
| Scénarios dupliqués | 6 annoncés contre 9 | Neuf cas générés du Python par `outils/generer_cas.py` ; concordance testée |
| Justification d'architecture dans le starter | « bibliothèque non étudiée » | Explication du FIFO du point de vue de l'élève |
| Charge cognitive | BFS + classe + replanification d'un seul bloc | Quatre étapes de travail, avant/après obstacle, consignes et guide enseignant |

## Preuves automatiques issues de cette archive

| Suite | Retour | Résultat observé |
|---|---:|---|
| `premiere` | 0 | succès |
| `integration` | 0 | succès |
| `qa` | 0 | succès |
| `indentation` | 0 | succès |
| `javascript` | 0 | succès |

Le dossier `qa_enseignant/preuves` conserve les sorties exactes. L’inventaire éditorial `qa_enseignant/INVENTAIRE_TEXTE_V13.csv` regroupe 187 fragments ; il constitue une aide à la relecture et non une validation pédagogique humaine exhaustive. Les 10 tests de redressement comprennent les deux contre-exemples, la solution de référence, les coordonnées incorrectes, les métadonnées et la cohérence du code de départ.

## Vérification visuelle limitée mais reproductible

- Chromium 1440×900, 900×700, 390×844 ; contrôles d'affichage et d'interaction sur le vrai HTML/CSS/JavaScript avec un Worker simulé.
- Les résultats simulés sont issus de CPython ; aucune assertion de démarrage réel de Pyodide ne peut être faite.
- Rendu HTML statique direct du site et accès `file:///` : bloqués par les restrictions de l'environnement.

## Risques résiduels / portes d'arrêt

1. **P0 déploiement :** Pyodide local absent ; Edge sur poste et réseau du lycée non testés. Recette `RECETTE_EDGE.md` obligatoire.
2. **P1 pédagogie :** les tests peuvent établir des observations de méthode mais pas la compréhension ni l'impossibilité de triche ; un contrôle humain du code et de la justification reste requis.
3. **P1 progression :** quatre étapes sont guidées dans le même atelier ; leurs évaluations indépendantes complètes et les séances DFS/récursivité restent à développer.
4. **P1 accessibilité :** zoom Edge 200 %, lecteur d'écran, navigation clavier complète et vidéoprojecteur physique non testés.
5. **P1 maintenance :** tests de navigateur réalisés avec Worker simulé ; tests E2E sous Pyodide réel à automatiser quand le runtime est disponible.

**Décision recommandée : NO-GO publication ; GO pour recette technique encadrée.** Aucune publication ni modification de Git n'a été effectuée.
