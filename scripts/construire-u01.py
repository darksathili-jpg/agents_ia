"""Pages U01.1 statiques : corpus approuvé unique, aucun convertisseur distant."""
from pathlib import Path
from html import escape
import hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'docs/pedagogie/refondation/u01'
REFERENCE = 'fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6'
FILES = ['COURS_ELEVE.md', 'ACTIVITES_ELEVE.md', 'PARCOURS_ENSEIGNANT.md', 'CORRIGES.md', 'GRILLE_EVALUATION.md']
def source(name):
    data=(SOURCE/name).read_bytes()
    original=subprocess.check_output(['git','show',f'{REFERENCE}:docs/pedagogie/refondation/u01/{name}'],cwd=ROOT)
    # Git peut normaliser CRLF lors du checkout ; le contenu doit rester identique.
    if data.replace(b'\r\n',b'\n') != original.replace(b'\r\n',b'\n'):
        raise ValueError(f'Source modifiée depuis la référence : {name}')
    return data.decode('utf-8-sig')
TEXT={name:source(name) for name in FILES}
POLICY_SOURCE=ROOT/'contenus/u01/regle-deplacement-v1.md'
POLICY=POLICY_SOURCE.read_text(encoding='utf-8')
LINKS={'COURS_ELEVE.md':'u01.html','ACTIVITES_ELEVE.md':'u01.html#entrainement','PARCOURS_ENSEIGNANT.md':'enseignant-u01.html','CORRIGES.md':'enseignant-u01.html#corriges','GRILLE_EVALUATION.md':'enseignant-u01.html#evaluation'}
def inline(text):
    tokens=[]
    def keep(value):tokens.append(value);return f'\x00{len(tokens)-1}\x00'
    text=re.sub(r'`([^`]+)`',lambda m:keep('<code>'+escape(m[1])+'</code>'),text)
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:keep('<a href="'+escape(LINKS.get(m[2],m[2]),quote=True)+'">'+escape(m[1])+'</a>'),text)
    text=escape(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',text)
    return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],text)

def answer(key,label):
    return f'<div class="answer"><label for="{key}">{escape(label)}</label><textarea id="{key}" data-answer="{key}" rows="3"></textarea></div>'

def markdown(text,form=False):
    lines=text.strip().splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>');i+=1
        elif line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*:?-+:?\s*',c) for c in cells):rows.append(cells)
                i+=1
            out.append('<p class="table-help">Si nécessaire, faites défiler le tableau horizontalement. Au clavier : sélectionnez le tableau, puis utilisez les flèches gauche et droite.</p><div class="table-scroll" role="region" aria-label="Tableau de la situation" tabindex="0"><table><thead><tr>'+''.join('<th scope="col">'+inline(c.strip())+'</th>' for c in rows[0])+'</tr></thead><tbody>')
            for ri,row in enumerate(rows[1:]):
                out.append('<tr>')
                for ci,c in enumerate(row):
                    c=c.strip()
                    if form and re.search(r'_{3,}',c):
                        key=f'{form}-ligne{ri+1}-col{ci+1}'
                        label=f'{rows[0][ci].strip()}, ligne {ri+1}'
                        prefix=re.sub(r'_{3,}', '',c).strip(' :')
                        out.append('<td>'+inline(prefix)+f'<label class="sr-only" for="{key}">{escape(label)}</label><textarea rows="2" id="{key}" data-answer="{key}"></textarea></td>')
                    else:out.append('<td>'+inline(c)+'</td>')
                out.append('</tr>')
            out.append('</tbody></table></div>')
        elif re.match(r'^#{1,6} ',line):
            level=min(4,len(line.split(' ')[0])+1)
            out.append(f'<h{level}>'+inline(line.lstrip('# '))+f'</h{level}>');i+=1
        elif line.startswith('- '):
            out.append('<ul>')
            while i<len(lines) and lines[i].strip().startswith('- '):out.append('<li>'+inline(lines[i].strip()[2:])+'</li>');i+=1
            out.append('</ul>')
        else:
            para=[line];i+=1
            while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|- )',lines[i].strip()):para.append(lines[i].strip());i+=1
            p=' '.join(para);out.append('<p>'+inline(p)+'</p>')
            if form:
                match=re.match(r'\*\*([CPEAITB]\d)[ .—]',p)
                if match and match[1] not in ('P1','E1','A1','T1','I1'):out.append(answer(match[1], 'Réponse '+match[1]))
                elif p.startswith('Commande :'):out.append(answer('P1-justification','P1 — Commande, case après et raison'))
            if p.startswith('**E1 —') and form:
                out.append('<div id="experience"><p class="callout">Laboratoire réel : les boutons ci-dessous agissent sur la grille. Conservez votre prédiction avant chaque tentative.</p><iframe id="u01-lab" src="laboratoire.html?u01=observation" title="Laboratoire Microduck — deux tentatives U01.1"></iframe><p><a href="laboratoire.html" target="_blank" rel="noopener">Ouvrir le laboratoire en pleine page (nouvel onglet)</a></p></div>')
    return '\n'.join(out)

