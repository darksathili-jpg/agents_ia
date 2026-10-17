# Audit critique du dossier et de la séance pilote

**Jalon A–D, 17 octobre 2026. Point d’arrêt E : validation humaine.**

> Audit historique du pilote `729f38b`. Pour l’état courant et le nouveau point d’arrêt avant S03, consulter [l’audit S01.1/S02](AUDIT_S01_1_S02.md). Les mentions de S02 non rédigée ci-dessous décrivent le jalon précédent.

## Périmètre effectivement produit

Sources et programmes examinés ; cartographie de dix objectifs ; progression des cinq séances ; séance 01 complète pour distribution élève et travail enseignant distinct ; cinq protocoles TP avec fichiers de départ ; quinze exercices ; corrigés et deux propositions d’évaluation sur 20. Les cours détaillés S2–S5 ne sont pas écrits. Leur absence est volontaire, conformément à la méthode de production demandée.

Le plan en cinq séances remplace, pour cette mission, l’organisation exploratoire antérieure. Les TP futurs ont un support technique de référence pour vérifier la faisabilité ; ils ne sont pas des activités intégrées à la plateforme. Aucune interface, ressource graphique ni mécanique du laboratoire n’a été ajoutée.

## Audit scientifique : points vérifiés et décisions

| Point examiné | Décision / preuve de vigilance |
|---|---|
| Définition d’un agent | Cadre annoncé, frontières discutées, aucun monopole du LLM. R1/R2 distingués plutôt que fusionnés en définition universelle. |
| Automate, chatbot, agent, LLM | Descriptions selon des axes différents ; les recouvrements sont admis et les cas frontières doivent être justifiés. |
| Autonomie et rationalité | Autonomie opérationnelle présentée comme convention de travail ; rationalité relative à information/critère, distincte de réussite et de conscience. |
| Histoire | Repères Brooks/Wooldridge/ReAct documentés ; distinction rapport 1985/article 1986 et arXiv 2022/publication 2023. Aucune chronologie exhaustive inventée. |
| Notation | État s, observation o, action a, mémoire m et historique h définis ; mémoire ne signifie pas modèle complet. Hasard de politique et hasard de transition séparés. |
| Expérience masquée | Deux mondes ont la même observation finale, mais le contrôleur ne lit pas leur indice caché ; preuve d’insuffisance sans mémoire limitée à ce contre-exemple. |
| Gloutonne | La règle horizontale est un témoin local, pas un alias de toute recherche best-first. Un refus est une propriété du couplage politique-environnement. |
| BFS | Coûts uniformes, graphe fini et carte fixe explicités ; un autre trajet de même longueur reste valide. Le coût abstrait ne vaut pas automatiquement pour tout programme. |
| Performances | Tentatives et déplacements distincts ; longueurs des échecs non définies ; effectif et accessibilité précisés. |
| Sources LLM | Article de recherche, revue, manuel, ressource pédagogique et guide industriel distingués. Une justification textuelle n’est pas une preuve de causalité interne. |

Les résultats des expériences sont des résultats du code et des cartes définis ici, pas une validation indépendante de tous les énoncés du cours. Les preuves et conventions sont séparées des métaphores de Microduck.

## Audit des références et programmes

La page éduscol « Programme en vigueur » et les deux annexes officielles ont été consultées. Les correspondances D/A/F sont identifiées dans `OBJECTIFS_ET_PREREQUIS.md`. Graphes et parcours sont mobilisés en Terminale ; un élève de Première ne doit pas les connaître implicitement. Ensembles Python, probabilités de politique, utilité et formalisation d’agent sont introduits ou fournis, pas annoncés comme acquis réglementaires.

R1 : édition/année vérifiées sur le site des auteurs et extrait consulté, pas l’intégralité du manuel ; le PDF non daté n’est pas attribué avec certitude à la 4e édition sur la seule foi de son chemin. R2 : notice, sommaire et support officiel consultés, pas le livre complet. R4 : statut ICLR/camera-ready et texte v3 consultés. R5 : DOI résolu, métadonnées et contenu consultés, article de revue publié en 2024. R6 évolutif, sans année unique supposée. R7 : noms conservés tels qu’affichés et convention industrielle explicitée. R8 : rapport MIT lu, publication ultérieure confirmée par l’auteur. Aucun numéro de page non contrôlé ni citation textuelle longue.

**Limite documentaire** : cette vérification concerne les ressources accessibles à la date du contrôle ; elle ne remplace pas une expertise externe ni une lecture exhaustive de tous les ouvrages. Aucun programme officiel requis n’a été laissé non consulté. Aucun référentiel de certification propre à Agent Academy n’est prétendu officiel.

## Audit technique exécuté

