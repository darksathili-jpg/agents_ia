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

## Vérification de la revue artistique V2
Branche conservée : `feature/agent-academy-art-direction`. Base de comparaison : commit V1 `75e1eee`. Ni changement d’architecture ni dépendance supplémentaire. `index.html`, `academy.css` et `accueil.js` portent la composition et les interactions ; `assets/carnet-reperes.svg` et `assets/mission-obstacles.svg` ajoutent les dessins. Les deux PNG validés, `laboratoire.html` et `python-worker.js` sont identiques à V1 (comparaison des contenus, fins de ligne normalisées pour les textes).

### Résultats exécutés
- `node --check accueil.js` : réussi ; `git diff --check` : réussi.
- Suite précédente, hors Pyodide : 14/14 réussis pendant l’implémentation.
- `npm run test:browser` avec accès au CDN autorisé : **21/21 réussis en 9,3 s**, dont les 15 scénarios précédents et le véritable Pyodide.
- Six nouveaux scénarios : explications de Microduck au clavier et conservation du choix ; couleurs et tailles calculées en projection ; trois modes à chacune des largeurs 390, 768 et 1440 px ; animations finies, réduction du mouvement et focus visible.
- Le test de projection mesure les couleurs réellement calculées et les fonds opaques hérités : contraste textuel **≥ 4,5:1** et taille **≥ 18 px** sur l’échantillon accueil/labo, incluant code, journal, console, navigation, légendes et mentions secondaires. Les surfaces de lecture testées ont chaque canal RGB ≥ 230. Ceci ne constitue pas un audit WCAG exhaustif.

### Revue visuelle effectuée
[Comparatif avant/après](captures/v2/index.html) : 10 vues V1 à 1440 px (390 et 768 pour les vues responsive), puis 11 vues V2 dont un détail supplémentaire de la bienvenue mobile. Reproduction : `node scripts/capture-art.mjs avant` avant modification, puis `node scripts/capture-art.mjs apres` après modification. Le script utilise un serveur local éphémère et ferme son navigateur et son serveur.

Captures examinées : accueil clair, sombre, projection, mobile et tablette ; bienvenue de Microduck, fiche de mission, parcours et méthode ; laboratoire en projection. Constats : signature de marque visible sans la scène ; bulle associée au robot ; obstacle et détour visibles dans la mission ; dessins de méthode lisibles dans les deux thèmes ; code et console sur papier clair. La bulle mobile a été élargie après la première revue pour raccourcir les empilements de lignes. Les états interactifs et les trois modes n’ajoutent aucun débordement horizontal aux largeurs testées.

Limites restantes : lecture depuis le fond d’une vraie salle, rendu d’un vidéoprojecteur matériel, lecteur d’écran et perception humaine de la mascotte à valider. La V2 demeure une proposition artistique en PR brouillon, sans fusion ni publication.

Dernière précision pédagogique : le détour bleu est un trajet possible, pas une prédiction de la route choisie par BFS. Après cet ajustement du texte, `npx playwright test tests/art-v2.spec.mjs` : **6/6 réussis en 5,3 s** ; captures V2 régénérées.
