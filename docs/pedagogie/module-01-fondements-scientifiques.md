# Module 01 — Fondements scientifiques des agents intelligents

**Statut : conception proposée, à valider avant implémentation.** Formation en français, niveau universitaire progressif, durée centrale de **10 heures**. L’accueil V2 et le moteur existant restent inchangés. Ce document décrit des activités à préparer ; il ne les annonce pas comme disponibles dans l’application.

## 1. Public, prérequis et acquis visés

Public principal du parcours approfondi : enseignants de NSI et étudiants de début de licence, BUT, CPGE ou formation équivalente. Une entrée accompagnée s’adresse aux élèves de Première et Terminale NSI. Le niveau universitaire progressif porte la rigueur du parcours enseignant ; il ne doit pas devenir un prérequis implicite pour les lycéens. Aucun prérequis sur les LLM ou l’apprentissage automatique.

Prérequis Python : fonctions et retours, conditions, boucles, tuples, listes, ensembles et lecture d’une exception. Savoir repérer des coordonnées dans une grille et lire un graphe simple. Un diagnostic initial de 15 minutes vérifie ces capacités ; les difficultés déclenchent un soutien ciblé, sans confondre erreur de syntaxe et incompréhension scientifique. Calcul matriciel, probabilités avancées et API payante sont exclus des prérequis.

À la fin, l’étudiant doit pouvoir :

1. **Définir et délimiter** un agent par ses observations, actions, environnement et critères de performance.
2. **Modéliser** une tâche en séparant état du monde, observation accessible et état interne du contrôleur.
3. **Expliquer et prédire** une politique sur une trace, y compris un déplacement refusé.
4. **Implémenter** en Python une politique réactive et une recherche de chemin simple sous le contrat fourni.
5. **Comparer** une décision locale et une délibération en identifiant leurs hypothèses et coûts.
6. **Évaluer** des stratégies sur plusieurs cas, justifier leurs échecs et borner les conclusions.
7. **Transférer** le vocabulaire vers un système conversationnel ou un agent LLM sans assimiler génération de texte et garantie d’action correcte.

Les objectifs 1 à 7 sont évalués par des productions identifiées dans les TP et l’épreuve finale ; une animation réussie ne suffit pas à les valider.

### Deux niveaux complémentaires pour chaque notion

Conformément à `AGENTS.md`, chaque support devra proposer une entrée NSI et un approfondissement enseignant, sans les fondre dans un texte de difficulté uniforme. Le parcours de 10 h ci-dessous est la référence approfondie ; sa transposition NSI se prépare à partir des acquis réels de la classe. En Première, on fournit les structures de données de BFS et on n’exige pas une preuve de complexité ; en Terminale, graphes et parcours peuvent être mobilisés lorsqu’ils ont été enseignés. Le diagnostic permet d’ajuster ces choix.

| Notion | Entrée NSI : activité et preuve | Approfondissement enseignant : tâche et preuve |
|---|---|---|
| Définition d’un agent | Annoter capteur, action et environnement sur deux systèmes ; justifier un cas ambigu | Confronter les cadres généraux et LLM ; justifier la frontière du système et discuter l’autonomie sans définition marketing. |
| Agent, automate, chatbot, LLM | Classer sans catégories exclusives ; donner un système appartenant à deux colonnes | Construire un contrôleur à états en Python autonome et montrer son interprétation comme agent situé. |
| État, observation, action | Compléter une trace de grille et prédire une collision | Formaliser `O`, `T`, historique et mémoire ; produire deux historiques indiscernables pour une politique sans mémoire. |
| Politique | Compléter une fonction de décision et tester ses retours | Comparer politique déterministe et distribution d’actions ; séparer contrat, représentation et objectif de performance. |
| Réaction et délibération | Observer le témoin glouton puis compléter BFS avec aide | Justifier complétude, optimalité conditionnelle et complexité de l’algorithme conventionnel ; analyser les surcoûts du programme réel. |
| Boucle et contrôle | Distinguer choix, exécution et nouvel état sur trois pas | Décrire responsabilités du contrôleur, de l’environnement, du Worker et de l’opérateur ; discuter latence et interruption. |
| Erreurs et évaluation | Fournir un contre-exemple et corriger une erreur locale | Définir un protocole reproductible, des métriques valides sur les échecs et un domaine de validité des conclusions. |
| Transfert LLM | Analyser un dossier d’interaction sans prétendre exécuter un LLM | Lire la méthode et les évaluations de ReAct, distinguer preuve expérimentale et généralisation ; proposer une transposition de 30 minutes en classe. |

