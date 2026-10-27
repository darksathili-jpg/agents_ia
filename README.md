# ORCHESTRA NSI — Redressement v1.3 (candidat de recette)

**Statut : NON VALIDÉ POUR DIFFUSION AUX ÉLÈVES.** Cette version ne modifie pas la Première v5.1 ; elle renforce la Terminale T01 à partir de la version intégrée v1.2.

## Contenu réel

- **Première NSI :** séance pilote `decider(observation)` et terrain dynamique ; 52 tests CPython livrés.
- **Terminale NSI :** atelier `AgentPlanificateur`, graphe de grille, classe `File`, BFS, plan et replanification, neuf situations ; guide en quatre étapes. Ce n'est pas encore une formation Terminale multi-modules.
- **Visualisation Terminale :** déplacements réels, requêtes à `monde.voisins`, opérations `enfiler/defiler` observées sur le calcul initial. Deux critères sont distingués : trajet correct et méthode réellement observée.
- **Agents déterministes uniquement :** aucun LLM, aucune connexion à un robot physique.

## Lancer sous Windows

1. Extraire **tous** les fichiers dans un nouveau dossier.
2. Exécuter `LANCER_ORCHESTRA.cmd` à la racine, puis ouvrir l'adresse locale affichée dans Edge.
3. Pour une installation réseau : `INSTALLER_PYODIDE.cmd` sur un poste connecté ; copier ensuite `pyodide/` avec les fichiers récupérés et vérifier avec `RECETTE_EDGE.md`.

**Important : le ZIP ne contient PAS les binaires Pyodide** et l'exécution véritable dans Edge / réseau du lycée n'a pas été validée. Le navigateur peut échouer si le CDN est filtré. Le site ne manipule pas de données sensibles ; l'exécution de code élève n'est pas un sandbox sécurisé contre des attaques intentionnelles.

## Tests reproductibles

À la racine, dans `cmd` :

```cmd
python -m unittest discover -s premiere/tests -p "test_*.py" -v
python -m unittest discover -s tests -p "test_*.py" -v
node premiere/tests/editor_indent.test.cjs
node --check terminale/app.js
```

Le dossier **enseignant** est fourni séparément afin de ne pas publier les sources d'évaluation/référence. Après extraction du dossier `qa_enseignant/` à la racine, utiliser :

```cmd
python -m unittest discover -s qa_enseignant -p "test_*.py" -v
```

Les métadonnées des neuf situations sont générées depuis Python : `python outils/generer_cas.py`. Un test QA vérifie leur synchronisation avec l'interface.

## Distinguer compétence et réussite

- **Trajet :** chemin minimal et déplacements réels sûrs.
- **Méthode :** opérations FIFO observées pendant la recherche, et conservation / réutilisation du plan.
- **Compréhension :** à évaluer en complément par une justification écrite ou orale de l'élève. Les tests ne sont pas une preuve formelle de BFS et ne garantissent pas qu'un code volontairement trompeur ne puisse jamais contourner l'évaluation.

Voir `RAPPORT_VERIFICATION.md`, `GUIDE_ENSEIGNANT_V13.md` et `RECETTE_EDGE.md`.
