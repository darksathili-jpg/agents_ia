"""Regénère les données d’affichage depuis le moteur Python (source unique)."""
from pathlib import Path
import sys
import json
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'terminale'))
import runner
cases={case['id']:{
    'id':case['id'], 'name':case['name'], 'width':case['width'], 'height':case['height'],
    'start':list(case['start']), 'goal':list(case['goal']),
    'obstacles':[list(p) for p in case['obstacles']]
} for case in runner.CASES}
payload='// Fichier généré par outils/generer_cas.py ; ne pas modifier manuellement.\n'
payload+='window.ORCHESTRA_CASES = '+json.dumps(cases,ensure_ascii=False,separators=(',',':'))+';\n'
(root/'terminale/cases.js').write_text(payload,encoding='utf-8')
print(len(cases),'situations exportées depuis runner.CASES')
