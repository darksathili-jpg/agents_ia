# Accueil et laboratoire — architecture et vérification

## Audit initial
`main` contenait seulement le README. Le prototype du jalon 03 se trouvait sur `origin/feature/agent-academy-mvp` (3670b3d). La branche artistique part de ce prototype. Aucun AGENTS.md dans le dépôt. Le laboratoire était une page statique autonome, avec un Worker Pyodide séparé et sept scénarios Playwright. Le mode projector appliquait #050b14 au fond : anomalie confirmée.

## Architecture
- `index.html` : cinq zones éditoriales, chemins relatifs compatibles avec un sous-répertoire GitHub Pages.
- `accueil.js` : préférence d’affichage partagée avec le labo et messages de la mascotte. Sans JavaScript, navigation et contenu restent disponibles en clair.
- `academy.css` : identité, responsive, mouvements réduits et corrections de présentation du laboratoire.
- `laboratoire.html` : ancien index, avec lien de retour et feuille de style partagée. Script du moteur conservé à l’identique ; `python-worker.js` inchangé. Aucun changement aux politiques, contrats ou exercices.
- `assets/` : illustration fournie, mascotte dérivée, polices et licences.

Tous les appels à l’action rejoignent une activité existante ou une section ; les chapitres futurs sont du texte sans faux bouton. Le cours, Python et BFS sont accessibles depuis le chapitre disponible. Aucune promesse d’agent LLM exécutable.

## Vérification du 17 octobre 2026
- `node --check accueil.js` : réussi.
- `npx playwright test --grep-invert "Pyodide réel"` : 14 tests réussis.
- `npx playwright test tests/lab.spec.mjs --grep "Pyodide réel"` avec accès réseau autorisé : 1 test réussi, véritable Pyodide chargé depuis le CDN.
- Premier essai sous réseau restreint : délai du test Pyodide dépassé. L’essai autorisé passe sans modification du Worker.
- Un premier sélecteur du nouveau test responsive désignait deux liens ; corrigé vers le lien nommé exactement « Le parcours ».
- Captures Playwright : accueil et laboratoire en clair, sombre, projection ; accueil mobile 390 px. Revue visuelle effectuée des captures clair, mobile et laboratoire projection. Tests de largeur à 390, 768 et 1440 px, sans débordement.
- Références Hugging Face, arXiv ReAct et Anthropic ouvertes et vérifiées sur leurs sites réels ; les tests vérifient les URL exactes, sans dépendre de ces sites à chaque exécution.

## Limites et validation humaine
Les contrôles automatisés vérifient les surfaces claires, le focus initial, le lien d’évitement, la navigation, la réduction du mouvement, les états du laboratoire et le responsive. Ils ne constituent pas un audit WCAG exhaustif. Les couleurs principales de texte sont choisies avec fort contraste ; les états secondaires et l’usage sur un vrai vidéoprojecteur restent à apprécier en classe. Tester également avec lecteur d’écran et appareil tactile réel. Validation artistique du commanditaire encore attendue. Aucun déploiement ni fusion.

## Lancer
`npm ci`, puis `npx playwright install chromium`, puis `python -m http.server 8765 --bind 127.0.0.1`. Ouvrir http://127.0.0.1:8765/. Suite complète : `npm run test:browser` (accès CDN nécessaire).

Vérification finale après ajustements : `npm run test:browser` avec accès réseau autorisé, **15/15 réussis (6,9 s)**. Comparaison automatisée du bloc script du laboratoire avec le prototype : identique. Diff de `python-worker.js` : vide. Revue visuelle complémentaire du mode sombre effectuée.
