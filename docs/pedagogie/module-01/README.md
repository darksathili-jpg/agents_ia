# Module 01 — Fondements scientifiques des agents intelligents

**Jalon courant : S03 conçue — validation humaine requise avant S04.**

La branche `docs/module-01-s03` part du commit `bf009acb226ce6a53453529d72fa27ebf6f7af96` de `docs/module-01-s01-1-s02`. Lire le [cours S03](SEANCE_03.md), le [support élève](SUPPORT_ELEVE_S03.md), le [parcours enseignant](ENSEIGNANT_S03.md), les [corrigés S03](CORRIGES_S03.md) et l’[audit S03](AUDIT_S03.md). Le TP03 courant utilise `python/s03_depart.py` et sa correction séparée `python/s03_tp.py` ; il remplace pour cette séance l’amorce générique historique `tp03_depart.py`.

Pilote de référence : `729f38b`, sur `docs/module-01-conception-pilote`, issu de la V2 et de sa stabilisation. Le jalon précédent est sur `docs/module-01-s01-1-s02`, créé depuis `4526e32` : ce dernier commit utilisateur a déjà versionné `AGENTS.md`, dont le contenu reste intact dans notre travail. Aucun changement de l’application, du laboratoire, du Worker ou des ressources graphiques. L’ancienne [note exploratoire](../module-01-fondements-scientifiques.md) reste historique : **le présent dossier remplace sa progression en sept séquences par cinq séances de deux heures**.

## Lire selon son rôle

- Préparer la formation : [références vérifiées](REFERENCES_SCIENTIFIQUES.md), [objectifs et prérequis](OBJECTIFS_ET_PREREQUIS.md), [progression et matrice d’évaluation](PROGRESSION.md).
- Distribuer aux élèves : [cours S01.1](SEANCE_01.md) avec [fiche de réponse S01.1](SUPPORT_ELEVE_S01.md) ; [cours S02](SEANCE_02.md), [fiche de réponse S02](SUPPORT_ELEVE_S02.md) et [activités S02](ACTIVITES_S02.md). Les [sujets TP du plan général](TP_ET_EXPERIENCES.md) restent disponibles. Les corrections sont distribuées séparément après recherche.
- Préparer et approfondir : [parcours enseignant](APPROFONDISSEMENTS_ENSEIGNANTS.md), [production attendue S01](PRODUCTION_ENSEIGNANT_S01.md), [enseignant S02](ENSEIGNANT_S02.md), [corrigés](CORRIGES.md), [évaluations](EVALUATIONS.md).
- Examiner la livraison courante : [audit S01.1/S02](AUDIT_S01_1_S02.md). L’[audit du pilote](AUDIT_SCIENTIFIQUE.md) est conservé comme historique.

Les corrections sont séparées matériellement pour leur distribution ; un dépôt public ne permet pas de les rendre confidentielles. L’enseignant distribue les seuls sujets avant la restitution.

## Périmètre de ce jalon

S01.1/S02 ont reçu un avis favorable à la poursuite. S03 est maintenant conçue pour les deux publics, avec TP03 autonome, supports et corrigés. Les **cours détaillés S04/S05 ne sont pas rédigés** ; les fiches et codes du plan général ne valent pas autorisation de les poursuivre. Les évaluations finales proposées n’annoncent pas un module complet déjà livré.

Durée : 10 h, cinq séances de 120 min, activités et évaluation incluses. Le parcours enseignant remplace certaines aides élèves par de l’analyse et de la lecture ; il ne consiste pas à ajouter des heures de cours savant à une séance déjà pleine. Approfondissements longs : travail facultatif hors des 10 h, explicitement identifié.

## Python et application : deux usages distincts

Le laboratoire existant sait afficher une grille fixe, exécuter une politique Python, choisir entre gloutonne/BFS/Python, tracer les actions et arrêter un Worker. Il ne propose ni éditeur de carte, ni observation masquée, ni mémoire Python persistante entre deux décisions, ni moteur d’agent LLM.

| Usage | Code / commande utilisateur | Effet réel |
|---|---|---|
| Console | Copier un script puis Exécuter Python | Exécute ses appels et imprime ses résultats ; ne modifie pas la carte graphique. |
| Politique de grille | Fournir `decider(position, objectif, obstacles)` puis Mon agent Python, Réinitialiser, Exécuter une étape | Le retour de `decider` commande un mouvement contrôlé par le moteur existant. |
| Diagnostic / transition / masque / glissement S02 | Fichiers `s01_diagnostic.py` et `s02_*` dans la console | Modèles et traces textuels autonomes, aucune fonction `decider` fournie pour piloter la grille. |

Seul un script comportant la fonction `decider` conforme peut être utilisé en mode politique ; `appliquer` n’est pas un point d’extension du moteur. Les exemples de mémoire du plan général gardent leur boucle dans **une seule exécution**, sans changement de Worker. Aucun appel à une API LLM.

Les scripts corrigés et les vérifications techniques sont rangés dans `python/`, avec les fichiers de départ distincts. Voir l’audit pour les commandes effectivement exécutées et la distinction CPython/Pyodide. Pour le pilote élève, copier seulement `python/tp01_depart.py` ; ne pas distribuer d’emblée le fichier de correction.

## Point d’arrêt

Validation attendue sur S03 : précision scientifique, progressivité, profondeur enseignant, adéquation Première/Terminale et temps proposés. **Arrêt après S03 : pas de rédaction des séances 04/05, pas d’intégration d’interface, pas de fusion, pas de déploiement.**
