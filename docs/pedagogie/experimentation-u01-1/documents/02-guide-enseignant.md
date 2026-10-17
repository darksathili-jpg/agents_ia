# Guide d’accompagnement et de formation — U01.1

Réservé à l’enseignant. Préparation documentaire : aucun résultat d’essai n’est annoncé.

## Objectif, prérequis et organisation

L’élève distingue commande choisie et effet obtenu, explique un refus puis réutilise le raisonnement avec Nora et le curseur. Il sait repérer la droite et comparer deux positions ; aucun programme ni vocabulaire de théorie des agents n’est requis. La préparation scientifique enseignante qui suit ne suppose pas cette théorie et se déroule hors du temps élève.

Lire la procédure jointe et vérifier le laboratoire avant l’accueil. Imprimer le support élève en recto, garder ce guide et ses corrigés hors de vue. Distribuer progressivement : page 1, pages 2–3, puis page 4 après E2/E3, page 5 et page 6. La page 4 est l’explication de cours après observation ; elle ne doit pas anticiper les prédictions. Les références Markdown citées dans la reprise des sources désignent ici les parties correspondantes du dossier imprimé.

| Phase essentielle | Budget hypothétique | Intervention prévue |
|---|---|---|
| Contexte et C0 | 0–3 min | Faire repérer les données, sans annoncer l’issue. |
| P1, E1, P2, E2, E3 | 3–10 min | Lecture guidée du journal en E1 ; garder les prédictions. |
| Explication | 10–12 min | Faire distinguer ce qui est demandé et ce que vérifie le moteur. |
| Entraînement A1 | 12–14 min | Essais papier indépendants. |
| Nora T1–T2 | 14–17 min | Recueillir sans dicter la règle pertinente. |
| Curseur I1–I2 | 17–20 min | Réponse individuelle avant correction de Nora. |

Ce budget est à mesurer, non une durée validée. Noter pauses et temps techniques séparément ; ne supprimer aucune phase pour tenir vingt minutes. Les prolongements A2/B1 figurent seulement dans les corrigés de référence, hors de cet essai essentiel.

## Observer sans donner la réponse

Demander « quelle donnée du sujet utilises-tu ? » ou « peux-tu montrer ce que tu lis ? ». Éviter « le mur bloque, n’est-ce pas ? » et toute annonce du nombre de déplacements. Une relance peut néanmoins influencer : transcrire ses mots et conserver réponse initiale et réponse revue. Aider l’accès au journal en E1 est prévu, sans équivaloir à une preuve d’autonomie conceptuelle.

Recueillir Nora et le curseur avant correction ; distinguer autonome, avec relance, non établi, non observable. Un tableau juste sans explication ne suffit pas. Ne pas confondre erreur de repérage et confusion conceptuelle. Après recueil, employer les remédiations détaillées plus loin ; ne pas laisser un élève en échec pour préserver une mesure.

Pour un enseignant découvrant la notion : étudier d’abord le parcours complet ci-dessous, résoudre l’exercice enseignant avant ses corrigés, puis remplir le retour enseignant. Le Python est une préparation distincte et facultative, exécutée dans un interpréteur local ; il ne pilote pas le laboratoire.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# U01 — Parcours enseignant

Vous connaissez l’informatique, mais aucune connaissance préalable de la théorie des agents n’est supposée. Cette préparation est distincte des vingt minutes élève. Elle ne reprend pas les anciennes séances comme des cours validés.

## 1. Partir du phénomène

Dans le cours élève, la première commande droite conduit de A à B ; la seconde demande C, occupée par un mur, et la position reste B. La commande est choisie deux fois. Le mouvement n’est accompli qu’une fois. Ce résultat est entièrement déterminé par la règle de déplacement et les positions successives.

Le but de l’unité n’est pas de faire apprendre une définition d’agent, mais de séparer deux responsabilités informatiques. **La décision sélectionne une commande ; l’application de cette commande calcule et produit l’état suivant selon les règles du modèle.** Une commande n’atteste pas sa propre réalisation.

Dans le laboratoire, la fonction de décision gloutonne compare la position à la destination. Le moteur examine ensuite la case demandée et refuse une case interdite. La vérification ne remplace pas la commande par une autre. Le message « Bloqué » décrit une issue de l’épisode, pas une nouvelle décision du contrôleur.

## 2. Analyser la trace sans lui faire dire davantage

| Tentative | Données avant | Commande sélectionnée | Vérification | Résultat |
|---|---|---|---|---|
| 1 | Robot A ; arrivée G | droite | B est libre | Robot B ; un déplacement. |
| 2 | Robot B ; arrivée G | droite | C contient un mur | Robot B ; aucun déplacement supplémentaire. |