Pour chaque support : une définition précise, un exemple, une manipulation, du Python lorsque pertinent, un exercice avec retour et une limite. Le volet enseignant ajoute formalisation, hypothèses, lecture scientifique et justification de la transposition. Les exercices de mémoire s’exécutent en un seul script console, sans modifier le contrat du laboratoire.

## 2. Définitions et conventions scientifiques

### Agent et rationalité

Dans le cadre classique, un agent relie des perceptions à des actions sur un environnement. Son comportement peut dépendre de la séquence des perceptions ; le programme est l’implémentation de cette fonction. La rationalité se juge relativement aux informations disponibles et à un critère de performance, pas à une omniscience supposée. L’objectif est ici d’apprendre à choisir les frontières de ce modèle et à le mettre à l’épreuve. Il ne s’agit ni d’attribuer une conscience au robot ni de réserver le terme agent aux logiciels apprenants. [R1]

Les formulations varient selon les communautés. Une définition plus exigeante peut insister sur autonomie, réactivité ou initiative. Dans ce module, « agent intelligent » désigne un objet d’étude et une ambition de comportement approprié, pas un certificat de compétence générale. L’étudiant doit annoncer la définition qu’il utilise.

### Des notions qui se recouvrent

| Notion | Ce que le terme décrit | Exemple étudié | Confusion à éviter |
|---|---|---|---|
| Agent | Relation entre observations, choix d’actions et environnement | Robot de grille couplé à une politique | « Agent » ne signifie pas nécessairement LLM, autonomie totale ou apprentissage. |
| Automate | Modèle de calcul ou contrôleur à états et transitions | Porte automatique : fermé, ouverture, ouvert | Un automate peut implémenter un agent ; les catégories ne s’excluent pas. |
| Chatbot | Modalité d’interaction conversationnelle | Répondeur à règles ou interface de dialogue | Produire une réponse ne prouve ni planification ni action externe ; selon la frontière choisie, dialoguer constitue déjà une interaction agent-environnement. |
| Agent fondé sur un LLM | Système dans lequel un modèle de langage contribue au choix des prochaines actions | Proposition d’un appel d’outil, exécution contrôlée, retour du résultat | Le LLM seul ne constitue pas toute l’architecture ; le contrôle peut être partagé avec du code déterministe et un humain. |

Cette grille est une convention d’analyse du cours. Elle ne constitue pas une partition universelle des systèmes. Exemple de transfert original : comparer un thermostat à deux états, un assistant qui répond à une question et un programme qui consulte un agenda. Pour chacun, demander : « Qu’observe-t-il ? Que peut-il changer ? Qui fixe son objectif ? Qui autorise l’action ? »

Pour l’état interne et les automates de contrôle, la distinction entre environnement, percepts et mémoire du contrôleur est établie dans [R2]. Pour les usages LLM, [R5] propose une entrée pédagogique française ; son vocabulaire spécialisé ne remplace pas la définition générale.

## 3. Modèle de travail et boucle d’interaction

On adopte la notation du module, en temps discret :

- `s_t ∈ S` : état de l’environnement ;
- `o_t = O(s_t)` : observation, éventuellement incomplète ;
- `h_t = (o_0, a_0, o_1, …, a_(t−1), o_t)` : historique accessible en principe ;
- `a_t = π(h_t)` : politique déterministe ; une politique aléatoire s’écrit `π(a | h_t)` ;
- `m_t` : mémoire effectivement conservée par le programme, qui peut résumer cet historique ;
- `s_(t+1) = T(s_t, a_t)` : transition déterministe dans nos premiers exercices.

Il n’est pas nécessaire de stocker tout `h_t`. Une politique peut se limiter à `o_t` ; une autre utilise `(m_t, o_t)`. En environnement incertain, `T` et `O` doivent pouvoir représenter des distributions ; cette extension est discutée sans calcul probabiliste approfondi. Ces symboles sont une formalisation de travail du cours, à distinguer des noms de variables employés dans les références.

