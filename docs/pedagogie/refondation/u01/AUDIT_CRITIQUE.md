# U01 — Deux audits internes de la version expérimentale

Base : cadrage de refondation `5041bfd8035065479747edd745cf95988559c779`. Périmètre : U01 seulement ; ni ancien cours corrigé, ni interface modifiée, ni nouvelle unité.

## Méthode et indépendance : ce qui a réellement été fait

Deux contrôles distincts sont conduits : **A, compréhension et suffisance des consignes** ; **B, rigueur scientifique et cohérence des mécanismes**. Ils sont réalisés par le même agent rédacteur, à partir de grilles différentes. Ils ne constituent donc pas deux expertises externes indépendantes. Aucune observation humaine, aucun score de qualité et aucune efficacité mesurée ne sont revendiqués.

Ordre du travail : rédaction du cours, des activités élève et du sujet enseignant ; résolution de toutes leurs questions à partir de ces seuls sujets, consignée ci-dessous **avant la création de CORRIGES.md** ; vérification des mécanismes et des ambiguïtés ; rédaction ultérieure du corrigé et confrontation à cette résolution. Cette séparation contrôle la dépendance aux corrigés mais ne rend pas le rédacteur indépendant de sa propre conception. Une relecture externe reste nécessaire.

## A — Résolution à partir des sujets, sans corrigé

Les références C0 à E3 appartiennent au cours, A1 à B1 aux activités, et E1–E4 au sujet enseignant ; les lignes « enseignant » ci-dessous évitent toute confusion d’identifiant.

| Question | Données suffisantes dans le sujet | Résolution obtenue avant corrigé |
|---|---|---|
| C0 | Ordre des cases et ligne de contenu | B est à droite de A ; C contient un mur. |
| P1 | Départ A ; arrivée G à droite ; B libre ; règle droite | Commande droite ; position B après application. |
| E1 | Bouton pas à pas et correspondance A/0,2, B/1,2 | Ligne 1 : A, droite, B. C’est une prévision du modèle à confronter au journal réel ou au relevé explicitement fourni. |
| P2 | Pas de réinitialisation ; position B après le premier pas ; C mur | Encore droite ; position conservée en B. |
| E2 | Même règle et contrôle du journal/position | Ligne 2 : B, droite, B ; refus devant l’obstacle. |
| E3 | Deux lignes avant/après | Deux commandes, un seul changement de case. Le commentaire sur l’écart dépend de la prédiction réellement écrite par l’élève ; aucun écart n’est obligatoire. |
| A1, essai 1 | Départ D ; droite ; E libre | Case demandée E, case après E ; mouvement autorisé. |
| A1, essai 2 | Départ B ; droite ; C mur | Case demandée C, case après B ; mouvement refusé. Les essais sont indépendants. |
| A2 | Commande droite donnée dans l’essai 2 | Affirmation incompatible : droite a bien été choisie, mais le moteur a refusé C. |
| T1, essai 1 | Nora dans le hall ; porte fermée et fixe ; AVANCER | Après : hall ; aucun déplacement. La porte ne s’ouvre pas en recevant la commande. |
| T1, essai 2 | Nouveau départ dans le hall ; porte ouverte ; AVANCER | Après : bureau ; déplacement réalisé. Aucun délai ni obstacle supplémentaire. |
| T2 | Commande identique et état de porte différent | Pas de changement de commande. La règle autorise le passage seulement lorsque la porte est ouverte. |
| B1 | Essai 1 du transfert entièrement défini | AVANCER ne suffit pas à conclure au changement de pièce : hall avant et après, porte fermée. |
| Enseignant E1 | Quatre lignes et règles complètes | J1, J2, J3 compatibles ; J4 incompatible, résultat conforme hall. |
| Enseignant E2, affirmation 1 | J1 compatible | J1 réfute « toujours un changement de pièce » ; J3 serait aussi recevable. |
| Enseignant E2, affirmation 2 | J3 compatible et règle depuis le bureau | J3 réfute « toujours bloqué par la porte » : Nora est déjà au bureau, sans destination plus loin. |
| Enseignant E3 | État complet = position et porte | Pas de contradiction au déterminisme : les positions initiales coïncident mais les états de porte diffèrent. |
| Enseignant E4 | J1 indique commande et positions ; règles de transfert fournies | Relance possible : faire identifier les colonnes qui établissent commande et déplacement, sans donner la conclusion. Attendu : AVANCER a été choisi mais refusé depuis le hall. Situation de contrôle possible : Nora déjà au bureau, porte ouverte, AVANCER ; elle reste au bureau malgré la commande. Plusieurs relances et situations sont recevables si entièrement spécifiées et correctement expliquées. |

