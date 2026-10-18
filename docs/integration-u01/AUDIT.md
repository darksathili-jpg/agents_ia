# Intégration U01.1 — audit des accès et limites

Branche : `feature/u01-1-integration-interactive`. Référence scientifique : `fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6`. Inspection et contrôles techniques le 18 octobre 2026 ; aucun essai humain déclaré.

## Chemins qui présentaient le prototype invalidé

| Accès constaté avant intervention | Problème | Traitement |
|---|---|---|
| `Ouvrir-Agent-Academy.cmd` → `scripts/ouvrir-academy.py` → `module01.html` | Ouvre le catalogue S01–S03 ; S01 est annoncée intégrée, les autres contenus disponibles. | Le même lanceur ouvre directement `u01.html`. |
| `index.html`, lien Module 01 et carte du parcours | Annonce « S01 intégrée », programme Python et documents S02/S03 disponibles. | Carte U01.1 ; module réduit aux accès élève et enseignant U01.1. Identité V2 conservée. |
| Accueil → « Commencer l’aventure » et liens laboratoire | Commencer conduisait au laboratoire ancien sans la nouvelle leçon. | Commencer ouvre U01.1 ; les accès laboratoire restants ouvrent la présentation U01.1 du moteur réel. |
| Accueil, présentation du labo et texte interactif `accueil.js` | Demande de comparer BFS et gloutonne, hors de cette unité. | Invitation à l’observation des deux tentatives ; aucune comparaison BFS demandée. L’illustration historique de détour est conservée comme illustration, pas comme expérience à réaliser dans U01.1. |
| `seance01.html` | Diagnostic print/return, catégories d’agents, TP01, bilan et seuils non validés. | Favori remplacé par une redirection relative vers U01.1, avec lien de secours. |
| `enseignant-s01.html` | Préparation scientifique rattachée à l’ancienne séance. | Redirection vers le parcours enseignant U01.1 complet. |
| `ressources-module01.html` et ses ancres | Présente tout le corpus historique S01–S03 comme documents de formation accessibles. | Redirection vers la préparation U01.1 ; pas de liens ordinaires vers l’ancien corpus. |
| `laboratoire.html`, et variantes `?s01=observation` / `?s01=python` | Contient des définitions, QCM, consignes BFS et atelier de l’ancien prototype. | Présentation active reconstruite sans ces textes. Seuls la grille gloutonne et le Python de la porte du guide sont proposés. Les anciennes variantes ne réactivent pas l’adaptateur S01. |
| `formation.js`, `laboratoire-s01.js` | Ancien diagnostic, bilan, sauvegarde et adaptateur S01. | Fichiers historiques conservés, plus chargés par les pages actives. U01.1 possède ses propres clés de sauvegarde. |
| `scripts/construire-formation.py` | Régénère les pages anciennes depuis `docs/pedagogie/module-01/` et ajoute des consignes en dur. | Corps archivé ; point d’entrée compatible qui lance maintenant `construire-u01.py`. |
| `scripts/verifier-formation.py`, `scripts/capturer-formation.mjs` | Vérifient et illustrent l’ancienne interface. | Versions archivées ; points d’entrée remplacés pour contrôler et capturer U01.1. |
| `README.md` | Demande d’ouvrir S01 et présente les anciens accès comme opérationnels. | Démarrage U01.1, commandes courantes et statut explicite des archives. |
| `docs/visualisation-s01/`, `docs/art/captures/`, anciens Markdown et tests | Démonstrations et instantanés historiques, non une preuve de validation pédagogique actuelle. | Conservés ; aucune liaison depuis les accès pédagogiques ordinaires. Les anciens scénarios de formation sont rangés dans `tests/historique/`, exclus explicitement de la suite courante. |

Les archives restent inspectables dans le dépôt. Elles ne sont ni supprimées ni rendues confidentielles. Les HTML et générateurs du dernier prototype sont conservés dans `docs/historique/interface-s01/` avec empreintes et commit d’origine ; ils ne constituent pas une formation réhabilitée.

## Source et mécanismes actifs

Les cinq Markdown U01.1 approuvés constituent l’unique corpus éditorial de la leçon : cours, activités, parcours enseignant, corrigés, grille. Ils ne sont pas modifiés. `construire-u01.py` vérifie leur concordance avec le commit de référence et en dérive les pages statiques. `u01-sources.json` consigne leur provenance et les SHA-256 normalisés en LF. Les textes d’exercice ne sont pas dupliqués dans le JavaScript d’interface. Les données des tableaux et les questions sont contrôlées lors de la génération et de la vérification.

