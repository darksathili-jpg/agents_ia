# S01.1 — Exemple complet de production enseignant attendue

Exemple de référence, à discuter après la production personnelle ; il ne constitue pas une réponse unique. Il traite le système réellement présent, sans attribuer au Worker une mémoire qu’il n’a pas.

## 1. Modélisation explicitée

**Tâche** : atteindre `(6,2)` sur une carte fixe 7 × 5. Critères de comparaison : réussite, nombre de commandes et déplacements acceptés. Les obstacles sont ceux du labo ; notamment `(2,2)` est occupé. Le budget et la convention de refus doivent être spécifiés avant de comparer des programmes.

```text
Monde : position, carte et cible
    → données connues (position, objectif, obstacles)
    → politique Python decider
    → chaîne de commande
    → vérification et application par le moteur
    → position/état/journal observés au pas suivant
```

Je choisis comme agent le contrôleur en interaction avec ce monde ; la fonction `decider` est son composant de décision. Le Worker est son mécanisme d’exécution, pas un deuxième robot. Le moteur applique la commande et peut la refuser. La carte et la cible sont connues dans cette expérience : nous ne modélisons pas une caméra ou un vrai robot physique.

Si l’on choisit seulement `decider` comme frontière, ses entrées sont trois objets et sa sortie une chaîne. Cette description aide à tester le contrat mais ne suffit pas à affirmer que le monde a changé. La frontière contrôleur-environnement permet de comparer plusieurs politiques sur une même transition.

## 2. Argumentation par programme et trace

La règle locale compare des coordonnées ; elle n’appelle pas de modèle de langage. Elle reçoit les murs, mais n’en déduit pas de détour. Une comparaison de code et d’appels discriminants est une preuve plus pertinente que l’apparence expressive de Microduck.

| Tentative | Position avant | Choix et raison | Vérification / effet | Position après |
|---|---|---|---|---|
| 1 | `(0,2)` | droite, car 0 < 6 | `(1,2)` libre, accepté | `(1,2)` |
| 2 | `(1,2)` | droite, car 1 < 6 | `(2,2)` mur, refusé ; épisode bloqué | `(1,2)` |

Deux commandes, un déplacement. Le code peut être conforme à l’alphabet et insuffisant pour cette tâche : cette insuffisance ne doit pas être imputée à Pyodide. Un retour constant droite expliquerait ces deux commandes aussi ; pour le départager d’une comparaison, je teste une cible à gauche par appel console. Cet appel n’a pas changé la cible de la grille.

## 3. Critique du modèle et du critère

Cette trace montre une limite de la règle locale sur une carte, non l’impossibilité de programmer un détour. Une carte connue et une transition déterministe favorisent l’analyse ; elles ne représentent pas la perception bruitée d’un robot réel. Un autre test de réussite, une autre carte ou un droit de réessai peuvent modifier le classement des stratégies.

Je ne confonds pas autonomie opérationnelle et succès : en mode automatique, le contrôleur peut enchaîner des choix sans que l’humain indique chaque commande, tout en échouant. Le mode pas à pas suspend l’exécution pour l’observation pédagogique ; il ne remplace pas la politique par une décision manuelle. Le fait qu’une action ait été expliquée dans le journal ne prouve pas une conscience ou une justification interne de LLM.

## 4. Transposition et contrôle des acquis

Première : distribuer le repère x/y et faire remplir les quatre dernières colonnes de la trace avant de discuter la définition. Terminale : demander un contre-test qui départage deux fonctions et une spécification de retour. Je valide la compréhension si l’élève distingue observation, commande et effet, justifie une limite et propose un test susceptible d’invalider sa première explication.

Si l’élève écrit « le robot décide de rester car il voit le mur », je demande : « Quel return du code produit cela ? Qui vérifie ensuite la candidate ? » Dans ce cas la commande reste droite ; c’est la transition qui refuse. Une réponse corrigée par cette lecture vaut davantage qu’un vocabulaire appris sans trace.
