# ORCHESTRA NSI — Laboratoire d'agents, séance 01 (v5.1)

**Public :** Première NSI, initiation aux agents déterministes en Python. **Durée indicative :** 35 à 45 min.

## Pourquoi ce site ?

L'élève programme **une fonction** `decider(observation)` qui choisit l'action d'un robot virtuel. Le simulateur reçoit cette action, modifie sa position et enregistre une trace d'exécution. L'élève anticipe une première décision, observe puis explique l'écart éventuel entre son hypothèse et le programme.

Il s'agit d'un **agent réflexe déterministe**. Aucun LLM, aucun robot physique et aucune orchestration multi-agents ne sont impliqués. Le personnage est un sprite 2D issu de l'illustration fournie ; il ne représente pas un lien matériel avec Microduck.

## Démarrage

Sous Windows : décompresser l'archive et ouvrir `LANCER_ORCHESTRA.cmd`, puis Edge à `http://127.0.0.1:8000/`. Ou lancer depuis le dossier :

```sh
python -m http.server 8000
```

Le site utilise Pyodide localement si le dossier `../pyodide/` a été installé avec `../INSTALLER_PYODIDE.cmd` ; sinon un accès Internet au CDN est nécessaire. La coloration Prism est intégrée localement.

## Contrat de la séance

`decider(observation)` reçoit quatre valeurs : `arrive` (booléen), `orientation` (`N`, `E`, `S`, `O`), `balise` (direction suggérée ou `None`) et `devant_libre` (booléen). Elle retourne **une chaîne** parmi `AVANCER`, `TOURNER_DROITE`, `TOURNER_GAUCHE`, `STOP`.

- Les terrains 1 à 3 sont visibles avant le test ; le terrain 4, « de contrôle », se révèle après le premier essai.
- Le capteur `balise` est calculé par un parcours en largeur (BFS) dans les quatre terrains. L'élève ne programme pas ce parcours.
- Le **terrain 2** comporte un obstacle mobile qui apparaît entre le calcul de la balise et la décision du robot. Une observation réelle de la trace contient alors `balise='E'` et `devant_libre=False`. Un cinquième contrôle, regroupant **16 sondes** (`4 orientations × 4 directions de balise`), vérifie l'interdiction d'avancer lorsque `devant_libre=False`. Ce contrôle n'est pas un terrain supplémentaire.
- L'élève doit atteindre le colis et renvoyer `STOP` dans les quatre terrains, **et** réussir le contrôle de sûreté.

Le contrôle de sûreté est **un ensemble de tests de fonction**, pas un cinquième terrain. L'apparition du nouvel obstacle dans le terrain 2 est aussi visible dans la trace Python réelle. Aucune batterie finie ne prouve une propriété de sûreté pour l'ensemble des programmes possibles.

## Éditeur et conservation des données

Le vrai `textarea` contient le programme exécuté : Prism colore un calque visuel. `Entrée` reprend l'indentation et ajoute quatre espaces après une instruction de bloc (`if`, `for`, `def`…), `Tab` indente, `Maj+Tab` désindente, `Retour arrière` retire un palier d'indentation, `Ctrl+Entrée` lance l'évaluation. Une aide méthodologique est accessible qu'après deux **versions d'AST Python distinctes**, évaluées avec une prédiction, et deux indices consultés. Le second indice exige une première tentative et le troisième une deuxième : cliquer plusieurs fois ne suffit plus. Les variations d'espaces et de commentaires sont ignorées. Il s'agit d'une aide pédagogique, pas d'un dispositif anti-triche sécurisé.

Le code, la prédiction et les vingt derniers bilans synthétiques sont sauvegardés dans `localStorage`, si celui-ci est accessible. La remise à zéro du code exige une confirmation ; « Redémarrer Python » conserve le brouillon. Après neuf secondes de calcul sans réponse, le Worker est détruit puis recréé **sans perdre le code**. L'élève peut exporter un fichier `orchestra-bilan-agent.json` (code, prédiction, essais et verdicts).

**Attention :** le stockage est propre au navigateur et à l'origine web ; il n'est ni synchronisé avec un compte ni garanti en navigation privée. Exporter le bilan pour le conserver.

## Accessibilité visuelle

Modes **clair, sombre et vidéoprojecteur**, disponibles dans l'en-tête. Le bloc de démonstration et la zone de programmation suivent le mode sélectionné. La préférence est conservée localement. Le mode projection agrandit les textes importants et masque la navigation secondaire.

## Tests et limites

```sh
python -m unittest discover -s tests -v
node tests/editor_indent.test.cjs
node --check app.js
node --check ../shared/editor-indent.js
node --check python-worker.js
```

Voir `TESTS_ET_LIMITES.md` et `../RECETTE_EDGE.md` pour les limites des tests et la recette réelle sous Edge/Pyodide. Un Worker n'est pas une frontière de sécurité pour exécuter du code hostile : réserver l'outil à un environnement pédagogique contrôlé.

Projet pilote **indépendant** d'ORCHESTRA NSI v2.1 : aucun fichier du dépôt Git de référence n'a été modifié, fusionné ni publié.


### Correctifs v5 : navigation, identité et animation

- La colonne de gauche possède désormais son propre défilement vertical au-dessus de 920 px, même sur des écrans peu hauts. Clavier : cliquer/focaliser la colonne puis utiliser les flèches ou Pg↓.
- Tablette/téléphone : le parcours devient un rail horizontal défilable. Les séances 02–04 sont annoncées comme prochaines séances, non accessibles dans ce pilote.
- Le logo Lycée Watteau fourni (sans mention MicroDuckLab) est visible dans la barre supérieure et dans la colonne.
- La scène de présentation anime trois poses de marche de la planche sprite fournie, sans Canvas ni téléchargement réseau. Bouton pause/reprise ; animation suspendue lorsque hors écran ou onglet masqué et désactivée par défaut en cas de préférence de mouvement réduit. **Animation de présentation seulement** : le robot du terrain reste piloté par l’exécution Python.
- Aucun changement à `engine.py`, `python-worker.js`, `app.js` ou aux tests de sécurité Python.


### Correctifs v5.1 : fiabilité pédagogique

- Niveau assumé : **Première NSI**, agent réflexe déterministe. Aucune séance Terminale n'est incluse.
- Terrain 2 : obstacle réellement inséré pendant l'exécution ; la balise mémorisée devient périmée sur une décision, visible dans la trace et sur la grille.
- Contrôle de sûreté : 16 observations pour couvrir toutes les combinaisons de quatre orientations et directions indiquées.
- Accès progressif à la solution : versions évaluées différenciées par l'AST Python, prédiction demandée, indice 2 après la première tentative et indice 3 après deux tentatives distinctes.
- Données de version : l'export JSON porte désormais le format `orchestra-nsi-lab-v5.1` ; les nouvelles données locales sont stockées sous une nouvelle clé pour éviter de confondre les bilans antérieurs.
- Limites inchangées : Pyodide exige une installation locale préalable ou un accès CDN ; aucune intégration au matériel Microduck ; pas de LLM ni d'agent multi-outils.