Le journal permet de constater les commandes et les positions. Pour affirmer comment les commandes ont été choisies, il faut disposer de la règle donnée dans le sujet ou examiner le code. La présence de droite deux fois ne suffit pas à prouver que le programme choisit droite dans toutes les situations.

Contre-exemple à la conclusion « une commande de déplacement provoque toujours un déplacement » : la deuxième ligne. À l’inverse, rester sur place ne prouve pas l’absence de commande : une demande de déplacement peut avoir été refusée. Ce sont des implications sur le modèle observé, pas des explications par l’intention du robot.

## 3. Pourquoi ce transfert porte sur le même mécanisme

Le sujet de transfert fournit la position initiale, la commande, les deux états possibles de la porte et la règle qui relie ces données au résultat. Une porte fermée empêche le passage ; AVANCER ne l’ouvre pas. Chaque essai repart du hall. La destination et le changement de vocabulaire ne demandent aucune connaissance sur les portes automatiques réelles.

La commande reste AVANCER dans les deux essais ; c’est l’état de la porte qui change. On n’évalue ni le choix d’une commande optimale, ni une action d’ouverture, ni une attente temporelle. Si l’élève invente une clé ou une ouverture automatique, faire localiser l’hypothèse dans le sujet avant de conclure à une erreur de raisonnement. Les règles décrivent un jeu simplifié, pas une norme de contrôle de portes physiques.

## 4. Formalisation facultative, après les cas concrets

Cette section n’est pas remise aux élèves pour valider U01. Son intérêt est de rendre explicites les informations nécessaires au calcul du résultat et de vérifier toutes les situations du modèle de la porte.

Un **état** est ici une description complète des deux informations pertinentes : la position de Nora et l’état de la porte. On note un état par un couple, par exemple `(hall, fermée)`. La première composante nomme la pièce où se trouve Nora ; la seconde indique si la porte est ouverte ou fermée. Il ne s’agit pas de coordonnées.

Appelons `S` l’ensemble des quatre états possibles : `(hall, fermée)`, `(hall, ouverte)`, `(bureau, fermée)` et `(bureau, ouverte)`. Appelons `C` l’ensemble des commandes de ce modèle ; il ne contient ici que `AVANCER`. La lettre `c` désignera une commande de cet ensemble et `s` un état de `S`.

Une fonction `T` associe à un état avant et à une commande un état après. L’écriture `T(s, c)` signifie « l’état obtenu en appliquant la commande c à l’état s ». On peut résumer le contrat par `T : S × C → S` : `×` signifie que l’entrée comporte un état et une commande ; la flèche indique que le résultat est un état. Cette notation ne remplace pas la définition de T, donnée par la table suivante.

| État avant `s` | Commande `c` | État après `T(s,c)` | Changement de pièce ? |
|---|---|---|---|
| (hall, fermée) | AVANCER | (hall, fermée) | Non : passage refusé. |
| (hall, ouverte) | AVANCER | (bureau, ouverte) | Oui. |
| (bureau, fermée) | AVANCER | (bureau, fermée) | Non : aucune destination plus loin n’est prévue. |
| (bureau, ouverte) | AVANCER | (bureau, ouverte) | Non : même raison. |

Hypothèses : ces deux informations suffisent pour ce jeu ; la porte ne change pas d’état pendant la commande ; aucun autre obstacle ni délai n’intervient. Chaque couple état/commande a alors un résultat unique : c’est le sens de **déterministe** dans ce modèle. Des effets différents avec la même commande restent compatibles avec le déterminisme si l’état avant est différent. Comparer les deux premières lignes ne met pas en évidence une part de hasard.

Une même commande ne détermine donc pas à elle seule l’état après. En outre, l’absence de déplacement ne signifie pas toujours un refus devant un obstacle : Nora déjà dans le bureau ne se déplace pas davantage. La preuve élève reste volontairement centrée sur le refus depuis le hall ; ce troisième cas approfondit les limites d’une inférence à partir du seul effet.

### Exemple Python facultatif — reproduire les quatre lignes de la table

Cet exemple appartient à la préparation enseignante, hors des vingt minutes élèves. Il ne demande aucune connaissance de la théorie des agents et ne modifie pas le laboratoire. On peut copier le bloc entier dans un interpréteur Python local. La commande est fournie à la fonction ; celle-ci applique la commande, elle ne la choisit pas.

