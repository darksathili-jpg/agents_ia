# G1 — Recette contradictoire des parcours ORCHESTRA

**Référence analysée :** commit `35158f326976c33635a17430300c437c8aa93711` de `main`.

## Périmètre

Mission de tests seulement : aucun changement apporté aux moteurs Python, au Worker,
aux exercices, au graphisme, à la construction Pages ni aux ressources Pyodide.

### Contrôles automatisés ajoutés

- BFS de référence accepté sur six graines (0, 1, 2, 7, 42, 2026).
- BFS également correct avec un ordre d'exploration inversé : ne pas imposer
  arbitrairement **un** chemin lorsqu'il existe plusieurs plus courts chemins.
- Remplacement erroné de la file FIFO par une pile LIFO : rejet.
- File appelée uniquement dans une branche morte : trajet correct reconnu,
  mais critère méthodologique rejeté.
- Recalcul inutile du plan à chaque pas : trajet correct reconnu,
  mais mémorisation du plan rejetée.
- Cohérence calculée des quatre verdicts par situation et des totaux de réussite.
- Oracle de distance minimale comparé à une recherche indépendante sur
  **60 petites grilles reproductibles**.
- Rejet des coordonnées décimales, booléennes et non structurées.
- Contrôle des imports interdits et accès directs aux attributs internes
  (cela **ne sécurise pas** un programme Python hostile).
- Première NSI : vérification des sondes de sûreté et acceptation d'une
  variante correcte tournant à gauche.

### Commandes de recette

```bash
python -m pytest -q premiere/tests tests qa_enseignant/test_redressement.py qa_enseignant/test_variantes.py qa_enseignant/test_visualiseur_bfs.py
node premiere/tests/editor_indent.test.cjs
node tests/microduck_sprite.test.cjs
```

Dans la copie locale de référence, après ajout du fichier de tests G1 :
**119 tests Python réussis, 138 sous-tests réussis**, plus 13 assertions
d'indentation ; à confirmer par GitHub Actions sur la PR.

## Réserves explicites

1. **Pyodide réel dans Edge et autonomie hors connexion : non vérifiés.**
   La branche `main` ne contient que `pyodide/README.txt`, pas les binaires
   et leur manifeste. La construction stricte doit donc échouer.
2. **Sécurité :** le code élève s'exécute dans le navigateur, mais les règles
   AST ne forment pas une sandbox de sécurité contre un adversaire.
3. **Pédagogie :** un score de 9/9 ou une trace FIFO cohérente ne prouvent
   pas la compréhension ; demander une explication par l'élève.
4. **Confidentialité :** le dépôt public contient encore des fichiers
   enseignants ; leur suppression dans le HEAD n'efface pas l'historique.
5. **Interface :** l'éditeur, les thèmes, le zoom, le lecteur d'écran et
   l'interruption réelle du Worker doivent encore faire l'objet d'une recette
   sur un poste élève et avec une connexion de lycée.

## Départage G1

**G1 automatique :** peut être validé lorsque les tests de la PR sont verts,
sans échec ni contournement connu non documenté.

**G1 pédagogique et navigateur :** restent en attente de recette humaine.
Aucune fusion, aucune mise en ligne ni publication implicite.
