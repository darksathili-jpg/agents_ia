# Audit critique — jalon S03

Date : 17 octobre 2026. Statut : conception complète soumise à validation humaine, pas validation en classe.

## Origine et périmètre

Branche `docs/module-01-s03`, créée directement depuis `bf009acb226ce6a53453529d72fa27ebf6f7af96` de `docs/module-01-s01-1-s02`, après contrôle d’un arbre propre et lecture d’AGENTS.md, S01 et S02. Les modifications restent dans ce dossier. AGENTS.md, interface, moteur, Worker, dépendances et ressources graphiques sont préservés. La publication de cette branche est autorisée par la mission ; aucune fusion ni aucun déploiement. S04 et S05 ne sont pas rédigées.

Livrables : [cours](SEANCE_03.md), [support élève](SUPPORT_ELEVE_S03.md), [enseignant](ENSEIGNANT_S03.md), [corrigés](CORRIGES_S03.md), [amorce](python/s03_depart.py), [solution autonome](python/s03_tp.py) et [tests](python/tests_s03.py). L’amorce historique `tp03_depart.py` reste une archive du plan général : le parcours courant pointe explicitement vers les nouveaux fichiers.

## Examen scientifique

Le TP conserve la carte, les deux mondes et le budget de S02. Il ajoute la transmission explicite de mémoire, pas une observation supplémentaire du monde caché. L’instant d’actualisation est défini avant la décision. Les traces séparent observation, mémoire avant, action, mémoire après et effet. Les modèles objectifs/utilités sont discutés sur table ; le code de règles n’est pas abusivement appelé planificateur.

Le contraste oubli/écrasement/conservation est expérimental. L’invariant et la preuve par histoires indiscernables apportent l’argument conditionnel, distinct de tests finis. La représentation de mémoire est finie et volontairement réduite ; elle n’est ni un modèle complet du monde ni une distribution probabiliste. Un indice jamais reçu, une mémoire erronée et une observation corrective sont explicitement testés. La possibilité d’un indice périmé est un contre-exemple discuté, pas une nouvelle fonctionnalité annoncée.

La politique stochastique varie les commandes avec une transition fixe, contrairement au glissement S02. Les deux branches sont forcées dans les tests ; la série à graine fixe illustre la reproductibilité, sans estimation statistique. L’analyse p et 1−p ne suppose pas que les mondes sont équiprobables. Les catégories d’architectures sont des repères combinables et non une taxonomie exhaustive.

**Établi et simplifié :** le cadre histoire/mémoire et les repères d’architectures proviennent de manuels scientifiques ; les trois valeurs de mémoire, la carte, les conventions temporelles et les choix de prudence sont des constructions pédagogiques originales. Les preuves ne portent que sur leurs hypothèses. La boucle est autonome pour cette tâche, sans LLM ni apprentissage.

## Références et programmes

Reconsultation en ligne de Poole–Mackworth 2023, §2.1, et de l’extrait Russell–Norvig, §2.4 : liens et questions critiques dans le parcours enseignant et la bibliographie. Ce sont des manuels de synthèse ; aucune prétention à présenter un résultat expérimental inédit des auteurs. L’extrait Russell–Norvig reste non daté et ne reçoit pas une pagination de quatrième édition non vérifiée.

La page institutionnelle éduscol des programmes NSI a été reconsultée. Fonctions, boucles, représentations et tests constituent les appuis ; la théorie d’architectures et les politiques stochastiques sont un approfondissement choisi, pas une obligation réglementaire ajoutée. La voie Première reçoit le conducteur ; la voie Terminale approfondit l’invariant et les conditions de validité.

## Charge et accessibilité pédagogique

Minutage prévu : 10 + 15 + 15 + 40 + 15 + 15 + 10 = 120 minutes, quarante de TP préservées. Exercices intégrés, non ajoutés au créneau. Les longues lectures enseignantes sont préparatoires ; la discussion de quinze minutes remplace le guidage correspondant. Le dernier créneau conceptuel est dense : limiter le calcul d’utilité à deux coûts et réserver la preuve probabiliste aux enseignants.

Support élève à réponses ouvertes distinct des corrections, tableaux avec en-têtes et descriptions textuelles, aucune information dépendant d’une couleur visuelle seule. Le terme bleu/orange est une donnée textuelle. Les durées ne sont pas mesurées auprès d’élèves. Impression, lisibilité en projection et usage au lecteur d’écran nécessitent des essais humains, non réalisés ici.

## Vérifications techniques reproductibles

```text
python docs/pedagogie/module-01/python/valider_dossier.py
node --check docs/pedagogie/module-01/python/verifier_pyodide.mjs
node docs/pedagogie/module-01/python/verifier_pyodide.mjs
git diff --check
```

Le validateur inclut les seize tests historiques et sept nouveaux tests S03, exécute amorce et solution, vérifie liens locaux et syntaxe, les trois minutages de 120 minutes et l’arrêt documentaire avant S04. Le vérificateur navigateur charge le véritable Pyodide du laboratoire existant et reprend aussi les contrôles historiques. Le succès attendu de l’amorce est un marqueur d’exécution, pas la réussite de sa politique initiale.

Cas couverts : deux réussites avec actions exactes, oubli et écrasement, information absente, mémoire erronée corrigée ou non, conservation du souvenir et de l’observation, budgets 0/2/3, refus, arrêt, commandes/mémoires/mondes/budgets invalides et choix stochastiques reproductibles.

Résultats : les 23 tests (9 historiques, 7 S01/S02, 7 S03) passent sous CPython et dans Pyodide réel. Les démonstrations S03 et l’amorce complète produisent leurs marqueurs attendus dans les deux environnements. Le contrôle syntaxique JavaScript passe. Les minutages sont vérifiés comme sommes et plages continues ; cette vérification ne mesure pas le temps d’apprentissage.

La boucle appelle au plus trois fois le contrôleur, s’arrête sur issue, arrêt ou refus. Cette borne n’interrompt pas une boucle infinie introduite dans une fonction élève : utiliser Stop. Les épisodes réinitialisent la mémoire par défaut. Le script est copié intégralement et exécuté en console en une seule fois ; il n’ajoute aucune persistance entre décisions de la grille. Ces tests ne constituent pas un audit complet de l’interface inchangée.

## Réserves et prochain accord

La réussite technique ne vaut pas validation pédagogique. Faire relire les hypothèses de preuve et les distinctions mémoire/modèle, puis essayer les supports et mesurer les temps réels avec les deux publics. Critères du prochain accord : code élève explicable, deux mondes réussis avec traces correctes, cas d’absence et de mémoire erronée interprétés, différences de hasard comprises, seuil formatif discuté et transposition enseignante évaluée. Arrêt après S03 pour cet accord humain.