```text
environnement s_t → observation o_t → politique (+ mémoire) → action proposée a_t
       ↑                                                          │
       └──── nouvel état ← vérification et application de l’action ┘
```

L’action proposée et son effet doivent être distingués : « droite » n’implique pas que le robot s’est déplacé. Une trace demandée dans le TP contient au minimum position avant, observation utilisée, action choisie, résultat, position après et condition d’arrêt.

### Instanciation exacte dans le laboratoire disponible

Grille 7 × 5 ; `x` augmente vers la droite, `y` vers le bas ; départ `(0,2)`, cible `(6,2)`. Obstacles : `(2,1), (2,2), (2,3), (4,0), (4,1), (4,3), (4,4)`. Environnement discret, déterministe, statique pendant l’épisode, connu, mono-agent et séquentiel. Dans cette tâche, position, cible et carte suffisent pour choisir les déplacements ; cette observation complète ne représente pas une caméra réelle.

Contrat **actuellement disponible** : `decider(position, objectif, obstacles)` retourne `droite`, `gauche`, `haut`, `bas` ou `arrêt`. Le moteur accepte aussi `None` comme absence d’action. Une collision est refusée et interrompt l’épisode avec l’état « Bloqué ». `arrêt` avant la cible ne signifie pas réussite. Le journal compte les tentatives d’action : on distingue donc tentatives et déplacements acceptés dans une analyse.

Le code du contrôleur Python est réévalué dans un espace de noms frais à chaque décision ; une variable globale Python ne fournit pas une mémoire persistante entre les pas. Le BFS fourni recalcule une recherche depuis la position courante, il n’exécute pas un plan stocké d’un pas au suivant. Ces propriétés doivent être enseignées explicitement ; aucune modification du Worker n’est nécessaire pour ce module.

## 4. Réactif, délibératif et hybride

Une architecture réactive relie rapidement une situation perçue à une action ; une architecture délibérative mobilise une représentation et recherche des conséquences possibles avant de choisir. On les compare par leurs accès à l’information, leur horizon et leur coût, plutôt que par une opposition « simple contre intelligent ». Une hiérarchie peut combiner contrôle rapide et planification à plus long terme. [R3]

Dans notre démonstration, la règle « avancer horizontalement vers la cible » sert de politique locale ; BFS sert de mécanisme délibératif sur un graphe connu. Utiliser une carte complète ne rend pas cette règle locale aveugle au sens informatique : elle reçoit la carte, mais n’en exploite pas les contraintes. Chercher un chemin n’est pas apprendre une politique.

BFS explore par niveaux. Dans un graphe fini avec gestion des sommets déjà visités, il trouve un chemin s’il en existe ; il minimise le nombre d’arêtes lorsque les coûts sont uniformes. Cette garantie ne porte pas sur une consommation d’énergie variable, ni sur un monde qui change après le calcul. L’ordre des voisins peut changer le trajet choisi sans changer sa longueur optimale. [R4]

Pour l’analyse de complexité, on étudie le BFS conventionnel avec file efficace et prédécesseurs : temps `O(|V|+|E|)`, mémoire `O(|V|)` sur le graphe exploré. Ne pas attribuer automatiquement ces coûts d’implémentation au code actuel qui copie des chemins, ni au `shift()` d’une liste JavaScript. Le TP ne vise pas à optimiser ou remplacer le moteur existant.

## 5. Ce qui est établi, ce qui est simplifié

