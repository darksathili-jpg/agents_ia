"""Construction locale : Python standard + Pandoc. Aucune source U01.1 modifiée."""
from pathlib import Path
import subprocess, zipfile, io, re, json, hashlib
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / 'refondation' / 'u01'
OUT = ROOT / 'documents'
OUT.mkdir(exist_ok=True)
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
E.register_namespace('w', W)
def q(s): return '{'+W+'}'+s
def read(name): return (SRC/name).read_text(encoding='utf-8')
BREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
def lines(n=3):
    row='<w:p><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="exact"/><w:pBdr><w:bottom w:val="single" w:sz="2" w:color="999999"/><w:between w:val="single" w:sz="2" w:color="999999"/></w:pBdr></w:pPr><w:r><w:t xml:space="preserve"> </w:t></w:r></w:p>'
    return '\n\n```{=openxml}\n'+row*n+'\n```\n\n'

# Une base Word connue, sans paquet Python supplémentaire.
template = subprocess.check_output(['pandoc', '--print-default-data-file', 'reference.docx'])
with zipfile.ZipFile(io.BytesIO(template)) as z: parts={n:z.read(n) for n in z.namelist()}
styles=E.fromstring(parts['word/styles.xml'])
defaults=styles.find(q('docDefaults'))
rp=defaults.find(q('rPrDefault')).find(q('rPr'))
for tag, attrs in [('rFonts',{'ascii':'Arial','hAnsi':'Arial','eastAsia':'Arial'}),('sz',{'val':'22'}),('lang',{'val':'fr-FR'})]:
    old=rp.find(q(tag))
    if old is not None: rp.remove(old)
    E.SubElement(rp,q(tag),{q(k):v for k,v in attrs.items()})
for st in styles.findall(q('style')):
    sid=st.get(q('styleId'))
    r=st.find(q('rPr'))
    if r is None:r=E.SubElement(st,q('rPr'))
    for old in list(r):
        if old.tag in [q('color'),q('rFonts')]:r.remove(old)
    E.SubElement(r,q('color'),{q('val'):'000000'})
    E.SubElement(r,q('rFonts'),{q('ascii'):'Arial',q('hAnsi'):'Arial'})
    pp=st.find(q('pPr'))
    if pp is None: pp=E.SubElement(st,q('pPr'))
    spacing=pp.find(q('spacing'))
    if spacing is not None: pp.remove(spacing)
    E.SubElement(pp,q('spacing'),{q('after'):'100',q('line'):'252',q('lineRule'):'auto'})
    if sid and ('Heading' in sid): E.SubElement(pp,q('keepNext'))
    if sid in ('SourceCode','VerbatimChar'):
        r=st.find(q('rPr'))
        if r is None:r=E.SubElement(st,q('rPr'))
        E.SubElement(r,q('rFonts'),{q('ascii'):'Courier New',q('hAnsi'):'Courier New'})
        E.SubElement(r,q('sz'),{q('val'):'18'})
parts['word/styles.xml']=E.tostring(styles,encoding='utf-8',xml_declaration=True)
ref=ROOT/'reference.docx'
with zipfile.ZipFile(ref,'w',zipfile.ZIP_DEFLATED) as z:
    for n,b in parts.items():z.writestr(n,b)

