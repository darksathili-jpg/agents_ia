'use strict';
// ORCHESTRA Terminale T01 : résultats et traces produits exclusivement par
// runner.py exécuté par Pyodide. Aucun score « simulé » dans la page.
const $=id=>document.getElementById(id);
const source=$('code');
const STARTER=`"""Terminale NSI - séance T01 : BFS avec une file FIFO.

La classe File suit la règle FIFO : le premier sommet ajouté est le premier retiré.
Tu dois écrire toi-même la recherche en largeur et la replanification.
"""

class File:
    """File : le premier élément ajouté est le premier retiré (FIFO)."""
    def __init__(self):
        self.elements = []

    def enfiler(self, valeur):
        self.elements.append(valeur)

    def defiler(self):
        return self.elements.pop(0)

    def est_vide(self):
        return len(self.elements) == 0


class AgentPlanificateur:
    def __init__(self, position):
        self.position = position
        self.plan = []

    def planifier(self, monde, objectif):
        """Renvoie le plus court chemin [départ, ..., arrivée] ou [].

        À faire : utiliser File, monde.voisins et les prédécesseurs.
        """
        raise NotImplementedError("Programme le parcours en largeur")

    def pas_suivant(self, monde, objectif):
        """Renvoie la prochaine case après vérification du plan.

        Si un obstacle apparaît, calcule un nouveau chemin.
        Renvoie None si l'agent doit s'arrêter.
        """
        raise NotImplementedError("Programme la décision et la replanification")`;
