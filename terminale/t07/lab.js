/* T07 — audit de journal et rejeu distinct de la vérification Python.
 * L'agent n'est pas source de confiance. Registre pédagogique indépendant simulé.
 */
(function(){
'use strict';
const STATES=['JOURNAL_REÇU','AUDIT_EN_COURS','ANOMALIE','ATTENTE_HUMAINE','CONFORME','REJEU_TERMINÉ'];
function baseline(){
 return {
  mission:{revision:'r107',depart:[0,1],objectif:[2,1],
    outils_autorises:['observer','avancer'],accord_requis:false,decision_humaine:null},
  journal:[
   {sequence:0,type:'DEBUT',revision:'r107',position:[0,1],preuve:null},
   {sequence:1,type:'OBSERVATION',revision:'r107',position:[0,1],preuve:null},
   {sequence:2,type:'DEPLACEMENT',revision:'r107',position:[1,1],preuve:'p1'},
   {sequence:3,type:'OBSERVATION',revision:'r107',position:[1,1],preuve:null},
   {sequence:4,type:'DEPLACEMENT',revision:'r107',position:[2,1],preuve:'p2'},
   {sequence:5,type:'FIN',revision:'r107',position:[2,1],preuve:null}
  ],
  registre:{
   p1:{revision:'r107',outil:'avancer',origine:[0,1],destination:[1,1],reussi:true},
   p2:{revision:'r107',outil:'avancer',origine:[1,1],destination:[2,1],reussi:true}
  }
 };
}
function scenario(index){
 const a=baseline();
 switch(index){
  case 1:a.journal[2].preuve='preuve_inventee';break;
  case 2:a.registre.p1.reussi=false;break;
  case 3:a.registre.p2.revision='r106';break;
  case 4:a.journal.splice(1,1);break;
  case 5:a.journal[2].position=[5,1];break;
  case 6:a.mission.accord_requis=true;break;
  case 7:a.journal.push({sequence:6,type:'OBSERVATION',revision:'r107',position:[2,1],preuve:null});break;
  case 8:a.journal[3].sequence=7;break;
 }
 return a;
}
const exact=(obj,keys)=>obj!==null&&typeof obj==='object'&&!Array.isArray(obj)&&
  Object.keys(obj).length===keys.length&&keys.every(k=>Object.hasOwn(obj,k));
const same=(a,b)=>Array.isArray(a)&&Array.isArray(b)&&a.length===2&&b.length===2&&
 a[0]===b[0]&&a[1]===b[1];
const valid=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isInteger)&&
 p[0]>=0&&p[0]<6&&p[1]>=0&&p[1]<3;
const distance=(a,b)=>Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1]);
function audit(mission,journal,registre){
 const fail=motif=>({etat:'ANOMALIE',motif,moves:0});
 if(!exact(mission,['revision','depart','objectif','outils_autorises','accord_requis','decision_humaine'])||
    !Array.isArray(journal)||journal.length<4||!registre||typeof registre!=='object'||Array.isArray(registre))
  return fail('Contrat incomplet : les structures ne correspondent pas à la mission.');
 const rev=mission.revision;
 if(typeof rev!=='string'||!rev||!valid(mission.depart)||!valid(mission.objectif)||
   !Array.isArray(mission.outils_autorises)||
   !mission.outils_autorises.includes('observer')||!mission.outils_autorises.includes('avancer')||
   typeof mission.accord_requis!=='boolean'||![null,true,false].includes(mission.decision_humaine))
  return fail('Mission ou permissions invalides : aucun rejeu possible.');
 let current=mission.depart.slice(),previous=null,moves=0;
 const used=new Set();
 for(let index=0;index<journal.length;index++){
  const item=journal[index];
  if(!exact(item,['sequence','type','revision','position','preuve'])||
    !Number.isInteger(item.sequence)||item.sequence!==index||
    typeof item.type!=='string'||typeof item.revision!=='string'||item.revision!==rev||
    !valid(item.position))
   return fail('Événement mal formé, numéro manquant ou révision incohérente.');
  const kind=item.type,point=item.position,proofId=item.preuve;
  if(index===0){
   if(kind!=='DEBUT'||!same(point,current)||proofId!==null)
    return fail('Départ non attesté ou première ligne incohérente.');
  }else if(index===journal.length-1){
   if(kind!=='FIN'||!same(point,current)||!same(point,mission.objectif)||proofId!==null||moves===0)
    return fail('Fin du journal incohérente avec le parcours reconstitué.');
  }else if(kind==='OBSERVATION'){
   if(!same(point,current)||proofId!==null||!['DEBUT','DEPLACEMENT'].includes(previous))
    return fail('Observation manquante, décalée ou sans point de mesure valide.');
  }else if(kind==='DEPLACEMENT'){
   if(previous!=='OBSERVATION'||distance(current,point)!==1||
     typeof proofId!=='string'||!proofId||used.has(proofId))
    return fail('Déplacement non préparé, non adjacent ou preuve déjà utilisée.');
   const proof=Object.hasOwn(registre,proofId)?registre[proofId]:null;
   if(!exact(proof,['revision','outil','origine','destination','reussi'])||
     typeof proof.revision!=='string'||proof.revision!==rev||
     proof.outil!=='avancer'||proof.reussi!==true||
     !valid(proof.origine)||!valid(proof.destination)||
     !same(proof.origine,current)||!same(proof.destination,point))
    return fail('Preuve indépendante absente, échouée, ancienne ou incompatible avec la position.');
   used.add(proofId);current=point.slice();moves++;
  }else return fail('Type d’événement non prévu ou fin prématurée.');
  previous=kind;
 }
 if(mission.accord_requis){
  if(mission.decision_humaine===null)
   return {etat:'ATTENTE_HUMAINE',motif:'Trace conforme ; approbation humaine encore indispensable.',moves};
  if(mission.decision_humaine===false)return fail('Approbation humaine refusée.');
 }
 return {etat:'CONFORME',motif:'Ordre, positions et preuves de la révision courante vérifiés.',moves};
}
const api={baseline,scenario,audit,STATES};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
if(typeof document==='undefined')return;
const $=id=>document.getElementById(id);
let index=1,data=scenario(1),state='JOURNAL_REÇU',stage=0,step=0,
    pos=[0,1],sprite=null,poseTimers=[];