L’exemple guidé du cours donne un résultat après l’expérience : il enseigne la relation et n’est pas présenté comme une épreuve sans aide. La tâche de transfert change le contexte, mais conserve la même relation entre demande, condition de passage et effet ; elle n’exige ni action d’ouverture ni connaissance des portes réelles.

## A — Contrôle de compréhension des consignes

| Point vérifié | Constat de lecture | Décision / réserve |
|---|---|---|
| Documents effectivement remis | Le cours exige explicitement le cours et les activités ; aucun renvoi obligatoire à S01–S03 | Les règles de la piste sont répétées dans l’entraînement, celles de la porte sont intégrales dans le transfert. |
| Repérage | Lettres, contenu et repères du journal sont mis en correspondance ; aucune opération sur coordonnées demandée | Vérifier avec des lecteurs réels si la double désignation ajoute trop de charge. |
| Vocabulaire | Commande et moteur sont expliqués ; le nom « Gloutonne » sert uniquement à identifier une option | La lecture du laboratoire nécessite un accompagnement initial, pas une connaissance théorique du terme. |
| Ordre d’exécution | Réinitialiser avant le premier pas, pas avant le second ; ni auto ni changement de règle | Les essais d’entraînement et de porte annoncent au contraire leurs réinitialisations indépendantes. |
| Données du transfert | Position initiale, porte ouverte/fermée, commande donnée, ouverture automatique exclue, effets et délai définis | Aucune clé, vitesse ou stratégie cachée n’intervient. |
| Attendus des questions | Tables à compléter et justifications ciblées ; réponses personnelles admises pour l’écart prédiction/observation | Ne pas exiger une prédiction fausse ou la récitation exacte du corrigé. |
| Énoncés ouverts enseignants | E4 appelle une relance et une situation conçues par l’enseignant | Pas de réponse unique ; la grille doit juger données, pertinence et raisonnement. |

## B — Audit de rigueur scientifique et des mécanismes

1. **Séparation des responsabilités.** Le choix de droite reste distinct de la vérification de la case suivante. Le sujet n’attribue pas au contrôleur la décision de « rester » après un refus. Les deux opérations décrivent notre programme ; elles ne sont pas posées comme une décomposition matérielle universelle.
2. **État avant pertinent.** Même carte et même commande ne signifient pas même état : A avant le premier pas, B avant le second. La table de la porte inclut sa fermeture ou son ouverture dans l’état. Les effets différents n’introduisent pas de hasard.
3. **Modèle complet de la porte.** Quatre états possibles, une commande, quatre résultats explicités ; porte inchangée, absence de clé, autre obstacle ou délai. Le cas Nora déjà au bureau reste distinct d’un refus devant porte fermée.
4. **Portée des inférences.** Une commande de déplacement peut être refusée. L’absence de déplacement ne prouve ni absence de commande ni obstacle dans tous les cas. Un journal de deux commandes ne prouve pas une règle constante sur tous les cas.
5. **Formalisme facultatif.** S, C, s, c, T, le couple et le produit sont expliqués avant usage. La table définit T ; la formule seule n’est pas présentée comme une preuve. Aucune notation n’est exigée des élèves.
6. **Transfert.** Il s’agit d’un raisonnement sur règles fournies, pas d’une nouvelle fonctionnalité graphique. Les deux essais ont la même commande et des états différents explicitement fixés. Le résultat n’exige pas une connaissance extérieure au dossier.
7. **Références.** Les passages auteur/institution consultés appuient des notions ou une précision de rédaction ; ils ne valident pas l’efficacité de l’unité. Aucune citation longue, figure ou activité de ces sources n’est reproduite.

## Ambiguïtés détectées et état de traitement

| Risque détecté lors de la conception/relecture | Traitement dans le sujet | État |
|---|---|---|
| « AVANCER » ouvrirait une porte automatique | Porte fixée avant l’essai, ouverture automatique explicitement exclue | Traité dans l’énoncé ; compréhension à éprouver. |
| Le second essai partirait de la position du premier | Distinction explicite entre séquence Microduck et essais indépendants A/T | Traité. |
| Nora arriverait seulement plus tard | Mouvement autorisé entièrement réalisé quand on lit la position après | Traité. |
| Le modèle ne dirait rien d’une commande depuis le bureau | Cas déjà au bureau défini dans le sujet et le formalisme | Traité ; non ajouté aux questions élève obligatoires. |
| Une réponse à E4 serait réputée seule correcte | Demande de données et d’attendus ; résolution annonce plusieurs possibilités | À conserver explicitement dans corrigé et grille. |
| Des relevés de remplacement seraient présentés comme une manipulation réelle | Modalité déclarée dans le cours et préparation enseignante | Traité, mais modalités de l’essai à tracer. |

