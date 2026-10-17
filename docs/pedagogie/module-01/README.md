# Module 01 — Fondements scientifiques des agents intelligents

**Dossier de conception et séance pilote — validation humaine requise.**

Branche `docs/module-01-conception-pilote`, issue de `2a9ed39` (V2 `13d5284` et stabilisation locale). Aucun changement de l’application, du laboratoire, du Worker ou des ressources graphiques. `AGENTS.md` est lu mais laissé intact, hors commit. L’ancienne [note exploratoire](../module-01-fondements-scientifiques.md) reste historique : **le présent dossier remplace sa progression en sept séquences par cinq séances de deux heures**.

## Lire selon son rôle

- Préparer la formation : [références vérifiées](REFERENCES_SCIENTIFIQUES.md), [objectifs et prérequis](OBJECTIFS_ET_PREREQUIS.md), [progression et matrice d’évaluation](PROGRESSION.md).
- Distribuer aux élèves : [séance 01](SEANCE_01.md) et [sujets de TP et exercices](TP_ET_EXPERIENCES.md). Les liens de correction n’y figurent pas dans le déroulé élève.
- Préparer et approfondir : [parcours enseignant](APPROFONDISSEMENTS_ENSEIGNANTS.md), [corrigés réservés à la préparation](CORRIGES.md), [évaluations](EVALUATIONS.md).
- Examiner la livraison : [audit scientifique, technique et pédagogique](AUDIT_SCIENTIFIQUE.md).

Les corrections sont séparées matériellement pour leur distribution ; un dépôt public ne permet pas de les rendre confidentielles. L’enseignant distribue les seuls sujets avant la restitution.

## Périmètre de ce jalon

Les étapes A et B sont documentées. La séance 01 est rédigée intégralement pour les deux publics, avec TP01, exercices, retour et corrections. Les TP02–05 ont des fiches de conception et des supports Python vérifiables ; les **cours détaillés des séances 02 à 05 ne sont pas rédigés**. Leur rédaction attend la validation du pilote. Les évaluations finales proposées servent à vérifier l’alignement de la progression ; elles ne prouvent pas que le module complet est livré.

Durée : 10 h, cinq séances de 120 min, activités et évaluation incluses. Le parcours enseignant remplace certaines aides élèves par de l’analyse et de la lecture ; il ne consiste pas à ajouter des heures de cours savant à une séance déjà pleine. Approfondissements longs : travail facultatif hors des 10 h, explicitement identifié.

## Python et application : deux usages distincts

Le laboratoire existant sait afficher une grille fixe, exécuter une politique Python, choisir entre gloutonne/BFS/Python, tracer les actions et arrêter un Worker. Il ne propose ni éditeur de carte, ni observation masquée, ni mémoire Python persistante entre deux décisions, ni moteur d’agent LLM.

Les scripts pédagogiques de ce dossier sont des expériences textuelles autonomes, à copier intégralement dans l’éditeur Python et à lancer avec **Exécuter Python**. Ils n’animent pas automatiquement la grille. TP01/TP02 fournissent aussi une fonction compatible avec le contrat `decider(position, objectif, obstacles)`. Les TP de mémoire/masquage gardent leur boucle dans **une seule exécution**, sans changement de Worker. Aucun appel à une API LLM.

Les scripts corrigés et les vérifications techniques sont rangés dans `python/`, avec les fichiers de départ distincts. Voir l’audit pour les commandes effectivement exécutées et la distinction CPython/Pyodide. Pour le pilote élève, copier seulement `python/tp01_depart.py` ; ne pas distribuer d’emblée le fichier de correction.

## Point d’arrêt

Validation attendue sur la précision scientifique, la progressivité du pilote, la profondeur enseignant, l’adéquation Première/Terminale et les temps proposés. **Arrêt après audit : pas de rédaction des séances 02–05, pas d’intégration d’interface, pas de fusion, pas de déploiement.**
