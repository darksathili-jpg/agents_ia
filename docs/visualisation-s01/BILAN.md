# Jalon de visualisation pédagogique S01

Date : 17 octobre 2026. Branche locale : `feature/module-01-s01-visible`, issue de S03 `a27fbff516129ad5915916b659386692c8cc7021`. Point d’arrêt : démonstration S01, puis validation humaine.

## Ouvrir et démontrer

1. Dans le dossier du dépôt, double-cliquer sur **Ouvrir-Agent-Academy.cmd**. Python doit être installé ; aucune installation npm n’est requise pour consulter l’application.
2. Le navigateur par défaut ouvre le module. Pour Edge ou Chrome, y ouvrir `http://127.0.0.1:8765/module01.html`. Laisser la fenêtre du serveur ouverte ; Ctrl+C l’arrête. Si le port est occupé : `python scripts/ouvrir-academy.py --port 8766`.
3. Choisir **Suivre S01**, écrire une prédiction dans la partie Observer, lancer deux étapes puis comparer à la trace. Dans le TP, compléter la politique, exécuter la console, puis choisir Mon agent Python pour tester la grille. Terminer par l’analyse, le transfert et le bilan argumenté. Ouvrir ensuite **Enseignants** pour préparer et approfondir.

Alternative terminal : `python -m http.server 8765 --bind 127.0.0.1`, puis la même adresse. Ne pas ouvrir directement les HTML avec `file://` : le Worker demande un serveur HTTP.

La [séquence commentée](index.html) contient douze captures : module, entrée S01, expérience, atelier exécuté, bilan, parcours enseignant, deux pages complètes, formalisation, sombre, projection et mobile. Les images complètes s’ouvrent en résolution originale. Elles ont été examinées visuellement, avec lectures détaillées de l’expérience, de l’atelier, du bilan et de la formalisation, et examen de la structure des deux pages complètes.

## Audit de l’existant et dépendances Git

L’arbre était propre au démarrage. La lignée S03 contient l’accueil V2 `13d5284` et sa stabilisation ; aucune sélection de fichiers n’a remplacé les travaux scientifiques. `main` reste à `9843544acd036fce668dfe2a128727e09720ca24`.

