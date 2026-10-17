# S01.1 — Fiche de travail élève

Nom : ____________________ Classe : __________ Date : __________ Binôme : ____________________

À distribuer avec le cours S01 et le fichier Python de départ. Écrire d’abord une prédiction, puis la comparer à une exécution réelle. Les traits et cases ci-dessous sont des espaces de travail, pas des réponses proposées.

## 1. Diagnostic — 8 min, sans note

Lire ce code ; ne pas lancer Python avant d’avoir répondu aux cinq questions.

```python
def choisir_x(x, cible_x):
    if x < cible_x:
        return "droite"
    if x > cible_x:
        return "gauche"
    return "arrêt"

def annoncer():
    print("haut")
```

| Question | Ma réponse avant exécution | Après vérification, ce que je corrige |
|---|---|---|
| D1. Que renvoie `choisir_x(1, 4)` ? | __________________ | __________________ |
| D2. Que renvoie `choisir_x(4, 1)` ? | __________________ | __________________ |
| D3. Quelle branche sert si `x == cible_x` ? | __________________ | __________________ |
| D4. `resultat = annoncer()` : affichage et valeur de `resultat` ? | __________________ | __________________ |
| D5. Si `position = (3, 1)`, que valent `position[0]` et `position[1]` ? | __________________ | __________________ |

Vérification : copier entièrement [s01_diagnostic.py](python/s01_diagnostic.py) dans l’éditeur puis Exécuter Python. Ce script est **console seulement** : il ne contient pas de politique `decider` pour la grille. Une confusion persistante à signaler au professeur : ____________________________________________

## 2. Notre question — 7 min

Le robot a une destination mais se bloque devant un mur. Quelle information reçoit-il ? Quelle commande produit-il ? Pourquoi la commande n’implique-t-elle pas sa réussite ?

Mon schéma avec quatre boîtes (environnement, observation, politique, action) :

________________________________________________________________________________

________________________________________________________________________________

## 3. Trace réelle — 6 min

**Mode grille :** politique gloutonne → Réinitialiser → deux clics sur Exécuter une étape. Après chaque clic, lire position et journal. Ne pas recopier les coordonnées de l’illustration de classe.

| Tentative | Position avant | Commande | Résultat accepté/refusé | Position après |
|---|---|---|---|---|
| 1 | __________ | __________ | __________ | __________ |
| 2 | __________ | __________ | __________ | __________ |

Nombre de commandes : ______ Nombre de déplacements acceptés : ______

## 4. Hypothèses — 4 min

H1 : direction fixe ; H2 : comparaison des coordonnées ; H3 : LLM interprétant du langage. Choisir une contre-épreuve qui distingue H1 et H2, puis dire quelle preuve manquerait pour H3.

Mon cas de test et sa prédiction : ___________________________________________________

Une preuve dans le programme, plutôt que dans l’apparence du robot : ______________________

## 5. Modélisation et classification — 20 min

Lire les définitions du cours. Pour la porte automatique puis la grille, remplir ; un système peut appartenir à plusieurs descriptions. Les deux autres cas sont répartis entre les groupes.

| Système | Frontière choisie | Observation | Commande / effet possible | Pourquoi les termes choisis sont pertinents |
|---|---|---|---|---|
| Porte | __________ | __________ | __________ | __________________ |
| Grille | __________ | __________ | __________ | __________________ |
| Cas de mon groupe : ______ | __________ | __________ | __________ | __________________ |

Pourquoi « automate », « chatbot » et « agent » ne désignent-ils pas nécessairement trois groupes disjoints ?

________________________________________________________________________________

## 6. Programmation TP01 — 40 min protégées

**Étape A, console.** Copier [tp01_depart.py](python/tp01_depart.py). Avant de lancer, prédire ses sorties. Exécuter le retour constant, puis modifier `decider` pour les deux directions horizontales et l’arrivée. Ajouter ensuite haut/bas. Ne pas remplacer `return` par `print`.

| Appel : position → objectif | Prédiction | Retour réel | Ce que ce test vérifie |
|---|---|---|---|
| `(0,2)` → `(2,2)` | ______ | ______ | __________________ |
| `(4,2)` → `(2,2)` | ______ | ______ | __________________ |
| `(2,2)` → `(2,2)` | ______ | ______ | __________________ |
| `(2,1)` → `(2,2)` | ______ | ______ | __________________ |
| `(2,3)` → `(2,2)` | ______ | ______ | __________________ |

Ma modification et un test écrit avant exécution :

________________________________________________________________________________

________________________________________________________________________________

**Étape B, grille.** Garder la définition complète de `decider(position, objectif, obstacles)`. Les appels/prints en bas du script sont des essais ; ils ne choisissent pas les coordonnées de la grille. Choisir Mon agent Python, Réinitialiser, puis deux pas. Compléter une trace en distinguant le retour Python et le déplacement accepté/refusé :

________________________________________________________________________________

Une difficulté et sa correction : ____________________________________________________

## 7. Analyse et transfert — 25 min

Analyse (15 min) : la fonction reçoit-elle les murs ? Les exploite-t-elle ? Un nom d’action correct prouve-t-il qu’il existe un trajet ?

________________________________________________________________________________

Transfert (10 min) : personnage à clé, trois commandes possibles : ______ / ______ / ______

Une observation utile : __________________ Un effet à vérifier : _________________________

Si l’indice disparaît, quelle question faut-il résoudre ? __________________________________

## 8. Billet individuel — 10 min

Définition avec frontière : __________________________________________________________

Un recouvrement automate-agent justifié : _____________________________________________

Pourquoi notre expérience ne prouve pas l’emploi d’un LLM : ______________________________

Un cas de test manquant : __________________________________________________________

À la fin, rendre la fiche et le code. Cocher : [ ] prédictions [ ] exécution console [ ] essais grille [ ] limite expliquée. Le professeur fournit les corrections après la recherche ; aucun succès d’animation ne remplace les explications.
