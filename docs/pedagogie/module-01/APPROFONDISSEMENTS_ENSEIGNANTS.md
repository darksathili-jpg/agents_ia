# Parcours enseignant — modèle scientifique et transposition du pilote

Ce parcours possède ses propres problèmes, preuves et productions. Pour S01.1, conserver 40 min d’activité Python, avec des tests et analyses plus approfondis pour les enseignants ; adapter les apports et les cas discutés dans les autres créneaux. Un [exemple complet de production S01](PRODUCTION_ENSEIGNANT_S01.md) explicite modélisation, trace, argument et critique. Le [parcours scientifique S02](ENSEIGNANT_S02.md) est maintenant rédigé séparément. Les repères S3–S5 ci-dessous restent des orientations historiques du plan, pas des cours rédigés. Les démonstrations longues sont facultatives hors des 10 h.

## 1. Une définition est un instrument d’analyse

Le cadre fonctionnel classique de R1 décrit le comportement à partir de perceptions et d’actions. R2 met davantage l’accent sur le contrôle autonome et l’interaction ; parler d’un agent implique alors des choix de délimitation et de capacité. La proposition « tout programme est un agent » peut se défendre avec des frontières très larges, mais perdre presque toute puissance explicative.

**Problème enseignant S1** : choisir successivement comme système la fonction `decider`, son Worker et l’ensemble contrôleur-environnement. Pour chacun, indiquer entrées, sorties, état conservé et décisions effectivement sous contrôle. La fonction seule retourne une chaîne ; la boucle et le moteur lui donnent une portée d’action. Ni le mot « agent » ni l’emploi de Python ne démontrent de compétence générale.

Production attendue : trois schémas de frontière et un paragraphe justifiant le plus utile pour l’activité. Contre-épreuve : peut-on remplacer la politique tout en conservant l’environnement ? Si oui, ce découpage aide à comparer des stratégies plutôt qu’à attribuer leurs propriétés au moteur.

## 2. Notation progressive et information disponible

Adoptons nos propres conventions. `S` est l’ensemble des états du monde ; `A` l’alphabet des actions ; `Ω` celui des observations. À l’instant `t`, `s_t ∈ S`, `o_t ∈ Ω`, `a_t ∈ A`. Le modèle déterministe d’environnement est `s_(t+1)=T(s_t,a_t)` et `o_t=O(s_t)`. Une politique sans mémoire est `a_t=π(o_t)` ; cela ne suffit à toutes les tâches que sous des hypothèses d’information appropriées. L’action peut néanmoins être légale sans atteindre l’objectif.

Historique `h_t=(o_0,a_0,…,a_(t−1),o_t)` ; politique générale déterministe `a_t=π(h_t)`. Une réalisation finie emploie une mémoire `m_t ∈ M` avec `a_t=g(m_t,o_t)` et `m_(t+1)=u(m_t,o_t,a_t)`. La mémoire peut être un seul bit, un compteur ou une représentation structurée ; stocker un historique ne lui donne pas automatiquement le statut de modèle complet ou correct du monde. [R3]

Pour une politique stochastique, `π(a|h_t)` désigne une distribution de probabilité sur les actions : valeurs positives ou nulles, somme égale à 1. Cela est distinct d’une transition stochastique `P(s'|s,a)` ou d’une observation bruitée. Une politique déterministe dans un environnement stochastique reste déterministe ; réciproquement, une marche aléatoire dans une carte fixe ne rend pas cette carte aléatoire.

**Dérivation originale pour la formation** : si deux états `s` et `s'` donnent la même observation `o` mais exigent respectivement `gauche` et `droite` pour réussir immédiatement, une fonction déterministe de `o` seul choisit la même action dans les deux cas. Elle ne peut donc pas garantir les deux réussites. Une mémoire d’un indice antérieur peut lever l’ambiguïté dans notre exemple ; elle n’élimine pas toute incertitude dans tous les environnements. Le TP03 est un contre-exemple construit, pas une preuve universelle de suffisance d’un bit de mémoire.

## 3. Objectif, performance, autonomie et rationalité

Une tâche doit spécifier ce qui compte comme réussite et le coût des erreurs. Un objectif terminal n’est pas une fonction de performance complète : deux trajets réussis peuvent différer par la durée, les actions dangereuses ou les ressources. La rationalité classique raisonne relativement à ce critère et à l’information disponible [R1]. L’autonomie se discute selon les choix laissés au contrôleur, les limites d’autorisation et l’éventuel apprentissage ; elle n’efface ni concepteur ni opérateur.

**Étude originale S1** : deux stratégies atteignent une sortie. A accomplit 6 déplacements et 2 refus, B accomplit 8 déplacements sans refus. Pour le coût `C = déplacements + k × refus`, A coûte `6+2k`, B coûte 8. A est meilleure si `k<1`, elles sont à égalité si `k=1`, B est meilleure si `k>1`. Les nombres sont ceux d’un dossier d’analyse, pas une mesure du labo où un refus arrête l’épisode. Cette variation rend observable la dépendance au critère ; elle ne prétend pas démontrer une rationalité absolue.

Question de lecture S1 : le critère vient-il de la politique ou de la tâche ? Réponse attendue : il sert à juger un comportement ; sa représentation explicite dans le contrôleur varie. Une politique peut poursuivre implicitement un but sans contenir un objet logiciel `objectif`.

