# Architecture corrigée proposée — à approuver

## Principe de progression

Organiser la formation par difficultés à surmonter, non par chapitres d’une taxonomie. Une unité de 15 à 25 minutes vise une capacité centrale et se termine par une preuve individuelle courte sur un cas différent. Une activité réussie avec indices n’est pas encore une capacité autonome. Le découpage ci-dessous est une hypothèse de conception, pas un programme validé ni une autorisation de produire ses contenus.

L’ancien périmètre S01–S03 est un réservoir. Il n’est pas conservé sous forme de trois pages de deux heures simplement découpées par titres. S04/S05 restent suspendues, y compris sous un autre nom. Le tronc commun ci-dessous ne développe ni recherche de chemin ni agents LLM.

## Contrat de chaque unité future

Avant rédaction : préciser la question, ce que l’apprenant sait déjà, la seule capacité nouvelle, le modèle utilisé et ce qui ne peut pas être conclu. Concevoir ensuite un exemple guidé, une pratique avec aide décroissante, une tâche nouvelle sans aide et une remédiation ciblée. L’apprenant doit pouvoir expliquer le résultat avant d’être invité à employer un vocabulaire général.

Unité attendue : une situation stable ; quelques manipulations ou lignes pertinentes ; des traces lisibles ; une correction qui explique une erreur plausible ; un critère de passage. Un cas nouveau change une condition pertinente sans changer simultanément l’outil, le contexte et le vocabulaire. La navigation et les téléchargements ne doivent pas consommer l’essentiel du temps d’apprentissage.

## Tronc commun NSI : ordre et preuves de passage

| Unité proposée | Budget indicatif | Dépendance | Capacité centrale et preuve envisagée | Matériau ancien candidat |
|---|---|---|---|---|
| U01 — Commander n’est pas déplacer | 20 min | Lire une trace très simple ; remise à niveau du repérage si nécessaire | Distinguer commande et position obtenue lors d’un refus, puis sur un cas inédit | Deux tentatives S01, sans vocabulaire de classification. |
| U02 — Une règle utilise des informations | 20 min | U01 | Prédire un choix à partir de données et d’une règle donnée ; identifier une donnée non utilisée | Comparaison des coordonnées, d’abord en langage courant. |
| U03 — Délimiter le système étudié | 20 min | U01/U02 | Relier informations reçues, règle, commande et environnement sur un cas connu puis un cas différent | Définition d’agent et frontières S01, après construction du mécanisme. |
| U04 — Ce qu’une fonction retourne | 25 min | U02 et diagnostic Python ciblé | Prévoir une valeur retournée ; distinguer affichage et retour sur un appel nouveau | Diagnostic et appel simple TP01. |
| U05 — Modifier une politique | 25 min | U01/U04 et lecture d’une condition | Modifier une seule règle ; prévoir puis vérifier son effet sans confondre console et grille | TP01 simplifié ultérieurement ; aucun BFS exigé. |
| U06 — Quel test départage deux explications ? | 20 min | U02/U05 | Construire un cas discriminant et interpréter ce qu’il permet ou non de conclure | Direction constante contre comparaison S01. |
| U07 — Ce qui existe et ce qui est reçu | 20 min | U02/U03 | Distinguer état du modèle et observation sur deux cas ; ne pas confondre inconnu et absent | S02, sans glissement et sans notation ensembliste initiale. |
| U08 — Une information peut disparaître | 20 min | U07 | Montrer ce que perd une décision finale qui ne reçoit que l’observation courante | Deux mondes S02, après garantie d’un parcours commun. |
| U09 — Conserver une information utile | 25 min | U04/U05/U08 ; tuple de retour et `None` vérifiés séparément | Tracer puis programmer une mise à jour ; expliquer qui réinjecte la mémoire au pas suivant | S03, protocole à corriger après autorisation. |
| U10 — Quand la mémoire ne suffit pas | 20 min | U08/U09 | Expliquer un échec dû à une information jamais reçue ou erronée ; borner une garantie | Cas d’absence/erreur et limites S03. |

Total indicatif : **215 minutes**, hors remédiations, pauses et prolongements. Il ne s’agit pas d’une promesse de traiter le périmètre antérieur en 215 minutes : les classifications détaillées, le hasard et les architectures orientées objectif/utilité sortent du premier noyau obligatoire. Les temps de programmation pourront nécessiter une deuxième unité de pratique. Aucune durée globale ne sera figée à partir de la seule addition des budgets.

La programmation réelle reste essentielle aux unités qui l’annoncent. Elle n’est pas imposée dans U01, où elle ajouterait plusieurs obstacles syntaxiques à la question commande/effet. La compréhension conceptuelle et la maîtrise de l’outil sont observées séparément ; l’une ne sert pas à masquer l’autre.