1. CPython local : `python docs/pedagogie/module-01/python/tests_experiences.py` — **9 tests réussis**, comprenant les retours réactifs/prudents, murs/bords, refus et compteurs, cas terminaux, observation masquée, mémoire, six oracles BFS avec rejeu des chemins, tableau de douze résultats et graines reproductibles.
2. Pyodide réel du laboratoire : `node docs/pedagogie/module-01/python/verifier_pyodide.mjs` — **5 fichiers de départ exécutés**, marqueur initial attendu pour chacun ; **9 tests réussis** et démonstrations TP01–05 exécutées. Le runtime est celui du Worker existant ; aucun résultat simulé et aucune bibliothèque Python tierce.
3. Validation documentaire : `python docs/pedagogie/module-01/python/valider_dossier.py` — **réussie : 18 liens locaux**, clôture des blocs, syntaxe de tous les fichiers Python, dix objectifs, quinze exercices, cinq TP et cinq départs ; absence des cours S2–S5 vérifiée. Les neuf tests locaux sont également relancés par cette commande et passent.
4. Préservation : diff depuis `2a9ed39` contrôlé sur accueil, scripts, CSS, laboratoire, Worker, assets et documentation artistique : vide. La suite applicative de 24 tests n’est pas relancée pour ce travail documentaire sans modification de l’application ; sa dernière campagne appartient au bilan précédent.

Les fichiers de départ ne sont **pas** des agents complets : TP01 renvoie initialement arrêt ; TP02–05 contiennent une fonction à compléter et affichent explicitement ce statut. Exécuter ces fichiers valide leur syntaxe et le comportement initial annoncé, pas la réussite de leur futur code élève. Les corrections sont exécutées séparément. Les fonctions auxiliaires y sont fournies pour maîtriser la charge de programmation.

### Portée de la transposition dans le laboratoire

TP01/02 : le contrat `decider` peut être relié à la grille ; le dossier exploite aussi des appels directs. TP03 : observation masquée et mémoire conservées uniquement dans une boucle console autonome. TP04/05 : cartes définies dans le script, pas dans un nouvel éditeur graphique. Le Worker recrée l’espace de noms des décisions ; une variable globale ne fournit pas de mémoire persistante entre ses appels. Le code aléatoire permet de comparer des graines dans une exécution contrôlée, pas d’inférer des propriétés d’un LLM.

La boucle du conducteur est bornée à 35 commandes ; départ=cible, arrêt anticipé, mur, bord et cible inaccessible sont distingués. Les fonctions fournies attendent des entrées respectant le contrat indiqué ; elles ne sont pas un parseur robuste de n’importe quelle donnée hostile. Le test `libre` sur une liste de murs a un coût linéaire dans le nombre de murs : la borne abstraite de BFS avec accès efficace aux voisins ne doit pas être attribuée sans réserve à ce support lisible.

## Audit pédagogique : acquis et insuffisances ouvertes

**Acquis du pilote** : problème observable, hypothèses départagées par cas, fonction réellement exécutée, comparaison commande/effet, transfert et synthèse individuelle. Les corrections sont séparées. Le parcours enseignant comporte ses propres tâches : choix de frontière, contre-exemple d’information, coût paramétré et lecture critique, avec indicateurs de compréhension et transposition par notion.

**Réserves à lever avant validation** :

- Les 120 min de S1 n’ont pas été mesurées avec des élèves ; classification et vocabulaire pourraient prendre trop de temps. Si nécessaire, réduire les cas de classification, sans supprimer la programmation ni la confrontation prédiction/résultat.
- Les 10 h supposent Python élémentaire acquis. Fournir les auxiliaires et une aide de lecture ; prévoir une remise à niveau séparée si le diagnostic révèle un besoin collectif.
- BFS en 50 min vise une complétion guidée en Terminale préparée ; une construction intégrale sans prérequis serait irréaliste. La variante Première doit rester fournie/observée.
- Quinze exercices constituent une banque, pas une charge ajoutée à chaque séance. L’épreuve finale de 60 min est incluse dans S5 ; la durée réelle reste à tester.
- Les supports enseignants demandent une lecture attentive et une production ; leurs prolongements facultatifs ne sont pas cachés dans les 10 h.
- Les solutions sont séparées des fiches distribuées, mais le dépôt ne les rend pas confidentielles. L’enseignant gère la distribution.
- La grille graphique ne dispose pas encore d’une équivalence textuelle complète validée au lecteur d’écran. Les scripts textuels et la description des cartes aident, mais ne prouvent pas une accessibilité totale. Essais lecteur d’écran, projection et apprenants restent nécessaires.
- Le protocole à six cartes teste des situations choisies, pas la robustesse générale. Une réussite du corrigé n’établit pas l’efficacité pédagogique de l’énoncé.

## Points soumis à validation humaine avant S2–S5

1. Les élèves comprennent-ils le choix des frontières sans conclure « tout programme est une IA » ?
2. Le niveau enseignant constitue-t-il un approfondissement suffisant, tout en restant transposable ?
3. La séance laisse-t-elle réellement 40 min de Python et 10 min de retour individuel ?
4. Les versions Première/Terminale et les auxiliaires fournis sont-ils adaptés aux groupes visés ?
5. Les critères de réussite, le barème 4/5/7/4 et la séparation sujets/corrigés conviennent-ils ?

**Travail arrêté à ce jalon. Aucune rédaction des cours S2–S5 ni intégration complète avant accord.**
