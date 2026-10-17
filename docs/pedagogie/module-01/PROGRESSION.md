# Architecture pédagogique — cinq séances de deux heures

Chaque séance suit situation, observation, hypothèses, formalisation, Python, analyse, transfert et synthèse. Les minutes ci-dessous sont **une hypothèse de planification**, pas des temps mesurés en classe. Les séances 01, 02 et [03](SEANCE_03.md) sont rédigées ; les lignes S4/S5 restent des spécifications, sans cours rédigés.

| Séance | Répartition des 120 min | Production et évaluation formative |
|---|---|---|
| S1 — Qu’est-ce qu’un agent intelligent ? | Diagnostic 8 ; problème 7 ; observation 6 ; hypothèses 4 ; concepts/classification 20 ; TP01 40 ; analyse 15 ; transfert 10 ; bilan 10 | Fiche élève remplie, diagnostic, code, deux traces et billet individuel. E01–05 ; O1/O3/O4/O5. |
| S2 — Environnement, observations et actions | Retour/problème 10 ; état/observation 15 ; TP02 30 ; déterminisme/glissement 15 ; masque 25 ; formalisation/transfert 15 ; bilan 10 | Trace, transition modifiée, deux mondes indiscernables, bilan B1–B5. Exercices S02-A–G ; O2/O4/O8, préparation O6. |
| S3 — Architectures, politiques et mémoire | Rappel 10 ; traces prédictives 15 ; contrat/mémoire 15 ; TP03 40 ; limites 15 ; architectures et hasard 15 ; bilan 10 | Deux mondes testés, mémoire tracée, erreur expliquée et limite explicitée. Exercices S03-A–G et B1–B5 ; O4/O6/O9. |
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

- TP01 : appels directs puis connexion à la grille existante ; TP02 courant : transition textuelle en console, sans substitution au moteur.
- TP03 : grille masquée textuelle et mémoire dans un script console autonome ; aucune persistance ajoutée au Worker.
- TP04/05 : banc textuel avec cartes passées en paramètres ; pas d’éditeur de cartes annoncé.
- Comparaison LLM : dossier d’interaction fourni et lecture, sans API ni agent LLM prétendument exécuté.

Si une classe de Première découvre les tuples : réduire le nombre de cas, fournir le conducteur et observer BFS sans exiger sa construction. Si un groupe enseignant nécessite une remise à niveau Python : prévoir un pré-module, pas une surcharge dissimulée. Un essai de durée avec des apprenants reste indispensable avant de figer les 10 h.