Le parcours élève conserve les six phases essentielles, avec explication présentée après observation dans le fil proposé. Les liens du fil permettent aussi l’inspection libre ; ils ne prétendent pas verrouiller une passation. A2/B1 restent dans un volet distinct, après le parcours essentiel. Les réponses des tableaux et les justifications sont éditables, conservées localement si possible et exportables ; aucun score ni validation de compétence n’est calculé.

Le parcours enseignant reprend intégralement le texte approuvé, y compris les notions, hypothèses, limites, paramètres et valeurs Python, contre-exemples, exercice, remédiations et références. Les corrigés sont repliés et explicitement proposés après recherche. Les anciens noms de fichiers conservés dans le texte du guide sont expliqués comme des références aux documents réunis dans cette présentation web.

Le moteur inline du laboratoire antérieur a été extrait à l’identique dans `laboratoire-moteur.js`. Aucun changement à sa carte, sa politique gloutonne, ses transitions ou ses arrêts. Le Worker `python-worker.js` est inchangé. Le nouvel habillage restreint les contrôles visibles aux deux tentatives ; il ajoute seulement les lettres A–G sur la rangée étudiée, les thèmes et le redimensionnement du cadre. Les éléments techniques conservés pour les écouteurs du moteur mais sans usage U01.1 sont cachés, sans ancien texte pédagogique visible.

La porte et le curseur restent des situations de raisonnement et de saisie, sans simulation inventée. Le Python facultatif du guide est exécuté dans le Worker existant ; ses quatre appels indépendants ne pilotent pas la grille.

## Vérifications et revue visuelle

La suite active couvre les parcours et anciens favoris, les commandes réelles au clavier, les textes attendus, les sauvegardes distinctes de S01, l’export, les trois thèmes, les transferts, le mobile, les chemins relatifs en sous-dossier et Pyodide réel avec erreur, interruption et reprise. Les assertions sont des contrôles techniques, pas une notation des apprenants.

La revue des captures Chromium a porté sur l’entrée de la leçon, l’expérience dans les trois thèmes, Nora, le curseur mobile, la préparation enseignante et le Python réel. Corrections apportées pendant cette revue : collision d’un nom de variable dans l’adaptateur, débordement de libellés masqués des tableaux à 390 px, et attente de navigation dans le test de focus. Les tableaux larges défilent dans leur région propre, au clavier également ; ils ne débordent plus sur le document. Leur défilement est annoncé.

Les liens bibliographiques conservés ont été ouverts : [Poole et Mackworth, §2.1](https://artint.info/3e/html/ArtInt3e.Ch2.S1.html), [extrait public AIMA](https://aima.cs.berkeley.edu/4th-ed/pdfs/newchap02.pdf), [sujet institutionnel NSI](https://eduscol.education.gouv.fr/sites/default/files/document/25-nsij2me1v1pdf-112650.pdf). Le passage après l’exemple 2.1 de Poole et Mackworth distingue bien commande et réalisation. Les réserves du guide sur l’édition du PDF AIMA sont conservées. Cela ne constitue pas une nouvelle validation de l’efficacité pédagogique de l’unité.

## Points encore à examiner

- Inspection humaine de l’intégralité du parcours et adéquation des champs de réponse ; temps réel et charge de lecture.
- Essai accompagné autorisé : compréhension des consignes, distinction commande/effet, transferts Nora ET curseur, influence des relances. Aucun résultat d’essai n’est inventé.
- Usage réel avec un lecteur d’écran, touches de navigation propres aux aides techniques, appareils tactiles et vidéoprojecteur physique. Les tests de clavier et de contraste ne constituent pas une certification complète d’accessibilité.
- Aucun déploiement GitHub Pages effectué ; le sous-chemin a été vérifié localement. Pas de fusion ni publication de branche dans cette livraison.
- Pyodide nécessite le CDN lors du premier chargement. L’activité élève n’en dépend pas ; le Python enseignant, oui. Le Worker reste interrompable et ne constitue pas une sandbox de sécurité.
- Les liens enseignants et le code source public permettent d’accéder aux corrigés : l’accompagnement organise le recueil avant leur consultation. La progression d’écran n’est pas une protection contre la lecture anticipée.

Arrêt pour inspection humaine avant toute suite. U02 n’est pas commencée.
