"""Contrôles reproductibles, après export par Word ; ne simule aucun essai humain."""
from pathlib import Path
import subprocess, tempfile, json, re, hashlib, zipfile
import xml.etree.ElementTree as E
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'documents'; CHECK=ROOT/'controle';CHECK.mkdir(exist_ok=True)
SRC=ROOT.parent/'refondation'/'u01'
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def norm(s):return re.sub(r'\s+','',s)
manifest=json.loads((ROOT/'sources-sha256.json').read_text(encoding='utf-8'))
for n,h in manifest.items():assert hashlib.sha256((SRC/n).read_bytes()).hexdigest()==h,n
reports=[]
with tempfile.TemporaryDirectory(prefix='u01-docx-') as temp:
    for doc in sorted(OUT.glob('*.docx')):
        pdf=doc.with_suffix('.pdf')
        assert pdf.exists(),pdf
        with zipfile.ZipFile(doc) as z:
            xml=E.fromstring(z.read('word/document.xml'))
            paragraphs=[''.join(p.itertext()) for p in xml.iter(W+'p')]
            text='\n'.join(paragraphs)
            assert not xml.findall('.//'+W+'ins') and not xml.findall('.//'+W+'del')
        txt=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode('utf-8')
        pages=txt.split('\f')
        if not pages[-1].strip():pages.pop()
        assert all(re.sub(r'U01\.1 · Document expérimental ·\s*\d+\s*/\s*\d+', '',p).strip() for p in pages),'Page vide hors pied de page'
        if doc.name.startswith('01'):
            assert len(pages)==6
            assert 'A2' not in text and 'B1' not in text
            assert 'Corrigé' not in text
            assert 'Il y a donc deux commandes' in pages[3]
            assert all('Il y a donc deux commandes' not in p for p in pages[:3])
            for marker,page in [('C0',0),('P1',1),('P2',1),('E2',2),('E3',2),('A1',3),('T1',4),('T2',4),('I1',5),('I2',5)]:assert marker in pages[page],marker
        if doc.name.startswith('02'):
            # Tous les paragraphes scientifiques sources doivent subsister, hors syntaxe Markdown.
            for name in ['PARCOURS_ENSEIGNANT.md','CORRIGES.md']:
                ast=json.loads(subprocess.check_output(['pandoc',str(SRC/name),'-t','json']))
                plain=subprocess.check_output(['pandoc',str(SRC/name),'-t','plain','--wrap=none']).decode('utf-8')
                # Contrôle textuel élémentaire des segments longs, avec tolérance typographique.
                def canon(s):return re.sub(r'[^\w]', '',s).casefold()
                clean=re.sub(r'U01\.1 · Document expérimental ·\s*\d+\s*/\s*\d+', '',txt)
                for line in plain.splitlines():
                    if len(line)>60 and not line.startswith(' '):
                        assert canon(line) in canon(clean), (name,line[:80])
            code=re.search(r'```python\n(.*?)```',(SRC/'PARCOURS_ENSEIGNANT.md').read_text(encoding='utf-8'),re.S).group(1)
            cp=next(p for p in xml.iter(W+'p') if 'def appliquer_porte' in ''.join(p.itertext()))
            extracted=''.join(n.text or '' if n.tag==W+'t' else '\n' if n.tag==W+'br' else '\t' if n.tag==W+'tab' else '' for n in cp.iter())
            assert extracted.strip()==code.strip(),'Code DOCX différent de la source'
            namespace={}
            exec(compile(extracted,'U01.1-DOCX','exec'),namespace)
            for args in [('inconnu','ouverte','AVANCER'),('hall','inconnue','AVANCER'),('hall','ouverte','RECULER')]:
                try:namespace['appliquer_porte'](*args)
                except ValueError:pass
                else:raise AssertionError(('Entrée invalide non refusée',args))
            for code_line in code.splitlines():
                if code_line.strip():assert code_line.strip() in txt,code_line
            for line in ['def appliquer_porte','assert resultat == attendu','print((position, porte)']:
                assert any(line in p for p in pages)
            codepages=[i+1 for i,p in enumerate(pages) if 'def appliquer_porte' in p or 'assert resultat == attendu' in p]
            assert len(set(codepages))==1,codepages
        # Vérifier les coordonnées du texte PDF : pas de mot hors page.
        bbox=subprocess.check_output(['pdftotext','-bbox',str(pdf),'-']).decode('utf-8')
        bt=E.fromstring(bbox)
        for page in bt.iter('{http://www.w3.org/1999/xhtml}page'):
            width=float(page.get('width'));height=float(page.get('height'))
            for word in page.iter('{http://www.w3.org/1999/xhtml}word'):
                assert 0<=float(word.get('xMin'))<=float(word.get('xMax'))<=width
                assert 0<=float(word.get('yMin'))<=float(word.get('yMax'))<=height
        prefix=str(Path(temp)/doc.stem)
        subprocess.run(['pdftoppm','-scale-to','1100','-png',str(pdf),prefix],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        imgs=sorted(Path(temp).glob(doc.stem+'-*.png'))
        # Planches exhaustives, trois pages au maximum par ligne.
        thumbw=480;thumbh=720 if not doc.name.startswith('03') else 380
        board=Image.new('RGB',(thumbw*min(3,len(imgs)),(thumbh+30)*((len(imgs)+2)//3)),'#cccccc')
        draw=ImageDraw.Draw(board)
        for i,path in enumerate(imgs):
            im=Image.open(path).convert('RGB');im.thumbnail((thumbw-12,thumbh-12))
            x=(i%3)*thumbw;y=(i//3)*(thumbh+30)
            board.paste(im,(x,y+22));draw.text((x+8,y+4),f'{doc.stem} / {i+1}',fill='black')
            if doc.name.startswith('01') or doc.name.startswith('03') or (doc.name.startswith('02') and i in (2,5)):
                Image.open(path).save(CHECK/f'{doc.stem}-page-{i+1}.png')
        board.save(CHECK/(doc.stem+'-planche.png'))
        reports.append({'document':doc.name,'pages':len(pages),'texte_hors_page':False,'pages_vides':False,'sha256':hashlib.sha256(doc.read_bytes()).hexdigest()})
(CHECK/'verification.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(reports,ensure_ascii=True,indent=2))
