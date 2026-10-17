# S03 — Corrigés argumentés

À distribuer après la recherche. La solution exécutable et les contrôleurs comparatifs se trouvent dans [s03_tp.py](python/s03_tp.py). La fonction `retenir` est le corps attendu pour `a_completer` ; le conducteur réutilise sa mémoire retournée. On attend un argument et des tests, pas seulement un code identique.

## Exercices A à G

A. Les deux observations finales sont `{"position": (1,1), "indice": None}`. Avec une commande restante, bleu exige gauche et orange droite. Une fonction déterministe de cette seule observation doit rendre le même mot.

B. Toujours gauche réussit en bleu et échoue en orange. Le cas bleu seul ne départage pas une règle correcte et cette règle insuffisante.

C. Au pas 1, l’indice n’est plus visible et l’affectation inconditionnelle remplace la couleur par `None`. Le contrôleur `ecraser` atteint la bifurcation sans couleur et s’arrête dans les deux mondes.

D. N’actualiser que si l’indice n’est pas `None`, puis retourner l’action calculée et la mémoire. La mémoire orange est conservée sous observation invisible ; une observation bleue remplace la mémoire initiale.

E. Sans indice reçu ni mémoire initiale, `retenir` retourne arrêt à la bifurcation. L’issue est `arrêt`, distincte de la réussite. La règle de prudence est un choix de conception, pas une garantie de sécurité physique.

F. Monde orange, mémoire bleu et indice absent : droite, bas, gauche, puis `mauvaise sortie`. Avec indice visible, la couleur orange corrige la mémoire dès le pas 0. Stocker une information ne certifie pas sa vérité. Terminale : après le pas 0 fiable, `m=couleur` ; aux pas 1 et 2, l’indice est `None` et la mise à jour conserve `m`. Cette induction ne vaut que pour les trajectoires et capteurs annoncés.

G. Les deux plans satisfont le même but ; l’utilité proposée vaut respectivement −2 et −5, donc préfère le premier. Cette préférence dépend du coût choisi. Les règles du TP n’effectuent aucune simulation prospective. L’hybridation est une possibilité de conception : par exemple planifier, conserver un indice et laisser un arrêt de sécurité prioritaire annuler la commande. Cela ne décrit pas une fonctionnalité ajoutée à l’application.

## Traces attendues du contrôleur correct

`b` désigne la couleur réellement observée au départ ; lire une fois avec bleu, une fois avec orange.

| Pas | Position observée | Indice | Mémoire avant | Action | Mémoire après | Position suivante |
|---|---|---|---|---|---|---|
| 0 | (0,0) | b | None | droite | b | (1,0) |
| 1 | (1,0) | None | b | bas | b | (1,1) |
| 2, bleu | (1,1) | None | bleu | gauche | bleu | (0,1) |
| 2, orange | (1,1) | None | orange | droite | orange | (2,1) |

`oublier` garde `None` à tous les pas ; `ecraser` garde la couleur seulement au pas 0, puis `None`. Les trois contrôleurs partagent le même conducteur et les mêmes observations, ce qui évite de changer simultanément la tâche et la mémoire.

## Bilan et remédiation

B1 : mise à jour conditionnelle et retour double conformes au contrat ; B2 : `(droite, orange)` ; B3 : absence d’observation confondue avec invalidation du souvenir ; B4 : commandes variables à transition fixe pour la politique, effet variable à commande fixe pour le glissement ; B5 : par exemple indice jamais reçu ou mémoire erronée non corrigée, avec issue explicitée.

Critères : chaque réponse doit être correcte et justifiée ; quatre sur cinq, B1/B2 nécessaires, seuil indicatif. B1 incorrect : refaire l’appel avec observation invisible et mémoire orange, sans boucle ; B2 incorrect : suivre l’ordre mise à jour/décision ; B3 incorrect : comparer les valeurs au pas 1 ; B4 incorrect : dessiner deux flèches choix puis effet ; B5 vague : demander un état initial et un résultat vérifiable.

## Conditions d’arrêt et cas limites

Le conducteur accepte 0 à 3 commandes, s’arrête à la bonne ou mauvaise sortie, sur arrêt, sur refus ou à épuisement du budget. Un budget nul produit une trace vide. Monde, mémoire, action ou budget invalides provoquent une erreur explicite. Le conducteur ne capture pas toutes les erreurs élèves : une exception doit rester visible et une boucle interne exige Stop. Les épisodes réinitialisent leur mémoire par défaut pour empêcher une fuite entre mondes. Les tests contrôlent aussi la correction d’une mémoire initiale erronée par un indice visible et l’absence de mutation de l’observation fournie.

Le tirage forcé 0 donne gauche, 1 donne droite ; les deux transitions depuis la bifurcation sont fixes. Une série pseudo-aléatoire à graine égale est reproductible. Elle ne démontre ni une fréquence limite ni une supériorité sur la mémoire.
