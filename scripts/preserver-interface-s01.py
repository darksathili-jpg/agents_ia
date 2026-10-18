"""Conserve le dernier état historique ; n’écrit jamais dans le corpus U01.1."""
from pathlib import Path
import subprocess, hashlib, json, re
ROOT=Path(__file__).resolve().parent.parent
BASE='7197a1d7f854034425c8b0141aed6ad141f07ab9'
ARCHIVE=ROOT/'docs/historique/interface-s01'
ARCHIVE.mkdir(parents=True,exist_ok=True)
names=['module01.html','seance01.html','enseignant-s01.html','ressources-module01.html','laboratoire.html','formation.js','laboratoire-s01.js','README.md','scripts/construire-formation.py','scripts/verifier-formation.py','scripts/capturer-formation.mjs','docs/visualisation-s01/index.html']
manifest={}
for name in names:
    data=subprocess.check_output(['git','show',f'{BASE}:{name}'],cwd=ROOT)
    target=ARCHIVE/Path(name).name
    if target.exists() and target.read_bytes()!=data:raise ValueError(f'Archive différente : {target}')
    target.write_bytes(data);manifest[name]=hashlib.sha256(data).hexdigest()
original=(ARCHIVE/'laboratoire.html').read_text(encoding='utf-8')
engine=re.search(r'<script>\s*("use strict";.*?)</script>',original,re.S).group(1)
(ROOT/'laboratoire-moteur.js').write_text(engine,encoding='utf-8')
(ARCHIVE/'empreintes.json').write_text(json.dumps({'commit':BASE,'fichiers':manifest},indent=2)+'\n',encoding='utf-8')
(ROOT/'scripts/construire-formation.py').write_text('''"""Ancien point d’entrée : construit uniquement U01.1."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('construire-u01.py')), run_name='__main__')
''',encoding='utf-8')
(ROOT/'scripts/verifier-formation.py').write_text('''"""Ancien point d’entrée : vérifie uniquement le parcours U01.1 courant."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('verifier-u01.py')), run_name='__main__')
''',encoding='utf-8')
(ROOT/'scripts/capturer-formation.mjs').write_text('''// Ancien point d’entrée : captures U01.1 produites par les tests navigateur réels.
import {spawnSync} from 'node:child_process';
const run=spawnSync(process.execPath,['node_modules/@playwright/test/cli.js','test','tests/u01.spec.mjs','--workers=1'],{stdio:'inherit'});
process.exit(run.status ?? 1);
''',encoding='utf-8')
old_gallery=(ARCHIVE/'index.html').read_text(encoding='utf-8')
notice='<aside role="note" style="border:3px solid #963c15;padding:20px"><strong>ARCHIVE — prototype S01 retiré ; contenu pédagogique non validé.</strong> Ces captures ne décrivent plus le parcours actif. <a href="../../u01.html">Ouvrir U01.1</a> · <a href="../integration-u01/index.html">Inspection actuelle</a></aside>'
(ROOT/'docs/visualisation-s01/index.html').write_text(old_gallery.replace('<h1>',notice+'<h1>',1),encoding='utf-8')
