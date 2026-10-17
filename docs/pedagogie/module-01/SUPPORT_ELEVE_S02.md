# S02 — Feuille d’enquête : environnement, observations et actions

Nom : ____________________ Classe : __________ Date : __________ Binôme : ____________________

Question : pourquoi l’agent ne peut-il pas toujours choisir ce qui convient avec les seules informations reçues ? Suivre les temps du cours ; ne pas lire les corrections avant la mise en commun.

## Rappel et hypothèse — 10 min

Une commande refusée dont je me souviens : ___________________________________________

Mon explication provisoire : ________________________________________________________

Ce que je dois observer pour la vérifier : ______________________________________________

## État et observation — 15 min

| Fait du monde | Donnée effectivement reçue par le programme | Ce qui reste inconnu |
|---|---|---|
| __________________ | __________________ | __________________ |
| __________________ | __________________ | __________________ |

S02-A. Une donnée du robot accessible à sa politique : __________________________________

S02-B. Deux mondes possibles quand le capteur ne transmet rien : _________________________

« Inconnu » et « absent » sont différents parce que : ___________________________________

## TP02 : décider n’est pas appliquer — 30 min

**Console :** copier `python/s02_obstacle_depart.py`. Le code ne pilote pas la grille ; compléter `appliquer` seulement. Prédire puis lancer. Dans la grille 7 × 5, x augmente vers la droite, y vers le bas.

| État : position / carte | Commande | Candidate | Effet prédit / constaté | Position après |
|---|---|---|---|---|
| `(0,2)`, libre | droite | ______ | ______ / ______ | ______ |
| `(1,2)`, mur `(2,2)` | droite | ______ | ______ / ______ | ______ |
| `(0,0)`, libre | haut | ______ | ______ / ______ | ______ |
| `(0,2)`, libre | arrêt | sans déplacement | ______ / ______ | ______ |

S02-C. Écrire la transition devant le mur sans inventer de déplacement : ______________________

S02-D. Ma modification de fonction et un test discriminant : _________________________________

________________________________________________________________________________

S02-E. Pourquoi ce code n’invente-t-il pas un détour ? ____________________________________

Une erreur, son message et ce que j’ai corrigé : _________________________________________

## Déterminisme et glissement — 15 min

Les essais ci-dessous repartent chaque fois de `(0,2)` sans mur et commandent droite.

| Modèle / essai | Ce qui varie | Position après | Ce qui reste contrôlé |
|---|---|---|---|
| Transition sans glissement | ______ | ______ | ______ |
| Tirage forcé 0 | ______ | ______ | ______ |
| Tirage forcé 1 | ______ | ______ | ______ |

S02-F. La politique a-t-elle changé ? __________ Le mur est-il devenu traversable ? __________

Une chose que huit tirages ne prouvent pas : __________________________________________

## Observation masquée — 25 min

**Console uniquement :** copier `python/s02_observation_masquee.py`. Les deux commandes droite/bas sont imposées ; elles ne sont pas choisies par un nouvel agent autonome. Dessiner le repère 3 × 2 ; `(2,0)` est un mur. Compléter avant de lancer.

| Étape | Position | Monde bleu : indice réel / indice observé | Monde orange : indice réel / indice observé |
|---|---|---|---|
| Départ | `(0,0)` | ______ / ______ | ______ / ______ |
| Après droite | `(1,0)` | ______ / ______ | ______ / ______ |
| Après bas | `(1,1)` | ______ / ______ | ______ / ______ |

S02-G. Observation finale commune : _________________________________________________

Sortie requise monde bleu : ______________ Sortie requise monde orange : ______________

Pourquoi une même règle de l’observation finale ne garantit-elle pas les deux ? _______________

________________________________________________________________________________

Une information à conserver ou à redemander : _________________________________________

Pourquoi retourner au départ ne répond-il pas à la tâche avec une seule commande restante ?

________________________________________________________________________________

## Formalisation et transfert — 15 min

Mon schéma état / observation / commande / transition / effet :

________________________________________________________________________________

Navigation avec route fermée inconnue : état réel ______ ; observation ______ ; résultat à vérifier ______

## Bilan individuel — 10 min

B1. État et observation, différence et exemple : __________________________________________

B2. Position avant, commande et position après d’un refus : _______________________________

B3. Déterministe ou stochastique : quel composant ? _____________________________________

B4. Mon contre-exemple sans mémoire et sa limite : _____________________________________

B5. Pour piloter la grille, on fournit ______ ; les scripts de masque/glissement s’exécutent en ______.

[ ] prédictions confrontées [ ] fonction modifiée [ ] limite écrite [ ] code remis au professeur