| Proposition | Statut dans le cours | Limite ou prolongement à expliquer |
|---|---|---|
| Un agent est étudié par son couplage perceptions/actions | Cadre classique établi [R1, R2] | Les frontières du système se choisissent ; toute interface conversationnelle n’est pas une nouvelle classe disjointe. |
| L’observation ne se confond pas avec l’état du monde | Distinction établie [R2] | Nous commençons avec une carte exacte et complète. |
| Trois boîtes « observation → décision → action » | Simplification didactique | Les systèmes réels peuvent avoir latence, concurrence, mémoire et contrôle humain. |
| Coûts unitaires et murs immobiles | Hypothèses des exercices | La validité des conclusions change si les déplacements ont des coûts différents ou si la carte évolue. |
| Politique gloutonne horizontale = témoin local | Choix pédagogique original | Ce n’est pas une implémentation générale de la recherche gloutonne best-first. |
| Obstacle rencontré = épisode interrompu | Convention du laboratoire | Un robot réel peut rester sur place, réessayer ou replanifier ; aucune règle universelle n’est inférée. |
| Le BFS illustre la délibération | Exemple borné [R4] | Une recherche dans une carte connue ne résume pas toute la planification. |
| Microduck « voit », « veut » ou « réfléchit » | Métaphores d’accueil | Dans les explications scientifiques : données d’entrée, objectif fixé et calcul effectué. |
| Une trace explique un choix | Valable pour le code instrumenté de nos TP | Une justification en langage naturel n’est pas nécessairement une preuve fidèle du calcul interne d’un LLM. |

## 6. Progression centrale : 10 heures, pauses non comprises

Chaque séquence suit **comprendre → expérimenter → programmer → tester → transférer** ; selon le temps disponible, les phases peuvent être plus courtes, mais aucune validation n’est seulement déclarative.

| Séquence | Durée | Objectifs observables | TP / production et vérification |
|---|---:|---|---|
| S1 — Qu’appelle-t-on agent ? | 1 h | Délimiter quatre systèmes et justifier les recouvrements de catégories | Diagnostic 15 min ; comparaison argumentée agent/automate/chatbot/LLM ; fiche de quatre cas, corrigée collectivement. |
| S2 — Modéliser une tâche | 1 h 15 | Décrire état, observation, action et performance sans les confondre | Fiche de tâche du robot ; prédiction des deux premières tentatives ; trace réelle confrontée à la prédiction. |
| S3 — Programmer une réaction | 1 h 30 | Écrire une fonction conforme et diagnostiquer une collision | TP1 : politique locale, tests de contrat, contre-exemple du mur ; version commentée et trace. |
| S4 — Chercher avant d’agir | 1 h 45 | Construire BFS, expliquer file et visites, borner une garantie | TP2 : compléter BFS par étapes, vérifier un chemin de longueur 10 et expliquer pourquoi il est minimal dans cette carte. |
| S5 — Tester et comparer | 1 h 30 | Concevoir des cas discriminants et séparer échec de stratégie et bug | TP3 : plusieurs situations en Python, tableau de mesures, cas sans solution et limite d’observation/mémoire. |
| S6 — Transférer et prendre du recul | 1 h | Réutiliser le modèle pour un agent LLM et identifier des garde-fous | TP4 court : contrat d’action JSON décrit sur papier, résultat d’outil fictif explicitement fourni comme donnée d’étude ; aucune API ni agent LLM exécutable annoncé. |
| S7 — Évaluation finale individuelle | 2 h | Mobiliser modélisation, code, preuves et analyse critique | Sujet décrit en section 9, avec code exécuté dans le navigateur et note d’analyse. |
| **Total** | **10 h** | | |

Répartition indicative de chaque séance : 20–30 % d’explicitation guidée, 50–60 % d’enquête et de programmation, reste en confrontation des preuves et transfert. Le rythme est ajusté à partir des productions, pas de la seule vitesse de clic.

Variante **8 h** : fusionner une partie des études de cas de S1/S2, fournir le squelette et la structure de file de BFS, réduire le nombre de restitutions ; conserver le cas sans solution, les distinctions scientifiques et les 2 h d’évaluation. Variante **12 h** : ajouter 1 h de remise à niveau Python et 1 h d’étude de mémoire/observation partielle dans un script console autonome. Aucune variante ne suppose une nouvelle interface.

## 7. Expériences Python progressives : cahier de préparation

### TP0 — Prédire puis observer (S2)

**Disponible dans le laboratoire actuel.** À partir du départ, prédire deux actions gloutonnes : la première mène en `(1,2)` ; la deuxième tente `(2,2)`, occupée, et le robot reste en `(1,2)` avec l’état « Bloqué ». Changer de politique, relancer, commenter trois lignes de journal.

Livrable : tableau avant/après et explication du déplacement refusé. Critère : au moins quatre éléments correctement distingués — observation, action proposée, effet, arrêt — sans attribuer le refus à une décision du LLM.

