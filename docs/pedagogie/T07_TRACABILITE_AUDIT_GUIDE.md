# ORCHESTRA NSI — T07 · Traçabilité et audit des décisions

## Statut et positionnement

**Terminale NSI — 3 séances de 55 minutes, à la suite de T06.**
La traçabilité des agents est un **contexte pédagogique complémentaire**.
Elle permet d'exercer des compétences du programme officiel : parcours
de listes, dictionnaires, tuples, ensembles, spécification de fonctions,
mise au point et tests de programmes, vérification d'invariants, distinction
entre données et décisions.

La représentation des événements en liste et du registre en dictionnaire
est un choix de modélisation. Les termes à employer rigoureusement en classe
sont : **variable de type entier**, **affecter une valeur à une variable**,
**boucle bornée**, **instruction conditionnelle**, **clé**, **valeur**,
**dictionnaire**, **ensemble** et **fonction**.

## Contrat de l'audit Python

L'élève programme `auditer_journal(mission, journal, registre)`.
La fonction n'a pas d'effet sur Microduck et renvoie exactement :

`{"etat": "ANOMALIE" / "ATTENTE_HUMAINE" / "CONFORME", "motif": "..."}`.

Une mission contient la révision, le départ, l'objectif, un ensemble d'outils
autorisés et l'éventuelle décision humaine indépendante.

Le journal est une **liste non fiable** de dictionnaires contenant exactement
`sequence` (variable de type entier), `type`, `revision`, `position`
et `preuve`. Les types possibles sont `DEBUT`, `OBSERVATION`,
`DEPLACEMENT` et `FIN`. Le terrain mesure six colonnes sur trois lignes.

Le registre indépendant **simulé** indexe les résultats par leur identifiant.
Chaque preuve donne la révision, l'outil, l'origine, la destination et
le résultat réel du test.

**Contrôle attendu :**
- départ conforme et séquences consécutives à partir de zéro ;
- contrôle de la révision et refus des attributs inconnus ;
- observation sur la position courante avant chaque déplacement ;
- déplacement vers un voisin orthogonal du terrain ;
- preuve unique provenant du registre, réussie et correspondant
  à la révision, à l'origine et à la destination ;
- fin en dernière position, atteignant l'objectif ;
- permissions `observer` et `avancer` présentes ;
- validation humaine indépendante si la mission le requiert ;
- entrées non modifiées.

Le journal ne remplace jamais le registre indépendant. Une preuve provenant
d'une autre révision est refusée, même si elle indique « réussi ».

## Machine à états de démonstration

`JOURNAL_REÇU` → `AUDIT_EN_COURS` →
`ANOMALIE` / `ATTENTE_HUMAINE` / `CONFORME`.

Après validation humaine éventuelle, une trace `CONFORME`
peut passer à `REJEU_TERMINÉ` **uniquement après un rejeu manuel**.

**Invariant :** aucune action dans les états `ANOMALIE`,
`ATTENTE_HUMAINE` et `AUDIT_EN_COURS`.
Un clic sur **Rejouer l'événement suivant** exécute au plus une action :
`DEBUT`, `OBSERVATION` et `FIN` n'entraînent aucun mouvement ;
`DEPLACEMENT` entraîne exactement un pas d'une case.
La trace conforme de six événements correspond à deux pas de Microduck,
de `(0,1)` vers `(2,1)`, et non six.

## Séance 1 — Confronter (55 min)

Exécuter les cas « Journal conforme » et « Déplacement sans preuve ».
Avant chaque audit, demander aux élèves de prédire le verdict.
Comparer ensuite une preuve d'ancienne révision, un test échoué,
une observation manquante, un numéro de séquence non consécutif,
une téléportation déclarée et un événement après `FIN`.
Préciser pourquoi la seule cohérence géométrique du trajet ne
prouve pas l'exécution réelle.

## Séance 2 — Programmer (55 min)

Compléter le squelette `terminale/t07/eleve.py`.
Aides progressives : liste des clés requises, vérification des types,
initialisation d'une variable `position`, boucle bornée avec
`enumerate`, test de la distance de Manhattan égale à 1,
consultation du registre, mémorisation des identifiants utilisés
dans un ensemble pour interdire leur réutilisation.

Exécuter 19 situations Python réelles. Trois cas à noms ou
coordonnées variables préviennent les réponses codées en dur.
Le moteur Pyodide affiche uniquement des résultats effectivement produits
par le programme élève, jamais par la démonstration JavaScript.

## Séance 3 — Argumenter et transférer (55 min)

Faire expliquer par écrit comment un faux journal peut être plausible.
Demander ce qu'il faudrait ajouter à un dispositif réel pour disposer
d'une **origine de preuve vérifiable** : contrôle des permissions de la
source, isolation du vérificateur, horodatage fiable, protection contre
l'effacement et, suivant les besoins, mécanismes cryptographiques
d'authenticité ou d'intégrité. Les valeurs du registre pédagogique ne
suffisent pas à prouver cela.

Pour les élèves rapides : proposer une stratégie de collecte de preuves
inaccessible à l'agent et un contrôle supplémentaire du rejeu.

## Recette, sécurité et séparation des ressources

- `python -m pytest -q qa_enseignant/test_t07.py`
- `node tests/test_t07_visualizer.cjs`
- `python tests/browser_t07.py` avec Chromium et Pyodide local.
- Non-régression T01→T06 et contrôle de la liste blanche via CI.

La solution témoin reste dans `qa_enseignant/test_t07.py`, exclue
du site distribué. Les traces et preuves de démonstration sont
**simulées**, non authentifiées et non issues d'un dépôt ou d'un robot réel.
La vérification de code Python dans un Worker et le filtrage AST ne
constituent pas une sandbox contre du code malveillant : usage scolaire
supervisé.

**Statut de livraison :** branche de recette uniquement ; aucune
fusion dans `main` et aucune publication sans validation humaine.
