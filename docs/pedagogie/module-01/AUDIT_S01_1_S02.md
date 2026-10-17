# Audit du jalon S01.1 et S02

Date : 17 octobre 2026. Statut : dossier proposé à la validation humaine ; durées pédagogiques estimées, sans expérimentation en classe.

## Périmètre et conservation

La branche `docs/module-01-s01-1-s02` prolonge la conception pilote `729f38b`, puis le commit utilisateur `4526e32` qui contient déjà `AGENTS.md`. Au démarrage, l'arbre était propre : contrairement à l'hypothèse du mandat, ce fichier n'était plus simplement indexé. Il est conservé sans modification.

Les changements portent exclusivement sur ce dossier documentaire et ses scripts de vérification. L'accueil V2, les captures, le laboratoire, le Worker et les dépendances restent inchangés. Aucun déploiement, aucune fusion et aucune publication distante ne font partie de ce jalon. Les spécifications antérieures des TP ultérieurs sont conservées ; les séances 03 à 05 ne sont pas rédigées.

## Consolidation S01.1

- [Support élève](SUPPORT_ELEVE_S01.md) utilisable avec espaces de réponse, hypothèses, traces et bilan.
- Diagnostic de huit minutes : fonctions, conditions, retour et coordonnées ; corrigé et remédiation dans [les corrigés](CORRIGES.md).
- Programmation maintenue de 45 à 85 minutes, soit quarante minutes. Les activités de classification obligatoires sont resserrées pour respecter les 120 minutes prévues.
- [Production enseignante complète](PRODUCTION_ENSEIGNANT_S01.md) : modèle, traces, argumentation, contre-test et critique.
- Distinction répétée entre exécuter un script dans la console et choisir une politique Python pour faire évoluer la grille. Les appels de test imprimés ne déplacent pas le robot.

## Construction S02

La [séance](SEANCE_02.md), le [support élève](SUPPORT_ELEVE_S02.md), les [protocoles](ACTIVITES_S02.md), le [parcours enseignant](ENSEIGNANT_S02.md) et les corrigés couvrent état, observation, action, transition, refus, déterminisme, effets stochastiques et information partielle.

Le TP02 programme une transition dans la console : son script ne fournit pas une politique `decider` et n'installe pas sa fonction de transition dans le laboratoire. Le TP03 est préparé par une expérience d'observation masquée ; aucune architecture à mémoire n'est implémentée à ce stade.

Le contre-exemple masque réellement une information dans la fonction d'observation. Cacher une image ne suffirait pas, puisque la politique du laboratoire reçoit la carte. Deux historiques différents conduisent ici à une même observation courante. Après deux actions imposées, une seule commande reste disponible : les actions qui réussissent dans les deux mondes sont disjointes. Cette contrainte empêche de contourner le problème en revenant lire l'indice. La conclusion concerne cette tâche et une politique sans mémoire, pas une impossibilité générale de résoudre tout environnement partiellement observable.

Le modèle de glissement choisit deux effets équiprobables pour une action acceptée. Les deux tirages sont forcés dans les tests ; huit essais avec réinitialisation illustrent ensuite une série reproductible. Ils ne démontrent ni la valeur d'une probabilité ni l'indépendance statistique des tirages. Une graine fixe rend un générateur reproductible ; le parcours enseignant distingue ce calcul du modèle probabiliste du milieu.

## Cohérence scientifique et programmes

Les références R1 et R3 et les programmes officiels de Première et Terminale ont été reconsultés : voir [la bibliographie et ses réserves](REFERENCES_SCIENTIFIQUES.md). Les liens institutionnels et les passages de Poole et Mackworth sur les agents, l'historique et les probabilités étayent les distinctions employées. La réserve sur l'édition et la pagination de l'extrait public de Russell et Norvig reste explicite. Les grilles, preuves et expériences proposées sont des constructions pédagogiques originales, sans attribution abusive à ces ouvrages.

Fonctions, conditions, coordonnées, dictionnaires et tests mobilisent les acquis NSI. Le formalisme des agents, les noyaux de transition et la relation d'équivalence observationnelle sont des approfondissements ; ils ne sont pas présentés comme des rubriques obligatoires des programmes. Aucun prérequis de probabilités conditionnelles, réseaux neuronaux ou graphes n'est exigé pour réaliser S02. Le parcours enseignant définit les variables, distingue observation instantanée et historique, et ne confond pas équivalence observationnelle et bisimulation.

## Vérifications reproductibles

Depuis la racine du dépôt :

```text
python docs/pedagogie/module-01/python/valider_dossier.py
node --check docs/pedagogie/module-01/python/verifier_pyodide.mjs
node docs/pedagogie/module-01/python/verifier_pyodide.mjs
git diff --check
```

Le validateur contrôle les liens locaux, la syntaxe des fichiers et extraits Python, les objectifs et exercices existants, les cinq amorces historiques, neuf tests antérieurs et sept nouveaux tests. Il vérifie la continuité des deux minutages jusqu'à 120 minutes, les quarante minutes de programmation S01 et l'absence des fichiers de séances 03 à 05.

Le contrôle navigateur charge le véritable Pyodide du laboratoire existant : cinq amorces historiques, neuf tests antérieurs et leurs démonstrations, sept nouveaux tests et quatre nouveaux scripts sont exécutés. Une amorce qui signale volontairement une fonction à compléter ne constitue pas un corrigé exécutable : ses marqueurs attendus sont distingués des marqueurs de réussite des solutions.

Ces contrôles vérifient des comportements et la reproductibilité des supports ; ils ne valident pas à eux seuls leur efficacité pédagogique. Aucun changement applicatif ne justifie ici de présenter une nouvelle campagne complète des tests d'interface comme réalisée.

Résultats du contrôle final : 49 liens locaux résolus, neuf tests historiques et sept nouveaux tests réussis sous CPython ; ces seize tests réussissent également dans Pyodide réel, ainsi que les amorces et démonstrations décrites ci-dessus. La syntaxe JavaScript du vérificateur et le contrôle des espaces Git passent. Les quatre nouvelles exécutions individuelles produisent les marqueurs attendus, dont `A_COMPLETER_S02` pour l'amorce volontairement incomplète.

## Limites et critères du prochain accord

- Les 120 minutes de chaque séance sont un budget estimé, non une durée mesurée auprès d'élèves. Les difficultés de lecture et de saisie doivent être observées en classe.
- L'impression des fiches, la lisibilité au vidéoprojecteur et l'usage avec lecteur d'écran demandent une vérification humaine dans les conditions réelles.
- La profondeur du parcours enseignant et les seuils proposés pour l'évaluation formative restent soumis à une relecture scientifique et didactique.
- L'expérience stochastique et les observations masquées fonctionnent dans la console ; elles ne deviennent pas des fonctionnalités de la grille de l'application.
- Avant S03 : faire valider les deux supports, le diagnostic, les traces attendues, le contre-exemple avec son budget d'actions, les corrigés et l'adéquation aux deux publics. Relever les temps réellement observés et ajuster le découpage si nécessaire.

Point d'arrêt : attendre l'accord humain sur ce jalon avant toute rédaction de S03 ou extension de l'application.