def build(stem,md,landscape=False):
    # Liens internes vers les anciens Markdown : conserver le libellé imprimable.
    md=re.sub(r'\[([^\]]+)\]\((?!https?://)[^)]+\)',r'\1',md)
    md='\n'.join(line.rstrip() for line in md.splitlines()).rstrip()+'\n'
    src=OUT/(stem+'.md');src.write_text(md,encoding='utf-8')
    dst=OUT/(stem+'.docx')
    subprocess.run(['pandoc',str(src),'-o',str(dst),'--reference-doc',str(ref),'--metadata','lang=fr-FR','--highlight-style','monochrome'],check=True)
    with zipfile.ZipFile(dst) as z: data={n:z.read(n) for n in z.namelist()}
    tree=E.fromstring(data['word/document.xml']);body=tree.find(q('body'));sect=body.find(q('sectPr'))
    pending=False
    for child in list(body):
        if child.tag==q('p') and any(br.get(q('type'))=='page' for br in child.iter(q('br'))):
            body.remove(child);pending=True;continue
        if pending and child.tag==q('p'):
            pp=child.find(q('pPr'))
            if pp is None:pp=E.SubElement(child,q('pPr'))
            E.SubElement(pp,q('pageBreakBefore'));pending=False
    if stem.startswith('02'):
        st=E.fromstring(data['word/styles.xml'])
        for sp in st.iter(q('spacing')):sp.set(q('after'),'60');sp.set(q('line'),'240')
        data['word/styles.xml']=E.tostring(st,encoding='utf-8',xml_declaration=True)
    for p in tree.iter(q('p')):
        sty=p.find(q('pPr')+'/'+q('pStyle'))
        if sty is not None and sty.get(q('val'))=='SourceCode':
            E.SubElement(p.find(q('pPr')),q('keepLines'))
    if sect is None:sect=E.SubElement(body,q('sectPr'))
    for tag in ['pgSz','pgMar']:
        old=sect.find(q(tag))
        if old is not None:sect.remove(old)
    E.SubElement(sect,q('pgSz'),{q('w'):'16838' if landscape else '11906',q('h'):'11906' if landscape else '16838',q('orient'):'landscape' if landscape else 'portrait'})
    E.SubElement(sect,q('pgMar'),{q('top'):'850',q('bottom'):'850',q('left'):'1000',q('right'):'1000',q('header'):'350',q('footer'):'350',q('gutter'):'0'})
    for ti,table in enumerate(tree.iter(q('tbl'))):
        rows=table.findall(q('tr'));cols=len(rows[0].findall(q('tc')))
        if stem.startswith('02') and len(rows)<=6:
            ps=list(table.iter(q('p')))
            for p in ps[:-1]:
                pp=p.find(q('pPr'))
                if pp is None:pp=E.SubElement(p,q('pPr'))
                E.SubElement(pp,q('keepNext'))
        if landscape and cols==6:fractions=[.16,.10,.10,.10,.10,.44]
        elif landscape and cols==3:fractions=[.30,.60,.10]
        elif landscape and cols==5 and ti==3:fractions=[.13,.24,.18,.24,.21]
        elif landscape and cols==5:fractions=[.22,.24,.24,.20,.10]
        elif stem.startswith('01') and ti==3:fractions=[.08,.15,.22,.18,.20,.17]
        elif cols==6: fractions=[.08,.12,.15,.14,.16,.35]
        elif cols==8:fractions=[.30]+[.10]*7
        elif cols==5:fractions=[.12,.22,.22,.22,.22]
        else:fractions=[1/cols]*cols
        width=14838 if landscape else 9906
        widths=[int(width*f/sum(fractions)) for f in fractions]
        grid=table.find(q('tblGrid'))
        tpr=table.find(q('tblPr'))
        if tpr is None:tpr=E.SubElement(table,q('tblPr'))
        borders=tpr.find(q('tblBorders'))
        if borders is not None:tpr.remove(borders)
        borders=E.SubElement(tpr,q('tblBorders'))
        for edge in ['top','left','bottom','right','insideH','insideV']:
            E.SubElement(borders,q(edge),{q('val'):'single',q('sz'):'4',q('color'):'888888'})
        if grid is not None:
            for col,wid in zip(grid,widths):col.set(q('w'),str(wid))
        for i,row in enumerate(table.findall(q('tr'))):
            for cell,wid in zip(row.findall(q('tc')),widths):
                cw=cell.find(q('tcPr')+'/'+q('tcW'))
                if cw is not None:cw.set(q('w'),str(wid));cw.set(q('type'),'dxa')
            pr=row.find(q('trPr'))
            if pr is None:pr=E.SubElement(row,q('trPr'))
            E.SubElement(pr,q('cantSplit'))
            if i==0:E.SubElement(pr,q('tblHeader'))
            if stem.startswith('01') and i>0:
                E.SubElement(pr,q('trHeight'),{q('val'):'1000',q('hRule'):'atLeast'})
            if stem.startswith('03') and i>0:
                E.SubElement(pr,q('trHeight'),{q('val'):'650',q('hRule'):'atLeast'})
        for t in table.iter(q('rPr')):E.SubElement(t,q('sz'),{q('val'):'20'})
    # Numérotation réelle Word, sans dépendre du nombre final de pages.
    relns='http://schemas.openxmlformats.org/package/2006/relationships'
    rel=E.fromstring(data['word/_rels/document.xml.rels'])
    E.SubElement(rel,'{'+relns+'}Relationship',{'Id':'rIdDossierFooter','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer','Target':'footer-dossier.xml'})
    E.SubElement(sect,q('footerReference'),{q('type'):'default','{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id':'rIdDossierFooter'})
    footer=E.Element(q('ftr'));p=E.SubElement(footer,q('p'));pp=E.SubElement(p,q('pPr'));E.SubElement(pp,q('jc'),{q('val'):'right'})
    for text,field in [('U01.1 · Document expérimental · ',None),('', 'PAGE'),(' / ',None),('', 'NUMPAGES')]:
        if field:E.SubElement(p,q('fldSimple'),{q('instr'):field})
        else:E.SubElement(E.SubElement(p,q('r')),q('t')).text=text
    data['word/footer-dossier.xml']=E.tostring(footer,encoding='utf-8',xml_declaration=True)
    ct=E.fromstring(data['[Content_Types].xml'])
    E.SubElement(ct,'{http://schemas.openxmlformats.org/package/2006/content-types}Override',{'PartName':'/word/footer-dossier.xml','ContentType':'application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml'})
    data['[Content_Types].xml']=E.tostring(ct,encoding='utf-8',xml_declaration=True)
    data['word/_rels/document.xml.rels']=E.tostring(rel,encoding='utf-8',xml_declaration=True)
    data['word/document.xml']=E.tostring(tree,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in data.items():z.writestr(n,b)

c=read('COURS_ELEVE.md');a=read('ACTIVITES_ELEVE.md')
p1=c[:c.index('## 2.')].replace('de ce cours et des [activités élève](ACTIVITES_ELEVE.md), sur papier ou à l’écran','de ce document réunissant cours et activités').replace('Les corrigés sont remis après votre recherche.','')
p1=p1.replace('____________________.', '')+lines(2)
p1=p1.replace('# U01 — Commander n’est pas déplacer','# U01 — Commander n’est pas déplacer\n\nCode non nominatif : ____________________')
phase=c[c.index('## 2.'):c.index('## 3.')]
p2=phase[:phase.index('**E2')]
p2=p2.replace('Commande : __________ Case après : __________ Raison : ____________________.','Commande : __________ Case après : __________'+lines(2))
p2=p2.replace('puis justifiez : ____________________.','puis justifiez :'+lines(3))
p3='# Observer la deuxième tentative et comparer\n\n'+phase[phase.index('**E2'):]
p3=p3.replace('____________________.',lines(4))
p4=c[c.index('## 3.'):c.index('## 4.')]+ '\n\n'+a[a.index('## A.'):a.index('**A2')]
p5=a[a.index('## T.'):a.index('## I.')].replace('____________________.',lines(5))
p6=a[a.index('## I.'):a.index('## B.')].replace('____________________.',lines(4))
p6+='\nAvant de rendre votre travail, vérifiez que vous avez écrit une explication, pas seulement « oui » ou « non ».\n'
build('01-support-eleve',BREAK.join([p1,p2,p3,p4,p5,p6]))

intro='''# Guide d’accompagnement et de formation — U01.1

Réservé à l’enseignant. Préparation documentaire : aucun résultat d’essai n’est annoncé.

## Objectif, prérequis et organisation

L’élève distingue commande choisie et effet obtenu, explique un refus puis réutilise le raisonnement avec Nora et le curseur. Il sait repérer la droite et comparer deux positions ; aucun programme ni vocabulaire de théorie des agents n’est requis. La préparation scientifique enseignante qui suit ne suppose pas cette théorie et se déroule hors du temps élève.

Lire la procédure jointe et vérifier le laboratoire avant l’accueil. Imprimer le support élève en recto, garder ce guide et ses corrigés hors de vue. Distribuer progressivement : page 1, pages 2–3, puis page 4 après E2/E3, page 5 et page 6. La page 4 est l’explication de cours après observation ; elle ne doit pas anticiper les prédictions. Les références Markdown citées dans la reprise des sources désignent ici les parties correspondantes du dossier imprimé.

| Phase essentielle | Budget hypothétique | Intervention prévue |
|---|---|---|
| Contexte et C0 | 0–3 min | Faire repérer les données, sans annoncer l’issue. |
| P1, E1, P2, E2, E3 | 3–10 min | Lecture guidée du journal en E1 ; garder les prédictions. |
| Explication | 10–12 min | Faire distinguer ce qui est demandé et ce que vérifie le moteur. |
| Entraînement A1 | 12–14 min | Essais papier indépendants. |
| Nora T1–T2 | 14–17 min | Recueillir sans dicter la règle pertinente. |
| Curseur I1–I2 | 17–20 min | Réponse individuelle avant correction de Nora. |

Ce budget est à mesurer, non une durée validée. Noter pauses et temps techniques séparément ; ne supprimer aucune phase pour tenir vingt minutes. Les prolongements A2/B1 figurent seulement dans les corrigés de référence, hors de cet essai essentiel.

## Observer sans donner la réponse

Demander « quelle donnée du sujet utilises-tu ? » ou « peux-tu montrer ce que tu lis ? ». Éviter « le mur bloque, n’est-ce pas ? » et toute annonce du nombre de déplacements. Une relance peut néanmoins influencer : transcrire ses mots et conserver réponse initiale et réponse revue. Aider l’accès au journal en E1 est prévu, sans équivaloir à une preuve d’autonomie conceptuelle.

Recueillir Nora et le curseur avant correction ; distinguer autonome, avec relance, non établi, non observable. Un tableau juste sans explication ne suffit pas. Ne pas confondre erreur de repérage et confusion conceptuelle. Après recueil, employer les remédiations détaillées plus loin ; ne pas laisser un élève en échec pour préserver une mesure.

Pour un enseignant découvrant la notion : étudier d’abord le parcours complet ci-dessous, résoudre l’exercice enseignant avant ses corrigés, puis remplir le retour enseignant. Le Python est une préparation distincte et facultative, exécutée dans un interpréteur local ; il ne pilote pas le laboratoire.
'''
teacher=read('PARCOURS_ENSEIGNANT.md').replace('## 7. Références',BREAK+'## 7. Références')
build('02-guide-enseignant',intro+BREAK+teacher+BREAK+read('CORRIGES.md'))

obs='''# Grille d’observation — U01.1

Une grille par participant. Aucun nom ni correspondance code/identité. Ne rien préremplir comme résultat.

Code participant : __________ Code séance : __________ Version : __________

Public : Première / Terminale / enseignant : __________ Modalité : individuel accompagné / groupe : __________

Support : laboratoire réel / relevés fournis : __________ Temps relevés : individuels observés / collectifs : __________

## Temps réels et accès aux consignes

Inscrire heures/minutes/secondes selon le chronomètre retenu. Durée = fin − début ; pauses détaillées séparément. Une durée collective n’est pas une mesure individuelle. Écrire « non observé » si nécessaire.

| Phase | Budget cible, non mesuré | Début réel | Fin réelle | Durée réelle | Pauses / lecture / aide d’accès |
|---|---|---|---|---|---|
| Contexte C0 | 3 min | | | | |
| P1–E3 | 7 min | | | | |
| Explication | 2 min | | | | |
| A1 | 2 min | | | | |
| Nora T1–T2 | 3 min | | | | |
| Curseur I1–I2 | 3 min | | | | |
| Installation, hors budget | aucune cible | | | | |
| Remédiation, hors budget | aucune cible | | | | |

Lecture : noter la question et les mots précis qui posent problème, pas seulement « difficile ».
'''+lines(2)+BREAK+'''# Productions et transferts individuels

Code participant : __________ Code séance : __________

Codes : A = autonome ; R = avec relance (préciser laquelle page suivante) ; NE = non établi par la production ; NO = non observable. L’exactitude et l’aide sont deux informations distinctes : une réponse après indice ne devient pas autonome. Conserver la copie initiale.

| Tâche | Réponse initiale / emplacement sur la copie | Justification donnée / règle invoquée | Réponse après aide, si différente | Code A / R / NE / NO |
|---|---|---|---|---|
| Nora T1 : deux positions et effets | | | | |
| Nora T2 : commande et explication | | | | |
| Curseur I1 : deux positions, effets, règles | | | | |
| Curseur I2 : réfutation argumentée | | | | |

| Critère, sans note globale | Indice précis / incohérence à examiner | Code |
|---|---|---|
| V1 : distinguer commande et effet | | |
| V2 : expliquer un non-déplacement par la règle du cas | | |
| V3 : réemployer dans Nora ET curseur | | |

Un résultat correct sans raison explicite ne démontre pas à lui seul le mécanisme. Une tâche non traitée faute de temps n’établit pas une erreur conceptuelle. Consulter les corrigés réservés au guide après le recueil.
'''+BREAK+'''# Difficultés, interventions et suites à examiner

Code participant : __________ Code séance : __________

| Moment / tâche | Fait observé ou citation sans identité | Type : lecture / compréhension / technique / autre | Relance exacte ou aide matérielle | Réponse après intervention |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

Incident technique et conséquence sur le temps ou la modalité :
'''+lines(3)+'''
Analyse après recueil : indice constaté, hypothèse explicative, autre explication possible. Ne pas transformer une hypothèse en fait :
'''+lines(3)+'''
Proposition de correction à soumettre et preuve à rechercher lors d’un prochain essai :
'''+lines(3)
(ROOT/'OBSERVATION.md').write_text(obs.rstrip()+'\n',encoding='utf-8')
build('03-grille-observation',obs,True)
r=(ROOT/'RETOUR_ENSEIGNANT.md').read_text(encoding='utf-8')
# Chaque question garde son texte et dispose d’un espace de réponse.
r=re.sub(r'(?m)^(## [23]\. [^\n]+)',BREAK+r'\1',r)
r=r.replace('Réponse :', 'Réponse :'+lines(5))
r=r.replace('Prévision / exécution éventuelle / interprétation :','Prévision / exécution éventuelle / interprétation :'+lines(4))
r=r.replace('Ce qui reste à clarifier avant réutilisation en classe :','Ce qui reste à clarifier avant réutilisation en classe :'+lines(3))
build('04-retour-enseignant',r)
build('05-procedure',(ROOT/'PROCEDURE.md').read_text(encoding='utf-8'))
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.glob('*.md')}
(ROOT/'sources-sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Cinq DOCX construits ; contrôle Word et visuel encore nécessaire.')