Les trois paramètres sont des chaînes de caractères : `position` vaut exactement `"hall"` ou `"bureau"` ; `porte` vaut exactement `"fermée"` ou `"ouverte"` ; `commande` vaut uniquement `"AVANCER"`. Le résultat est un couple `(position_apres, porte_apres)` qui décrit l’état après. L’état de la porte est toujours conservé. Une valeur hors de ces listes déclenche `ValueError`, pour signaler une entrée étrangère au modèle au lieu de lui inventer un résultat.

```python
def appliquer_porte(position, porte, commande):
    if position not in ("hall", "bureau"):
        raise ValueError("Position inconnue")
    if porte not in ("fermée", "ouverte"):
        raise ValueError("État de porte inconnu")
    if commande != "AVANCER":
        raise ValueError("Commande inconnue")
    if position == "hall" and porte == "ouverte":
        return "bureau", porte
    return position, porte


# Chaque ligne donne : position avant, porte avant, état après attendu.
cas = [
    ("hall", "fermée", ("hall", "fermée")),
    ("hall", "ouverte", ("bureau", "ouverte")),
    ("bureau", "fermée", ("bureau", "fermée")),
    ("bureau", "ouverte", ("bureau", "ouverte")),
]
for position, porte, attendu in cas:
    resultat = appliquer_porte(position, porte, "AVANCER")
    assert resultat == attendu
    print((position, porte), "AVANCER ->", resultat)
```

Les trois premiers tests de la fonction vérifient le contrat d’entrée. Le test avec `and` exige à la fois le départ dans le hall et une porte ouverte : c’est la seule situation qui change la position. Dans ce cas, le premier `return` renvoie bureau et la porte inchangée. Dans les trois autres cas valides, le dernier `return` conserve les deux informations : refus depuis le hall fermé, ou absence de destination plus loin depuis le bureau.

La liste `cas` reprend les quatre états avant, avec leur état après attendu selon la table. À chaque tour de la boucle, la fonction calcule le résultat ; `assert` vérifie son égalité avec l’attendu et signale un échec si la comparaison est fausse ; `print` affiche l’état avant et le résultat. Les quatre lignes sont des appels indépendants, pas un trajet de Nora : le résultat précédent ne devient pas le départ suivant. Aucune variable cachée ni mémoire entre appels n’est nécessaire.

Les sorties correspondent, dans l’ordre, à `(hall, fermée)`, `(bureau, ouverte)`, `(bureau, fermée)` et `(bureau, ouverte)` comme états après. Le couple retourné est la valeur calculée ; son affichage ne déplace pas un personnage dans l’application. Cette fonction représente exactement T sur les quatre états du modèle ; les erreurs d’entrée sont un contrôle supplémentaire, hors de cette table.

## 5. Erreurs possibles et remédiations

Ces erreurs sont anticipées ; elles ne sont pas présentées comme observées auprès d’une classe.

| Production possible | Analyse à vérifier | Intervention ciblée | Preuve à demander après aide |
|---|---|---|---|
| « Deux commandes, donc deux déplacements. » | Confusion entre demande et réalisation | Faire suivre la position après chaque ligne, en gardant la colonne commande visible | Un cas de passage refusé, sur une autre situation. |
| « Il a décidé de rester en B. » | L’effet est utilisé pour reconstruire la décision | Faire citer le mot écrit dans la colonne commande, puis la règle sur la case C | Une explication conservant droite comme commande et B comme résultat. |
| « La porte s’ouvre quand on avance. » | Import d’une règle familière mais absente du jeu | Faire retrouver la phrase qui exclut l’ouverture automatique | Un nouveau raisonnement sur l’essai à porte fermée, sans suggérer sa réponse. |
| Repères numériques mal recopiés, explication correcte avec A/B | Difficulté de lecture de grille, non nécessairement confusion conceptuelle | Utiliser la correspondance fournie entre lettres et repères | Réponse en noms de cases ou par désignation, puis reprise séparée du repérage. |
| « Puisqu’elle reste au même endroit, aucune commande n’a été choisie. » | Raisonnement inverse non valide | Comparer entrée commandée et position avant/après ; voir l’exercice E4 ci-dessous | Cas inédit après remédiation, avec une explication personnelle. |

Une relance sur le repérage ne doit pas être comptée comme un indice sur le mécanisme. Noter séparément ce que l’apprenant établit seul et ce qui apparaît après intervention.

## 6. Exercice enseignant — sujet

À résoudre avant de consulter le corrigé enseignant. Cet exercice emploie exactement les règles de la porte définies dans le sujet élève et rappelées par la table de la section 4. La seule commande est AVANCER ; l’état de la porte reste constant pendant son application.

Voici quatre lignes de journal proposées. Une ligne n’est pas nécessairement compatible avec ces règles.

