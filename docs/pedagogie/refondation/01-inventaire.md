# Refondation — inventaire et état conservé

Date : 17 octobre 2026. **Tous les contenus sont à réexaminer. Aucune validation pédagogique antérieure n’est tenue pour acquise.** « Réutilisable » signifie matériau candidat, jamais cours validé ou prêt à distribuer.

Livraison limitée à cinq documents : cet [inventaire](01-inventaire.md), l’[audit et registre des défauts](02-audit.md), l’[architecture proposée](03-architecture.md), le [cahier de conception de la première unité](04-premiere-unite.md) et ses [critères de validation](05-validation.md). Aucun nouveau cours, support élève, exercice prêt à distribuer ou code applicatif n’est produit.

## État exact de départ et préservation

Arbre propre au démarrage. Branche créée : `docs/refondation-pedagogique`, depuis `feature/module-01-s01-visible`, commit `a1d977bd1cfb6699dd7b9db053c5c662b0565151`. Toutes les branches existantes sont conservées. La vérification distante est une lecture `git ls-remote --heads origin`, pas un push ni un fetch modifiant les références locales.

| Branche | Pointe locale observée | Pointe distante observée | Interprétation |
|---|---|---|---|
| `main` | `9843544acd036fce668dfe2a128727e09720ca24` | Identique | Non modifiée. |
| `docs/module-01-conception-pilote` | `4526e321a205babb7390e75dfc036ac7aedf884d` | Identique | Pilote et AGENTS.md conservés. |
| `docs/module-01-s01-1-s02` | `bf009acb226ce6a53453529d72fa27ebf6f7af96` | Identique | Consolidation S01/S02 conservée. |
| `docs/module-01-s03` | `a27fbff516129ad5915916b659386692c8cc7021` | Identique | Conception S03 conservée. |
| `feature/agent-academy-art-direction` | `2a9ed397c6aea27e12c99700adecafee1670fae7` | `13d5284b2700341b493404dbe50549ea5c1a64ea` | Un commit local de stabilisation supplémentaire ; aucune tentative de synchronisation. |
| `feature/agent-academy-mvp` | Pas de branche locale de ce nom | `3670b3dc40a4d5b558413d6830a8e852485bef38` | Référence distante seulement. |
| `feature/module-01-s01-visible` | `a1d977bd1cfb6699dd7b9db053c5c662b0565151` | Absente de la liste distante | Prototype local préservé ; ne pas annoncer sa publication. |

Les SHA de cette table sont complets. L’audit n’effectue ni fusion, ni déploiement, ni publication de branche. AGENTS.md, les cours, le générateur et les pages restent intacts ; leurs annonces historiques ne sont pas mises à jour pour ne pas modifier l’application indirectement. S04/S05 restent suspendues.

## Corpus documentaire S01–S03

Base des chemins de ce tableau : `docs/pedagogie/module-01/`.

| Ensemble | Fichiers inventoriés | Matériau à conserver | Condition de réemploi |
|---|---|---|---|
| S01 élève | `SEANCE_01.md`, `SUPPORT_ELEVE_S01.md` | Deux tentatives devant un mur, distinction commande/effet, contre-test d’une cible à gauche | Extraire une question par unité ; différer la classification et le vocabulaire abstrait. |
| S01 enseignant | `PRODUCTION_ENSEIGNANT_S01.md`, parties S01 de `APPROFONDISSEMENTS_ENSEIGNANTS.md` | Trace complète, frontières fonction/contrôleur/moteur, comparaison conditionnelle des coûts | Partir d’un problème résolu et d’une erreur commentée avant les symboles. |
| S02 élève | `SEANCE_02.md`, `SUPPORT_ELEVE_S02.md`, `ACTIVITES_S02.md` | Tests de refus et de bord, comparaison état/observation, deux historiques sous parcours imposé | Séparer transition, information partielle et hasard ; expliciter tuples, dictionnaires et `None`. |
| S02 enseignant | `ENSEIGNANT_S02.md` | Différence entre information présente et reçue, conditions du contre-exemple | Conserver la portée conditionnelle ; différer noyaux probabilistes et équivalences formelles. |
| S03 élève | `SEANCE_03.md`, `SUPPORT_ELEVE_S03.md`, `CORRIGES_S03.md` | Comparaison oubli/écrasement/conservation, traces mémoire avant/après, indice absent ou faux | Protocole à revoir avant toute utilisation comme preuve de nécessité de mémoire ; défaut F01. |
| S03 enseignant | `ENSEIGNANT_S03.md` | Invariant, hypothèses du modèle, contre-exemples, distinction politique/transition stochastiques | Faire correspondre preuve, tâche réellement autorisée et code ; définir chaque notation à partir d’exemples. |
| Transversal | `OBJECTIFS_ET_PREREQUIS.md`, `PROGRESSION.md`, `TP_ET_EXPERIENCES.md` | Objectifs formulés comme capacités, cas de test, repères de progression | Reconstruire les dépendances ; les anciens blocs de 120 min ne sont pas des unités indivisibles. |
| Corrections et évaluation | `CORRIGES.md`, `EVALUATIONS.md` | Explications de refus, cas discriminants, possibilités de remédiation | Refaire l’alignement unité/épreuve et les niveaux de maîtrise ; seuils non validés. Les propositions S5 restent historiques. |
| Bibliographie | `REFERENCES_SCIENTIFIQUES.md` | Sources identifiées, distinction manuel/publication/guide, réserves d’édition | Rattacher un extrait précis et une question de lecture à un besoin, sans transformer la bibliographie en leçon. |
| Historiques | `README.md`, `AUDIT_SCIENTIFIQUE.md`, `AUDIT_S01_1_S02.md`, `AUDIT_S03.md` ; note `../module-01-fondements-scientifiques.md` | Traçabilité des choix, limites techniques et anciennes intentions | Les mentions favorables et tests passés ne constituent aucune validation pédagogique actuelle. |

