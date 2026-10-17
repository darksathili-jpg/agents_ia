# Sujets de TP et banque d’exercices

Les cinq TP constituent les supports expérimentaux de la progression, pas cinq nouvelles interfaces. TP01 accompagne le pilote rédigé. TP02–05 sont des **fiches de conception et supports exécutables à relire lors de la rédaction future**, sans cours S2–S5 anticipé. Les corrections sont distribuées séparément par l’enseignant.

## Mode opératoire commun

Copier le fichier de départ entier dans l’éditeur du laboratoire, puis utiliser **Exécuter Python**. Il est autonome, sans bibliothèque tierce. Les auxiliaires fournis ne sont pas tous à réécrire. TP02–05 affichent initialement `A_COMPLETER_TPxx` : ce message identifie les parties à construire, il ne signifie pas que l’exercice est réussi. Les tests de réussite s’appliquent après complétion. Conserver prédiction, code et sortie réelle. Si le texte ne correspond pas à la grille animée, rappeler que les expériences console peuvent avoir leur propre modèle.

Pour TP01/TP02, le branchement visuel n’est utilisé qu’avec une fonction `decider` conforme. Pour TP03, **ne pas sélectionner Mon agent Python** en espérant que ses globales persistent : toute la séquence de mémoire s’exécute en un seul lancement dans la console.

## TP01 — Mon premier agent réactif (40 min en S1)

**Objectifs :** O4/O5 ; écrire une fonction à partir d’une observation et vérifier ses retours. **Prérequis :** fonction, condition, coordonnées. [Code initial](python/tp01_depart.py).

**Question :** une comparaison de coordonnées suffit-elle à choisir une action ? **Hypothèse :** dans une ligne libre, une règle réactive réduit la distance horizontale. **Contrôlés :** même fonction, mêmes noms d’actions, pas de mur dans les premiers appels. **Variable :** position par rapport à la cible. **Observations :** retour exact et, ensuite, effet dans la grille. **Attendu :** droite, gauche, arrêt pour les trois cas initiaux une fois le code modifié. **Réussite :** retours conformes, trois prédictions confrontées au résultat puis cas vertical ajouté. **Limite :** on n’a pas prouvé l’existence d’un chemin dans une carte avec obstacles.

Consignes graduées : (1) prédire les trois sorties du code constant ; (2) exécuter sans rien changer et expliquer ce qui manque ; (3) ajouter le choix droite/gauche ; (4) traiter l’arrivée avant de lancer un déplacement ; (5) ajouter haut/bas avec `y` croissant vers le bas ; (6) essayer la fonction sur la grille initiale et garder la trace d’un échec.

Indices, à demander successivement : I1, comparer `position[0]` et `objectif[0]` ; I2, chaque branche doit retourner une chaîne exacte ; I3, tester l’égalité complète avant le déplacement vertical. Tests après complétion : `(0,2)→(2,2)` donne droite ; `(4,2)→(2,2)` gauche ; cible égale arrêt ; `(2,1)→(2,2)` bas ; `(2,3)→(2,2)` haut.

Erreurs à analyser : `print` au lieu de `return`, oubli de branche, inversion haut/bas, idée que le retour constitue le mouvement. Production : fonction, cinq appels, trace et une limite. **Prolongement enseignant :** spécifier domaine, alphabet d’actions et information effectivement exploitée ; construire un cas révélant que conformité et réussite sont deux propriétés distinctes.

## TP02 — Un agent face à un obstacle (30 min en S2)

**Objectifs :** O2/O7/O8 ; dissocier décision et transition. **Prérequis :** TP01, appartenance à une liste, conducteur fourni. [Code initial](python/tp02_depart.py).

**Question :** la commande « droite » implique-t-elle un déplacement ? **Hypothèse :** une transition valide refuse un mur tout en conservant la position. **Contrôlés :** départ `(0,2)`, cible `(6,2)`, règle locale du TP01, dimensions 7 × 5. **Variable :** carte libre puis obstacles du laboratoire. **Observations :** position avant, commande, position après, refus. **Attendu :** cas libre réussi ; devant le mur, position `(1,2)` conservée. **Réussite :** transition correcte aux bords et obstacles, résultat d’arrêt documenté. **Limite :** détecter un refus n’invente pas un détour.

Consignes : compléter `appliquer` pour chercher la direction, calculer la case candidate et appeler `libre` ; conserver la position si refus ; traiter `arrêt` ; signaler une commande inconnue. Tester la transition isolément avant de l’insérer dans une boucle. Comparer ensuite les deux tentatives gloutonnes du laboratoire à votre trace textuelle.

