# ORCHESTRA NSI — T04 · Outils, contrats et autorisations

## Positionnement et statut

**Terminale NSI — prolongement de T03 (trois séances de 55 minutes).**
Le thème « agents utilisant des outils » est une **mise en situation pédagogique
complémentaire**, et non un nouveau chapitre officiel du programme NSI.
Les capacités NSI effectivement mobilisées sont :
- spécifier l'interface d'une fonction et vérifier ses préconditions ;
- programmer des conditions et des dictionnaires, tester les types ;
- distinguer une valeur calculée de l'effet d'une instruction ;
- construire des tests et justifier un programme, notamment ses refus ;
- décomposer un système en composants ayant chacun une responsabilité.

Textes de référence :
- Programme de Terminale : https://eduscol.education.fr/document/30010/download
- Ressources pédagogiques Terminale : https://eduscol.education.fr/document/7319/download
- Épreuve de spécialité applicable dès la session 2027 : https://sti.eduscol.education.fr/actualites/epreuve-terminale-de-lenseignement-de-specialite-numerique-et-sciences-informatiques-nsi

Ce laboratoire n'est pas un moteur LLM. Les appels fictifs de Microduck sont
déterministes, les vérifications et les effets sont des fonctions explicites,
et toute « décision humaine » proposée par la page est locale et simulée.
On ne présente donc pas ce résultat comme une preuve de sûreté pour des agents réels.

## Contrat de l'activité Python

L'élève écrit `verifier_appel(appel, permissions)`, **sans effet de bord**.

`appel` est un dictionnaire contenant exactement `outil` et `arguments`.
`permissions` est un ensemble de noms d'outils autorisables. Il ne faut jamais
le modifier. La fonction renvoie un dictionnaire à deux clés exactement :
`{"statut": ..., "motif": ...}`.

| Outil | Arguments valides | Droit requis | Verdict si le droit existe |
|---|---|---|---|
| `observer` | `{}` | `observer` | `AUTORISÉ` |
| `avancer` | `{"direction": "N" / "E" / "S" / "O"}` | `avancer` | `AUTORISÉ` |
| `ouvrir_porte` | `{"position": (x, y)}`, où x est de 0 à 5 et y de 0 à 2 | `ouvrir_porte` | `ATTENTE_HUMAINE` |
| Tout autre outil | — | — | `REFUSÉ` |

Pour les coordonnées, `type(x) is int` est nécessaire : un booléen ne constitue
pas une coordonnée admissible. Les arguments supplémentaires sont refusés.
Un appel proposant son propre accord `"approuve": True` est mal formé,
**même si l'utilisateur approuve ultérieurement une autre action**.
En l'absence d'une permission, le refus est immédiat.
`teleporter` est interdit même si ce mot apparaît dans `permissions`.

La fonction **n'ouvre pas** de porte et **ne déplace pas** Microduck :
elle produit un verdict de contrat. Le monde examine une action autorisée
et peut la refuser pour collision, limite géographique ou absence d'objet.

### Point particulièrement important

`AUTORISÉ` signifie *appel autorisé*, pas *effet garanti*.
`ATTENTE_HUMAINE` signifie *aucune action immédiate* ; le système doit
solliciter une décision distincte. Dans les tests, cette décision est fournie
par le banc de vérification et explicitement marquée
`accord_humain_simule`. Elle n'est jamais produite par le programme élève.

## Séance 1 — Comprendre le poste de contrôle

1. Situation « Observer » : aucune modification du terrain.
2. Situation « Avancer » : un appel autorisé donne au plus un déplacement
   d'une case, avec animation d'une pose Microduck à la suivante.
3. Situation « Droit manquant » : vérifier l'absence de déplacement.
4. Situation « Ouvrir une porte » : observer l'état `ATTENTE_HUMAINE`,
   puis comparer refus et approbation ponctuelle.
5. « Fausse auto-approbation » : justifier pourquoi ce champ est exclu.
6. « Téléportation » : montrer le refus par liste blanche.
7. « Collision » : distinguer autorisation d'appel et effet physique.

Question flash : « L'agent peut-il fournir lui-même une preuve de consentement
humain dans ses arguments ? » Réponse : **non**.

## Séance 2 — Programmer le vérificateur

- Compléter `terminale/t04/eleve.py` avec le vocabulaire exact :
  *dictionnaire*, *clé*, *valeur*, *ensemble*, *variable de type entier*,
  *fonction*, *instruction conditionnelle* et *instruction d'affectation*.
- Contrôler d'abord la **structure et les types**, ensuite la liste blanche,
  puis les permissions, enfin le caractère sensible de l'outil.
- Écrire au moins trois exemples de requêtes invalides avant les tests.
- Exécuter les **treize situations Python réelles**.
- Observer un extrait de trace vérifiée, sans confondre la démonstration
  en JavaScript et l'exécution du programme élève dans Pyodide.

### Aides graduées

Niveau 1 : citer les deux clés de l'appel et les deux clés de retour.
Niveau 2 : distinguer l'autorisation générique `ouvrir_porte` de
l'approbation ponctuelle nécessaire pour une porte particulière.
Niveau 3 : comparer `type(v) is int` à `isinstance(v, int)`.
Niveau 4 : faire écrire d'abord des refus explicites (*fail closed*).
Pour les élèves rapides : tester les champs supplémentaires et justifier
pourquoi modifier `permissions` serait une faute de conception.

## Séance 3 — Transférer, argumenter, évaluer

Faire rédiger, sans indices, la raison pour laquelle une chaîne
« approuvé » ajoutée par un agent n'est pas une approbation humaine.
Faire tracer une opération sensible :
appel → validation du contrat → vérification du droit → attente humaine →
décision indépendante → tentative d'exécution → validation par le monde.
Faire établir un lien avec T03 (décision distincte de l'action).

Critères de validation humaine :
1. définition exacte de l'interface de `verifier_appel` ;
2. absence d'effet dans une fonction de vérification ;
3. refus par défaut de tout outil inconnu et de tout argument non prévu ;
4. distinction permission / approbation ponctuelle / effet réel ;
5. justification du caractère non fiable d'une auto-approbation.

## Tests, traçabilité et garde-fous

- `python -m pytest -q qa_enseignant/test_t04.py`
- `node tests/test_t04_visualizer.cjs`
- `python tests/browser_t04.py` : Chromium et véritable Pyodide local
- `python scripts/build_site.py --allow-cdn` : vérification de la liste
  blanche en développement, sans publier.
- Intégration dans `.github/workflows/pages.yml`, vérification de T01 à T04.

**La solution de référence est dans `qa_enseignant/test_t04.py`**, exclue
de la distribution élève. La liste blanche publie uniquement l'énoncé,
le code élève, les ressources graphiques et le moteur de vérification.
La compilation de code Python dans Pyodide, même avec un filtrage syntaxique,
n'est **pas** une sandbox de sécurité : seules des activités scolaires
supervisées sont autorisées. La diffusion demeure conditionnée à une
validation humaine explicite et ne doit pas modifier `main` automatiquement.
