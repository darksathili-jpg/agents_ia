// Ancien point d’entrée : captures U01.1 produites par les tests navigateur réels.
import {spawnSync} from 'node:child_process';
const run=spawnSync(process.execPath,['node_modules/@playwright/test/cli.js','test','tests/u01.spec.mjs','--workers=1'],{stdio:'inherit'});
process.exit(run.status ?? 1);
