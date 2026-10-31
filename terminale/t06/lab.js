/* T06 — démonstration déterministe distincte du code Python élève.
 * Aucun mouvement avant une reprise explicitement déclenchée.
 * Sources et approbations simulées, pas une vérification cryptographique. */
(function(){
'use strict';
const TARGETS=['INCIDENT_DÉTECTÉ','BLOQUÉE','CORRECTIF_PROPOSÉ',
 'EN_REVÉRIFICATION','ATTENTE_HUMAINE','REPRISE_AUTORISÉE','REPRISE_EXÉCUTÉE'];
function baseline(){
 return {
  mission:{revision_cible:'r2',fichiers_autorises:['robot.py'],
   tests_requis:['test_un_pas','test_collision'],approbation_requise:false,
   decision_humaine:null,position_reprise:[0,1]},
  incident:{etat:'BLOQUÉE',revision:'r1',position_sure:[0,1],cause:'collision'},
  correctif:{revision:'r2',fichiers_modifies:['robot.py'],
   preuves:['p1','p2'],succes_annonce:true},
  registre:{p1:{test:'test_un_pas',revision:'r2',reussi:true},
   p2:{test:'test_collision',revision:'r2',reussi:true}}
 };
}
function makeScenario(index){
 const d=baseline();
 switch(index){
  case 1:d.registre.p2.reussi=false;break;
  case 2:d.registre.p2.revision='r1';break;
  case 3:d.correctif.fichiers_modifies.push('secrets.txt');break;
  case 4:d.incident.position_sure=[1,1];break;
  case 5:d.correctif.accord_humain=true;break;
  case 6:d.mission.approbation_requise=true;break;
  case 7:d.correctif.preuves.push('p999');break;
  case 8:d.mission.revision_cible='r1';break;
 }
 return d;
}
function exact(obj,keys){
 return obj!==null&&typeof obj==='object'&&!Array.isArray(obj)&&
  Object.keys(obj).length===keys.length&&keys.every(k=>Object.hasOwn(obj,k));
}
function validPosition(p){
 return Array.isArray(p)&&p.length===2&&p.every(Number.isInteger)&&
  p[0]>=0&&p[0]<6&&p[1]>=0&&p[1]<3;
}
function verifyRecovery(m,i,c,r){
 const reject=motif=>({etat:'BLOQUÉE',motif,validated:0});
 if(!exact(m,['revision_cible','fichiers_autorises','tests_requis','approbation_requise','decision_humaine','position_reprise'])
  ||!exact(i,['etat','revision','position_sure','cause'])
  ||!exact(c,['revision','fichiers_modifies','preuves','succes_annonce'])
  ||!r||typeof r!=='object'||Array.isArray(r))
  return reject('Contrat invalide ou champ de validation fabriqué par l’agent.');
 if(typeof m.revision_cible!=='string'||!m.revision_cible||
  typeof i.revision!=='string'||!i.revision||i.revision===m.revision_cible||
  typeof i.cause!=='string'||!i.cause||i.etat!=='BLOQUÉE'||
  !validPosition(m.position_reprise)||!validPosition(i.position_sure)||
  JSON.stringify(m.position_reprise)!==JSON.stringify(i.position_sure)||
  !Array.isArray(m.fichiers_autorises)||!Array.isArray(m.tests_requis)||
  !m.tests_requis.length||m.fichiers_autorises.some(x=>typeof x!=='string'||!x)||
  m.tests_requis.some(x=>typeof x!=='string'||!x)||
  typeof m.approbation_requise!=='boolean'||
  ![null,true,false].includes(m.decision_humaine)||
  typeof c.revision!=='string'||c.revision!==m.revision_cible||
  c.succes_annonce!==true)
  return reject('Incident, révision ou point de reprise incohérent.');
 if(!Array.isArray(c.fichiers_modifies)||!c.fichiers_modifies.length||
  c.fichiers_modifies.some(x=>typeof x!=='string'||!x)||
  new Set(c.fichiers_modifies).size!==c.fichiers_modifies.length||
  c.fichiers_modifies.some(x=>!m.fichiers_autorises.includes(x)))
  return reject('Fichier interdit ou déclaration des modifications invalide.');
 if(!Array.isArray(c.preuves)||!c.preuves.length||
  c.preuves.some(x=>typeof x!=='string'||!x)||
  new Set(c.preuves).size!==c.preuves.length)
  return reject('Preuve absente ou identifiant dupliqué.');
 const tested=new Set();
 for(const pid of c.preuves){
  const p=Object.hasOwn(r,pid)?r[pid]:undefined;
  if(!exact(p,['test','revision','reussi'])||
    typeof p.test!=='string'||!p.test||
    typeof p.revision!=='string'||typeof p.reussi!=='boolean'||
    p.reussi!==true||p.revision!==m.revision_cible||
    !m.tests_requis.includes(p.test)||tested.has(p.test))
   return reject('Preuve inconnue, échouée, ancienne ou en double.');
  tested.add(p.test);
 }
 if(tested.size!==m.tests_requis.length||m.tests_requis.some(t=>!tested.has(t)))
  return reject('Un test obligatoire n’a pas de preuve réussie.');
 if(m.approbation_requise){
  if(m.decision_humaine===null)
   return {etat:'ATTENTE_HUMAINE',motif:'Correctif vérifié ; approbation humaine indépendante nécessaire.',validated:tested.size};
  if(m.decision_humaine===false)return reject('Refus de reprise par une personne.');
 }
 return {etat:'REPRISE_AUTORISÉE',motif:'Nouvelle révision et point sûr conformes, tests indépendants réussis.',validated:tested.size};
}
const api={makeScenario,verifyRecovery,states:TARGETS};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
if(typeof document==='undefined')return;
const $=id=>document.getElementById(id);
let current=1,dossier=makeScenario(1),phase=0,state='INCIDENT_DÉTECTÉ',
 pos=[0,1],sprite=null,poseTimers=[];
let worker=null,workerVersion=0,ready=false,runId=0,runTimer=null,
 submitted=null,validated=null,starter=null;
function cancelPose(){for(const t of poseTimers)clearTimeout(t);poseTimers=[];}
function setPose(file){const src='../../assets/'+file;
 if(sprite.getAttribute('src')!==src)sprite.setAttribute('src',src);}
function draw(moving=false){
 const host=$('board');
 for(const cell of host.querySelectorAll('.cell')){
  const x=Number(cell.dataset.x),y=Number(cell.dataset.y);
  cell.className='cell';
  if(x===5&&y===1)cell.classList.add('goal');
  if(x===pos[0]&&y===pos[1])cell.classList.add('current');
  cell.textContent=x===5&&y===1?'A':x===0&&y===1?'D':'';
  cell.setAttribute('aria-label','Case ('+x+', '+y+')');
 }
 const cell=host.querySelector('.cell[data-x="'+pos[0]+'"][data-y="'+pos[1]+'"]');
 const reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 sprite.style.transition=moving&&!reduced?'left 430ms linear, top 430ms linear':'none';
 sprite.style.left=(cell.offsetLeft+cell.offsetWidth/2)+'px';
 sprite.style.top=(cell.offsetTop+cell.offsetHeight/2)+'px';
 sprite.style.width=Math.max(26,Math.min(91,cell.offsetWidth*1.06))+'px';
 cancelPose();
 if(moving&&!reduced){
  setPose('microduck-east-0.webp');
  poseTimers=[setTimeout(()=>setPose('microduck-east-1.webp'),140),
   setTimeout(()=>setPose('microduck-east-2.webp'),280),
   setTimeout(()=>{setPose('microduck-idle-east.webp');poseTimers=[];},430)];
 }else setPose('microduck-idle-east.webp');
 $('position-label').textContent='('+pos.join(', ')+')';
}
function log(message){const li=document.createElement('li');li.textContent=message;
 $('audit-log').appendChild(li);}
function updateStatus(note){
 $('status').textContent=state;
 $('status').dataset.state=state;
 $('status-note').textContent=note;
 document.querySelectorAll('[data-state-marker]').forEach(el=>{
  const label=el.dataset.stateMarker;
  el.classList.toggle('active',label===state);
  el.classList.toggle('blocked',label===state&&state==='BLOQUÉE');
  el.classList.toggle('pending',label===state&&state==='ATTENTE_HUMAINE');
 });
 $('next').disabled=phase>=4;
 $('approval').hidden=state!=='ATTENTE_HUMAINE';
 $('resume').disabled=state!=='REPRISE_AUTORISÉE';
}
function reset(){
 current=Number($('scenario').value);
 dossier=makeScenario(current);phase=0;state='INCIDENT_DÉTECTÉ';pos=[0,1];
 cancelPose();$('correctif-code').textContent=JSON.stringify(dossier.correctif,null,2);
 $('scope').textContent='Incident : '+dossier.incident.cause+
  '\nRévision de l’incident : '+dossier.incident.revision+
  '\nNouvelle révision exigée : '+dossier.mission.revision_cible+
  '\nFichiers autorisés : '+dossier.mission.fichiers_autorises.join(', ')+
  '\nTests à refaire : '+dossier.mission.tests_requis.join(', ')+
  '\nPoint sûr attendu : ('+dossier.mission.position_reprise.join(', ')+')'+
  '\nPoint du signalement : ('+dossier.incident.position_sure.join(', ')+')'+
  '\nAccord humain requis : '+(dossier.mission.approbation_requise?'oui':'non');
 $('registry-rows').replaceChildren();
 for(const [id,p] of Object.entries(dossier.registre)){
  const row=document.createElement('div');row.className='proof '+(p.reussi?'pass':'fail');
  const b=document.createElement('b');b.textContent=(p.reussi?'✓ ':'× ')+id+' · '+p.test;
  const small=document.createElement('small');
  small.textContent='Révision '+p.revision+' · '+(p.reussi?'Réussi':'ÉCHEC');
  row.append(b,small);$('registry-rows').appendChild(row);
 }
 $('audit-log').replaceChildren();log('INCIDENT_DÉTECTÉ : action arrêtée immédiatement.');
 $('effect').textContent='Incident détecté : aucun déplacement permis.';
 $('proofs-status').textContent='Aucun contrôle exécuté';
 updateStatus('Microduck reste au point sûr ; aucune reprise implicite.');
 draw();
}
function next(){
 if(phase===0){
  phase=1;state='BLOQUÉE';
  updateStatus('Quarantaine : aucune action autorisée avant un correctif vérifié.');
  log('INCIDENT_DÉTECTÉ → BLOQUÉE. Point sûr conservé.');
  $('effect').textContent='Mission BLOQUÉE : aucun déplacement.';
 }else if(phase===1){
  phase=2;state='CORRECTIF_PROPOSÉ';
  updateStatus('Rapport de correctif reçu, mais aucune preuve encore vérifiée.');
  log('BLOQUÉE → CORRECTIF_PROPOSÉ. Déclaration de l’agent non fiable.');
 }else if(phase===2){
  phase=3;state='EN_REVÉRIFICATION';
  updateStatus('Contrôle du point sûr, du périmètre et des nouveaux résultats de tests.');
  $('proofs-status').textContent='Révérification en cours…';
  log('CORRECTIF_PROPOSÉ → EN_REVÉRIFICATION.');
 }else if(phase===3){
  phase=4;
  const verdict=verifyRecovery(dossier.mission,dossier.incident,dossier.correctif,dossier.registre);
  state=verdict.etat;
  $('proofs-status').textContent=state==='BLOQUÉE'?
   'Preuves ou état de reprise non conformes':
   verdict.validated+' / '+dossier.mission.tests_requis.length+
     ' tests réussis sur la nouvelle révision';
  updateStatus(verdict.motif);
  log('EN_REVÉRIFICATION → '+state+' : '+verdict.motif);
  if(state==='BLOQUÉE')$('effect').textContent='Reprise BLOQUÉE : Microduck ne bouge pas.';
  else if(state==='ATTENTE_HUMAINE')$('effect').textContent='Attente d’accord : Microduck ne bouge pas.';
  else $('effect').textContent='Reprise autorisée : déplacement NON exécuté. Clique sur « Reprendre Microduck ».';
 }
}
function human(allow){
 if(state!=='ATTENTE_HUMAINE')return;
 dossier.mission.decision_humaine=allow;
 const verdict=verifyRecovery(dossier.mission,dossier.incident,dossier.correctif,dossier.registre);
 state=verdict.etat;
 updateStatus(allow?'Accord humain simulé : '+verdict.motif:'Refus humain : aucune reprise possible.');
 log(allow?'Décision humaine : accord unique simulé, sans mouvement automatique.':
  'Décision humaine : refus. Reprise BLOQUÉE.');
 $('effect').textContent=allow&&state==='REPRISE_AUTORISÉE'?
  'Accord enregistré. L’action reste à déclencher explicitement.':
  'Mission BLOQUÉE par décision humaine : aucun déplacement.';
}
function resume(){
 if(state!=='REPRISE_AUTORISÉE'||pos[0]!==0||pos[1]!==1)return;
 pos=[1,1];state='REPRISE_EXÉCUTÉE';
 updateStatus('Un déplacement autorisé de (0, 1) vers (1, 1) a été exécuté.');
 $('effect').textContent='REPRISE_EXÉCUTÉE : exactement un déplacement réel d’une case.';
 log('Action de reprise explicite : Microduck avance d’une seule case.');
 draw(true);
}
function setTheme(theme){
 if(!['light','dark','projection'].includes(theme))return;
 document.body.dataset.theme=theme;
 document.querySelectorAll('.themes button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.theme===theme)));
 try{localStorage.setItem('orchestra-t06-theme',theme);}catch(_){}
}
function remember(){
 try{localStorage.setItem('orchestra-t06-draft',
  JSON.stringify({code:$('python-code').value,justification:$('justification').value}));}catch(_){}
}
function invalidate(){
 remember();
 if(validated!==null||submitted!==null){
  validated=null;$('score').textContent='— / 19';
  $('result-summary').textContent='Code modifié : anciens résultats invalidés. Relance les tests.';
  $('result-cases').replaceChildren();$('student-proof').hidden=true;
 }
}
async function loadStarter(){
 try{
  const response=await fetch('eleve.py',{cache:'no-store'});
  if(!response.ok)throw Error('eleve.py HTTP '+response.status);
  starter=await response.text();
  let saved=null;try{saved=JSON.parse(localStorage.getItem('orchestra-t06-draft')||'null');}catch(_){}
  $('python-code').value=saved&&typeof saved.code==='string'?saved.code:starter;
  if(saved&&typeof saved.justification==='string')$('justification').value=saved.justification;
  const theme=localStorage.getItem('orchestra-t06-theme');if(theme)setTheme(theme);
 }catch(e){$('python-status').textContent='Squelette indisponible : '+e.message;}
}
function closeWorker(){
 if(worker){worker.terminate();worker=null;}
 clearTimeout(runTimer);runTimer=null;ready=false;$('run-python').disabled=true;
}
function bootWorker(){
 closeWorker();const version=++workerVersion;
 if(typeof Worker==='undefined'){$('python-status').textContent='Web Worker indisponible.';return;}
 worker=new Worker('python-worker.js');
 worker.onmessage=({data})=>{
  if(version!==workerVersion)return;
  if(data.type==='ready'){
   ready=true;$('run-python').disabled=false;
   $('python-status').textContent=data.source==='local'?'Python prêt · distribution locale':'Python prêt · secours réseau';
  }else if(data.type==='error'){
   if(data.stage==='run'&&data.id!==runId)return;
   submitted=null;validated=null;
   clearTimeout(runTimer);runTimer=null;$('run-python').disabled=!ready;
   $('python-status').textContent='Erreur Python : '+data.message;
   $('result-summary').textContent='Exécution interrompue : aucun verdict attribué.';
   if(data.stage==='load')closeWorker();
  }else if(data.type==='result'){
   if(data.id!==runId)return;
   clearTimeout(runTimer);runTimer=null;$('run-python').disabled=false;
   if(submitted===null||$('python-code').value!==submitted){
    submitted=null;validated=null;
    $('result-summary').textContent='Code modifié pendant le contrôle : verdict ignoré.';
    return;
   }
   validated=submitted;submitted=null;
   showResults(data.data);
   $('python-status').textContent='Exécution Python terminée · résultats réels';
  }
 };
 worker.onerror=()=>{$('python-status').textContent='Erreur du moteur Python';closeWorker();};
 $('python-status').textContent='Préparation de Pyodide…';
}
function showResults(data){
 const rows=data.results||[];
 $('score').textContent=(data.passed??0)+' / '+(data.total??19);
 $('result-summary').textContent=data.error||(
  data.success?'19 contrôles réussis. Complète ensuite la justification écrite.':
  'Certains contrôles ont échoué : consulte les écarts avant une nouvelle tentative.');
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 rows.forEach(item=>{
  const div=document.createElement('div');div.className='test-row'+(item.ok?'':' failed');
  const labels=document.createElement('div');
  const title=document.createElement('strong');title.textContent=(item.ok?'✓ ':'× ')+item.name;
  const small=document.createElement('small');small.textContent=item.message;
  labels.append(title,small);div.appendChild(labels);
  if(item.ok&&item.trace){
   const b=document.createElement('button');b.type='button';b.textContent='Preuve Python';
   b.addEventListener('click',()=>{
    $('student-proof').hidden=false;
    $('student-proof-data').textContent=JSON.stringify(item.trace,null,2);
   });div.appendChild(b);
  }
  $('result-cases').appendChild(div);
 });
}
function runPython(){
 if(!ready||!worker)return;
 submitted=$('python-code').value;validated=null;
 const id=++runId;$('run-python').disabled=true;
 $('score').textContent='— / 19';
 $('result-summary').textContent='Tests en cours : aucun score anticipé.';
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 worker.postMessage({type:'run',id,source:submitted});
 clearTimeout(runTimer);
 runTimer=setTimeout(()=>{
  if(submitted===null)return;
  submitted=null;validated=null;closeWorker();
  $('python-status').textContent='Temps limite dépassé : moteur Python relancé.';
  $('result-summary').textContent='Programme non terminé : aucune réussite attribuée.';
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
 $('next').addEventListener('click',next);
 $('approve').addEventListener('click',()=>human(true));
 $('deny').addEventListener('click',()=>human(false));
 $('resume').addEventListener('click',resume);
 document.querySelectorAll('.themes button').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.theme)));
 $('python-code').addEventListener('input',invalidate);
 $('justification').addEventListener('input',remember);
 $('run-python').addEventListener('click',runPython);
 $('restore').addEventListener('click',()=>{if(starter!==null){$('python-code').value=starter;invalidate();}});
 $('python-code').addEventListener('keydown',event=>{
  if(!window.OrchestraIndent)return;
  const type=event.key==='Tab'?(event.shiftKey?'unindent':'indent'):
   event.key==='Enter'?'enter':event.key==='Backspace'?'backspace':null;
  if(type&&window.OrchestraIndent.applyToTextarea($('python-code'),type))event.preventDefault();
 });
 loadStarter();bootWorker();
}
init();
})();