### TP1 — Écrire une politique réactive (S3)

**Éditeur et exécution disponibles ; énoncé, aides et correction à produire.** Partir d’une fonction qui renvoie toujours `arrêt`, puis écrire la règle horizontale avec test préalable de cible. Tester le type du retour et l’appartenance à l’alphabet d’actions. Reproduire volontairement la collision avant toute tentative de réparation.

Exercices : E1, écrire deux assertions sur des appels directs ; E2, expliquer pourquoi « se rapprocher de la cible à chaque pas » n’assure pas de l’atteindre ; E3, ajouter une vérification locale des obstacles et chercher un cas où la stratégie reste insuffisante. Critères : fonction conforme, exception lisible si erreur de code, au moins un contre-exemple expliqué. Aucun succès universel n’est promis à la stratégie réparée.

### TP2 — Délibérer avec BFS (S4)

**Exemple BFS actuellement disponible ; version à trous et corrigé à produire.** Décomposer en génération des voisins, file FIFO, ensemble visité, condition d’arrivée et restitution de la première action. Demander pourquoi la file ne doit pas devenir une pile et pourquoi `vus` est nécessaire.

E4 : compléter deux parties du code et les tester directement dans la console. E5 : faire piloter la grille à la fonction. E6 : reconstruire la longueur du trajet et argumenter la minimalité avec une exploration par niveaux, pas avec une ressemblance visuelle. Critères : cible `(6,2)` atteinte en **10 déplacements acceptés**, aucune action refusée, explication de plusieurs chemins possibles. Des sorties de débogage ne sont pas exigées pour que le code fonctionne.

Le corrigé doit traiter départ déjà à la cible et cible inaccessible. Pas de mémorisation globale entre deux décisions : l’explication doit correspondre au contrat réel du Worker.

### TP3 — Évaluer au-delà de la carte connue (S5)

**À préparer : un énoncé et un petit banc d’essai Python à coller dans l’éditeur existant**, exécuté en un seul lancement. Il modélise ses propres cas en mémoire Python ; il ne modifie pas la carte visuelle, ne prétend pas débloquer un éditeur de cartes et ne dépend pas d’un état persistant entre décisions du laboratoire.

Jeu de cas proposé, grille 7 × 5, déplacements orthogonaux :

| Cas | Départ → cible | Obstacles | Résultat de référence à vérifier dans le futur corrigé |
|---|---|---|---|
| C0 | `(0,2)` → `(6,2)` | Aucun | 6 déplacements minimaux. |
| C1 | `(0,2)` → `(6,2)` | Carte du laboratoire, section 3 | 10 déplacements minimaux ; gloutonne bloquée à sa deuxième tentative. |
| C2 | `(0,2)` → `(0,2)` | Aucun | Réussite sans déplacement ; condition terminale testée avant de solliciter la politique. |
| C3 | `(0,2)` → `(6,2)` | `(5,2), (6,1), (6,3)` | Cible isolée ; aucune solution, signalement explicite. |
| C4 | `(0,0)` → `(6,4)` | Aucun | 10 déplacements minimaux ; attention aux bords. |
| C5 | `(0,2)` → `(2,2)` | `(1,2)` | 4 déplacements minimaux ; deux détours de même longueur. |

Ces cas sont des **spécifications proposées**, pas un jeu déjà intégré au produit. Le prochain jalon doit en exécuter et vérifier les oracles indépendamment du code étudiant.

Mesures : réussite, cause d’arrêt, tentatives, déplacements acceptés, longueur sur les réussites, nombre d’états explorés si instrumenté, temps de calcul à titre indicatif. Le taux de réussite est `réussites / cas exécutés`, avec effectif affiché. Le surcoût de trajet `L−L*` n’est défini que si une solution existe et que l’agent réussit ; ne pas transformer les échecs en trajets de longueur nulle. Répéter les mesures temporelles, distinguer téléchargement initial et temps de décision, ne pas conclure qu’une politique est supérieure à partir d’un seul parcours.

E7 : fournir un tableau de résultats et deux explications d’échec de nature différente. E8 : produire un cas de test qui invalide une affirmation trop générale. Critères : résultats reproductibles, désaccords discutés et conclusions limitées à l’environnement étudié.

