# U01 — Parcours enseignant

Vous connaissez l’informatique, mais aucune connaissance préalable de la théorie des agents n’est supposée. Cette préparation est distincte des vingt minutes élève. Elle ne reprend pas les anciennes séances comme des cours validés.

## 1. Partir du phénomène

Dans le [cours élève](COURS_ELEVE.md), la première commande droite conduit de A à B ; la seconde demande C, occupée par un mur, et la position reste B. La commande est choisie deux fois. Le mouvement n’est accompli qu’une fois. Ce résultat est entièrement déterminé par la règle de déplacement et les positions successives.

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

Le [sujet de transfert](ACTIVITES_ELEVE.md) fournit la position initiale, la commande, les deux états possibles de la porte et la règle qui relie ces données au résultat. Une porte fermée empêche le passage ; AVANCER ne l’ouvre pas. Chaque essai repart du hall. La destination et le changement de vocabulaire ne demandent aucune connaissance sur les portes automatiques réelles.

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

À résoudre avant de consulter [le corrigé enseignant](CORRIGES.md). Cet exercice emploie exactement les règles de la porte définies dans le sujet élève et rappelées par la table de la section 4. La seule commande est AVANCER ; l’état de la porte reste constant pendant son application.

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