Lecture GitHub en direct : [PR #1](https://github.com/darksathili-jpg/agents_ia/pull/1), brouillon ouvert, branche MVP vers main ; [PR #2](https://github.com/darksathili-jpg/agents_ia/pull/2), brouillon ouvert, direction artistique vers MVP. La description de #1 contient des limites historiques dépassées par le code actuel ; les vérifications portent sur le code, pas sur ces anciennes annonces. Ordre de dépendance éventuel : MVP, direction artistique, conception scientifique et intégration visible. Aucune fusion n’a été réalisée ; cette branche cumule déjà ces ancêtres. Revoir les différences et les bases des futures PR avant toute décision de fusion.

AGENTS.md, S01–S03, les tests existants et les contraintes de chemins relatifs ont été examinés. S04/S05 restent suspendues. Aucun nouveau cours de ces séances n’est produit.

## Ce qui est réellement intégré

L’accueil V2 garde sa composition, ses illustrations et ses ressources. Un lien de navigation et la destination de la vignette disponible conduisent maintenant au module. S01 est une leçon complète : diagnostic, situation, observation, hypothèses, notions et catégories, TP, analyse, transfert et bilan. Son texte source est converti intégralement, puis enrichi de réponses écrites et d’expériences ; les paragraphes scientifiques ne sont pas remplacés par des résumés.

Le parcours enseignant est une autre page de préparation : frontières, notations, problème de critère et seuil, démonstration conditionnelle, limites, production complète attendue, tableau didactique, correction Python et références avec leur statut. Il ne s’agit pas d’une augmentation de texte dans la même carte élève. Les lectures longues sont préparatoires ; le budget initial de 120 minutes reste estimé, pas mesuré après intégration.

S02/S03 disposent d’une présentation et d’une lecture documentaire HTML, avec liens lisibles dans le navigateur. Leurs expériences ne sont pas annoncées comme intégrées. S04/S05 sont des mentions à venir, sans boutons inactifs. Le carnet documentaire conserve également des spécifications antérieures du module, explicitement préparatoires : leur présence ne vaut pas réalisation d’une activité.

Les notes écrites restent dans le navigateur et sont exportables en JSON. Aucun envoi à l’enseignant, score de certification ou suivi distant fictif. Le bilan donne un retour sur trois repères, mais demande aussi justification et test ; les productions libres restent à discuter avec un enseignant.

## Expériences et justification technique

Deux cadres du laboratoire existant sont utilisés : observation puis atelier. Leurs états sont indépendants, ce qui permet un nouveau départ au TP. Le premier journal montre les commandes réelles ; la comparaison reprend ce texte, sans simuler une exécution. Le second cadre exécute la politique modifiée dans le véritable Pyodide et permet de la tester sur la grille. La console ne déplace pas la grille ; les instructions rendent cette distinction explicite.

`laboratoire.html` reçoit seulement le chargement de `laboratoire-s01.js`. L’adaptateur agit uniquement pour les paramètres `s01=observation` ou `s01=python` : présentation, code initial adapté, restauration de ce départ, thème et hauteur du cadre. Le moteur de décision, les transitions et `python-worker.js` sont inchangés. Le laboratoire indépendant conserve son exemple BFS et ses contrôles.

Les pages sont statiques, avec les polices et matières V2, sans nouvelle dépendance. `scripts/construire-formation.py` produit quatre pages HTML depuis nos sources ; ce convertisseur est limité à leur syntaxe, ce n’est pas un parseur Markdown général. Les pages produites sont versionnées : aucune compilation ni récupération de Markdown à l’exécution. Les liens, CSS, cadres et Worker sont relatifs, compatibles avec un dépôt GitHub Pages sous préfixe ; aucun déploiement n’a été déclenché.

## Vérifications et anomalies corrigées

**Campagne finale : 34/34 tests navigateur réussis en 38,8 s avec `npx playwright test --workers=1`.** Les dix scénarios nouveaux et les vingt-quatre historiques sont inclus. La réserve sur le lancement parallèle est conservée ci-dessous.

- Les 24 tests historiques ont passé séparément, notamment le véritable Pyodide, BFS complet, erreur, interruption et reprise.
- Les dix nouveaux scénarios S01 couvrent navigation, dix étapes conservées, parcours enseignant, prédiction/trace réelle, notes persistées, export téléchargé et relu, diagnostic, bilan, Python réel, console/grille, erreur, Stop, reprise, restauration, auto/pause/reset et activation clavier.
- Les trois thèmes sont contrôlés sur les pages de formation à 390, 768 et 1440 px. Le code, le journal et la console projetés sont contrôlés sur fond clair, à au moins 20 px et avec contraste calculé d’au moins 4,5:1. Le cadre projeté est contrôlé sans débordement aux trois largeurs.
- Le parcours sous `/agents_ia/` est testé en navigateur par réécriture locale des requêtes, sans hébergement public. Le validateur statique résout 172 liens et ressources locaux, avec contrôle des ancres, IDs uniques et un seul h1 par page.
- Le dossier scientifique conserve ses 23 tests CPython réussis et ses contrôles de minutages. La correction Python affichée est aussi exécutée et ses quatre assertions passent sous CPython et dans l’atelier Pyodide réel.
- Le lanceur local a été exécuté sans ouverture automatique de navigateur sur un port libre ; une vraie requête HTTP a reçu la page module avec statut 200. Le lancement automatique du navigateur par défaut reste dépendant de l’association du poste.

La revue visuelle a conduit à corriger des indicateurs tronqués et la hauteur de l’atelier intégré. Les essais mobiles ont révélé une largeur minimale implicite de la colonne de lecture, corrigée sans masquer le contenu. Un test devait faire défiler le cadre chargé à la demande avant de l’utiliser. Le test de préfixe attend maintenant la fin de ses requêtes avant fermeture. Enfin, le test historique de l’illustration vérifiait immédiatement son chargement : il attend désormais effectivement l’image, sans modifier celle-ci ni supprimer le contrôle.

Commandes reproductibles :

```text
python scripts/construire-formation.py
python scripts/verifier-formation.py
python docs/pedagogie/module-01/python/valider_dossier.py
node --check formation.js
node --check laboratoire-s01.js
npx playwright test --workers=1
node scripts/capturer-formation.mjs
git diff --check
```

## Limites et critères de validation humaine

Le prototype reste à éprouver avec de vrais élèves et enseignants : temps de lecture, charge du TP, compréhension des consignes et qualité du raisonnement. Les tests techniques ne valident pas cette efficacité. Revue sur projecteur réel, lecteur d’écran, appareils mobiles physiques et navigation à fort zoom encore nécessaire. Les contrôles automatisés sont Chromium, pas une campagne distincte sur les versions installées d’Edge/Chrome.

Le premier chargement Python exige Internet et le CDN ; aucun fonctionnement hors ligne garanti. Deux expériences indépendantes peuvent charger deux Workers si l’on utilise les deux ateliers ; ce coût reste à mesurer sur les ordinateurs les plus modestes. Le code édité, la grille et les radios ne sont pas restaurés après rechargement ; les notes écrites le sont lorsque le stockage est disponible. Une réponse libre ou du code doit être exporté ou copié avant de quitter la page. L’export n’est pas une remise automatique à un serveur.

La page complète est longue ; le sommaire et les liens précédent/suivant permettent une lecture par étapes. La correction publique est volontairement séparée pour la distribution, sans prétendre à la confidentialité. L’examen visuel juge une cohérence avec la V2, pas une validation artistique humaine acquise.

La campagne parallèle à cinq workers a révélé une instabilité du scénario clavier V2 existant : le bouton reste parfois non activé après Espace, alors que le même scénario passe isolément. Le test cible désormais explicitement le bouton visible, sans supprimer le contrôle clavier. La commande de vérification de livraison utilise un seul worker ; l’exécution parallèle reste une limite du dispositif de tests à examiner, pas une preuve que cette instabilité est résolue.

Validation demandée : qualité du cours, lisibilité, programmation réelle, ergonomie, profondeur enseignante, cohérence artistique et fonctionnement sur le matériel de formation. Arrêt après cette démonstration. Aucun push, fusion ou déploiement dans ce jalon ; le commit local constitue le résultat révisable.
