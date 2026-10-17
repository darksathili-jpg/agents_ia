# U01 — Corrigés expliqués

À remettre après la recherche. Les formulations proposées ne sont pas les seules réponses recevables : on évalue les données identifiées et le raisonnement. Le cours et les activités restent nécessaires pour connaître les règles des situations.

## 1. Cours élève : repérage, prédictions et expérience

**C0.** B est immédiatement à droite de A. C contient un mur. L’ordre et le contenu figurent dans le tableau de la piste ; aucune connaissance de coordonnées n’est nécessaire.

**P1.** La commande prévue est droite, parce que l’arrivée G se trouve à droite du robot. Depuis A, cette commande demande B. B étant libre, le moteur y place Microduck : la case après est B.

**E1.** La première ligne à relever est : case avant A (`0,2`), commande droite, case après B (`1,2`). Le mot de la commande et la position sont deux données différentes du journal et de l’affichage. Une éventuelle différence avec ces données doit conduire à vérifier le départ, la règle sélectionnée et la réinitialisation ; elle ne doit pas être masquée pour obtenir le résultat attendu.

**P2.** Après la première tentative, Microduck est en B : on ne le replace pas en A. G est encore à sa droite ; la règle choisit donc encore droite. Cette commande demande C, qui contient un mur. Le résultat prévu est le maintien en B, et non un passage en C.

**E2.** La deuxième ligne est : case avant B (`1,2`), commande droite, case après B (`1,2`). Le journal signale un obstacle et un mouvement refusé. La commande est bien droite : le refus ne signifie pas que la règle a choisi une autre commande.

**E3.** Deux commandes ont été choisies ; un seul déplacement a été réalisé, de A à B. Lors de la deuxième tentative, les positions avant et après sont identiques. Si l’élève avait prévu un second déplacement, il doit rapprocher sa prévision de la présence du mur en C. Si sa prévision était correcte, il explique pourquoi les données la confirment ; on n’exige pas d’inventer une erreur.

Une prédiction initiale incorrecte n’annule pas l’apprentissage. La preuve de compréhension est l’explication produite après confrontation et son réemploi dans une autre situation, pas le seul fait d’avoir deviné juste au départ.

## 2. Entraînement A1–A2

**A1.** Les essais sont indépendants ; le départ est imposé par chaque ligne.

| Essai | Case avant | Commande | Case demandée | Case après | Raisonnement |
|---|---|---|---|---|---|
| 1 | D | droite | E | E | E est immédiatement à droite de D et est libre : le mouvement est autorisé. |
| 2 | B | droite | C | B | C est immédiatement à droite de B et contient un mur : le mouvement est refusé. |

Le deuxième essai ne part pas de E : ce serait appliquer à tort une règle d’enchaînement alors que l’indépendance est explicitement annoncée. Les cas sont étudiés sur papier ; ils ne supposent pas un changement du départ de la grille réelle.

**A2 — Prolongement facultatif.** L’affirmation de Maya n’est pas compatible avec les données. Le sujet indique que la commande droite a déjà été choisie dans l’essai 2. Le maintien en B est le résultat de la vérification de C par le moteur. Conclure à l’absence de droite à partir du seul non-déplacement confond le choix et sa réalisation.

## 3. Transfert T1–T2

**T1.** Dans chaque essai, Nora repart du hall. La commande reste AVANCER ; elle ne provoque pas une ouverture de porte.

| Essai | Porte | Commande | Position après | Déplacement réalisé ? | Raison |
|---|---|---|---|---|---|
| 1 | fermée | AVANCER | hall | Non | La règle interdit de franchir une porte fermée ; le moteur conserve la position. |
| 2 | ouverte | AVANCER | bureau | Oui | La règle autorise le passage depuis le hall ; le mouvement est entièrement réalisé. |

Dans l’essai 1, aucune clé ou ouverture automatique ne peut être invoquée : elles sont exclues par le sujet. Dans l’essai 2, il ne faut pas imaginer un délai qui laisserait temporairement Nora dans le hall : le modèle donne le résultat après application complète.

**T2.** La commande choisie est la même dans les deux essais. Les positions obtenues diffèrent parce que l’état de la porte avant la commande n’est pas le même. La commande demande le passage ; la règle du moteur l’autorise pour la porte ouverte et le refuse pour la porte fermée. Il n’est pas nécessaire d’inventer un changement de décision.

Ce transfert vérifie la même distinction que la piste : un déplacement demandé n’est pas nécessairement accompli. La réponse ne demande pas de connaître le fonctionnement d’une porte réelle.

## 4. Vérification individuelle I1–I2 : troisième scénario

**I1.** Les essais sont indépendants : leur ordre ne change pas les positions avant données par le tableau.

| Essai | Position avant | Commande choisie | Position après | Déplacement ? | Justification |
|---|---|---|---|---|---|
| 1 | fin | DROITE | fin | Non | Depuis fin, la règle conserve fin : aucune position plus à droite n’est autorisée. |
| 2 | début | DROITE | fin | Oui | Depuis début, la règle place le curseur à fin ; il change donc de position. |