let worker=null,generation=0,ready=false,runId=0,runTimer=null,
    submitted=null,validated=null,starter=null;
const reduced=()=>window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function cancelPose(){for(const timer of poseTimers)clearTimeout(timer);poseTimers=[];}
function setPose(name){const url='../../assets/'+name;if(sprite.getAttribute('src')!==url)sprite.setAttribute('src',url);}
function draw(moving=false){
 for(const cell of $('board').querySelectorAll('.cell')){
  const x=Number(cell.dataset.x),y=Number(cell.dataset.y);
  cell.className='cell';
  if(same([x,y],data.mission.objectif))cell.classList.add('goal');
  if(same([x,y],pos))cell.classList.add('current');
  cell.textContent=same([x,y],data.mission.objectif)?'A':same([x,y],data.mission.depart)?'D':'';
  cell.setAttribute('aria-label','Case ('+x+', '+y+')');
 }
 const cell=$('board').querySelector('.cell[data-x="'+pos[0]+'"][data-y="'+pos[1]+'"]');
 sprite.style.transition=moving&&!reduced()?'left 430ms linear, top 430ms linear':'none';
 sprite.style.left=(cell.offsetLeft+cell.offsetWidth/2)+'px';
 sprite.style.top=(cell.offsetTop+cell.offsetHeight/2)+'px';
 sprite.style.width=Math.max(26,Math.min(90,cell.offsetWidth*1.06))+'px';
 cancelPose();
 if(moving&&!reduced()){
  setPose('microduck-east-0.webp');
  poseTimers=[setTimeout(()=>setPose('microduck-east-1.webp'),140),
    setTimeout(()=>setPose('microduck-east-2.webp'),280),
    setTimeout(()=>{setPose('microduck-idle-east.webp');poseTimers=[];},430)];
 }else setPose('microduck-idle-east.webp');
 $('position-label').textContent='('+pos.join(', ')+')';
}
function auditLog(message){
 const li=document.createElement('li');li.textContent=message;$('audit-log').appendChild(li);
}
function update(){
 $('status').textContent=state;$('status').dataset.state=state;
 $('approval').hidden=state!=='ATTENTE_HUMAINE';
 $('audit').disabled=state!=='JOURNAL_REÇU'&&state!=='AUDIT_EN_COURS';
 $('replay').disabled=state!=='CONFORME';
 $('replay-progress').textContent=step+' / '+data.journal.length+' événements';
 document.querySelectorAll('[data-state-marker]').forEach(node=>{
  const s=node.dataset.stateMarker;
  node.classList.toggle('active',s===state);
  node.classList.toggle('blocked',s===state&&s==='ANOMALIE');
  node.classList.toggle('pending',s===state&&s==='ATTENTE_HUMAINE');
 });
 $('event-list').querySelectorAll('li').forEach((li,k)=>li.classList.toggle('replayed',k<step));
}
function reset(){
 index=Number($('scenario').value);data=scenario(index);
 state='JOURNAL_REÇU';stage=0;step=0;pos=data.mission.depart.slice();
 cancelPose();
 $('scope').textContent='Révision attendue : '+data.mission.revision+
  '\nDépart : ('+data.mission.depart.join(', ')+')'+
  '\nObjectif : ('+data.mission.objectif.join(', ')+')'+
  '\nOutils autorisés : '+data.mission.outils_autorises.join(', ')+
  '\nApprobation requise : '+(data.mission.accord_requis?'oui':'non');
 $('event-list').replaceChildren();
 data.journal.forEach(item=>{
  const li=document.createElement('li');
  const seq=document.createElement('b');seq.textContent=String(item.sequence).padStart(2,'0')+' · '+item.type;
  const detail=document.createElement('small');
  detail.textContent='('+item.position.join(', ')+') · '+(item.preuve||'sans preuve');
  li.append(seq,detail);$('event-list').appendChild(li);
 });
 $('registry-rows').replaceChildren();
 for(const [pid,p] of Object.entries(data.registre)){
  const row=document.createElement('div');row.className='proof '+(p.reussi?'pass':'fail');
  const label=document.createElement('b');
  label.textContent=(p.reussi?'✓ ':'× ')+pid+' · '+p.outil;
  const detail=document.createElement('small');
  detail.textContent=p.origine.join(',')+' → '+p.destination.join(',')+' · '+p.revision+
    ' · '+(p.reussi?'réussi':'ÉCHEC');
  row.append(label,detail);$('registry-rows').appendChild(row);
 }
 $('effect').textContent='Journal reçu : aucun déplacement avant audit.';
 $('proofs-status').textContent='Non vérifié';
 $('status-note').textContent="Le journal n'a pas encore été contrôlé.";
 $('audit-log').replaceChildren();auditLog('JOURNAL_REÇU : déclaration non fiable.');
 update();draw();
}
function doAudit(){
 if(state==='JOURNAL_REÇU'){
  stage=1;state='AUDIT_EN_COURS';
  $('status-note').textContent='Réconciliation avec les preuves indépendantes simulées.';
  $('proofs-status').textContent='Contrôle de la chronologie en cours…';
  auditLog('JOURNAL_REÇU → AUDIT_EN_COURS.');
  update();return;
 }
 if(state!=='AUDIT_EN_COURS')return;
 stage=2;const result=audit(data.mission,data.journal,data.registre);
 state=result.etat;
 $('proofs-status').textContent=result.etat==='ANOMALIE'?
   'Preuve ou chronologie insuffisante':result.moves+' déplacements corroborés';
 $('status-note').textContent=result.motif;
 $('effect').textContent=result.etat==='CONFORME'?
   'Journal conforme : aucun mouvement. Clique sur « Rejouer l’événement suivant ».':
   result.etat==='ATTENTE_HUMAINE'?
   'Attente humaine : aucun rejeu autorisé.':'ANOMALIE : rejeu interdit, Microduck immobile.';
 auditLog('AUDIT_EN_COURS → '+state+' : '+result.motif);
 update();
}
function human(allow){
 if(state!=='ATTENTE_HUMAINE')return;
 data.mission.decision_humaine=allow;
 const result=audit(data.mission,data.journal,data.registre);
 state=result.etat;
 $('status-note').textContent=allow?'Décision humaine simulée : '+result.motif:'Refus humain : aucun rejeu.';
 $('effect').textContent=state==='CONFORME'?
  'Audit validé après accord. Le rejeu reste à déclencher manuellement.':
  'Refus humain : Microduck reste immobile.';
 auditLog(allow?'Approbation humaine indépendante simulée : rejeu désormais possible.':
   'Refus humain : anomalie ; aucun rejeu.');
 update();
}
function replay(){
 if(state!=='CONFORME'||step>=data.journal.length)return;
 const item=data.journal[step];
 const previous=pos.slice();
 // Seuls les déplacements corroborés par l'audit changent le monde.
 if(item.type==='DEPLACEMENT')pos=item.position.slice();
 step++;
 if(item.type==='DEPLACEMENT'){
  $('effect').textContent='Événement '+item.sequence+' : déplacement réel unique de '+
   '('+previous.join(', ')+') vers ('+pos.join(', ')+').';
 }else $('effect').textContent='Événement '+item.sequence+' · '+item.type+
   ' : aucun déplacement.';
 auditLog('Rejeu '+item.sequence+' · '+item.type+' (journal contrôlé).');
 draw(item.type==='DEPLACEMENT');
 if(step===data.journal.length){
  state='REJEU_TERMINÉ';
  $('status-note').textContent='Rejeu terminé ; aucun autre déplacement autorisé.';
  auditLog('REJEU_TERMINÉ : arrivée au point demandé.');
 }
 update();
}
function theme(name){
 if(!['light','dark','projection'].includes(name))return;
 document.body.dataset.theme=name;
 document.querySelectorAll('.themes button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.theme===name)));
 try{localStorage.setItem('orchestra-t07-theme',name);}catch(_){}
}
function save(){
 try{localStorage.setItem('orchestra-t07-draft',
  JSON.stringify({code:$('python-code').value,justification:$('justification').value}));}catch(_){}
}
function invalidate(){
 save();if(validated!==null||submitted!==null){
  validated=null;$('score').textContent='— / 19';
  $('result-summary').textContent='Code modifié : résultats précédents invalidés.';
  $('result-cases').replaceChildren();$('student-proof').hidden=true;
 }
}
async function loadStudent(){
 try{
  const r=await fetch('eleve.py',{cache:'no-store'});
  if(!r.ok)throw Error('eleve.py HTTP '+r.status);
  starter=await r.text();
  let old=null;try{old=JSON.parse(localStorage.getItem('orchestra-t07-draft')||'null');}catch(_){}
  $('python-code').value=old&&typeof old.code==='string'?old.code:starter;
  if(old&&typeof old.justification==='string')$('justification').value=old.justification;
  const storedTheme=localStorage.getItem('orchestra-t07-theme');
  if(storedTheme)theme(storedTheme);
 }catch(e){$('python-status').textContent='Squelette introuvable : '+e.message;}
}
function closeWorker(){
 if(worker){worker.terminate();worker=null;}
 clearTimeout(runTimer);runTimer=null;ready=false;$('run-python').disabled=true;
}
function bootWorker(){
 closeWorker();const version=++generation;
 if(typeof Worker==='undefined'){$('python-status').textContent='Worker indisponible.';return;}
 worker=new Worker('python-worker.js');
 worker.onmessage=({data})=>{
  if(version!==generation)return;
  if(data.type==='ready'){
   ready=true;$('run-python').disabled=false;
   $('python-status').textContent=data.source==='local'?'Python prêt · distribution locale':'Python prêt · secours réseau';
  }else if(data.type==='error'){
   if(data.stage==='run'&&data.id!==runId)return;
   clearTimeout(runTimer);runTimer=null;submitted=null;validated=null;
   $('run-python').disabled=!ready;
   $('python-status').textContent='Erreur Python : '+data.message;
   $('result-summary').textContent='Exécution interrompue, aucun verdict attribué.';
   if(data.stage==='load')closeWorker();
  }else if(data.type==='result'){
   if(data.id!==runId)return;
   clearTimeout(runTimer);runTimer=null;$('run-python').disabled=false;
   if(submitted===null||$('python-code').value!==submitted){
    submitted=null;validated=null;
    $('result-summary').textContent='Code modifié pendant les tests : verdict ignoré.';
    return;
   }
   validated=submitted;submitted=null;showResults(data.data);
   $('python-status').textContent='Exécution Python terminée · verdicts réels';
  }
 };
 worker.onerror=()=>{$('python-status').textContent='Erreur moteur Python';closeWorker();};
 $('python-status').textContent='Préparation de Pyodide…';
}
function showResults(data){
 $('score').textContent=(data.passed??0)+' / '+(data.total??19);
 $('result-summary').textContent=data.error||(
  data.success?'19 vérifications réussies. Rédige une justification écrite.':
  'Des anomalies sont mal classées : vérifie tes conditions et les preuves.');
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 for(const item of data.results||[]){
  const row=document.createElement('div');row.className='test-row'+(item.ok?'':' failed');
  const labels=document.createElement('div'),title=document.createElement('strong'),small=document.createElement('small');
  title.textContent=(item.ok?'✓ ':'× ')+item.name;small.textContent=item.message;
  labels.append(title,small);row.appendChild(labels);
  if(item.ok&&item.trace){
   const button=document.createElement('button');button.type='button';button.textContent='Preuve Python';
   button.addEventListener('click',()=>{
    $('student-proof').hidden=false;
    $('student-proof-data').textContent=JSON.stringify(item.trace,null,2);
   });row.appendChild(button);
  }
  $('result-cases').appendChild(row);
 }
}
function runTests(){
 if(!ready||!worker)return;
 submitted=$('python-code').value;validated=null;
 const id=++runId;$('run-python').disabled=true;
 $('score').textContent='— / 19';
 $('result-summary').textContent='Exécution Python en cours ; aucun résultat anticipé.';
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 worker.postMessage({type:'run',id,source:submitted});
 clearTimeout(runTimer);
 runTimer=setTimeout(()=>{
  if(submitted===null)return;
  submitted=null;validated=null;closeWorker();
  $('python-status').textContent='Délai dépassé : moteur redémarré.';
  $('result-summary').textContent='Le programme n’a pas terminé ; aucun point attribué.';
  bootWorker();
 },12000);
}
function init(){
 for(let y=0;y<3;y++)for(let x=0;x<6;x++){
  const cell=document.createElement('div');cell.className='cell';
  cell.dataset.x=x;cell.dataset.y=y;$('board').appendChild(cell);
 }
 sprite=document.createElement('img');sprite.className='board-microduck';
 sprite.src='../../assets/microduck-idle-east.webp';sprite.alt='';sprite.draggable=false;
 sprite.setAttribute('aria-hidden','true');$('board').appendChild(sprite);
 reset();
 for(let i=0;i<3;i++){const img=new Image();img.src='../../assets/microduck-east-'+i+'.webp';}
 $('scenario').addEventListener('change',reset);
 $('reset').addEventListener('click',reset);
 $('audit').addEventListener('click',doAudit);
 $('approve').addEventListener('click',()=>human(true));
 $('deny').addEventListener('click',()=>human(false));
 $('replay').addEventListener('click',replay);
 document.querySelectorAll('.themes button').forEach(b=>b.addEventListener('click',()=>theme(b.dataset.theme)));
 $('python-code').addEventListener('input',invalidate);
 $('justification').addEventListener('input',save);
 $('run-python').addEventListener('click',runTests);
 $('restore').addEventListener('click',()=>{if(starter!==null){$('python-code').value=starter;invalidate();}});
 $('python-code').addEventListener('keydown',event=>{
  if(!window.OrchestraIndent)return;
  const type=event.key==='Tab'?(event.shiftKey?'unindent':'indent'):
    event.key==='Enter'?'enter':event.key==='Backspace'?'backspace':null;
  if(type&&window.OrchestraIndent.applyToTextarea($('python-code'),type))event.preventDefault();
 });
 loadStudent();bootWorker();
}
init();
})();
