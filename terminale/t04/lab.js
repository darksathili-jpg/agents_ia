/* ORCHESTRA T04 — aucun effet sans décision de l'orchestrateur.
 * La démonstration JavaScript est indépendante de l'évaluation Python. */
(function () {
'use strict';
const WIDTH=6, HEIGHT=3, DELTA={N:[0,-1],E:[1,0],S:[0,1],O:[-1,0]};
const CASES=[
 {name:'Observation',call:{outil:'observer',arguments:{}},rights:['observer'],walls:[]},
 {name:'Avancer',call:{outil:'avancer',arguments:{direction:'E'}},rights:['avancer'],walls:[]},
 {name:'Droit absent',call:{outil:'avancer',arguments:{direction:'N'}},rights:['observer'],walls:[]},
 {name:'Porte sensible',call:{outil:'ouvrir_porte',arguments:{position:[2,1]}},rights:['ouvrir_porte'],walls:[[2,1]]},
 {name:'Faux accord',call:{outil:'ouvrir_porte',arguments:{position:[2,1]},approuve:true},rights:['ouvrir_porte'],walls:[[2,1]]},
 {name:'Téléportation',call:{outil:'teleporter',arguments:{position:[5,1]}},rights:['teleporter'],walls:[]},
 {name:'Collision',call:{outil:'avancer',arguments:{direction:'E'}},rights:['avancer'],walls:[[1,1]]}
];
const key=p=>p.join(',');
const same=(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1];
const inside=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isInteger)&&p[0]>=0&&p[0]<WIDTH&&p[1]>=0&&p[1]<HEIGHT;
const exact=(object,keys)=>object&&typeof object==='object'&&!Array.isArray(object)&&Object.keys(object).length===keys.length&&keys.every(k=>Object.prototype.hasOwnProperty.call(object,k));
function verify(call,rights) {
  if(!exact(call,['outil','arguments'])||typeof call.outil!=='string'||!exact(call.arguments,Object.keys(call.arguments||{})))
    return {statut:'REFUSÉ',motif:'Appel mal formé : deux clés exactement, outil et arguments.',contract:false};
  const tool=call.outil,args=call.arguments;
  if(!['observer','avancer','ouvrir_porte'].includes(tool))
    return {statut:'REFUSÉ',motif:'Outil absent de la liste blanche.',contract:false};
  if(tool==='observer'&&!exact(args,[]))
    return {statut:'REFUSÉ',motif:'observer ne reçoit aucun argument.',contract:false};
  if(tool==='avancer'&&(!exact(args,['direction'])||typeof args.direction!=='string'||!DELTA[args.direction]))
    return {statut:'REFUSÉ',motif:'avancer attend une direction N, E, S ou O.',contract:false};
  if(tool==='ouvrir_porte'&&(!exact(args,['position'])||!inside(args.position)))
    return {statut:'REFUSÉ',motif:'ouvrir_porte attend une position entière dans la grille.',contract:false};
  if(!rights.includes(tool))return {statut:'REFUSÉ',motif:'Outil valide mais droit absent pour cette mission.',contract:true};
  if(tool==='ouvrir_porte')return {statut:'ATTENTE_HUMAINE',motif:'Opération sensible : approbation humaine indispensable.',contract:true};
  return {statut:'AUTORISÉ',motif:'Contrat valide et permission explicite accordée.',contract:true};
}
function applyWorld(pos,walls,call) {
  const tool=call.outil;
  if(tool==='observer')return {position:pos.slice(),walls:walls.map(p=>p.slice()),effect:'Observation réalisée, sans déplacement.'};
  if(tool==='avancer') {
    const d=DELTA[call.arguments.direction];
    const target=[pos[0]+d[0],pos[1]+d[1]];
    if(!inside(target)||walls.some(p=>same(p,target)))return {position:pos.slice(),walls:walls.map(p=>p.slice()),effect:'Action autorisée, mais déplacement bloqué par le monde.'};
    return {position:target,walls:walls.map(p=>p.slice()),effect:'Déplacement validé : une seule case.'};
  }
  if(tool==='ouvrir_porte') {
    const target=call.arguments.position,rest=walls.filter(w=>!same(w,target));
    return {position:pos.slice(),walls:rest,effect:rest.length!==walls.length?'Porte ouverte après décision humaine.':'Aucun mur à ouvrir à cette position.'};
  }
  return {position:pos.slice(),walls:walls.map(p=>p.slice()),effect:'Outil inconnu : aucun effet.'};
}
const api={verify,applyWorld,CASES};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
if(typeof document==='undefined')return;
const $=id=>document.getElementById(id);
let index=0,pos=[0,1],walls=[],sprite=null,done=false,pending=false,poseTimers=[],previousFace='east';
let worker=null,workerGeneration=0,workerReady=false,runNumber=0,runTimer=null,submitted=null,validated=null,starter=null,results=null;
function stopPose(){for(const t of poseTimers)clearTimeout(t);poseTimers=[];}
function pose(filename){const url='../../assets/'+filename;if(sprite.getAttribute('src')!==url)sprite.setAttribute('src',url);}
function face(direction){return {N:'north',E:'east',S:'south',O:'west'}[direction]||previousFace;}
function animateMove(direction) {
 stopPose();previousFace=face(direction);
 pose('microduck-'+previousFace+'-0.webp');
 poseTimers=[setTimeout(()=>pose('microduck-'+previousFace+'-1.webp'),140),
  setTimeout(()=>pose('microduck-'+previousFace+'-2.webp'),275),
  setTimeout(()=>{pose('microduck-idle-'+previousFace+'.webp');poseTimers=[];},430)];
}
function draw(moveDirection=null) {
 const board=$('board');
 for(const cell of board.querySelectorAll('.cell')) {
  const p=[Number(cell.dataset.x),Number(cell.dataset.y)];
  cell.className='cell';
  if(walls.some(w=>same(p,w)))cell.classList.add('wall');
  if(same(p,[5,1]))cell.classList.add('goal');
  if(same(p,pos))cell.classList.add('current');
  cell.textContent=same(p,[5,1])?'A':same(p,[0,1])?'D':'';
  cell.setAttribute('aria-label','Case ('+p.join(', ')+')'+(walls.some(w=>same(p,w))?' mur':''));
 }
 const cell=board.querySelector('.cell[data-x="'+pos[0]+'"][data-y="'+pos[1]+'"]');
 const reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 sprite.style.transition=moveDirection&&!reduced?'left 430ms linear, top 430ms linear':'none';
 sprite.style.left=(cell.offsetLeft+cell.offsetWidth/2)+'px';
 sprite.style.top=(cell.offsetTop+cell.offsetHeight/2)+'px';
 sprite.style.width=Math.max(27,Math.min(92,cell.offsetWidth*1.06))+'px';
 if(moveDirection&&!reduced)animateMove(moveDirection);
 else{stopPose();pose('microduck-idle-'+previousFace+'.webp');}
 $('position-label').textContent='('+pos.join(', ')+')';
}
function log(message) {
 const host=$('audit-log');
 if(host.children.length===1&&host.firstElementChild.textContent==='Aucun appel exécuté.')host.replaceChildren();
 const item=document.createElement('li');item.textContent=message;host.appendChild(item);
}
function setStatus(status,note) {
 $('status').textContent=status;
 $('status').dataset.state=status;
 $('status-note').textContent=note;
}
function reset() {
 stopPose();index=Number($('scenario').value);const caseData=CASES[index];
 pos=[0,1];walls=caseData.walls.map(p=>p.slice());done=false;pending=false;previousFace='east';
 $('request-code').textContent=JSON.stringify(caseData.call,null,2);
 $('rights').replaceChildren();
 for(const item of caseData.rights){const tag=document.createElement('span');tag.textContent=item;$('rights').appendChild(tag);}
 $('contract').textContent='En attente d’analyse';
 setStatus('NON VÉRIFIÉ',"L'agent n'a pas encore soumis sa demande.");
 $('effect').textContent='Aucun effet';
 $('approval').hidden=true;
 $('audit-log').replaceChildren();
 const notice=document.createElement('li');notice.textContent='Aucun appel exécuté.';$('audit-log').appendChild(notice);
 $('inspect').disabled=false;
 draw();
}
function apply(call) {
 const before=pos.slice();
 const state=applyWorld(pos,walls,call);
 pos=state.position;walls=state.walls;
 $('effect').textContent=state.effect;
 log(state.effect);
 draw(!same(before,pos)?call.arguments.direction:null);
}
function inspect() {
 if(done||pending)return;
 const item=CASES[index],verdict=verify(item.call,item.rights);
 $('contract').textContent=verdict.contract?'Contrat valide':'Contrat invalide ou outil inconnu';
 setStatus(verdict.statut,verdict.motif);
 log('Vérification : '+verdict.statut+' — '+verdict.motif);
 $('inspect').disabled=true;
 if(verdict.statut==='AUTORISÉ'){apply(item.call);done=true;}
 else if(verdict.statut==='ATTENTE_HUMAINE'){pending=true;$('approval').hidden=false;log('Aucun effet : attente d’une décision explicite.');}
 else {done=true;$('effect').textContent='Refus : état du monde inchangé.';log('Refus : aucune action exécutée.');}
}
function humanDecision(allowed) {
 if(!pending||done)return;
 pending=false;done=true;$('approval').hidden=true;
 if(allowed) {
  log('Accord humain de démonstration : valable une fois pour cet appel.');
  apply(CASES[index].call);
  setStatus('AUTORISÉ APRÈS ACCORD','Approbation ponctuelle fournie par une personne dans cette simulation.');
 } else {
  $('effect').textContent='Refus humain : état du monde inchangé.';
  setStatus('REFUSÉ PAR HUMAIN','L’accord demandé a été refusé.');
  log('Refus humain : aucune action exécutée.');
 }
}
function setTheme(mode) {
 if(!['light','dark','projection'].includes(mode))return;
 document.body.dataset.theme=mode;
 document.querySelectorAll('.themes button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.theme===mode)));
 try{localStorage.setItem('orchestra-t04-theme',mode);}catch(_){}
}
function remember() {
 try{localStorage.setItem('orchestra-t04-draft',JSON.stringify({code:$('python-code').value,justification:$('justification').value}));}catch(_){}
}
function invalidate() {
 remember();
 if(validated!==null||submitted!==null) {
  validated=null;results=null;
  $('score').textContent='— / 13';
  $('result-summary').textContent='Code modifié : anciens résultats invalidés. Relance les tests.';
  $('result-cases').replaceChildren();$('student-proof').hidden=true;
 }
}
async function loadStarter() {
 try {
  const response=await fetch('eleve.py',{cache:'no-store'});
  if(!response.ok)throw Error('eleve.py HTTP '+response.status);
  starter=await response.text();
  let saved=null;
  try{saved=JSON.parse(localStorage.getItem('orchestra-t04-draft')||'null');}catch(_){}
  $('python-code').value=saved&&typeof saved.code==='string'?saved.code:starter;
  if(saved&&typeof saved.justification==='string')$('justification').value=saved.justification;
  const theme=localStorage.getItem('orchestra-t04-theme');if(theme)setTheme(theme);
 }catch(error){$('python-status').textContent='Squelette introuvable : '+error.message;}
}
function closeWorker(){
 if(worker){worker.terminate();worker=null;}
 clearTimeout(runTimer);runTimer=null;workerReady=false;$('run-python').disabled=true;
}
function bootWorker(){
 closeWorker();
 const generation=++workerGeneration;
 if(typeof Worker==='undefined'){$('python-status').textContent='Web Worker indisponible.';return;}
 worker=new Worker('python-worker.js');
 worker.onmessage=({data})=>{
  if(generation!==workerGeneration)return;
  if(data.type==='ready'){
   workerReady=true;$('run-python').disabled=false;
   $('python-status').textContent=data.source==='local'?'Python prêt · distribution locale':'Python prêt · secours réseau';
  } else if(data.type==='error'){
   if(data.stage==='run'&&data.id!==runNumber)return;
   submitted=null;validated=null;results=null;
   clearTimeout(runTimer);runTimer=null;$('run-python').disabled=!workerReady;
   $('python-status').textContent='Erreur Python : '+data.message;
   $('result-summary').textContent='Exécution interrompue sans résultat exploitable.';
   if(data.stage==='load')closeWorker();
  } else if(data.type==='result'){
   if(data.id!==runNumber)return;
   clearTimeout(runTimer);runTimer=null;
   $('run-python').disabled=false;
   if(submitted===null||$('python-code').value!==submitted){
    submitted=null;validated=null;
    $('result-summary').textContent='Code modifié pendant le test : résultat ignoré.';
    return;
   }
   validated=submitted;submitted=null;
   showResults(data.data);
   $('python-status').textContent='Exécution Python terminée · verdicts réels';
  }
 };
 worker.onerror=()=>{$('python-status').textContent='Erreur du moteur Python';closeWorker();};
 $('python-status').textContent='Préparation de Pyodide…';
}
function showResults(data){
 const rows=data.results||[];results=rows;
 $('score').textContent=(data.passed??0)+' / '+(data.total??13);
 $('result-summary').textContent=data.error||(
  data.success?'Tous les contrats et permissions sont validés. Rédige maintenant ta justification.':
  'Certains appels sont mal classés : compare les motifs et corrige ton code.');
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 rows.forEach((result,i)=>{
  const row=document.createElement('article');row.className='test-row'+(result.ok?'':' failed');
  const description=document.createElement('div');
  const name=document.createElement('strong');name.textContent=(result.ok?'✓ ':'× ')+result.name;
  const message=document.createElement('small');message.textContent=result.message;
  description.append(name,message);row.appendChild(description);
  if(result.ok&&result.trace){
   const button=document.createElement('button');button.type='button';button.textContent='Preuve Python';
   button.addEventListener('click',()=>{
    $('student-proof').hidden=false;
    $('student-proof-data').textContent=JSON.stringify(result.trace,null,2);
   });row.appendChild(button);
  }
  $('result-cases').appendChild(row);
 });
}
function runPython(){
 if(!workerReady||!worker)return;
 submitted=$('python-code').value;validated=null;results=null;
 const id=++runNumber;$('run-python').disabled=true;
 $('score').textContent='— / 13';
 $('result-summary').textContent='Tests en cours : aucun score anticipé.';
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 worker.postMessage({type:'run',id,source:submitted});
 clearTimeout(runTimer);
 runTimer=setTimeout(()=>{
  if(submitted===null)return;
  submitted=null;validated=null;closeWorker();
  $('python-status').textContent='Délai dépassé : moteur Python relancé.';
  $('result-summary').textContent='Le programme n’a pas terminé : aucun résultat attribué.';
  bootWorker();
 },12000);
}
function init() {
 for(let y=0;y<HEIGHT;y++)for(let x=0;x<WIDTH;x++){
  const cell=document.createElement('div');cell.className='cell';cell.dataset.x=x;cell.dataset.y=y;
  $('board').appendChild(cell);
 }
 sprite=document.createElement('img');sprite.className='board-microduck';sprite.src='../../assets/microduck-idle-east.webp';
 sprite.alt='';sprite.draggable=false;sprite.setAttribute('aria-hidden','true');$('board').appendChild(sprite);
 reset();
 for(const direction of ['north','east','south','west'])for(let pose=0;pose<3;pose++){
  const preload=new Image();preload.src='../../assets/microduck-'+direction+'-'+pose+'.webp';
 }
 $('scenario').addEventListener('change',reset);
 $('reset').addEventListener('click',reset);
 $('inspect').addEventListener('click',inspect);
 $('approve').addEventListener('click',()=>humanDecision(true));
 $('deny').addEventListener('click',()=>humanDecision(false));
 document.querySelectorAll('.themes button').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.theme)));
 $('python-code').addEventListener('input',invalidate);
 $('justification').addEventListener('input',remember);
 $('run-python').addEventListener('click',runPython);
 $('restore').addEventListener('click',()=>{if(starter!==null){$('python-code').value=starter;invalidate();}});
 $('python-code').addEventListener('keydown',event=>{
  if(!window.OrchestraIndent)return;
  const type=event.key==='Tab'?(event.shiftKey?'unindent':'indent'):event.key==='Enter'?'enter':
   event.key==='Backspace'?'backspace':null;
  if(type&&window.OrchestraIndent.applyToTextarea($('python-code'),type))event.preventDefault();
 });
 loadStarter();bootWorker();
}
init();
})();
