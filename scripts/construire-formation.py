"""Produit des pages statiques depuis notre corpus, sans dépendance ni CDN Markdown.

Convertisseur limité à la syntaxe employée dans ce dossier : titres, paragraphes,
listes simples, tableaux, code et liens. Le corpus source reste la référence.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs/pedagogie/module-01"


def destination(url):
    if url.startswith(("https://", "http://", "#")):
        return url
    if url.endswith(".md"):
        return "ressources-module01.html#" + Path(url).stem.lower()
    return "docs/pedagogie/module-01/" + url


def inline(text):
    tokens = []
    def keep(html):
        tokens.append(html)
        return f"\x00{len(tokens)-1}\x00"
    text = re.sub(r"`([^`]+)`", lambda m: keep("<code>"+escape(m[1])+"</code>"), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: keep(f'<a href="{escape(destination(m[2]), quote=True)}">{escape(m[1])}</a>'), text)
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m[1])], text)


def markdown(text):
    lines = text.strip().splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            code, i = [], i+1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            out.append("<pre><code>"+escape("\n".join(code))+"</code></pre>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = lines[i].strip().strip("|").split("|")
                if not all(re.fullmatch(r"\s*:?-+:?\s*", cell) for cell in cells):
                    rows.append(cells)
                i += 1
            out.append('<div class="table-scroll"><table><thead><tr>'+"".join('<th scope="col">'+inline(c)+"</th>" for c in rows[0])+"</tr></thead><tbody>"+"".join("<tr>"+"".join("<td>"+inline(c)+"</td>" for c in row)+"</tr>" for row in rows[1:])+"</tbody></table></div>")
        elif re.match(r"^#{1,6} ", line):
            heading = re.match(r"^(#+) (.*)", line)
            level = min(4, max(3, len(heading[1])+1))
            out.append(f"<h{level}>"+inline(heading[2])+f"</h{level}>"); i += 1
        elif re.match(r"^(- |\d+\. )", line):
            ordered = bool(re.match(r"^\d+\. ", line))
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>")
            pattern = r"^\d+\. " if ordered else r"^- "
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                out.append("<li>"+inline(re.sub(pattern,"",lines[i].strip()))+"</li>"); i += 1
            out.append(f"</{tag}>")
        else:
            paragraph = [line]; i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||```|- |\d+\. )",lines[i].strip()):
                paragraph.append(lines[i].strip()); i += 1
            out.append("<p>"+inline(" ".join(paragraph))+"</p>")
    return "\n".join(out)


def shell(title, content):
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} — Agent Academy</title><link rel="stylesheet" href="academy.css"><link rel="stylesheet" href="formation.css"><script src="formation.js" defer></script></head>
<body class="home formation light"><a class="skip" href="#formation">Aller au contenu</a>
<header class="masthead"><a class="brand" href="./"><svg class="brand-mark" aria-hidden="true"><use href="assets/carnet-reperes.svg#marque"/></svg><span class="brand-copy"><span class="brand-title">Agent Academy</span><span class="brand-subtitle">Le carnet des agents IA</span></span></a><nav aria-label="Navigation principale"><a href="module01.html">Module 01</a><a href="seance01.html">Séance S01</a><a href="enseignant-s01.html">Enseignants</a><label>Affichage <select id="formation-display"><option value="light">Clair</option><option value="dark">Sombre</option><option value="projector">Vidéoprojecteur</option></select></label></nav></header>
<main id="formation" tabindex="-1">{content}</main><footer><p>Comprendre avant d’automatiser. Tester avant de conclure.</p><a href="./">Retour à l’accueil</a> · <a href="module01.html">Le module 01</a> · <a href="laboratoire.html">Laboratoire indépendant</a><p>Prototype pédagogique S01 · Validation en classe à venir · Aucun LLM utilisé dans ces expériences.</p></footer></body></html>'''


def cover(title, description):
    return f'<div class="cover"><span class="robot-picture" role="img" aria-label="Microduck accompagne la lecture"></span><p class="eyebrow">MODULE 01 / CARNET SCIENTIFIQUE</p><h1>{title}</h1><p>{description}</p></div>'


def note(key, label):
    return f'<label for="{key}">{label}</label><textarea id="{key}" data-save="{key}" rows="3"></textarea>'


course = (DOC / "SEANCE_01.md").read_text(encoding="utf-8-sig")
parts = re.split(r"^## (.+)$", course, flags=re.M)
titles = parts[1::2]
questions = [
    "D1–D5 : notez vos prédictions et expliquez la différence entre print et return.",
    "Dessinez les frontières du système : que reçoit-il et quelle commande retourne-t-il ?",
    "Deux tentatives : relevez position avant, commande, effet et position après. Expliquez votre comparaison.",
    "H1, H2, H3 : quel test départage les hypothèses et pourquoi ?",
    "Porte, grille, FAQ ou assistant : justifiez un recouvrement de catégories et une limite du cadre.",
    "Consignez une prédiction, les appels testés, leurs sorties et le comportement réel sur la grille.",
    "Pourquoi la commande droite peut-elle être valide mais refusée ? Quelle amélioration demanderait un autre mécanisme ?",
    "Porte et clé : observations, actions, test proposé et question sur la mémoire.",
    "Définissez l’agent, justifiez automate et agent, expliquez l’absence de LLM et proposez un test manquant.",
    "Quelle adaptation Première ou Terminale retiendriez-vous ?"
]
extras = {}
extras[0] = '<div class="work"><h3>Diagnostic sans note · 5 min puis 3 min de confrontation</h3><p>Pour choisir_x(x,cible_x) : si x est inférieur, retourner droite ; s’il est supérieur, gauche ; sinon arrêt. Prédire choisir_x(0,2), choisir_x(4,2), choisir_x(2,2). Une fonction annoncer() contient seulement print("haut") : que retourne-t-elle ? Depuis (2,1), quelle position donne un mouvement droite ?</p><button id="diagnostic-check" type="button">Confronter le diagnostic</button><p id="diagnostic-feedback" class="feedback" aria-live="polite"></p><a href="docs/pedagogie/module-01/python/s01_diagnostic.py">Code exact du diagnostic</a></div>'
extras[2] = '<div class="work"><h3>Observer vraiment Microduck</h3><p>Avant le premier pas, écrivez une prédiction. Gardez la politique gloutonne, réinitialisez, puis exécutez deux étapes. Le journal ci-dessous provient du moteur existant.</p><label for="prediction">Ma prédiction avant de lancer</label><input id="prediction" type="text" data-save="prediction"><iframe id="observation-lab" class="observation-frame" src="laboratoire.html?s01=observation" title="Expérience S01 : grille et journal réels" loading="lazy"></iframe><button id="compare-prediction" type="button">Comparer ma prédiction à la trace</button><p id="comparison" class="feedback" aria-live="polite"></p></div>'
extras[5] = '<div class="work"><h3>TP01 · Quarante minutes pour programmer et tester</h3><p>Départ volontaire : arrêt. Complétez la comparaison horizontale, puis verticale. Testez cible à droite, à gauche, à la même position et au-dessus. Les appels console gardent leur propre cible ; la grille conserve (6,2). L’éditeur et le journal ci-dessous appartiennent au véritable laboratoire.</p><p><strong>Console :</strong> Exécuter Python. <strong>Grille :</strong> choisir Mon agent Python, Réinitialiser puis Exécuter une étape. Une boucle ajoutée par erreur peut être interrompue avec Stop Python. Internet est nécessaire au premier chargement.</p><iframe id="python-lab" src="laboratoire.html?s01=python" title="Atelier S01 : éditeur Python réel et grille" loading="lazy"></iframe><p><a href="laboratoire.html?s01=python" target="_blank" rel="noopener">Ouvrir cet atelier en pleine page (nouvel onglet)</a> si la fenêtre intégrée est trop étroite.</p><details><summary>Indices gradués pour le TP</summary><p>1. Décomposer position et objectif en x/y. 2. Comparer d’abord les abscisses. 3. En cas d’égalité, comparer les ordonnées. À la cible, retourner arrêt. Les obstacles sont reçus mais cette règle ne calcule pas de détour.</p></details></div>'
extras[8] = '''<div class="work"><h3>Bilan individuel : raisonner, tester, expliquer</h3>
<fieldset><legend>Un système à règles peut-il être un agent ?</legend><label><input type="radio" name="definition" value="a"> Seulement avec un LLM.</label><label><input type="radio" name="definition" value="b"> Oui, si l’on explicite observations, décisions, actions et environnement.</label></fieldset>
<fieldset><legend>La seconde commande gloutonne est droite, mais la position reste (1,2). Pourquoi ?</legend><label><input type="radio" name="transition" value="a"> Python a choisi gauche.</label><label><input type="radio" name="transition" value="c"> Le moteur a refusé l’entrée dans le mur.</label></fieldset>
<fieldset><legend>Quel test distingue un retour constant droite d’une comparaison ?</legend><label><input type="radio" name="preuve" value="a"> Proposer une cible à gauche en console.</label><label><input type="radio" name="preuve" value="b"> Rejouer seulement la même cible à droite.</label></fieldset>
'''+note('bilan-raisonnement','Justifiez vos choix ; donnez une limite et un cas de test Python avec résultat attendu.')+'''<button id="check-learning" type="button">Vérifier les repères et préparer la discussion</button><p id="learning-feedback" class="feedback" aria-live="polite"></p><details><summary>Critères de compréhension et remédiation</summary><p>On recherche un schéma cohérent, un recouvrement automate/agent justifié, l’explication sans LLM et un test discriminant. Trois éléments sur quatre dont commande/effet : seuil formatif proposé, à éprouver en classe. La programmation et les réponses argumentées doivent être relues par l’enseignant. Refaire un pas et son journal si la commande est confondue avec son effet.</p></details></div>'''
sections = []
for i, title in enumerate(titles):
    body = markdown(parts[2*i+2])
    previous = f'<a href="#etape-{i-1}">← Étape précédente</a>' if i else '<a href="module01.html">← Le module</a>'
    following = f'<a href="#etape-{i+1}">Étape suivante →</a>' if i+1 < len(titles) else '<a href="enseignant-s01.html">Approfondir côté enseignant →</a>'
    sections.append(f'<section class="sheet" id="etape-{i}"><p class="eyebrow">PAGE {i+1:02} / S01</p><h2>{escape(title)}</h2>'+body+extras.get(i,"")+note(f'reponse-{i}', questions[i])+f'<nav class="page-turn" aria-label="Suite de la page {i+1}">{previous}{following}</nav></section>')
toc = '<aside class="contents"><nav aria-label="Étapes de S01"><strong>Ton fil de séance</strong><ol>'+''.join(f'<li><a href="#etape-{i}">{escape(t.split(" — ")[0])}</a></li>' for i,t in enumerate(titles))+'</ol></nav><a href="enseignant-s01.html">Préparer et approfondir S01</a></aside>'
intro = markdown(parts[0].split('\n',1)[1])
content = cover('Qu’est-ce qu’un agent intelligent ?', 'S01 · 120 min estimées · Observer, formuler une hypothèse, programmer et interpréter. Une vraie séance avec Microduck, sans LLM.')+f'<section class="sheet"><h2>Avant d’ouvrir le carnet</h2>{intro}<p class="callout">Vos réponses écrites restent dans ce navigateur ; elles ne sont pas envoyées à un enseignant. Utilisez l’export pour les lui remettre. Les choix du bilan ne sont pas conservés : le raisonnement écrit l’est.</p><p id="save-status" class="local-state" role="status">Réponses écrites enregistrées localement lorsque le navigateur le permet.</p><button id="export-notes" type="button">Exporter mes réponses S01</button></section><div class="reading">{toc}<article aria-label="Cours complet S01">'+''.join(sections)+'</article></div>'
(ROOT/'seance01.html').write_text(shell('S01 — Qu’est-ce qu’un agent intelligent ?',content),encoding='utf-8')

# Parcours enseignant : un travail de préparation distinct, avec tout le contenu S01.
teacher = (DOC/'APPROFONDISSEMENTS_ENSEIGNANTS.md').read_text(encoding='utf-8-sig')
theory = teacher.split('## 1.',1)[1].split('## 4.',1)[0]
theory = '## 1.'+theory
theory = re.sub(r'\*\*Actualisation S03.*?\n\n','',theory,flags=re.S)
production=(DOC/'PRODUCTION_ENSEIGNANT_S01.md').read_text(encoding='utf-8-sig')
references=(DOC/'REFERENCES_SCIENTIFIQUES.md').read_text(encoding='utf-8-sig')
teacherparts=[('preparer','Préparer une séance, pas seulement lire plus', '<p>Objectifs : délimiter le système, formaliser observation et transition, construire une contre-épreuve, comparer un critère et transposer. Avant les corrigés, produire trois schémas de frontière et un paragraphe de justification. Conserver 40 min de Python dans les 120 min ; les lectures longues ci-dessous sont préparatoires.</p>'+note('enseignant-production','Votre production : frontières, trace, critère, test discriminant et adaptation au niveau choisi.')),
('formaliser','Définitions, formalisation et problèmes',markdown(theory)),
('production','Production attendue et critique du modèle',markdown(production.split('\n',1)[1])),
('didactique','Transposition et lecture critique', '<p>Comparer R1 et R2 : préciser le cadre retenu, puis un cas frontière. Le contrôleur, la fonction et le Worker sont des frontières différentes ; la réponse attendue doit annoncer ce qui est observé et ce qui est effectivement commandé. Une lecture de synthèse ne remplace pas la contre-épreuve du programme.</p>'+markdown(teacher.split('## 6.',1)[1].split('Prolongement enseignant facultatif',1)[0])),
('correction','Corrigés S01 et remédiations',''),
('references','Références et statut des sources',markdown(references))]
# La correction complète reste lisible dans le carnet documentaire ; la solution TP01 est ci-dessous.
solution='''def decider(position, objectif, obstacles):
    x, y = position
    gx, gy = objectif
    if x < gx:
        return "droite"
    if x > gx:
        return "gauche"
    if y < gy:
        return "bas"
    if y > gy:
        return "haut"
    return "arrêt"

assert decider((0, 2), (2, 2), []) == "droite"
assert decider((4, 2), (2, 2), []) == "gauche"
assert decider((2, 2), (2, 2), []) == "arrêt"
assert decider((2, 2), (2, 1), []) == "haut"
print("S01_CORRECTION_OK")
'''
(ROOT/'docs/pedagogie/module-01/python/s01_solution_interface.py').write_text(solution,encoding='utf-8')
teacherparts[4]=('correction','Corrigés S01 et remédiations','<p>Diagnostic : droite, gauche, arrêt ; print affiche mais ne remplace pas return ; la coordonnée suivante est (3,1). Le diagnostic ne doit pas absorber les quarante minutes de TP.</p><pre><code>'+escape(solution)+'</code></pre><p>Cette politique reçoit les murs mais ne recherche pas de détour : le deuxième pas est refusé sur cette carte. Le corrigé n’est pas une solution générale de navigation. Dans le transfert porte/clé, exiger observations, actions, un test et une question sur une information qui disparaît. Au bilan, vérifier la justification et le test proposé ; les réponses libres ne sont pas automatiquement notées.</p><a href="ressources-module01.html#corriges">Tous les corrigés documentaires, lisibles ici</a>')
teacherbody=''.join(f'<section class="sheet" id="{id}"><h2>{title}</h2>{body}</section>' for id,title,body in teacherparts)
teacherTOC='<aside class="contents"><nav aria-label="Préparation enseignante"><ol>'+''.join(f'<li><a href="#{id}">{title}</a></li>' for id,title,_ in teacherparts)+'</ol></nav><a href="seance01.html">Retour à la séance élève</a></aside>'
(ROOT/'enseignant-s01.html').write_text(shell('S01 — Parcours enseignant',cover('Préparer, éprouver, transmettre.', 'S01 / Enseignants NSI · Formaliser le système, confronter les modèles et préparer la transposition.')+'<p id="save-status" role="status">Notes de préparation conservées dans ce navigateur.</p><button id="export-notes" type="button">Exporter ma préparation</button><div class="reading">'+teacherTOC+'<article>'+teacherbody+'</article></div>'),encoding='utf-8')

cards=[('S01','Qu’est-ce qu’un agent intelligent ?', 'Leçon intégrée · diagnostic, expérience réelle, TP Python et bilan.', 'seance01.html','Suivre S01'),('S02','Environnement, observations et actions', 'Contenu scientifique disponible. Fiche et cours documentaire ; activités non intégrées dans l’application.', 'ressources-module01.html#seance_02','Lire les documents S02'),('S03','Architectures, politiques de décision et mémoire', 'Contenu scientifique disponible. Fiche et cours documentaire ; boucle mémoire en script, sans moteur graphique intégré.', 'ressources-module01.html#seance_03','Lire les documents S03')]
modulebody=cover('Fondements scientifiques des agents intelligents', 'Module 01 · Niveau NSI et préparation enseignante · Cinq séances prévues, une expérience intégrée aujourd’hui.')+'<div class="session-list">'+''.join(f'<section class="sheet"><p class="eyebrow">{n}</p><h2>{title}</h2><p>{desc}</p><a class="action-link" href="{link}">{label} →</a></section>' for n,title,desc,link,label in cards)+'<section class="sheet future"><p class="eyebrow">S04 · À venir</p><h2>Programmer et expérimenter</h2><p>Conception suspendue : aucune activité disponible.</p></section><section class="sheet future"><p class="eyebrow">S05 · À venir</p><h2>Évaluer et préparer les LLM</h2><p>Conception suspendue : aucune activité disponible.</p></section><section class="sheet"><p class="eyebrow">Préparation enseignante</p><h2>Le fond scientifique du carnet</h2><p>Problèmes, démonstrations conditionnelles, limites, transposition et corrigés S01.</p><a class="action-link" href="enseignant-s01.html">Préparer S01 →</a></section></div>'
(ROOT/'module01.html').write_text(shell('Module 01',modulebody),encoding='utf-8')
documents=[]
for path in sorted(DOC.glob('*.md')):
    if path.stem.startswith('AUDIT') or path.stem=='README':
        continue
    text=path.read_text(encoding='utf-8-sig'); title=text.splitlines()[0].lstrip('# ')
    documents.append((path.stem.lower(),title,markdown(text.split('\n',1)[1])))
resourceTOC='<nav class="sheet" aria-label="Documents du module"><ul>'+''.join(f'<li><a href="#{id}">{escape(title)}</a></li>' for id,title,_ in documents)+'</ul></nav>'
resourcebody=cover('Les pages scientifiques du module', 'Lecture documentaire S01–S03. Les documents S02 et S03 sont disponibles ; leur expérience de formation n’est pas encore intégrée.')+resourceTOC+''.join(f'<section class="sheet" id="{id}"><h2>{escape(title)}</h2>{body}<a href="#formation">Retour à l’index documentaire ↑</a></section>' for id,title,body in documents)
(ROOT/'ressources-module01.html').write_text(shell('Documents du module 01',resourcebody),encoding='utf-8')
print('FORMATION_CONSTRUITE : quatre pages HTML statiques, cours S01 entier et supports enseignants')
