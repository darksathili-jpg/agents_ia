# Agent Academy — U01.1 interactive

Première leçon expérimentale accompagnée : **Commander n’est pas déplacer**. Le parcours scientifique de référence est celui du commit `fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6`, conservé dans `docs/pedagogie/refondation/u01/`.

## Lancer localement

Depuis le dossier du dépôt :

```powershell
python scripts/ouvrir-academy.py
```

Ou double-cliquer sur **Ouvrir-Agent-Academy.cmd** sous Windows. Le navigateur ouvre `http://127.0.0.1:8765/u01.html`. Garder le serveur ouvert ; Ctrl+C l’arrête. Si le port est occupé : `python scripts/ouvrir-academy.py --port 8766`, puis `http://127.0.0.1:8766/u01.html`.

Les pages statiques sont déjà construites : aucun framework ni installation npm n’est nécessaire pour les lire. L’expérience Microduck fonctionne sans téléchargement de Python. Le Python facultatif du parcours enseignant utilise réellement Pyodide ; sa première exécution nécessite Internet.

## Parcourir la leçon

Le parcours élève comporte contexte et repérage, prédictions et deux tentatives réelles, explication, entraînement, transfert Nora et bilan curseur. Les prolongements sont séparés. Les réponses écrites et celles des tableaux sont conservées localement lorsque le navigateur le permet et exportables en JSON ; elles ne sont ni envoyées ni corrigées automatiquement.

Le parcours enseignant distinct conserve l’explication scientifique, la formalisation facultative entièrement définie, le code de la porte et ses quatre cas, les erreurs anticipées, les remédiations, l’exercice enseignant, les références, les corrigés repliés et la grille formative. Les réponses aux transferts doivent être recueillies avant consultation des corrigés ; le lien enseignant n’est pas une protection de confidentialité.

## Reconstruire et vérifier

```powershell
python scripts/construire-u01.py
python scripts/verifier-u01.py
npm install
npx playwright install chromium
npm run test:browser -- --workers=2
```

Le générateur refuse un écart entre les cinq documents scientifiques sources et le commit de référence. `u01-sources.json` consigne la provenance et leurs empreintes. Les anciens points d’entrée `construire-formation.py`, `verifier-formation.py` et `capturer-formation.mjs` ciblent désormais U01.1. Le générateur historique est conservé en archive et ne doit pas être utilisé pour publier les pages actives.

Les fichiers historiques et les scénarios du prototype S01 sont conservés respectivement dans `docs/historique/interface-s01/` et `tests/historique/`. Ils ne sont pas une formation validée. La suite active teste U01.1 et les régressions de l’identité V2 ; elle n’impose plus le diagnostic ou le TP de l’ancienne S01.

Les captures et l’audit de cette intégration sont dans `docs/integration-u01/`. Les cinq Word et leurs PDF restent dans `docs/pedagogie/experimentation-u01-1/documents/`, inchangés.

**Limites :** aucun essai auprès d’apprenants n’est revendiqué. Les vingt minutes, la compréhension réelle, l’autonomie et l’efficacité restent à examiner. Le Worker permet l’interruption de Python ; il ne constitue pas une sandbox de sécurité pour du code non fiable. Aucune fusion ni aucun déploiement n’est effectué.
