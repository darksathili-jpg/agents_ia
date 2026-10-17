# U01 — Premier cours expérimental

**Commander n’est pas déplacer — version U01.1.** Consolidation documentaire de la version `6eed4029726681d116e831d06d4eb3263a863757`, conservée sur `docs/u01-premier-cours-experimental`. Branche de travail : `docs/u01-1-consolidation`. Document à relire ; aucune validation pédagogique par des élèves ni aucun essai humain n’est acquis.

## Documents et distribution

| Destinataire | Documents remis | Usage |
|---|---|---|
| Élève | [Cours élève](COURS_ELEVE.md) **et** [activités élève](ACTIVITES_ELEVE.md) | Les deux documents sont nécessaires ; aucun ancien cours requis. |
| Enseignant, préparation | [Parcours enseignant](PARCOURS_ENSEIGNANT.md) | Phénomène, mécanismes, traces, contre-exemples, formalisation facultative et exercice enseignant. |
| Après recherche | [Corrigés élèves et enseignant](CORRIGES.md) | Raisonnements et réponses alternatives ; ne pas les utiliser pour remplacer la recherche. |
| Enseignant, évaluation | [Grille de lecture](GRILLE_EVALUATION.md) | Distinguer preuve autonome, réponse avec relance et absence de preuve ; aucune note globale. |
| Relecture | [Deux audits et réserves](AUDIT_CRITIQUE.md) | Suffisance des consignes puis cohérence scientifique, avec résolution des sujets avant rédaction des corrigés. |

Les fichiers sont séparés pour la distribution, pas rendus confidentiels par le dépôt. La version n’est pas intégrée à l’application : ne pas présenter l’ancienne S01 HTML comme le présent cours U01.

## Déroulement élève indicatif

| Plage | Travail | Support |
|---|---|---|
| 0–3 min | Contexte, repérage C0 | Cours, partie 1. |
| 3–5 min | Prédiction individuelle P1 | Cours, partie 2. |
| 5–8 min | Première tentative guidée E1 | Laboratoire existant ou relevé fourni déclaré. |
| 8–10 min | Prédiction P2, seconde tentative E2 et comparaison E3 | Cours, partie 2. |
| 10–12 min | Explication progressive | Cours, partie 3. |
| 12–14 min | Entraînement essentiel A1 | Activités, partie A. |
| 14–17 min | Transfert individuel T1–T2 : Nora | Activités, partie T. |
| 17–20 min | Vérification individuelle I1–I2 : curseur | Activités, partie I. |

Budget cible de vingt minutes, tolérance de conception jusqu’à vingt-cinq : **hypothèse non mesurée**. Le parcours essentiel comprend toutes les lignes du tableau : les deux prédictions, l’expérience, l’explication, l’entraînement A1, le transfert et la troisième situation individuelle sont conservés. A2 et B1 sont des prolongements facultatifs **hors de ce budget**, pour approfondir ou reprendre après l’unité. Le Python enseignant et la formalisation facultative appartiennent à la préparation, pas au temps élève.

Lors d’un essai futur, relever pour chaque phase le temps de lecture, de réponse, de manipulation et l’aide donnée. Relever séparément installation technique et remédiation supplémentaire. Si le parcours essentiel déborde, noter la durée réelle et reprendre le temps nécessaire ; ne pas sacrifier prédiction, explication, transfert ou vérification finale pour afficher vingt minutes. Un dépassement récurrent de vingt-cinq minutes exige une révision du budget ou du découpage après relecture humaine.

## Comparaison précise avec U01 au commit de référence

| Réserve | Avant : `6eed402` | Après : U01.1 | Fichiers concernés |
|---|---|---|---|
| Vérification sur un troisième scénario | Le bilan B1 reprenait l’essai de Nora à porte fermée | I1–I2 étudient un curseur avec deux positions et des règles complètes ; tableau de deux essais puis justification d’un non-déplacement malgré la commande | ACTIVITES_ELEVE, CORRIGES, GRILLE_EVALUATION, COURS_ELEVE. |
| Essentiel et prolongements | A1–A2, Nora et B1 étaient tous inclus dans vingt minutes | A1 essentiel à 12–14, Nora à 14–17, I1–I2 à 17–20 ; A2/B1 conservés mais facultatifs hors budget ; premières phases inchangées | README, COURS_ELEVE, ACTIVITES_ELEVE, GRILLE_EVALUATION. |
| Exemple Python enseignant | Table de transition et formalisation expliquées, sans programme associé | Une fonction à trois paramètres, retours définis, quatre cas avec assertions et affichage, explication des branches et des erreurs d’entrée | PARCOURS_ENSEIGNANT. |
| Statut des contrôles | Réserve ouverte sur l’absence de troisième situation ; durée et essais humains non mesurés | Réserves rédactionnelles traitées documentées séparément des durées, de la compréhension et de l’efficacité restant à expérimenter | AUDIT_CRITIQUE. |

Les sept documents du dossier sont modifiés ; aucun autre fichier applicatif ou pédagogique n’est changé. La structure générale, la piste, les règles de la porte et les exercices enseignants existants sont conservés. Seules les trois réserves de consolidation sont traitées.

## Périmètre et arrêt

Seule U01 est consolidée. Aucun nouveau cours ultérieur, ancien TP corrigé, générateur lancé, page HTML produite ou interface modifiée. Le laboratoire reste un outil d’observation préexistant ; les transferts sont sur papier, pas des fonctionnalités ajoutées. Aucune programmation Python n’est demandée aux élèves ; le nouvel exemple Python est destiné uniquement à la préparation enseignante, sans modification du laboratoire ni de Pyodide.

Les audits vérifient la suffisance des énoncés et les règles du modèle, sans se substituer à une relecture indépendante ni à un essai auprès d’apprenants. Arrêt après cette livraison : attendre la relecture humaine complète avant toute révision convenue, intégration ou extension. Aucune fusion ni aucun déploiement.