## 4. Architecture et politique : axes distincts

Repères pour S3, à développer seulement après validation : réflexe simple (observation courante), réflexe avec état interne (mise à jour d’une représentation), orienté objectif (conséquences et test de but), orienté utilité (comparaison de résultats ou compromis). Ces modèles conceptuels n’épuisent pas les architectures ; « utilisant un LLM » décrit un composant, pas une cinquième catégorie exclusive.

Un contrôleur peut réagir rapidement et planifier à un autre niveau. Les couches de contrôle de Brooks [R8] et les hiérarchies de R3 évitent une opposition simpliste entre tout-réactif et tout-délibératif. Une structure en couches n’est pas automatiquement une architecture BDI ; ne pas introduire cette dernière comme synonyme de mémoire ou de planification.

Dans le support BFS, la connaissance de la carte, le coût unitaire et le caractère statique sont des hypothèses. La file et les prédécesseurs permettent de discuter coût et correction. Le BFS fourni dans le laboratoire recalcule une recherche à chaque décision ; la copie de chemins y a un coût distinct du BFS de référence. Il ne faut pas attribuer au runtime une complexité démontrée seulement pour un algorithme abstrait.

## 5. Lecture critique accompagnée — tâches différentes par séance

| Séance | Lecture et question | Réponse ou production attendue |
|---|---|---|
| S1 | R1/R2 : les critères de reconnaissance sont-ils identiques ? | Comparer comportement et contrôle ; annoncer le cadre retenu et un cas frontière. |
| S2 | R3, contrôleurs : observation et état interne peuvent-ils être échangés ? | Deux histoires d’indices, observation identique, information mémorisée différente ; pas d’anticipation du futur. |
| S3 | R1/R3 : une mémoire suffit-elle à construire un modèle correct ? | Distinguer stockage, prédiction et validation ; proposer une mémoire erronée qui conduit à un mauvais choix. |
| S4 | R3, recherche : « plus court » par rapport à quoi ? | Nombre d’arêtes à coûts uniformes ; ni énergie variable, ni garantie dans une carte modifiée. |
| S5 | R4, sections méthodes/résultats : quelle référence compare-t-on ? | Identifier tâche, modèle, accès aux outils et métrique ; rechercher une condition où l’effet ne se généralise pas. R5 organise le domaine, R7 propose une convention d’ingénierie, aucun ne remplace cette preuve. |

Pour R4, lire une comparaison « Act-only / ReAct » sans reproduire de longs prompts : la méthode combine productions de texte et actions, évaluées sur des tâches délimitées. Un résultat favorable ne prouve ni introspection fidèle ni fiabilité d’un système quelconque doté d’un outil. Les sorties de raisonnement sont un matériau d’analyse et ne constituent pas, seules, une preuve de causalité interne.

## 6. Regard de l’enseignant — grille didactique par notion

| Notion | Prérequis / difficulté ou conception erronée | Relance et indicateur de compréhension | Adaptation et limite |
|---|---|---|---|
| Agent et frontière | Entrée/sortie ; « toute condition est intelligente » | « Où va le résultat du return ? » ; distingue fonction et effet | Première : dessin de boîtes. Terminale : interface. Prolongement : frontières imbriquées, sans hiérarchie d’intelligence. |
| Automate/chatbot/LLM | Contrôle et interface ; catégories vues comme exclusives | « Une porte peut-elle être les deux ? » ; justifie un recouvrement | Première : cas concrets. Terminale : états. Enseignant : changement de cadre, pas définition arbitraire. |
| Observation/état | Variables ; « cacher l’image suffit à cacher l’information au code » | « Quelles données reçoit exactement la fonction ? » ; cite un accès interdit | Première : carte couverte et dictionnaire fourni. Terminale : fonction d’observation. Pas de vrai capteur simulé par une image. |
| Action/transition | Contrat ; « action choisie = mouvement accompli » | « Que contient la ligne refusée ? » ; conserve la position | Trace commune aux deux niveaux ; prolongement : actionneur défaillant, hors expérience initiale. |
| Politique/mémoire | Fonctions et variables ; « globale = mémoire persistante du labo » | « Qui recrée les variables à chaque appel ? » ; place la mémoire dans une boucle unique | Première : une couleur retenue. Terminale : dictionnaire/automate. Mémoire partielle, pas omniscience. |
| Autonomie/rationalité | But et critère ; « autonome = toujours bon » | « Que change le coût d’un refus ? » ; compare les deux coûts | Première : nombres. Terminale : fonction. Enseignant : seuil k, sans optimisation universelle. |
| Architecture/utilité | Abstraction ; classement pris pour taxonomie exhaustive | « Même politique dans deux architectures ? » ; donne un hybride | Première : fonction fournie. Terminale : graphe. Enseignant : conditions de garantie et limites du modèle. |
| Évaluation/LLM | Tests ; « une réussite prouve la robustesse » | « Quel cas manque ? » ; propose un contre-exemple et une mesure | Première : quelques cas discriminants. Terminale : banc. Enseignant : contrôle expérimental et transposition en 30 min. |

Prolongement enseignant facultatif : produire une contre-épreuve de 15 minutes à faire en binôme, puis une correction qui distingue erreur Python, insuffisance d’information et objectif impossible. La formation gagne en profondeur par ce travail de diagnostic, pas par l’ajout d’un vocabulaire hors de portée des élèves.