Indices : I1, le test de liberté porte sur la candidate, pas la position avant ; I2, retourner `(position, "refuse")` devant le mur ; I3, le conducteur s’arrête sur refus, donc le compteur de déplacements n’est pas celui des commandes.

Tests : `(1,2), droite, MURS` reste `(1,2)` refusé ; `(0,0), haut, []` reste `(0,0)` ; `(0,2), droite, []` donne `(1,2)` accepté ; `voler` doit être signalé comme action inconnue. Production : transition, tests, tableau deux cartes. **Prolongement enseignant :** comparer la convention d’arrêt du labo et un environnement qui laisse l’agent réessayer ; même politique, autre dynamique, autre conclusion.

## TP03 — Ajouter un état interne (35 min en S3, préparation 25 min en S2)

**Objectifs :** O2/O6 ; mettre en évidence une information mémorisée. **Prérequis :** dictionnaire expliqué, fonction à deux résultats, séquence en une exécution. [Code initial](python/tp03_depart.py).

**Question :** comment retrouver une sortie si l’indice n’est plus visible ? **Hypothèse :** retenir une couleur permet de différencier deux histoires devenues identiques à l’écran. **Contrôlés :** grille textuelle 3 × 2, départ `(0,0)`, chemin vers `(1,0)` puis `(1,1)`, observations de position exactes. **Variable :** indice bleu ou orange visible seulement au départ. **Observations :** dictionnaire d’observation, mémoire entrée/sortie et action. **Attendu :** à la bifurcation, gauche pour bleu, droite pour orange. **Réussite :** deux sorties atteintes en trois commandes ; indice absent de l’observation finale mais conservé en mémoire. **Limite :** cette mémoire suffit à cet exemple construit, pas à tout monde partiellement observable.

Grille textuelle : départ en haut à gauche, couloir en haut au centre, bifurcation en bas au centre, sorties en bas à gauche et à droite. La règle de tâche est annoncée : bleu impose sortie gauche, orange impose droite. Le programme de décision doit lire la couleur **uniquement** dans l’observation, jamais dans la variable cachée de l’environnement.

Consignes : appeler `observer_case` au départ pour les deux couleurs ; appeler ensuite en `(1,1)` et comparer ; compléter `decider_memoire` avec mise à jour explicite ; dérouler les trois pas en conservant `memoire` dans la boucle console. Retour attendu : `(action, nouvelle_memoire)`.

Indices : I1, `None` signifie indice non visible, pas indice bleu ; I2, ne pas écraser une mémoire utile avec `None` ; I3, la mémoire est une entrée/sortie, pas une lecture clandestine de la couleur d’origine. Tests : même observation en bifurcation pour les deux mondes ; mémoire bleu donne gauche, orange droite ; mémoire absente doit signaler une information manquante. **Prolongement enseignant :** démontrer l’impossibilité d’une garantie des deux réussites pour une politique déterministe de l’observation courante seule ; discuter le cas aléatoire sans l’assimiler à un LLM.

## TP04 — Rechercher un chemin (50 min en S4)

**Objectifs :** O5/O7/O8 ; produire et contrôler un chemin. **Prérequis :** Terminale, graphe, file FIFO et dictionnaire de prédécesseurs ; en Première, guider ou fournir cette partie. [Code initial](python/tp04_depart.py).

**Question :** une recherche dans la carte peut-elle dépasser la décision locale ? **Hypothèse :** BFS trouve un chemin lorsqu’il existe dans ce graphe fini à coûts unitaires. **Contrôlés :** même carte, même départ/cible, ordre des directions donné. **Variable :** choix local versus recherche. **Observations :** chemin retourné, longueur, validité de chaque mouvement, état final. **Attendu :** 10 déplacements dans la carte du labo ; aucun chemin si la cible est isolée. **Réussite :** arrivée, départ=cible, impossibilité et bords correctement traités. **Limite :** minimum de pas ne signifie pas minimum d’énergie à coûts variables.

Consignes : enfiler le départ ; marquer un sommet lors de sa découverte ; visiter par `popleft` ; mémoriser prédécesseur et action ; reconstruire à l’arrivée ; renvoyer `None` si la file est vide sans arrivée. Vérifier chaque mouvement du chemin au moyen de la transition TP02.

Indices : I1, un dictionnaire de prédécesseurs sert aussi à savoir ce qui est découvert ; I2, pile et file ne donnent pas le même ordre ; I3, remonter les prédécesseurs puis inverser les actions. Tests : carte libre 6 ; carte labo 10 ; départ=cible liste vide ; cible entourée aucune solution ; détour autour de `(1,2)` vers `(2,2)` longueur 4. **Prolongement enseignant :** justifier exploration par niveaux et coût abstrait, puis identifier les surcoûts d’une implémentation qui copie des chemins.