## Approfondissements après maîtrise du noyau

| Prolongement proposé | Public / prérequis | Question à traiter ultérieurement | Statut |
|---|---|---|---|
| T1 — Même règle, effets variables ; choix variable, effet fixe | Terminale préparée et enseignants ; U06/U07 | Distinguer politique et transition stochastiques avec paramètres contrôlés, avant toute notation probabiliste | S02/S03 réorganisées ; budget initial 25 min à mesurer. |
| T2 — But, critère et choix entre résultats | Terminale préparée et enseignants ; U03/U06/U10 | Distinguer réussite, coût choisi et mécanisme de décision ; comparer deux alternatives entièrement explicitées | Comparaison sur table, sans concevoir un cours S04 de recherche ; 25 min à mesurer. |
| T3 — Classifications et systèmes hybrides | Enseignants ; T2 et lecture du mécanisme effectif | Justifier les dimensions combinables réflexe/état/but/utilité et les limites d’une classification | À dimensionner après les premiers essais ; aucune rédaction autorisée. |

Les élèves de Première partagent le même noyau scientifique ; on ne les définit pas par une version dépourvue d’explication. Les élèves de Terminale peuvent devoir revenir à U04 si les fonctions ne sont pas stabilisées. Le niveau de classe n’est pas une preuve de prérequis acquis.

## Parcours enseignant : un travail distinct, ancré dans le même phénomène

Les approfondissements ne sont pas une couche de symboles qui s’ajoute automatiquement au temps élève. L’enseignant commence par la situation et la preuve du tronc commun, puis réalise un travail de préparation séparé. Chaque approfondissement a ses propres prérequis, exercices d’analyse et critères ; leur durée n’est pas encore promise.

| Ancrage | Problème professionnel et scientifique | Production attendue / évaluation envisagée |
|---|---|---|
| U01/U02 | Délimiter commande, transition et résultat ; examiner ce que le journal établit réellement | Une table de cas, une distinction de responsabilités et une fausse explication analysée. Formaliser T seulement après cette table. |
| U03 | Comparer deux frontières du même système ; confronter une définition à un cas limite | Un argument de classement avec conditions et un contre-exemple, appuyé sur un extrait de source défini. |
| U04–U06 | Séparer erreur de syntaxe, erreur de contrat et insuffisance de stratégie | Diagnostic de productions contrastées et activité de remédiation vérifiable, pas seulement code correct. |
| U07/U08 | Démontrer ce qu’une observation identique autorise à conclure sous un protocole précis | Deux situations, hypothèses explicites, preuve expliquée puis tentative de réfutation. F01 doit être résolu avant usage. |
| U09/U10 | Relier histoire, état interne et mise à jour ; examiner les informations perdues ou fausses | Trace manuelle, invariant sous hypothèses, contre-exemple lorsque l’une change et transposition Première/Terminale. |
| T1–T3 | Situer hasard, utilité et repères d’architecture sans les ériger en hiérarchie d’intelligence | Modèle commenté, décision calculée et limite justifiée ; critique d’une source et de son transfert au cas étudié. |

La lecture scientifique future devra indiquer le passage utile, la question qu’il aide à résoudre et les limites d’attribution. Un manuel de synthèse, un article de recherche et un guide industriel restent distincts. Aucune nouvelle publication n’est inventée pour justifier ce découpage. Il s’agit d’une proposition pédagogique issue des défauts du corpus, à éprouver.

## Gestion des prérequis et des notations

Repérage spatial avant coordonnées ; exemple de valeur retournée avant contrat à trois paramètres ; donnée non reçue avant `None` ; comparaison de deux histoires avant mémoire finie ; deux tables de transition avant T et O ; tirages contrôlés avant distributions ; choix argumenté d’un coût avant utilité espérée. Une notation devient utile lorsqu’elle simplifie une relation déjà comprise, pas lorsqu’elle signale seulement un niveau universitaire.

En cas de difficulté, orienter vers une remédiation courte qui vise la même relation et demander une nouvelle preuve. Ne pas remplacer cette remédiation par un corrigé affiché, un clic « compris » ou une réduction générale d’exigence. Les conditions de passage sont des jugements sur des productions observables, pas des compteurs de pages lues.

## Passage de la proposition à la réalisation

Premier accord attendu : U01, sa durée cible, le choix d’un départ sans Python à programmer, le rôle de l’enseignant et ses critères. Après cet accord seulement : préparer les supports de cette unité, organiser son essai et recueillir les productions. Décider ensuite de l’ajustement, et non générer d’emblée U02 à U10. Aucune modification d’interface n’est requise ou autorisée par ce document.