def shell(title,content,teacher=False):
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} — Agent Academy</title><link rel="stylesheet" href="academy.css"><link rel="stylesheet" href="formation.css"><link rel="stylesheet" href="u01.css"><script src="u01.js" defer></script></head>
<body class="home formation light" data-course="U01.1" data-audience="{'enseignant' if teacher else 'eleve'}"><a class="skip" href="#formation">Aller au contenu</a><header class="masthead"><a class="brand" href="./"><span class="brand-title">Agent Academy</span></a><nav aria-label="Navigation principale"><a href="u01.html">U01.1 · Élève</a><a href="enseignant-u01.html">Parcours enseignant</a><label>Affichage <select id="formation-display"><option value="light">Clair</option><option value="dark">Sombre</option><option value="projector">Vidéoprojecteur</option></select></label></nav></header><main id="formation" tabindex="-1">{content}</main><footer><a href="./">Accueil</a> · <a href="u01.html">U01.1</a><p>Version expérimentale accompagnée · Durée et efficacité à examiner avec des apprenants.</p></footer></body></html>'''

def section(key,title,body,following=None):
    nav=f'<a class="action-link" href="#{following}">Continuer →</a>' if following else ''
    return f'<section class="sheet unit-stage" id="{key}" tabindex="-1"><h2>{escape(title)}</h2>{body}{nav}</section>'

course=TEXT['COURS_ELEVE.md'];activities=TEXT['ACTIVITES_ELEVE.md']
rule_explanation='<section id="regle-explication" class="rule-explanation" aria-labelledby="regle-titre"><h2 id="regle-titre">Comprendre la règle avant de manipuler</h2>'+markdown(POLICY.split('\n',1)[1])+'</section>'
parts=re.split(r'^## (.+)$',course,flags=re.M)
context=parts[0].split('\n',1)[1]+ '\n\n'+parts[2]
experiment=parts[4];explanation=parts[6];routing=parts[8]
training=activities.split('## A.',1)[1].split('**A2',1)[0]
optionalA='**A2'+activities.split('**A2',1)[1].split('## T.',1)[0]
nora=activities.split('## T.',1)[1].split('## I.',1)[0]
cursor=activities.split('## I.',1)[1].split('## B.',1)[0]
optionalB=activities.split('## B.',1)[1]
# Les titres de section sont déjà présentés par le fil ; aucun énoncé n’est réécrit.
training=training.split('\n',1)[1];nora=nora.split('\n',1)[1];cursor=cursor.split('\n',1)[1]
steps=[('contexte','1. Microduck et sa piste',markdown(context,'contexte')),
       ('essai','2. Prévoir, essayer et relever',rule_explanation+markdown(experiment,'essai')),
       ('comprendre','3. Comprendre ce qui s’est passé',markdown(explanation)),
       ('entrainement','4. Entraînement A1',markdown(training,'entrainement')),
       ('nora','5. Nora — transfert individuel',markdown(nora,'nora')),
       ('curseur','6. Curseur — bilan individuel',markdown(cursor,'curseur'))]
toc='<nav class="unit-toc" aria-label="Étapes U01.1">'+''.join(f'<a href="#{key}">{escape(title)}</a>' for key,title,_ in steps)+'</nav>'
intro='<div class="cover"><p class="eyebrow">U01.1 · PREMIÈRE UNITÉ</p><h1>Commander n’est pas déplacer</h1><p>Un parcours accompagné. Prévoir, observer deux tentatives, expliquer, puis réinvestir avec Nora et un curseur.</p></div><p class="callout">Vos réponses restent dans ce navigateur si son stockage est disponible. Elles ne sont pas envoyées à un enseignant et ne sont pas notées automatiquement. Exportez-les avant de changer de poste.</p><p id="save-status" role="status"></p><button id="export-notes" type="button">Exporter mes réponses U01.1</button>'+toc
body=intro+''.join(section(key,title,text,steps[i+1][0] if i+1<len(steps) else 'suite') for i,(key,title,text) in enumerate(steps))
body+='<section class="sheet unit-stage" id="suite" tabindex="-1"><h2>Après le parcours essentiel</h2>'+markdown(routing)+'<details><summary>Prolongements facultatifs A2 et B1 — hors du budget essentiel</summary>'+markdown(optionalA+'\n\n'+optionalB,'prolongements')+'</details><p><a href="enseignant-u01.html#corriges">Corrigés expliqués — à consulter après votre recherche</a></p></section>'
(ROOT/'u01.html').write_text(shell('U01.1 — Commander n’est pas déplacer',body),encoding='utf-8')

teacherparts=[]
for name,key,title in [('PARCOURS_ENSEIGNANT.md','preparation','Préparation scientifique complète'),('CORRIGES.md','corriges','Corrigés expliqués — après recherche'),('GRILLE_EVALUATION.md','evaluation','Grille de lecture des productions')]:
    rendered=markdown(TEXT[name].split('\n',1)[1])
    if name=='PARCOURS_ENSEIGNANT.md':
        rendered=rendered.replace('<h3>7. Références', '<h3 id="references">7. Références')
        marker='<h4>Exemple Python'
        rendered=rendered.replace(marker,'<h4 id="python">Exemple Python')
        rendered+='<details><summary>Exécuter le bloc Python de la porte dans le navigateur</summary><p>Préparation enseignante facultative, hors des vingt minutes élèves. Le code ci-dessous reprend exactement l’exemple du guide. Son affichage ne déplace pas Nora dans l’application. Le premier chargement nécessite Internet.</p><iframe src="laboratoire.html?u01=python" title="Python réel — table de transition de la porte" loading="lazy"></iframe></details>'
    if name=='CORRIGES.md':rendered='<details><summary>Afficher les corrigés U01.1 après recherche</summary>'+rendered+'</details>'
    teacherparts.append(section(key,title,rendered))
teacherintro='<div class="cover"><p class="eyebrow">U01.1 · ENSEIGNANTS NSI</p><h1>Comprendre pour accompagner</h1><p>La préparation scientifique est distincte du temps élève. Aucune connaissance préalable de la théorie des agents n’est supposée.</p></div><nav class="unit-toc" aria-label="Préparation enseignante"><a href="#preparation">Préparation complète</a><a href="#python">Python expliqué</a><a href="#references">Références</a><a href="#corriges">Corrigés</a><a href="#evaluation">Évaluation et remédiation</a></nav><p class="callout">Pour cette présentation web, le cours et les activités cités ci-dessous sont réunis dans U01.1. Les noms de fichiers mentionnés dans les consignes de distribution désignent ces documents sources. Conserver les prédictions et recueillir Nora et le curseur avant correction.</p>'
(ROOT/'enseignant-u01.html').write_text(shell('U01.1 — Parcours enseignant',teacherintro+''.join(teacherparts),True),encoding='utf-8')
landing='<div class="cover"><p class="eyebrow">MODULE 01</p><h1>Fondements scientifiques des agents intelligents</h1><p>Commencer par une distinction : commander n’est pas déplacer.</p></div><section class="sheet"><h2>U01.1 — Commander n’est pas déplacer</h2><p>Première version interactive pour essai accompagné. Vingt minutes constituent une hypothèse à mesurer.</p><a class="action-link" href="u01.html">Commencer U01.1 →</a><a class="action-link" href="enseignant-u01.html">Préparer côté enseignant →</a></section>'
(ROOT/'module01.html').write_text(shell('Module 01',landing),encoding='utf-8')
for filename,target in [('seance01.html','u01.html'),('enseignant-s01.html','enseignant-u01.html'),('ressources-module01.html','enseignant-u01.html')]:
    (ROOT/filename).write_text(f'<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><title>Ancien accès remplacé — Agent Academy</title><p>L’ancienne séance est retirée du parcours de formation. <a href="{target}">Ouvrir U01.1</a>.</p></html>\n',encoding='utf-8')

code=re.search(r'```python\n(.*?)```',TEXT['PARCOURS_ENSEIGNANT.md'],re.S).group(1)
lab=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Laboratoire U01.1 — Microduck</title><link rel="stylesheet" href="u01-laboratoire.css"><script src="laboratoire-moteur.js" defer></script><script src="u01-laboratoire.js" defer></script></head><body class="light"><a class="skip" href="#contenu-laboratoire">Aller au laboratoire</a><main id="contenu-laboratoire" tabindex="-1"><header class="lab-nav"><a href="u01.html#essai">Retour à U01.1</a><label>Affichage <select id="display"><option value="light">Clair</option><option value="dark">Sombre</option><option value="projector">Vidéoprojecteur</option></select></label></header><div id="navigation-lab"><h1>Microduck — deux tentatives</h1><label for="policy">Politique :</label><select id="policy"><option value="naive">Gloutonne (axe horizontal prioritaire)</option></select><div class="arena"><div id="grid" class="grid" role="img" aria-label="Grille de sept colonnes et cinq lignes ; sur la rangée étudiée, A (0,2), B (1,2), C mur (2,2), D (3,2), E (4,2), F (5,2), G arrivée (6,2)"></div><div class="stats"><div><span>Position actuelle</span><b id="position">0,2</b></div><div><span>Décisions prises</span><b id="steps">0</b></div><div><span>État</span><b id="state" role="status">Prêt</b></div><div><span>Dernière observation</span><span id="observation"></span></div></div></div><div class="controls"><button id="step">Exécuter une étape →</button><button id="reset">Réinitialiser</button></div><h2>Trace pédagogique</h2><div id="log" class="trace" role="log" tabindex="0" aria-live="polite"></div></div><section id="python-panel" hidden><h1>Python — la porte de Nora</h1><label for="code">Éditeur Python — exemple du parcours enseignant</label><textarea id="code" spellcheck="false" rows="25">{escape(code)}</textarea><div class="controls"><button id="py-run">Exécuter Python</button><button id="py-reset">Restaurer l’exemple de la porte</button><button id="py-stop">Stop Python</button></div><p id="py-status" role="status">Non chargé</p><h2>Console Python</h2><pre id="py-output" class="trace" tabindex="0" aria-live="polite">Le code sera exécuté uniquement à votre demande.</pre></section><div hidden><button id="run">Exécution auto</button><button id="check">Vérifier</button><p id="feedback"></p><p id="explain"></p><span id="statuspill"></span></div></main></body></html>'''
lab=lab.replace('<div class="arena">',rule_explanation+'<div class="arena">',1)
breakdown='''<section id="decision-detail" aria-labelledby="detail-title" aria-live="polite" aria-atomic="true"><h2 id="detail-title">Lire la tentative</h2><p id="detail-empty">Après une étape, les quatre informations ci-dessous décriront la tentative réellement exécutée.</p><dl id="detail-values" hidden><div><dt>1. Commande choisie</dt><dd id="detail-command"></dd></div><div><dt>2. Raison du choix par la règle</dt><dd id="detail-reason"></dd></div><div><dt>3. Vérification par le moteur</dt><dd id="detail-check"></dd></div><div><dt>4. Déplacement effectivement réalisé</dt><dd id="detail-effect"></dd></div></dl></section>'''
lab=lab.replace('<h2>Trace pédagogique</h2>',breakdown+'<h2>Trace pédagogique</h2>')
(ROOT/'laboratoire.html').write_text(lab,encoding='utf-8')
manifest={'version':'U01.1','reference':REFERENCE,'empreintes':'SHA-256 du texte UTF-8, fins de ligne LF','sources':{name:hashlib.sha256((SOURCE/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in FILES},'pages':['u01.html','enseignant-u01.html','module01.html','laboratoire.html']}
manifest['complement_pedagogique']={'version':1,'source':POLICY_SOURCE.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(POLICY_SOURCE.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),'objet':'Explication de la règle existante, sans modification des exercices ni du moteur'}
(ROOT/'u01-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('U01.1 construite depuis les cinq sources approuvées ; anciens accès remplacés.')