Les deux positions après sont identiques, mais cela ne signifie pas que les deux effets sont des déplacements : il faut comparer chaque position après à sa propre position avant. Le texte reste X ; il n’est ni déplacé ni effacé.

**I2.** L’affirmation est incompatible avec les données. La commande DROITE a explicitement été choisie dans l’essai 1. Le curseur est à fin avant et après, car aucune position plus à droite n’est autorisée. Le non-déplacement est donc compatible avec une commande de déplacement effectivement choisie. Il ne prouve pas l’absence de commande.

On n’a pas besoin d’inventer un mur, une porte, un retour au début ou un délai : la seule limite est celle des positions permises dans ce nouvel éditeur. Les réponses doivent expliquer cette règle, pas seulement reprendre « deux commandes, un déplacement » du cas Microduck.

## 4 bis. Bilan B1 — prolongement facultatif, hors budget essentiel

AVANCER indique une demande, pas la preuve d’un changement de pièce. Dans l’essai 1, Nora est dans le hall avant la commande et reste dans le hall après. La porte est fermée ; le moteur applique la règle qui empêche le passage. La commande a été choisie, mais le déplacement n’a pas été réalisé.

Réponse recevable, par exemple : « Elle a reçu AVANCER, mais la porte fermée l’empêche de passer : elle reste dans le hall. » Si la phrase ne donne pas la position avant, demander cette précision conformément à la question, sans imposer une terminologie savante.

« Nora reste parce qu’elle n’a pas choisi d’avancer » ne convient pas : le sujet donne explicitement AVANCER comme commande choisie. « Elle reste parce qu’elle a peur de la porte » n’explique pas le modèle : aucun comportement de ce type n’est défini.

## 5. Exercice enseignant E1–E4

**E1 — Compatibilité des lignes.**

| Ligne | Verdict | Justification |
|---|---|---|
| J1 | Compatible | Depuis le hall, porte fermée, AVANCER laisse Nora dans le hall. |
| J2 | Compatible | Depuis le hall, porte ouverte, AVANCER conduit au bureau. |
| J3 | Compatible | Nora est déjà dans le bureau ; la règle ne prévoit pas de déplacement plus loin, quelle que soit la porte. |
| J4 | Incompatible | Avec les données annoncées, Nora ne peut franchir la porte fermée. La position après conforme serait hall. |

J4 n’autorise pas à ajouter une ouverture automatique ou une autre action pour sauver la ligne : les règles les excluent. Si J4 provenait d’un vrai dispositif, il faudrait vérifier le relevé et les hypothèses du modèle avant de décider de la cause. Dans cet exercice, il s’agit de juger sa conformité aux données, pas de diagnostiquer une machine réelle.

**E2 — Deux conclusions abusives.** J1 fournit un contre-exemple à « AVANCER implique toujours un changement de pièce » : la commande est présente, mais la porte fermée empêche le mouvement. J3 serait également un contre-exemple valide à cette première affirmation.

J3 réfute « rester sur place signifie toujours que la porte a bloqué le passage ». Le personnage se trouve déjà dans le bureau : le modèle ne propose pas de nouvelle destination. La fermeture de la porte n’est donc pas ici la raison d’un passage refusé depuis le hall. Un même effet observable peut avoir des explications différentes selon la situation avant.

**E3 — Déterminisme.** J1 et J2 n’ont pas le même état avant. La position est la même, mais la porte est fermée dans J1 et ouverte dans J2. L’état a précisément été défini par les deux informations. Le modèle reste déterministe : pour un même état complet et la même commande, sa table donne un résultat unique. La commande ou la position seules ne suffisent pas pour effectuer cette comparaison.

**E4 — Relance et nouvelle preuve : un exemple de réponse.**

Relance possible : « Dans J1, quelle colonne t’indique ce qui a été commandé ? Quelles données permettent de vérifier s’il y a eu un changement de pièce ? » La question fait rechercher des indices distincts sans annoncer que le mouvement a été refusé. Une autre relance est recevable si elle vise cette séparation et ne fournit pas directement la conclusion à répéter.

Attendu après relance : l’élève cite AVANCER comme commande, hall comme position avant et après, puis relie ce maintien à la règle sur la porte fermée. L’apparition de cette explication après aide est notée comme telle, non comme preuve d’une réponse initialement autonome.

Situation de contrôle possible, entièrement spécifiée : Nora est déjà dans le bureau ; la porte est ouverte et ne change pas pendant l’essai ; une unique commande AVANCER est choisie ; on applique les mêmes règles du jeu. Résultat attendu : Nora reste dans le bureau, car aucune destination plus loin n’est prévue, bien qu’une commande ait été choisie. Cela vérifie la séparation commande/effet dans un autre état. Ce contrôle relève de l’approfondissement enseignant ; il ne remplace pas en cachette le transfert élève à partir du hall.

On peut proposer une autre situation si elle définit toutes les données utiles et ne fait appel à aucune règle nouvelle implicite. Avant d’utiliser une telle variante pour évaluer, il faut en fixer le résultat attendu et vérifier ce qu’elle mesure.
