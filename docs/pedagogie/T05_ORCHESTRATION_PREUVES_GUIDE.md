# ORCHESTRA NSI — Terminale T05 · Orchestration, états et preuves

**Statut :** candidate de recette. Ne pas fusionner dans `main` ni publier
avant une décision humaine et une recette visuelle.

## Positionnement pédagogique

Trois séances de 55 minutes après T04.
Les apprentissages en NSI s'appuient sur les structures de données
(dictionnaire, liste, ensemble), les instructions conditionnelles, la
décomposition fonctionnelle, la spécification d'interfaces, les tests
de programmes et le raisonnement sur les invariants.

L'« agent orchestré » et le « rapport trompeur » sont **un contexte d'application
complémentaire**, pas des notions annoncées comme faisant partie des programmes
officiels de Terminale NSI.

Les élèves distinguent les informations provenant de l'agent de celles
issues d'une vérification indépendante. Ils expliquent pourquoi un énoncé
« j'ai réussi » ne constitue ni une preuve ni une permission.

## Contrat Python

L'élève écrit `controler_mission(mission, rapport, registre)` et renvoie
**exactement** `{"etat": "...", "motif": "..."}` sans modifier les paramètres.

- `mission` : révision attendue, ensemble de fichiers autorisés, ensemble
  de tests requis, approbation humaine requise, décision humaine éventuelle.
- `rapport` : déclaration **non fiable** de l'agent (révision, fichiers
  déclarés, identifiants de preuves, succès annoncé).
- `registre` : résultats de tests **indépendants du rapport** dans le banc
  de vérification de l'activité. Pour chaque identifiant : test, révision,
  résultat réel booléen `reussi`.

### Machine à états

| État | Événement | Nouvel état | Effet autorisé |
|---|---|---|---|
| SPÉCIFIÉE | Début du contrôle | EN VÉRIFICATION | Aucun |
| EN VÉRIFICATION | Contrat invalide, fichier interdit ou preuve douteuse | BLOQUÉE | Aucun |
| EN VÉRIFICATION | Preuves conformes, validation humaine nécessaire | ATTENTE_HUMAINE | Aucun |
| EN VÉRIFICATION | Preuves conformes, pas de validation humaine nécessaire | VALIDÉE | Au plus un déplacement |
| ATTENTE_HUMAINE | Accord externe explicite après re-vérification | VALIDÉE | Au plus un déplacement |
| ATTENTE_HUMAINE | Refus de la personne | BLOQUÉE | Aucun |
| BLOQUÉE | Rapport inchangé | BLOQUÉE | Aucun |
| VALIDÉE | Rapport terminé | VALIDÉE | Aucun nouvel effet |

*Les deux premiers états sont pilotés par le simulateur d'orchestration.
La fonction Python élève renvoie l'un des trois états de sortie :
`BLOQUÉE`, `ATTENTE_HUMAINE`, `VALIDÉE`.*

### Vérifications minimales

L'orchestrateur rejette les structures mal formées et les champs inconnus.
Les modifications déclarées doivent être dans la liste blanche de la mission.
Le rapport doit porter exactement sur la révision attendue.
Les identifiants de preuves sont recherchés dans le registre ; un identifiant
inventé n'est jamais une preuve, même si le rapport annonce une réussite.
Tous les tests obligatoires doivent avoir un résultat réel réussi, vérifié
sur cette révision, exactement une fois. Les résultats échoués et les tests
imprévus sont des anomalies. Enfin, si l'opération requiert un humain,
l'accord doit venir du champ `decision_humaine` de la mission, **jamais
du rapport de l'agent**.

### Invariant central

**Si l'état n'est pas `VALIDÉE`, Microduck ne se déplace pas.**
Un changement d'état ne produit pas automatiquement une action.
Une validation ne doit donner lieu qu'à **un seul** déplacement réel,
pas un déplacement par instruction de journal ni par étape de vérification.

## Déroulement des trois séances

### Séance 1 — S'interroger sur la fiabilité d'un rapport

1. Choisir le scénario « Rapport honnête » et prédire le résultat.
2. Passer à « Agent trompeur : faux succès » : comparer sa déclaration
   avec l'échec visible dans le registre des tests.
3. Identifier la transition vers `BLOQUÉE` et constater l'absence de mouvement.
4. Répéter avec un fichier non autorisé, une preuve inventée et une mauvaise
   révision ; distinguer une **déclaration** d'une **observation vérifiée**.
5. Simuler une approbation nécessaire puis choisir de l'accepter ou la refuser.

Question diagnostic : « L'agent a indiqué une réussite : la mission doit-elle
être validée ? » Réponse attendue : **non, pas sans preuve indépendante valide**.

### Séance 2 — Programmer et vérifier

1. Lire le contrat de `controler_mission` dans `terminale/t05/eleve.py`.
2. Commencer par les conditions de refus : clés exactes, types, révision,
   périmètre et identifiants distincts.
3. Écrire une **boucle bornée** qui consulte chaque preuve dans le registre
   indépendant et mémorise les tests réellement validés dans un ensemble.
4. Comparer cet ensemble aux tests requis et gérer `ATTENTE_HUMAINE`.
5. Exécuter 19 tests Python ; trois situations changent leurs noms de
   fichiers et de tests afin de repérer les réponses codées en dur.
6. Consulter une trace réelle de l'exécution Python et la confronter
   à la démonstration JavaScript.

Aides calibrées : identifier les clés des dictionnaires, utiliser
`set(...)` pour les doublons, écrire un refus avant la validation,
relire le contrat d'approbation humaine.

### Séance 3 — Justifier et transférer

Faire rédiger une justification sans indices du blocage d'un agent qui ment,
puis demander pourquoi une preuve portant sur la bonne fonction mais la
mauvaise révision est insuffisante. Comparer les rôles :
l'agent propose, le vérificateur mesure, l'orchestrateur décide,
la personne approuve si nécessaire, le monde applique.

Pour aller plus loin : réfléchir à la chaîne de provenance d'un test réel,
notamment au risque de contrefaçon d'un registre purement déclaratif.
Un véritable dispositif de sécurité demanderait une attestation des
résultats, des permissions système et une isolation d'exécution adaptées.

## Recette et séparation des ressources

- `python -m pytest -q qa_enseignant/test_t05.py`
- `node tests/test_t05_visualizer.cjs`
- `python tests/browser_t05.py` (Chromium et Pyodide **local**)
- `python scripts/build_site.py --allow-cdn` en développement,
  uniquement pour inspecter la liste blanche.

Les tests Python utilisent 19 situations dont un agent qui annonce
un succès alors qu'un test du registre a échoué, une auto-approbation
fabriquée et des preuves d'une autre révision. La référence enseignant
est dans `qa_enseignant/test_t05.py`, hors du site publié.
La simulation JavaScript est **indépendante** de la réponse de l'élève ;
elle ne lui attribue aucun score. Les verdicts élève affichés par la page
proviennent de `runner_t05.py` dans un Worker Pyodide.

**Limites :** registre, accord humain et mouvement sont simulés.
Aucune action externe réelle, aucune preuve cryptographique et aucune
promesse de résistance à un utilisateur malveillant. L'AST filtré
et Pyodide ne constituent pas une sandbox sûre pour du code hostile.
Ce module s'utilise dans un contexte scolaire supervisé.

Pour examiner les traces navigateur et captures de recette, consulter
les artefacts `captures-t05-chromium` de la CI, sans publier `main`.
