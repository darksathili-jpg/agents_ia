"""Fidélité du corpus, liens locaux, conservation des archives et du moteur."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parent.parent
REFERENCE='fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.links=[];self.ids=[];self.text=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
    def handle_data(self,data):self.text.append(data)
def plain(s):
    s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)
    return re.sub(r'[^\w]','',s).casefold()
pages={n:Page((ROOT/n).read_text(encoding='utf-8')) for n in ['index.html','module01.html','u01.html','enseignant-u01.html','laboratoire.html','seance01.html','enseignant-s01.html','ressources-module01.html','docs/integration-u01/index.html']}
for name,page in pages.items():
    assert len(page.ids)==len(set(page.ids)),('Identifiant dupliqué',name)
    for link in page.links:
        url=urlsplit(link)
        if url.scheme or url.netloc:continue
        target=(ROOT/name).parent/unquote(url.path) if url.path else ROOT/name
        if target.is_dir():target=target/'index.html'
        assert target.exists(),(name,link)
        if url.fragment and target.suffix=='.html':
            other=Page(target.read_text(encoding='utf-8'))
            assert unquote(url.fragment) in other.ids,(name,link)
        assert 'historique/' not in link and 'module-01/' not in link,(name,link)
manifest=json.loads((ROOT/'u01-sources.json').read_text(encoding='utf-8'))
for name,digest in manifest['sources'].items():
    path=ROOT/'docs/pedagogie/refondation/u01'/name
    data=path.read_bytes();assert hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()==digest
    original=subprocess.check_output(['git','show',f'{REFERENCE}:{path.relative_to(ROOT).as_posix()}'],cwd=ROOT)
    assert data.replace(b'\r\n',b'\n')==original.replace(b'\r\n',b'\n')
    target=pages['u01.html' if name in ('COURS_ELEVE.md','ACTIVITES_ELEVE.md') else 'enseignant-u01.html']
    content=plain(' '.join(target.text))
    text=data.decode('utf-8-sig')
    # Chaque paragraphe scientifique, règle et question ; hors titres et routage éditorial.
    for paragraph in text.split('\n\n'):
        p=paragraph.strip()
        if not p or p.startswith(('#','|','```','À utiliser avec','Le parcours essentiel comprend')):continue
        if p.startswith('Vous avez seulement'):pass
        for segment in p.split('\n'):
            if len(segment)>55:assert plain(segment) in content,(name,segment[:100])
archive=ROOT/'docs/historique/interface-s01'
saved=json.loads((archive/'empreintes.json').read_text(encoding='utf-8'))
for name,digest in saved['fichiers'].items():assert hashlib.sha256((archive/Path(name).name).read_bytes()).hexdigest()==digest
historical=(archive/'laboratoire.html').read_text(encoding='utf-8')
engine=re.search(r'<script>\s*("use strict";.*?)</script>',historical,re.S).group(1)
assert (ROOT/'laboratoire-moteur.js').read_text(encoding='utf-8')==engine,'Moteur modifié'
worker=subprocess.check_output(['git','show',saved['commit']+':python-worker.js'],cwd=ROOT)
assert (ROOT/'python-worker.js').read_bytes().replace(b'\r\n',b'\n')==worker.replace(b'\r\n',b'\n')
code=re.search(r'```python\n(.*?)```',(ROOT/'docs/pedagogie/refondation/u01/PARCOURS_ENSEIGNANT.md').read_text(encoding='utf-8'),re.S).group(1)
exec(compile(code,'U01.1 référence','exec'),{})
print('U01_FIDELITE_OK : paragraphes, liens et ancres, archives, moteur et Worker inchangés ; Python CPython conforme.')
