# Guide enseignant — ORCHESTRA NSI v5.1, séance 01

## Positionnement

**Première NSI, 35–45 minutes.** Prérequis : savoir définir une fonction simple et utiliser `if`, `return`, dictionnaires et booléens. L'activité fait construire un **agent réflexe** (décision sans mémoire) ; elle ne prétend pas faire programmer un LLM, un outil distant ou un orchestrateur multi-agents.

## Compétences évaluables

1. Identifier l'objectif de l'agent et les limites du monde simulé.
2. Expliquer le sens des quatre données `arrive`, `orientation`, `balise`, `devant_libre`.
3. Rédiger une fonction de décision Python et respecter l'indentation des blocs.
4. Justifier pourquoi `devant_libre=False` interdit l'action `AVANCER`, même si une balise périmée suggère cette direction.
5. Distinguer une simulation visuelle des décisions effectivement produites par Python.
6. Analyser les traces de **quatre terrains**, dont un inédit, et expliquer pourquoi réussir trois terrains connus ne garantit pas une stratégie générale.
7. Exporter une preuve : prédiction, nombre d'essais, résultats et code.

## Déroulé possible

| Moment | Durée | Action de l'élève | Trace observable |
|---|---:|---|---|
| Comprendre | 5 min | Identifier le robot, son objectif, l'absence de robot réel et de LLM. | Définition orale de l'agent réflexe. |
| Observer sans coder | 5 min | Choisir l'action sur les quatre observations de démonstration. | Explication des choix. |
| Formuler une prédiction | 3 min | Anticiper la première action sur le terrain 1. | Prédiction enregistrée. |
| Programmer | 12–17 min | Créer `decider(observation)` et corriger les erreurs d'indentation. | Code Python et essais. |
| Vérifier | 7 min | Lancer quatre terrains + 16 sondes de sûreté ; explorer la trace. | Verdict et justification d'une décision. |
| Transférer | 5 min | Décrire la stratégie utilisée et ses limites ; exporter un bilan. | Bilan JSON et justification courte. |

## Différenciation

- **Débutant :** commencer par `arrive`, puis ajouter le contrôle `devant_libre` avant la décision d'avancer. Les indices progressifs ne dévoilent pas immédiatement le code.
- **Intermédiaire :** comparer deux solutions correctes (rotation à gauche/droite) et expliquer l'effet sur le nombre d'étapes.
- **Approfondissement :** expliquer pourquoi la balise BFS est un capteur **assisté par le moteur** et non une compétence codée par l'élève. En Terminale, étudier le parcours en largeur comme algorithme de graphe.

## Évaluation conseillée

- **Fonctionnement et sécurité (40 %) :** quatre terrains réussis et contrôle `devant_libre=False` satisfait.
- **Compréhension (30 %) :** identification d'un état, d'une action et de l'objectif.
- **Vérification (20 %) :** utilisation pertinente des traces et comparaison prédiction/résultat.
- **Qualité du code (10 %) :** fonctions simples, commentaires pertinents, indentation et absence de code inutile.

**Limite pédagogique assumée :** l'élève programme seulement la phase « décider » ; l'observation, l'action et la vérification sont prises en charge par le moteur Python. La balise BFS fournit déjà un chemin pour diminuer la difficulté ; cela ne doit pas être présenté comme une conception complète d'un agent autonome.

## Vérification avant le cours

Vérifier la connexion aux ressources Pyodide, l'exécution sous Edge, la récupération après boucle infinie, les trois modes d'affichage et l'export dans les conditions du lycée. Prévoir un plan alternatif si le CDN est bloqué.


## Expérience concrète de la balise périmée (v5.1)

1. Demander ce que le robot doit faire lorsque `balise == orientation` mais `devant_libre is False`.
2. Ouvrir le terrain 2, première décision. Le moteur a calculé une direction vers l'est, puis a ajouté un obstacle devant le robot avant l'appel à `decider`.
3. Comparer `balise = "E"`, `orientation = "E"`, `devant_libre = False` et la décision retournée.
4. Vérifier qu'une solution ignorant `devant_libre` échoue désormais sur le terrain 2 (collision refusée), pas uniquement sur le banc de tests.
5. Préciser : les 16 sondes de sûreté renforcent la couverture mais ne sont pas une preuve formelle de sûreté.

L'élève ne programme toujours ni BFS, ni classe d'agent. Ces compétences sont réservées à un **autre parcours**, adapté à la Terminale.
