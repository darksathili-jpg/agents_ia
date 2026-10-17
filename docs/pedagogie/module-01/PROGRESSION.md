# Architecture pédagogique — cinq séances de deux heures

Chaque séance suit situation, observation, hypothèses, formalisation, Python, analyse, transfert et synthèse. Les minutes ci-dessous sont **une hypothèse de planification**, pas des temps mesurés en classe. Seule la [séance 01](SEANCE_01.md) est un cours rédigé à ce jalon. Les autres lignes sont des spécifications à valider.

| Séance | Répartition des 120 min | Production et évaluation formative |
|---|---|---|
| S1 — Qu’est-ce qu’un agent intelligent ? | Problème 10 ; observation/hypothèses 15 ; concepts et classification 25 ; TP01 40 ; discussion/transfert 20 ; synthèse 10 | Carte de système, code réactif, deux traces et billet de sortie. E01–05 ; O1/O3/O4/O5. |
| S2 — Environnement, observations et actions | Retour 10 ; états/observations 20 ; TP02 obstacle 30 ; grille masquée préparatoire TP03 25 ; formalisation 15 ; transfert/synthèse 20 | Trace refus/transition, deux mondes indiscernables. E06–07/E10 ; O2/O8. |
| S3 — Architectures et politiques | Problème 10 ; modèles conceptuels 20 ; TP03 mémoire 35 ; comparaison déterministe/stochastique 20 ; objectifs/utilité 15 ; analyse/synthèse 20 | État interne mis à jour, distinction mémoire/modèle, classement non exhaustif. E08–09/E11 ; O4/O6/O9. |
| S4 — Programmer et expérimenter | Rappel 10 ; boucle et tests 20 ; TP04 recherche 50 ; comparaison et cas limites 25 ; transfert/synthèse 15 | Chemin, preuve conditionnelle, cas sans solution. E12/E14 ; O5/O7/O8. |
| S5 — Évaluer et préparer les LLM | Critères 10 ; TP05 mesures 25 ; transfert LLM et lecture 15 ; épreuve individuelle 60 ; retour ciblé 10 | Tableau reproductible, analyse et code ; E13/E15 ; O3/O7/O8/O9/O10 et épreuve finale. |

**Total : 600 min = 10 h**, pauses exclues. Les 15 exercices sont une banque : cinq brefs intégrés au pilote, les autres répartis dans les activités ou donnés comme variantes. Ne pas les ajouter tous aux créneaux de TP. L’évaluation finale est ramenée à 60 min, incluse en S5 ; une épreuve de 2 h rendrait cette progression incompatible avec 10 h.

## Parcours enseignant : travail différent dans la même enveloppe

Chaque séance inclut une lecture critique de 10–15 min, prise dans le temps de concepts/analyse : S1 confronter deux cadres ; S2 mémoire suffisante et observation ; S3 modèles d’architecture et utilité ; S4 garantie/coût BFS ; S5 limites de ReAct. Le code élève de base est alors fourni pour libérer du temps de conception, preuve et transposition. Le fichier d’approfondissement contient aussi des prolongements **facultatifs hors des 10 h** ; ils ne sont pas des prérequis de réussite.

## Matrice objectifs / activités / évaluation finale

| Objectifs | Activités préparatoires | Épreuve NSI | Épreuve enseignant |
|---|---|---|---|
| O1/O3 | Classification de S1, E01–03/E15 | Vocabulaire et frontière du système | Confrontation de définitions et contre-exemple |
| O2/O4/O6 | Trace, masque et mémoire, E04/E06–09 | Observation/action et trace | Deux historiques, insuffisance d’une politique sans mémoire |
| O5 | TP01/TP02/TP04, E05/E12 | Politique avec validation locale | Construction et tests d’un contrôleur à mémoire |
| O7/O8/O10 | TP05, E10/E13/E14 | Lecture de tableau et métrique | Protocole discriminant, traitement des échecs et hypothèses |
| O9 | Tirage contrôlé S3, transfert S5 | Hasard ≠ LLM | Portée d’une comparaison et séparation modèle/système |

## Frontières techniques et choix de charge

- TP01/02 : appels directs et, après explication, connexion à la grille existante.
- TP03 : grille masquée textuelle et mémoire dans un script console autonome ; aucune persistance ajoutée au Worker.
- TP04/05 : banc textuel avec cartes passées en paramètres ; pas d’éditeur de cartes annoncé.
- Comparaison LLM : dossier d’interaction fourni et lecture, sans API ni agent LLM prétendument exécuté.

Si une classe de Première découvre les tuples : réduire le nombre de cas, fournir le conducteur et observer BFS sans exiger sa construction. Si un groupe enseignant nécessite une remise à niveau Python : prévoir un pré-module, pas une surcharge dissimulée. Un essai de durée avec des apprenants reste indispensable avant de figer les 10 h.
