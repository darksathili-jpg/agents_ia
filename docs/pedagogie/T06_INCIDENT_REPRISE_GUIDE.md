# ORCHESTRA NSI — T06 · Incident et reprise contrôlée

## Statut et positionnement

**Mission Terminale NSI, trois séances de 55 minutes, après T05.**
La modélisation d'une machine à états et d'un orchestrateur d'agents est
un **contexte pédagogique d'application**. Il ne faut pas la présenter comme
un chapitre ajouté au programme officiel de Terminale NSI.

Compétences mobilisées : types construits et dictionnaires, ensembles, tuples,
instructions conditionnelles, boucles bornées, fonctions et contrats
d'interface, conception de jeux de tests, assertions, vérification d'invariants
et justification de choix algorithmiques.

**Objectif central :** un incident ne disparaît pas du seul fait qu'un agent
annonce un correctif. La reprise nécessite des preuves *nouvelles*, obtenues
par une source indépendante, un point sûr cohérent et, si nécessaire, une
approbation humaine. Même une reprise autorisée ne doit jamais déclencher
implicitement une action.

## Machine à états

La démonstration sépare les états successifs :

1. `INCIDENT_DÉTECTÉ` : arrêt immédiat, aucun mouvement.
2. `BLOQUÉE` : quarantaine, action impossible.
3. `CORRECTIF_PROPOSÉ` : le rapport non fiable est reçu, mais rien n'est validé.
4. `EN_REVÉRIFICATION` : contrôle des fichiers, de la révision, du point sûr
   et des preuves nouvelles.
5. Trois états de décision :
   - `BLOQUÉE` si le correctif ou les preuves sont insuffisants ;
   - `ATTENTE_HUMAINE` si tout est conforme sauf l'approbation ;
   - `REPRISE_AUTORISÉE` si toutes les conditions sont réunies.
6. `REPRISE_EXÉCUTÉE` seulement après une action distincte, explicite et unique.

Le premier état `BLOQUÉE` est un blocage temporaire permettant le dépôt
d'un correctif. Le second `BLOQUÉE`, en sortie de revérification, est une
décision définitive pour ce dossier : une nouvelle tentative requiert un
nouveau cycle, pas une validation automatique.

**Invariant visuel :** Microduck reste en `(0,1)` dans tous les états
autres que `REPRISE_EXÉCUTÉE`. Après l'autorisation et le clic de reprise,
il atteint `(1,1)` en un et un seul déplacement.

## Contrat Python de l'élève

Compléter `decider_reprise(mission, incident, correctif, registre)` dans
`terminale/t06/eleve.py`, sans import ni modification des paramètres.

La fonction renvoie exactement un dictionnaire avec :
`etat` parmi `BLOQUÉE`, `ATTENTE_HUMAINE`, `REPRISE_AUTORISÉE`
et `motif`, chaîne non vide.

Les quatre dictionnaires ont des clés strictement définies dans le squelette.
Le **registre** est construit indépendamment du rapport de l'agent dans la
simulation. Les preuves doivent correspondre à **tous** les tests obligatoires,
être marquées réussies et provenir de la **révision cible** différente de
celle de l'incident. Le correctif ne doit modifier aucun fichier hors de la
liste blanche ; toutes les déclarations et tous les identifiants de preuve
doivent être uniques et bien formés. Le dernier point sûr doit correspondre
au point de reprise attendu, dans la grille 6 × 3, avec des coordonnées de
type entier (et non des booléens).

L'approbation humaine éventuelle se trouve dans `mission`, et non dans
le rapport du correctif. La mention `accord_humain` ajoutée par l'agent
est un champ inattendu et provoque un refus.

**Principe de non-confiance :** un `succes_annonce=True` ne prouve jamais
à lui seul que les tests ont été refaits. Seul le registre distinct et
conforme permet de passer l'étape de vérification.

## Séance 1 — Observer un incident (55 minutes)

Faire comparer les scénarios « Correctif vérifié » et « Test encore en échec ».
Dans les deux cas, le rapport peut annoncer une réussite. Identifier le
statut effectif dans le registre ; mesurer le déplacement (zéro sans reprise).
Faire passer un dossier par les étapes de la machine et exiger une prédiction
argumentée du prochain état avant chaque clic.

Puis choisir « Preuve de l'ancienne révision » : le test peut avoir
réussi par le passé, mais il n'est pas une preuve du nouveau correctif.
Faire formuler cette nuance explicitement.

## Séance 2 — Programmer, confronter (55 minutes)

Travail individuel ou par binômes sur le squelette Python.
Aides progressives : relever les clés des dictionnaires, vérifier les types
et la révision, comparer les tuples du point sûr, utiliser des ensembles pour
refuser les doublons, consulter chaque preuve avec une boucle bornée,
et produire un motif explicite pour chaque décision.

Les **19 situations** incluent trois contrôles variables, où les noms de
fichiers, de tests et les révisions changent entre exécutions.
Les résultats affichés par la page proviennent du vrai code de l'élève
dans Pyodide, pas de l'animation JavaScript.

## Séance 3 — Justifier et transférer (55 minutes)

Faire expliquer sans indices les trois distinctions :
**proposer un correctif**, **prouver qu'il fonctionne**, **autoriser puis
déclencher sa reprise**. Demander pourquoi un point sûr discordant bloque
même si les tests sont réussis et pourquoi le clic de reprise est distinct
de l'état `REPRISE_AUTORISÉE`.

Évaluation humaine : cohérence de l'argumentation, vocabulaire des
dictionnaires et des variables, compréhension des invariants, capacité à
prévenir une répétition d'incident, distinction entre preuve indépendante
et déclaration de l'agent.

## Recette et limites

- `python -m pytest -q qa_enseignant/test_t06.py`
- `node tests/test_t06_visualizer.cjs`
- `python tests/browser_t06.py` (Playwright Chromium, Pyodide local)
- Contrôles de non-régression T01 à T05 via GitHub Actions.
- `python scripts/build_site.py --allow-cdn` pour inspecter uniquement
  le périmètre du site, **sans publier**.
- Captures T06 dans l'artefact `captures-t06-chromium` du workflow.

La solution témoin reste dans `qa_enseignant/test_t06.py`, exclue des
ressources publiques. Les trois approbations et les registres sont **simulés**.
Le module ne restaure pas de fichiers et ne lance aucune commande réelle
sur Git ou sur un robot physique. Aucun test ne remplace une attestation
cryptographique ni une politique de permissions système.

Pyodide et le filtrage AST ne sont pas une sandbox contre du code hostile :
activité scolaire supervisée uniquement.

**Garde-fou de livraison :** ne pas fusionner dans `main` ni déclencher
la publication sans décision humaine explicite et recette visuelle.
