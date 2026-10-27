"""Télécharge une fois la distribution Pyodide utilisée par ORCHESTRA.
À lancer par un responsable AVEC accès Internet ; pas d'accès requis ensuite.
N'exécute aucun code téléchargé sur l'ordinateur durant l'installation.
"""
from pathlib import Path
from urllib.request import urlopen, Request
import hashlib
import json
import sys

VERSION='0.27.7'
BASE=f'https://cdn.jsdelivr.net/pyodide/v{VERSION}/full/'
FILES=['pyodide.js','pyodide.asm.js','pyodide.asm.wasm','python_stdlib.zip','pyodide-lock.json']
ROOT=Path(__file__).resolve().parent/'pyodide'
ROOT.mkdir(exist_ok=True)
manifest={'version':VERSION,'source':BASE,'files':{}}
for name in FILES:
    target=ROOT/name
    try:
        if target.exists() and target.stat().st_size>100:
            data=target.read_bytes()
        else:
            print('Téléchargement',name,flush=True)
            req=Request(BASE+name,headers={'User-Agent':'ORCHESTRA-NSI-Pyodide-installer/1.1'})
            with urlopen(req,timeout=90) as response:
                data=response.read()
            if len(data)<100:
                raise RuntimeError('Fichier trop court')
            temp=target.with_suffix(target.suffix+'.part')
            temp.write_bytes(data)
            temp.replace(target)
        manifest['files'][name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        print('OK',name,len(data),'octets')
    except Exception as exc:
        print('ECHEC :',name,type(exc).__name__,str(exc),file=sys.stderr)
        sys.exit(1)
(ROOT/'MANIFEST_INSTALLATION.json').write_text(json.dumps(manifest,indent=2))
print('Installation locale terminée. Lance LANCER_ORCHESTRA.cmd pour travailler hors connexion.')