## Confrontation aux corrigés et vérifications réalisées

Après sa rédaction, CORRIGES.md a été comparé question par question au tableau de résolution préalable : mêmes positions, mêmes commandes, mêmes refus et mêmes limites pour C0, P1–P2, E1–E3, A1–A2, T1–T2, B1 et l’exercice enseignant E1–E4. Le corrigé d’E4 conserve explicitement le caractère non unique des relances et situations proposées. Aucun désaccord de résultat ne reste identifié par ces lectures.

Le cas Nora déjà au bureau est défini dans le sujet, pas ajouté dans le corrigé pour fabriquer un contre-exemple. Le corrigé ne demande pas une prédiction initiale fausse. Le transfert ne nécessite pas une ouverture de porte que l’élève n’aurait pas apprise.

Contrôle ciblé du laboratoire inchangé : `npx playwright test tests/lab.spec.mjs -g "politique gloutonne" --workers=1` ; **un scénario réussi en 3,7 s**, incluant le blocage après deux pas gloutons et un contrôle BFS existant. Le contrôle BFS est une vérification technique héritée, pas une activité ajoutée à U01. Les noms de cases et la correspondance avec les repères numériques ont aussi été confrontés à la carte et à la règle du laboratoire. Aucune campagne complète de non-régression n’est revendiquée pour cette livraison documentaire.

Les sources de la section Références ont été ouvertes : Poole–Mackworth §2.1, extrait Russell–Norvig chapitre 2 et sujet officiel NSI 25-NSIJ2ME1. Elles appuient les distinctions ou la précision rédactionnelle indiquées, pas les résultats d’un essai pédagogique.

Contrôle documentaire : sept fichiers U01, douze liens locaux résolus, blocs de code/diagramme fermés et plages du tableau de déroulement continues de 0 à 20 minutes. Le contrôle du budget vérifie une addition, pas un temps d’apprentissage. Le périmètre Git se limite au nouveau sous-dossier U01 ; les cinq documents de refondation, les anciennes séances, les TP, le moteur et le Worker sont conservés sans modification.

## Défauts ou limites non résolus par ce contrôle interne

| Réserve ouverte | Conséquence et vérification nécessaire |
|---|---|
| Absence d’expertise indépendante externe | Les deux audits sont des lectures distinctes du même rédacteur. Une autre personne doit relire les sujets seuls, les résoudre et contester les corrigés si nécessaire. |
| Durée de vingt minutes non mesurée | Le volume de lecture, l’écriture des justifications et l’accès au journal peuvent dépasser le budget. Mesurer les phases ; au-delà de vingt-cinq minutes récurrentes, revoir le découpage plutôt que supprimer l’explication ou le transfert. |
| Accès accompagné à un laboratoire contenant d’autres contrôles | Les interfaces BFS/Python/auto restent présentes. Observer leur éventuel effet de distraction ; ne pas prétendre disposer d’une interface U01 dédiée. |
| Double désignation lettres/repères du laboratoire | La table rend les données explicites, mais son coût de lecture n’est pas encore connu. Accepter les lettres pour éviter de confondre lecture de coordonnées et mécanisme. |
| Variante de transfert familière à certains lecteurs | Les règles excluent les hypothèses importées d’une porte réelle ; vérifier néanmoins si elles sont comprises et mobilisées sans aide. Aucune équivalence de difficulté avec la piste n’est démontrée. |
| Bilan utilisant le même transfert, et non une troisième situation | Il vérifie la formulation individuelle du mécanisme ; ce n’est pas une nouvelle preuve indépendante de généralisation ni de rétention différée. |
| Pas de banque de remédiations étalonnée | La grille décrit des interventions et les critères d’une nouvelle preuve ; elle ne prétend pas fournir des variantes déjà testées et équivalentes. |
| Lisibilité matérielle non essayée | Impression, projection, lecture d’écran et usage avec les apprenants restent à observer en conditions réelles. |

Ces réserves sont maintenues dans le dossier ; aucune note flatteuse ni qualification « validé » ne leur est substituée. Aucune ambiguïté mécanistique non traitée n’a été identifiée dans cette lecture, ce qui n’exclut pas une objection nouvelle en relecture. Arrêt après U01 pour relecture humaine complète, sans intégration applicative.
