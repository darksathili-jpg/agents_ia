# U01 — Deux audits internes de la version expérimentale

Version courante : **U01.1**, consolidée depuis `6eed4029726681d116e831d06d4eb3263a863757`, sur `docs/u01-1-consolidation`. Les contrôles U01 ci-dessous sont conservés comme historique ; la présente consolidation ne traite que les trois réserves autorisées. Périmètre : U01 seulement ; ni ancien TP corrigé, ni interface modifiée, ni nouvelle unité.

## U01.1 — Résolution des ajouts à partir des sujets

Cette résolution est consignée avant l’ajout du corrigé I1–I2. Le troisième scénario donne deux positions possibles du curseur, début et fin, et une commande DROITE déjà choisie. La règle conduit de début à fin et laisse fin inchangée ; les essais sont indépendants. **I1 :** essai 1, fin après, aucun déplacement ; essai 2, fin après, déplacement réalisé depuis début. **I2 :** l’affirmation est incompatible avec les données : DROITE a été choisie, mais aucun emplacement plus à droite n’est autorisé depuis fin. Ce résultat n’exige ni connaissance d’un éditeur réel ni règle de retour automatique, explicitement exclue.

L’exemple Python enseignant est confronté à la table de transition existante : hall/fermée reste hall/fermée ; hall/ouverte devient bureau/ouverte ; bureau/fermée et bureau/ouverte restent inchangés. La commande reste AVANCER. Les appels sont indépendants ; les valeurs invalides relèvent d’erreurs de contrat, pas d’états supplémentaires.

## U01.1 — Résultats des contrôles de consolidation

| Réserve demandée | Correction documentaire réalisée | Contrôle et limite |
|---|---|---|
| Troisième scénario individuel | I1–I2 : curseur dans un texte fixe X, positions début/fin, commande DROITE et règles intégrales | Résolution depuis le sujet avant ajout du corrigé, puis comparaison : fin/non et fin/oui ; I2 distingue commande présente et mouvement impossible depuis fin. Le corrigé et V1–V3 concordent. La réussite réelle d’apprenants n’est pas mesurée. |
| Essentiel et prolongements | A1, Nora et I1–I2 restent essentiels ; A2/B1 deviennent des prolongements facultatifs hors budget | Prédictions P1/P2, expérience et explication conservées. Plages essentielles continues de 0 à 20 min ; le budget réduit de l’entraînement et les trois minutes de vérification finale doivent être éprouvés, pas considérés acquis. |
| Python enseignant | Code court appliquant AVANCER aux quatre états, paramètres et retours définis, cas affichés et vérifiés | Bloc extrait du document et exécuté sous CPython : quatre résultats conformes à la table, quatre assertions réussies, quatre lignes affichées ; trois entrées invalides distinctes déclenchent ValueError comme annoncé. Aucun changement du laboratoire ou de Pyodide ; pas de test de ce code dans Pyodide revendiqué. |

Les deux ajouts questionnés, I1 et I2, n’exigent aucune donnée du corrigé : les positions et règles utiles figurent intégralement dans le sujet. La variante numérique n’est pas un test de connaissance d’un logiciel particulier. Deux positions finales identiques ne prouvent pas deux déplacements : comparer chaque avant/après évite ce raccourci. Les anciens exercices et les règles de la porte sont conservés ; les contrôles historiques ci-dessous ne sont pas présentés comme de nouveaux essais U01.1.

La réserve sur l’absence de troisième situation est donc traitée dans les documents. Le réalisme de la durée, la lisibilité, la compréhension du nouveau scénario et le caractère autonome des réponses restent à expérimenter. Les prolongements ne doivent pas être réintroduits implicitement dans les vingt minutes. Le Python reste une préparation enseignante séparée.

## Historique U01 — Méthode et indépendance : ce qui a réellement été fait

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
| Efficacité du troisième scénario non mesurée | U01.1 ajoute I1–I2, distinct de la piste et de la porte. L’énoncé fournit ses propres règles ; sa difficulté réelle et la compréhension sans aide restent à observer. |
| Pas de banque de remédiations étalonnée | La grille décrit des interventions et les critères d’une nouvelle preuve ; elle ne prétend pas fournir des variantes déjà testées et équivalentes. |
| Lisibilité matérielle non essayée | Impression, projection, lecture d’écran et usage avec les apprenants restent à observer en conditions réelles. |

Ces réserves sont maintenues dans le dossier ; aucune note flatteuse ni qualification « validé » ne leur est substituée. Aucune ambiguïté mécanistique non traitée n’a été identifiée dans cette lecture, ce qui n’exclut pas une objection nouvelle en relecture. Arrêt après U01 pour relecture humaine complète, sans intégration applicative.