## Python et tests : ressources, pas preuve d’apprentissage

| Fichiers dans `module-01/python/` | Usage réel / réutilisation envisageable |
|---|---|
| `s01_diagnostic.py`, `tp01_depart.py`, `s01_solution_interface.py` | Appels, retours et règle sur coordonnées ; réserver à l’unité où les fonctions ont été comprises. |
| `s02_obstacle_depart.py`, `s02_corrige.py` | Programmation de la transition en console ; ce ne sont pas des politiques branchées sur la grille. |
| `s02_observation_masquee.py` | Observations de deux mondes après droite puis bas imposés ; expérience textuelle, sans masque graphique. |
| `s03_depart.py`, `s03_tp.py` | Boucle autonome dans une seule exécution, mémoire explicite. **Réemploi suspendu comme protocole démonstratif jusqu’à traitement de F01.** |
| `tp02_depart.py` à `tp05_depart.py`, `corriges.py` | Anciens supports du plan général ; distinguer les amorces génériques des supports courants. Aucune reprise de S04/S05 autorisée. |
| `tests_experiences.py`, `tests_s01_s02.py`, `tests_s03.py` | Tests de comportements programmés et de cas limites ; couverture du protocole d’indiscernabilité insuffisante en S03. |
| `valider_dossier.py`, `verifier_pyodide.mjs` | Contrôles documentaires et d’exécution réelle ; ni mesure de compréhension ni validation de la progression. |

## Liens effectifs avec l’application

Les chemins de ce tableau sont relatifs à la racine du dépôt.

| Élément | Liens et contenu actuels | Limite pédagogique |
|---|---|---|
| `index.html` | Navigation Module 01 et vignette vers `module01.html` ; accès direct au laboratoire conservé | Plusieurs portes d’entrée, dont une peut contourner la progression. |
| `module01.html` | S01 intégrée ; S02/S03 vers les ancres documentaires ; S04/S05 à venir | Disponibilité technique à distinguer de validité pédagogique. |
| `seance01.html` | Dix sections issues de S01, questions, diagnostic, bilan ; deux cadres `laboratoire.html?s01=…` | Longue page et deux états de laboratoire indépendants, pas une unique expérience continue. |
| `enseignant-s01.html` | Sélection des approfondissements, production attendue, correction, bibliographie | Distinct du parcours élève mais juxtapose encore plusieurs niveaux d’abstraction. |
| `ressources-module01.html` | Conversion documentaire, notamment ancres `seance_02` et `seance_03` ; supports et corrigés | Lecture HTML des documents, pas intégration pédagogique S02/S03. |
| `scripts/construire-formation.py` | Génère les quatre pages précédentes depuis le corpus, avec compléments écrits dans le script | Questions, diagnostic et réponses attendues ont plusieurs sources de vérité. Ne pas le lancer dans cette mission. |
| `formation.js`, `formation.css` | Notes locales, export, affichage, comparaison avec le journal, trois questions de repérage | La comparaison juxtapose des textes ; le raisonnement libre n’est pas évalué. |
| `laboratoire.html`, `laboratoire-s01.js`, `python-worker.js` | Grille réelle, règles/BFS/Python ; adaptateur de départ S01 ; véritable Pyodide | Console et grille distinctes ; aucune mémoire Python persistante entre décisions de grille. |
| `tests/*.spec.mjs` | Tests navigateur, clavier, thèmes, Pyodide et parcours | Vérifient des interfaces et sorties attendues, pas le raisonnement d’apprenants. |
| `docs/visualisation-s01/`, `docs/art/captures/v2/` | Bilan, démonstration et captures conservées | Archives visuelles ; ni agrément pédagogique ni nouvelle validation artistique. |
| `Ouvrir-Agent-Academy.cmd`, `scripts/ouvrir-academy.py` | Lancement local HTTP | Infrastructure réutilisable, sans incidence sur la valeur d’une leçon. |

## Décision de conservation

Conserver sans modification les branches, sources, scripts, tests et captures. Priorité de réemploi : trace réelle commande/effet, cas discriminants, puis progression vers fonction et observation partielle. Les définitions, formalismes et bibliographies sont des ressources d’auteur à remanier ultérieurement, après accord ; ils ne sont pas validés par leur présence dans un dépôt ou par leur longueur.