**Limite de mémoire, sans refonte** : dans un script Python autonome de l’éditeur, présenter deux historiques donnant la même observation courante et exigeant des actions différentes. L’étudiant démontre l’insuffisance d’une politique sans mémoire sur cet exemple. Cet exercice n’ajoute ni capteur ni persistance au moteur. La variante 12 h permet de programmer un petit automate de contrôle dans ce script unique.

### TP4 — Transférer vers les agents LLM (S6)

Proposer une étude de cas originale : un programme reçoit une demande, choisit de consulter un outil de disponibilité, observe sa réponse puis propose une action. Les données sont un dossier écrit, explicitement simulé pour l’analyse, sans requête réelle ni opération sur un compte.

E9 : séparer message utilisateur, observation d’outil, action proposée et autorisation humaine. E10 : identifier une réponse mal formée et une donnée externe non fiable ; proposer validation de schéma, liste d’actions autorisées et arrêt borné. Critère : trois risques reliés chacun à un contrôle observable, sans annoncer une sécurité complète.

ReAct fournit un exemple de couplage entre productions de raisonnement et actions dans des tâches précises ; le module en examine un schéma, pas une garantie générale de raisonnement fiable. [R6] La distinction industrielle entre workflow déterminé et agent décidant de son déroulement est une convention utile, présentée comme telle. [R7]

## 8. Accompagnement, erreurs et retour pédagogique

Prévoir trois niveaux d’aide : indice conceptuel, exemple d’entrée/sortie puis squelette partiel. Le corrigé complet intervient après une tentative et une explication. Erreurs à anticiper : inversion de `x/y`, oubli d’un `return`, liste non hachable dans `vus`, absence de borne, confusion pile/file, oubli des cas terminaux et comparaison de temps incluant le téléchargement du runtime.

Pour une erreur de syntaxe : conserver le message réel, faire identifier sa ligne et demander une correction locale. Pour une politique insuffisante : conserver la trace et analyser le choix, sans appeler « bug Python » tout échec de la tâche. Pour une carte sans solution : distinguer impossibilité de la tâche et insuffisance de l’algorithme. Pour une boucle : utiliser Stop, vérifier la reprise et expliquer que terminer un Worker ne démontre pas une isolation de sécurité de code hostile.

Accessibilité prévue : consignes textuelles autonomes, énoncé de carte lisible hors image, noms d’actions sans dépendance à la couleur, code sélectionnable, navigation clavier et traces bornées. Les diagrammes devront avoir une alternative textuelle vérifiée. Le lecteur d’écran et la vidéoprojection réelle restent des essais humains requis, pas des résultats déduits des tests automatisés.

## 9. Évaluation finale individuelle — 2 heures

Sujet proposé : dans le même contrat Python, analyser une carte fournie, compléter ou corriger une politique, comparer son résultat à une référence, puis discuter un transfert vers une interface conversationnelle. Fournir des cas accessibles pendant l’épreuve et réserver au moins deux cas de vérification supplémentaires au corrigé. La tâche ne demande ni appel LLM ni nouvelle architecture.

| Partie | Temps indicatif | Barème /20 | Preuve attendue |
|---|---:|---:|---|
| Modélisation et vocabulaire | 20 min | 4 | État/observation/action/objectif distincts ; catégories non exclusives. |
| Politique Python et vérifications | 50 min | 7 | Code réel, contrat respecté, cas nominaux et terminaux ; trace de l’exécution. |
| Comparaison et analyse d’erreurs | 30 min | 6 | Résultats de plusieurs cas, coût de trajet défini correctement, hypothèses de BFS explicites. |
| Transfert et limites | 20 min | 3 | Distinction LLM/système agent, action/effet et contrôle humain ; une limite argumentée. |

Proposition de validation : au moins **12/20**, dont **4/7 en programmation**, et aucune confusion non corrigée entre action proposée et action réellement exécutée. Une courte remédiation ciblée permet de reprendre une compétence manquante. Les seuils sont des choix pédagogiques à valider, pas des exigences scientifiques établies.

Productions à remettre : fichier Python ou texte de code, tableau de traces/résultats et commentaire d’une page maximum. Ne pas noter l’esthétique des captures ni la vitesse du poste ; prévoir un incident réseau documenté et un créneau de reprise plutôt qu’une fausse exécution simulée. L’autoévaluation existante du labo demeure une vérification introductive, pas la certification du module.

