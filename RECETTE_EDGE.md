# Procédure de recette avant diffusion — Edge / Pyodide

**Statut initial : NON EFFECTUÉE sur un poste du lycée.** Ne pas cocher sans preuve datée.

## Préparation

- [ ] Décompresser dans un nouveau dossier et exécuter `LANCER_ORCHESTRA.cmd`.
- [ ] Ouvrir dans Edge l'adresse `http://127.0.0.1:8000/` (ne pas ouvrir le HTML en `file://`).
- [ ] Vérifier l'accueil, les deux parcours et le logo sans fond blanc.
- [ ] Tester l'absence de CDN : débrancher le réseau après installation des fichiers Pyodide locaux via `INSTALLER_PYODIDE.cmd` ; exécuter **dans les deux parcours**.

## Python / robustesse

- [ ] Première : exécuter un code erroné, puis une solution valide ; vérifier l'obstacle dynamique et les sondes.
- [ ] Terminale : compléter `planifier`, lancer les tests, distinguer échec de planification et échec de déplacement.
- [ ] Terminale : vérifier un scénario « obstacle imprévu » sur la trace réelle, avant/après la case (2,2).
- [ ] Terminale : contrôler les opérations FIFO (enfiler, defiler) réellement affichées.
- [ ] Déclencher `while True:` : le Worker doit redémarrer sans effacer le code.
- [ ] Tester `sys.exit()` ou une exception : aucun message technique brut incontrôlé.
- [ ] Vérifier l'export JSON et l'enregistrement du brouillon sans fuite hors du poste.

## UX / accessibilité

- [ ] Clavier seul : navigation, boutons, champ code, indentations `Entrée`, `Tab`, `Maj+Tab`.
- [ ] Vérifier que la colonne de numéros suit le défilement après 40 lignes.
- [ ] Modes clair, sombre et projection au vidéoprojecteur réel : contrastes et lisibilité.
- [ ] Zoom Edge 200 %, largeur 390 px et fenêtre basse (600 px) sans perte de commandes.
- [ ] Lecteur d'écran : contenu alternatif du plateau, annonces de résultats et navigation.
- [ ] Tester réseau filtré du lycée et poste sans connexion (Pyodide téléchargé localement).

**Décision de mise en service**

Date : ______   Poste / OS / Edge : ___________________   Réseau : ___________________

Résultats : ___________________________________________

Anomalies : ___________________________________________

Responsable de recette : ___________________  Décision GO / NO-GO : ______