## TP05 — Évaluer expérimentalement un agent (25 min en S5)

**Objectifs :** O7/O8/O10 ; utiliser un banc fourni pour produire une conclusion défendable. **Prérequis :** exécuter des fonctions et lire un tableau ; algorithmes fournis pour libérer du temps. [Code initial](python/tp05_depart.py).

**Question :** dans quels cas une politique est-elle meilleure selon le critère choisi ? **Hypothèse :** BFS réussit les cas accessibles du jeu ; la règle locale échoue sur certains obstacles. **Contrôlés :** jeu C0–C5, même borne de 35 commandes et même transition. **Variable :** politique. **Observations :** réussite, cause d’arrêt, tentatives, déplacements et surcoût lorsque défini. **Attendu :** BFS réussit 5 cas sur 6, politique locale 3 sur 6 ; le cas impossible n’est pas une faute de recherche. **Réussite :** 12 lignes complètes, échecs conservés, métriques valides et conclusion bornée. **Limite :** six cartes ne représentent pas tous les environnements.

Cas fournis : C0 libre, C1 labo, C2 départ=cible, C3 cible isolée, C4 deux coins opposés sans mur, C5 petit détour. Ils sont définis exactement dans le fichier initial. Consignes : appeler chaque politique sur chaque cas, garder tous les résultats, calculer le taux sur l’effectif complet ; ne calculer `L−L*` que pour les réussites accessibles. Formuler une conclusion et un prochain test susceptible de la contredire.

Indices : I1, `None` n’est pas un trajet de longueur zéro ; I2, annoncer le dénominateur ; I3, séparer impossibilité de la carte et défaut de stratégie. Tests : 12 lignes, surcoût nul des réussites de ce jeu, échecs avec surcoût non défini. **Prolongement enseignant :** séparer développement et cas de vérification ; plusieurs graines pour une politique aléatoire, même budget et incertitude mesurée plutôt qu’un unique trajet favorable.

## Banque de quinze exercices non redondants

La banque est répartie dans les séances ; ne pas ajouter ses quinze items à tous les TP. Les exercices de la séance pilote sont E01–05. Les autres sont des sujets de préparation de la progression, pas des leçons futures déjà rédigées.

| ID / niveau | Sujet et production demandée | Critère observable |
|---|---|---|
| E01 / comprendre | Refaire le schéma d’entrée/sortie du robot après deux tentatives. | Distingue programme et environnement. |
| E02 / comprendre | Classer porte, fonction de grille et chatbot sans cases exclusives. | Deux descriptions compatibles justifiées. |
| E03 / comprendre | Dans un assistant à outils, séparer modèle et exécuteur. | Identifie qui transforme une proposition en action. |
| E04 / comprendre | Prédire les trois sorties du code constant puis d’une règle horizontale. | Prédictions et retours exacts confrontés. |
| E05 / appliquer | Compléter la politique TP01 et ajouter les cas verticaux. | Cinq retours attendus et assertion d’arrivée. |
| E06 / comprendre | Décrire une information masquée sans modifier l’état du monde. | Ne confond pas inconnue et absence. |
| E07 / appliquer | Écrire une observation donnant position et indice seulement au départ. | Les deux mondes donnent la même observation ensuite. |
| E08 / appliquer | Mettre à jour une mémoire sans l’effacer à chaque `None`. | Les deux sorties du TP03 sont différenciées. |
| E09 / appliquer | Journaliser observation, mémoire, commande et effet sur trois pas. | N’invente pas un mouvement quand la transition refuse. |
| E10 / analyser | Construire un échec d’une règle qui diminue la distance horizontale. | Carte explicite, trace et explication du blocage. |
| E11 / appliquer | Rejouer deux politiques aléatoires avec graine 7, puis changer de graine. | Distingue reproductibilité de distribution et mécanisme LLM. |
| E12 / analyser | Remplacer FIFO par LIFO dans une recherche : quelle garantie faut-il réexaminer ? | Ne conclut pas à l’optimalité d’un simple chemin trouvé. |
| E13 / analyser | Lire « 5/6 réussites » et « longueur moyenne 0 sur les échecs ». Corriger le compte rendu. | Dénominateur et indicateur conditionnel définis. |
| E14 / concevoir | Proposer un cas où la longueur minimale ne minimise pas un coût variable. | Deux trajets et coûts explicites. |
| E15 / concevoir | Agent LLM : proposer une action invalide plausible, un contrôle et un test de ce contrôle. | Distingue génération, validation, exécution et observation. |