const KEY='orchestra-terminale-t01-draft';
// Métadonnées générées à partir des situations Python : outils/generer_cas.py
const CASES=window.ORCHESTRA_CASES||{};
const TEST_TOTAL=Object.keys(CASES).length;
let active='direct',results=null,frame=0,worker=null,ready=false,running=false,token=0,timer=null;
function remember(){try{localStorage.setItem(KEY,JSON.stringify({code:source.value,hypothesis:$('hypothesis').value}));$('saved').textContent='Brouillon enregistré dans ce navigateur';}catch(_){$('saved').textContent='Stockage local indisponible : exporte ton bilan.';}}
function restore(){let saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(_){} source.value=typeof saved.code==='string'?saved.code:STARTER;$('hypothesis').value=typeof saved.hypothesis==='string'?saved.hypothesis:'';}
function highlight(){const area=$('highlight-code');area.textContent=source.value+'\n';if(window.Prism?.languages?.python){try{window.Prism.highlightElement(area);$('code-shell').classList.add('syntax-ready')}catch(_){$('code-shell').classList.remove('syntax-ready')}}else{$('code-shell').classList.remove('syntax-ready')}const n=source.value.split('\n').length;$('lines').textContent=Array.from({length:n},(_,i)=>i+1).join('\n');syncScroll();}
function syncScroll(){const gutter=$('lines');gutter.style.height=`${source.clientHeight}px`;gutter.scrollTop=source.scrollTop;$('highlight').style.transform=`translate(${-source.scrollLeft}px,${-source.scrollTop}px)`;}
function execute(){if(!ready||running)return;running=true;$('run').disabled=true;$('run').textContent='Tests en cours…';setRuntime('Exécution de neuf situations Python…','loading');const id=++token;timer=setTimeout(()=>{if(id!==token)return;running=false;results=null;terminate();showFailure('Temps limite de 9 secondes dépassé. Ton code est conservé ; Python va redémarrer automatiquement.');startWorker();},9000);worker.postMessage({type:'run',id,source:source.value});}
function terminate(){if(timer){clearTimeout(timer);timer=null;}if(worker){worker.terminate();worker=null;}ready=false;}
function setRuntime(s,state){$('runtime-text').textContent=s;$('runtime-led').className=state==='ready'?'ready':state==='error'?'fail':'';}
function startWorker(){terminate();running=false;++token;$('run').disabled=true;$('run').textContent='Charger Python…';setRuntime('Préparation de Python : installation locale ou téléchargement…','loading');worker=new Worker('python-worker.js'); // Le chargement a son propre numéro de génération ; l'id de requête est libre.
 worker.onmessage=e=>{const m=e.data||{};if(worker!==currentWorker)return;if(m.type==='ready'){ready=true;$('run').disabled=false;$('run').textContent='▶ Exécuter mes tests';setRuntime('Python prêt. Le moteur exécutera ton programme.','ready');}else if(m.type==='error'){running=false;if(timer){clearTimeout(timer);timer=null;}setRuntime('Erreur Python : '+(m.message||'inconnue'),'error');showFailure('Python indisponible : '+(m.message||'erreur inconnue')+'. Vérifie INSTALLER_PYODIDE.cmd ou la connexion du lycée.');$('run').disabled=!ready;$('run').textContent='▶ Réessayer';}else if(m.type==='result'&&m.id===token){running=false;if(timer){clearTimeout(timer);timer=null;}results=m.data;hideFailure();frame=0;renderResults();drawBoard();renderEvents();renderFIFO();$('run').disabled=false;$('run').textContent='▶ Relancer mes tests';const done=results?.passed??0;setRuntime(`Évaluation terminée : ${done}/${TEST_TOTAL} situations réussies.`,'ready');}};
 const currentWorker=worker;
 worker.onerror=e=>{if(currentWorker!==worker)return;running=false;setRuntime('Worker indisponible : '+(e.message||'erreur de chargement'),'error');showFailure('Impossible de lancer Python dans ce navigateur. Vérifie la connexion ou installe Pyodide localement.');$('run').disabled=true;};
}
function onKey(e){if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();execute();return;}let act=null;if(e.key==='Tab'){e.preventDefault();act=e.shiftKey?'unindent':'indent';}else if(e.key==='Enter'){e.preventDefault();act='enter';}else if(e.key==='Backspace'&&!e.ctrlKey&&!e.metaKey&&!e.altKey){act='backspace';}if(act&&window.OrchestraIndent?.applyToTextarea(source,act)){if(e.key==='Backspace')e.preventDefault();}}
function showFailure(message){const el=$('failure-banner');el.hidden=false;el.textContent=message;$('score').textContent='Exécution interrompue';$('test-list').replaceChildren();}
function hideFailure(){$('failure-banner').hidden=true;$('failure-banner').textContent='';}
function resultFor(id){return results?.results?.find(r=>r.id===id)||null;}
function showCase(id){active=id;frame=0;document.querySelectorAll('[data-case]').forEach(b=>{const selected=b.dataset.case===id;b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected));});drawBoard();renderEvents();renderFIFO();}
function frameData(){const r=resultFor(active);return r?.trace?.[frame]||null;}
function node(name,attributes,parent,text){const e=document.createElementNS('http://www.w3.org/2000/svg',name);for(const [key,value] of Object.entries(attributes||{}))e.setAttribute(key,String(value));if(text!==undefined)e.textContent=text;(parent||$('board')).appendChild(e);return e;}
function drawBoard(){const svg=$('board');svg.replaceChildren();const example=CASES[active];const actual=resultFor(active);const world=actual?.world||example;const w=world.width,h=world.height;const cell=Math.min(64,450/w,315/h);const ox=(560-w*cell)/2,oy=(400-h*cell)/2;const trace=frameData();const pos=trace?.position||world.start,obstacles=trace?.obstacles||world.obstacles;
 node('rect',{x:0,y:0,width:560,height:400,fill:'transparent'});
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const blocked=obstacles.some(p=>p[0]===x&&p[1]===y);node('rect',{x:ox+x*cell+2,y:oy+y*cell+2,width:cell-4,height:cell-4,rx:8,fill:blocked?'#77959c':'#ffffff',stroke:blocked?'#506c74':'#d4e6e6','stroke-width':1.4});if(blocked){node('path',{d:`M ${ox+x*cell+cell*.32} ${oy+y*cell+cell*.32} L ${ox+x*cell+cell*.68} ${oy+y*cell+cell*.68} M ${ox+x*cell+cell*.68} ${oy+y*cell+cell*.32} L ${ox+x*cell+cell*.32} ${oy+y*cell+cell*.68}`,stroke:'#e2eeee','stroke-width':3,'stroke-linecap':'round'});}}
 const exploration=trace?.explored||[];exploration.forEach((p,i)=>{if(Array.isArray(p)&&p.length===2)node('circle',{cx:ox+(p[0]+.5)*cell,cy:oy+(p[1]+.5)*cell,r:cell*.12,fill:'#2865d5',opacity:.25+i/Math.max(1,exploration.length)*.4});});
 const plan=trace?.plan||[];if(plan.length>1){let d=plan.map((p,i)=>`${i?'L':'M'} ${ox+(p[0]+.5)*cell} ${oy+(p[1]+.5)*cell}`).join(' ');node('path',{d,fill:'none',stroke:'#15ab9d','stroke-width':7,'stroke-linecap':'round','stroke-linejoin':'round','stroke-dasharray':'8 7',opacity:.75})}
 const c=(p)=>[ox+(p[0]+.5)*cell,oy+(p[1]+.5)*cell];const g=c(world.goal);node('circle',{cx:g[0],cy:g[1],r:cell*.28,fill:'#f3bd51',stroke:'#bb8622','stroke-width':2});node('text',{x:g[0],y:g[1]+5,'text-anchor':'middle','font-size':Math.max(15,cell*.29),fill:'#5b4113','font-weight':'900'},null,'◆');
 const robot=c(pos);node('circle',{cx:robot[0],cy:robot[1],r:cell*.34,fill:'#bfe9ff',stroke:'#1d82ba','stroke-width':2});node('image',{href:'../assets/avatar-east.webp',x:robot[0]-cell*.39,y:robot[1]-cell*.39,width:cell*.78,height:cell*.78});
 const status=trace?`${trace.action} · position (${pos[0]}, ${pos[1]})`:(results?'Aucune trace pour ce test.':'Aperçu du terrain avant exécution.');$('scene-caption').textContent=trace?.event?`${trace.event} ${status}`:status;const seen=$('exploration');if(seen){seen.textContent=exploration.length?`${exploration.length} demande(s) de voisins enregistrée(s) lors de l’exploration : ${exploration.slice(0,12).map(p=>`(${p.join(',')})`).join(' → ')}${exploration.length>12?' …':''}`:'Les appels à monde.voisins apparaîtront après les tests : points bleus dans la grille.';}
 const steps=actual?.trace?.length||0;$('previous').disabled=steps===0||frame<=0;$('next').disabled=steps===0||frame>=steps-1;$('frame').textContent=steps?`Étape ${frame+1} / ${steps}`:'Aucune exécution';svg.setAttribute('aria-label',`Grille ${w} par ${h}. Robot en (${pos[0]}, ${pos[1]}), cible en (${world.goal[0]}, ${world.goal[1]}). ${obstacles.length} obstacles.`);
}
function renderEvents(){const el=$('events');el.replaceChildren();const entries=resultFor(active)?.trace||[];if(!entries.length){const li=document.createElement('li');li.textContent='Lance tes tests pour observer les événements.';el.appendChild(li);return;}entries.forEach((t,i)=>{const li=document.createElement('li');li.className=i===frame?'current':'';li.textContent=t.event?`⚠ ${t.event}`:`${String(t.step).padStart(2,'0')} · ${t.action} → (${t.position.join(', ')})`;el.appendChild(li);});}
function renderResults(){
 const el=$('test-list');el.replaceChildren();
 const total=results?.total??TEST_TOTAL;
 $('score').textContent=`${results?.passed||0} / ${total} contrats complets`;
 const breakdown=$('score-breakdown');
 if(breakdown)breakdown.textContent=results?.results?.length
  ?`Trajet correct : ${results.functional_passed??'—'}/${total} · Méthode observée : ${results.method_passed??'—'}/${total}. Une réussite technique ne prouve pas à elle seule la compréhension.`
  :'Les résultats du trajet et de la méthode seront affichés séparément.';
 if(results?.error){const p=document.createElement('p');p.className='placeholder';p.textContent=results.error;el.appendChild(p);return;}
 for(const test of results?.results||[]){
  const row=document.createElement('div');row.className='test-row '+(test.ok?'ok':'error');
  const s=document.createElement('span');s.className='status';s.textContent=test.ok?'✓':'!';
  const desc=document.createElement('div');
  const name=document.createElement('strong');name.textContent=test.name;
  const detail=document.createElement('small');
  const checks=[['Chemin',test.phases?.planifier],['FIFO observée',test.phases?.fifo],['Déplacements',test.phases?.pas_suivant],['Plan conservé',test.phases?.memoire]];
  detail.textContent=checks.map(([label,phase])=>`${label} ${phase?.ok?'✓':'✗'}`).join(' · ');
  const explanation=document.createElement('p');explanation.className='test-explanation';
  explanation.textContent=test.ok?`${test.steps} déplacement(s) ; aucune anomalie détectée.`:
    checks.filter(([_,phase])=>!phase?.ok).map(([label,phase])=>`${label} : ${phase?.message||'à revoir'}`).join(' — ');
  desc.append(name,detail,explanation);
  const b=document.createElement('b');b.textContent=test.ok?'CONFORME':test.functional_ok?'MÉTHODE À REVOIR':'À CORRIGER';
  row.append(s,desc,b);el.append(row);
 }
}
function renderFIFO(){
 const list=$('fifo-trace');if(!list)return;list.replaceChildren();
 const events=resultFor(active)?.fifo_trace||[];
 const shown=events.slice(0,18);
 if(!shown.length){const li=document.createElement('li');li.textContent='Aucune opération FIFO observée pour cette situation.';list.appendChild(li);return;}
 for(const event of shown){const li=document.createElement('li');
  const position=Array.isArray(event.valeur)?`(${event.valeur.join(', ')})`:event.valeur;
  li.textContent=`${event.operation==='enfiler'?'Ajouter à la file':'Retirer de la file'} : ${position}`;
  list.appendChild(li);}
 if(events.length>shown.length){const li=document.createElement('li');li.textContent=`… ${events.length-shown.length} opérations supplémentaires.`;list.appendChild(li);}
}
function exportSummary(){const data={project:'ORCHESTRA NSI',level:'Terminale NSI',lesson:'T01',date:new Date().toISOString(),code:source.value,hypothesis:$('hypothesis').value,results:results?{passed:results.passed,total:results.total,tests:results.results.map(x=>({name:x.name,ok:x.ok,message:x.message,steps:x.steps,phases:x.phases}))}:null,limits:'Tests du contrat observables uniquement, pas de preuve formelle ni de sécurité contre du code hostile.'};const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='orchestra-terminale-t01-bilan.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1200);}
function theme(v){document.body.dataset.theme=v;document.querySelectorAll('[data-theme]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.theme===v)));try{localStorage.setItem('orchestra-terminale-theme',v)}catch(_){} }
restore();highlight();try{theme(localStorage.getItem('orchestra-terminale-theme')||'light')}catch(_){theme('light')}
source.addEventListener('input',()=>{remember();highlight()});if('ResizeObserver' in window)new ResizeObserver(syncScroll).observe(source);source.addEventListener('scroll',syncScroll);source.addEventListener('keydown',onKey);$('hypothesis').addEventListener('input',remember);
$('run').addEventListener('click',execute);$('reboot').addEventListener('click',startWorker);$('reset').addEventListener('click',()=>{if(confirm('Remplacer ton code par le départ ? Ton brouillon actuel sera perdu.')){source.value=STARTER;remember();highlight();}});$('export').addEventListener('click',exportSummary);
$('next').addEventListener('click',()=>{const max=resultFor(active)?.trace?.length||0;if(frame+1<max){frame++;drawBoard();renderEvents()}});$('previous').addEventListener('click',()=>{if(frame>0){frame--;drawBoard();renderEvents()}});
document.querySelectorAll('[data-case]').forEach(b=>b.addEventListener('click',()=>showCase(b.dataset.case)));document.querySelectorAll('[data-theme]').forEach(b=>b.addEventListener('click',()=>theme(b.dataset.theme)));
drawBoard();startWorker();