| Ligne | Position avant | Porte pendant la commande | Commande choisie | Position après annoncée |
|---|---|---|---|---|
| J1 | hall | fermée | AVANCER | hall |
| J2 | hall | ouverte | AVANCER | bureau |
| J3 | bureau | fermée | AVANCER | bureau |
| J4 | hall | fermée | AVANCER | bureau |

**E1.** Pour chacune des quatre lignes, dire si elle respecte le modèle et justifier. Pour toute ligne incompatible, donner la position après qui serait conforme aux données avant et à la commande annoncées.

**E2.** Réfuter les deux affirmations suivantes avec une ligne compatible et une explication : « AVANCER implique toujours un changement de pièce » ; « rester sur place signifie toujours que la porte a bloqué le passage ».

**E3.** J1 et J2 ont la même position avant et la même commande. Leurs résultats différents contredisent-ils le caractère déterministe de T ? Nommer précisément l’information pertinente qui diffère.

**E4.** Un élève explique J1 par : « Nora est restée dans le hall, donc aucune commande n’a été choisie. » Proposer une relance qui l’amène à comparer les bonnes données sans lui dicter la conclusion. Préciser ce que vous attendrez de son explication après relance. Proposer ensuite une autre situation de la porte pour vérifier qu’il distingue encore commande et résultat ; expliciter ses données et son résultat attendu.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 7. Références reliées à cette unité

Références à consulter pour préparer, pas prérequis à lire avant l’activité. Les sources sont des manuels de synthèse, pas des expériences validant notre unité ; les exemples de piste et de porte sont originaux.

- **David L. Poole et Alan K. Mackworth, 2023**, *Artificial Intelligence: Foundations of Computational Agents*, 3e édition, [§2.1, Agents and Environments](https://artint.info/3e/html/ArtInt3e.Ch2.S1.html). Appuis précis : le passage qui suit l’exemple 2.1 distingue commande d’achat et réalisation ; §2.1.1 décrit le contrôleur. Usage U01 : justifier la distinction commande/effet. Limite : leur exemple économique ne fournit pas les règles de notre jeu.
- **Stuart Russell et Peter Norvig**, *Artificial Intelligence: A Modern Approach*, [extrait public du chapitre 2](https://aima.cs.berkeley.edu/4th-ed/pdfs/newchap02.pdf), §2.1, interaction avec l’environnement. Usage U01 : replacer ultérieurement la décision dans un système qui agit ; le découpage en décision et moteur de notre programme est une convention explicite du modèle pédagogique. Limite : le PDF public est non daté ; son emplacement dans un répertoire « 4th-ed » ne suffit pas à garantir sa correspondance exacte avec la pagination d’une édition. Aucune page de quatrième édition non contrôlée n’est invoquée.

Pour la précision rédactionnelle, le [sujet officiel NSI 25-NSIJ2ME1, 18 juin 2025](https://eduscol.education.gouv.fr/sites/default/files/document/25-nsij2me1v1pdf-112650.pdf) a été examiné, notamment la définition des données et des conventions avant les questions. C’est une référence de présentation, pas une preuve scientifique ou pédagogique pour U01. Aucun de ses exercices, figures ou textes n’est reproduit.

## 8. Préparer l’expérience existante, sans intégration applicative

Avant l’accueil des élèves, ouvrir le dépôt local par `Ouvrir-Agent-Academy.cmd`, puis le laboratoire indépendant à `http://127.0.0.1:8765/laboratoire.html`. Si votre serveur emploie un autre port, conserver celui-ci. Distribuer seulement COURS_ELEVE.md et ACTIVITES_ELEVE.md ; les liens vers les corrigés ne sont pas une barrière de confidentialité dans un dépôt public.

Choisir la politique gloutonne indiquée dans le cours et réinitialiser. Le départ doit être `0,2`, le compteur à 0. Ne pas lancer BFS, le mode automatique, une politique Python ou l’ancienne leçon intégrée. Ces interfaces ne sont pas modifiées et ne constituent pas la nouvelle unité. L’enseignant accompagne le repérage des contrôles nécessaires.

Préparer deux relevés de remplacement, issus des valeurs suivantes : première tentative, position avant `0,2`, commande droite, position après `1,2` ; deuxième tentative, position avant `1,2`, commande droite, mouvement refusé devant un obstacle, position après `1,2`. Les remettre successivement après chaque prédiction si l’outil n’est pas accessible. Dire explicitement qu’il s’agit de relevés fournis. Ne pas les présenter comme une manipulation effectuée par l’élève.

Les vingt minutes incluent la lecture et les réponses du parcours élève, pas l’installation technique ni cette préparation. Prévoir d’en relever les temps réels lors d’un essai futur. Aucun essai humain n’a encore été réalisé pour cette version.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

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