## 10. Périmètre du prochain jalon et critères d’acceptation

Après accord, le prochain jalon proposé est **M01-A : définir, modéliser et tester une politique réactive**, couvrant S1 à S3 (3 h 45), avant extension à BFS et à l’évaluation complète. Il évite d’annoncer 10 heures de formation comme réalisées alors que seuls quelques exercices sont prêts.

Acceptation de M01-A :

1. Cours en français et objectifs 1–3 explicités, références situées, recouvrements des catégories et simplifications signalés.
2. TP0 et TP1 avec consignes, entrées, résultats attendus, aides graduées et corrigé enseignant distinct.
3. Code exécuté par le véritable Pyodide sous le contrat existant ; preuve de collision refusée, d’arrêt et de reprise ; aucune simulation cachée du Python.
4. Traces textuelles permettant à l’étudiant de relier observation, politique et effet ; critères de réussite observables et sans faux suivi personnel.
5. Tests de non-régression conservés ; nouveaux tests limités aux comportements pédagogiques ajoutés ; chemins validés sous préfixe GitHub Pages.
6. Identité V2 conservée ; clavier, textes alternatifs et trois modes contrôlés ; essais humains encore non faits explicitement listés.
7. Revue scientifique et essai avec apprenant suivis d’un bilan des erreurs observées ; validation humaine avant M01-B.

Pour l’acceptation **du module complet** ultérieur : toutes les séquences et TP annoncés livrés ; oracles C0–C5 exécutés ; BFS vérifié et bornes expliquées ; évaluation finale et barème testés ; aucun agent LLM, tableau de bord ou mécanisme de progression annoncé sans implémentation correspondante. Le contenu supplémentaire reste documentaire jusqu’à sa livraison vérifiée.

## 11. Références et usage des sources

Sources consultées en ligne le 17 octobre 2026. Les formulations, exercices, jeux de cas, durées, barème et progression de ce document sont une proposition originale de conception ; aucune figure ni long passage de manuel n’est reproduit. Les ressources anglophones sont commentées en français dans les futurs supports.

- **[R1]** Russell et Norvig, *Artificial Intelligence: A Modern Approach*, 4e éd., chapitre 2, [Intelligent Agents — extrait officiel](https://aima.cs.berkeley.edu/4th-ed/pdfs/newchap02.pdf). Définitions de la fonction agent et de la rationalité ; ne pas confondre définition classique et terminologie récente des produits LLM.
- **[R2]** Poole et Mackworth, *Artificial Intelligence: Foundations of Computational Agents*, 3e éd., [§2.1 Agents and Environments](https://artint.info/3e/html/ArtInt3e.Ch2.S1.html). Contrôleur, observations et mémoire ; appui pour le modèle du TP.
- **[R3]** Même ouvrage, [§2.2 Hierarchical Control](https://artint.info/3e/html/ArtInt3e.Ch2.S2.html). Articulation des horizons et niveaux de contrôle ; lecture d’approfondissement.
- **[R4]** Même ouvrage, [§3.5 Uninformed Search Strategies](https://artint.info/3e/html/ArtInt3e.Ch3.S5.html). Exploration et garanties de recherche ; référence pour l’analyse de BFS.
- **[R5]** Hugging Face, [Qu’est-ce qu’un agent ? — cours français](https://huggingface.co/learn/agents-course/fr/unit1/what-are-agents). Ressource pédagogique spécialisée LLM, complément du cadre universitaire général.
- **[R6]** Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629), 2022, publication ICLR 2023. Article de recherche ; portée limitée aux méthodes et évaluations étudiées.
- **[R7]** Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents), 2024. Retour d’ingénierie industriel, utile pour le transfert ; ce n’est ni une norme ni une définition universelle des agents.

## 12. Décisions attendues avant mise en œuvre

Valider la cible universitaire et le diagnostic de prérequis ; choisir la durée centrale de 10 h ; accepter ou ajuster le barème ; confirmer le périmètre M01-A (S1–S3). Le laboratoire actuel est un support, pas le module complet déjà livré. **Aucun développement complet du module 01 ne commence avant cet accord.**
