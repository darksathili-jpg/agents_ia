/* T05 — une démonstration déterministe, distincte du code Python élève.
 * L'agent n'a accès qu'au rapport ; les preuves sont lues dans un registre
 * indépendant par l'orchestrateur. Aucune action réelle n'est réalisée. */
(function(){
'use strict';
const states=['SPÉCIFIÉE','EN VÉRIFICATION','BLOQUÉE','ATTENTE_HUMAINE','VALIDÉE'];
function baseline(){
 return {
  mission:{revision:'r105',fichiers_autorises:['robot.py'],
   tests_requis:['test_un_pas','test_collision'],approbation_requise:false,
   decision_humaine:null},
  rapport:{revision:'r105',fichiers_modifies:['robot.py'],
   preuves:['p1','p2'],succes_annonce:true},
  registre:{
   p1:{test:'test_un_pas',revision:'r105',reussi:true},
   p2:{test:'test_collision',revision:'r105',reussi:true}
  }
 };
}
const DESCRIPTIONS=[
 'Rapport honnête','Faux succès déclaré','Fichier hors périmètre',
 'Identifiant de preuve inventé','Preuve d’une autre révision',
 'Approbation humaine requise','Auto-approbation fabriquée'
];
function makeScenario(index){
 const data=baseline();
 switch(index){
  case 1:data.registre.p2.reussi=false;break;
  case 2:data.rapport.fichiers_modifies.push('secrets.txt');break;
  case 3:data.rapport.preuves.push('p999');break;
  case 4:data.registre.p1.revision='r104';break;
  case 5:data.mission.approbation_requise=true;break;
  case 6:data.rapport.accord_humain=true;break;
 }
 return data;
}
const exact=(v,keys)=>v&&typeof v==='object'&&!Array.isArray(v)&&
 Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
function verify(mission,rapport,registre){
 const blocked=motif=>({etat:'BLOQUÉE',motif,verified:0});
 if(!exact(mission,['revision','fichiers_autorises','tests_requis','approbation_requise','decision_humaine'])
  ||!exact(rapport,['revision','fichiers_modifies','preuves','succes_annonce'])
  ||!registre||typeof registre!=='object'||Array.isArray(registre))
  return blocked('Contrat de mission ou rapport invalide : refus par défaut.');
 if(typeof mission.revision!=='string'||!mission.revision||
  !Array.isArray(mission.fichiers_autorises)||!Array.isArray(mission.tests_requis)||
  !mission.tests_requis.length||typeof mission.approbation_requise!=='boolean'||
  ![null,true,false].includes(mission.decision_humaine)||
  typeof rapport.revision!=='string'||rapport.revision!==mission.revision||
  rapport.succes_annonce!==true)
  return blocked('Révision ou déclaration non conforme.');
 if(!Array.isArray(rapport.fichiers_modifies)||!rapport.fichiers_modifies.length||
  rapport.fichiers_modifies.some(x=>typeof x!=='string'||!x)||
  new Set(rapport.fichiers_modifies).size!==rapport.fichiers_modifies.length||
  rapport.fichiers_modifies.some(x=>!mission.fichiers_autorises.includes(x)))
  return blocked('Fichier modifié hors périmètre ou liste de fichiers invalide.');
 if(!Array.isArray(rapport.preuves)||!rapport.preuves.length||
  rapport.preuves.some(x=>typeof x!=='string'||!x)||
  new Set(rapport.preuves).size!==rapport.preuves.length)
  return blocked('Preuves absentes ou dupliquées.');
 const found=new Set();
 for(const id of rapport.preuves){
  const proof=registre[id];
  if(!exact(proof,['test','revision','reussi'])||
    typeof proof.test!=='string'||typeof proof.revision!=='string'||
    typeof proof.reussi!=='boolean'||proof.revision!==mission.revision||
    proof.reussi!==true||!mission.tests_requis.includes(proof.test)||found.has(proof.test))
   return blocked('Preuve non fiable : inconnue, échouée, révision différente ou test en double.');
  found.add(proof.test);
 }
 if(mission.tests_requis.some(t=>!found.has(t))||found.size!==mission.tests_requis.length)
  return blocked('Il manque la preuve d’un test obligatoire.');
 if(mission.approbation_requise){
  if(mission.decision_humaine===null)
   return {etat:'ATTENTE_HUMAINE',motif:'Tous les contrôles passent, mais l’approbation humaine manque.',verified:found.size};
  if(mission.decision_humaine===false)return blocked('Une personne a refusé cette action.');
 }
 return {etat:'VALIDÉE',motif:'Tous les tests sont réussis sur la bonne révision, dans le périmètre autorisé.',verified:found.size};
}
const api={makeScenario,verify,DESCRIPTIONS,states};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
if(typeof document==='undefined')return;
const $=id=>document.getElementById(id);
let selected=1,scene=makeScenario(1),state='SPÉCIFIÉE',pos=[0,1],sprite=null,timers=[];
let worker=null,generation=0,ready=false,runId=0,runTimer=null,submitted=null,validated=null,starter=null,results=null;
function stopPose(){for(const t of timers)clearTimeout(t);timers=[];}
function pose(name){const src='../../assets/'+name;if(sprite.getAttribute('src')!==src)sprite.setAttribute('src',src);}
function updateBoard(animate=false){
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
 sprite.style.transition=animate&&!reduced?'left 440ms linear, top 440ms linear':'none';
 sprite.style.left=(cell.offsetLeft+cell.offsetWidth/2)+'px';
 sprite.style.top=(cell.offsetTop+cell.offsetHeight/2)+'px';
 sprite.style.width=Math.max(26,Math.min(91,cell.offsetWidth*1.03))+'px';
 stopPose();
 if(animate&&!reduced){
  pose('microduck-east-0.webp');
  timers=[setTimeout(()=>pose('microduck-east-1.webp'),140),
   setTimeout(()=>pose('microduck-east-2.webp'),280),
   setTimeout(()=>{pose('microduck-idle-east.webp');timers=[];},440)];
 }else pose('microduck-idle-east.webp');
 $('position-label').textContent='('+pos.join(', ')+')';
}
function log(message){
 const item=document.createElement('li');item.textContent=message;
 $('audit-log').appendChild(item);
}
function updateStatus(note){
 $('status').textContent=state;
 $('status').dataset.state=state;
 $('status-note').textContent=note;
 document.querySelectorAll('[data-state-marker]').forEach(el=>{
  const label=el.getAttribute('data-state-marker');
  el.classList.toggle('active',label===state);
  el.classList.toggle('completed',
   (state!=='SPÉCIFIÉE'&&label==='SPÉCIFIÉE')||
   (state!=='SPÉCIFIÉE'&&state!=='EN VÉRIFICATION'&&label==='EN VÉRIFICATION'));
  el.classList.toggle('blocked',label===state&&state==='BLOQUÉE');
  el.classList.toggle('pending',label===state&&state==='ATTENTE_HUMAINE');
 });
 $('next').disabled=!['SPÉCIFIÉE','EN VÉRIFICATION'].includes(state);
 $('approval').hidden=state!=='ATTENTE_HUMAINE';
}
function reset(){
 selected=Number($('scenario').value);scene=makeScenario(selected);
 state='SPÉCIFIÉE';pos=[0,1];stopPose();
 $('report-code').textContent=JSON.stringify(scene.rapport,null,2);
 $('mission-scope').textContent=
  'Révision : '+scene.mission.revision+'\nFichiers autorisés : '+
  scene.mission.fichiers_autorises.join(', ')+
  '\nTests requis : '+scene.mission.tests_requis.join(', ')+
  '\nApprobation humaine : '+(scene.mission.approbation_requise?'oui':'non');
 $('registry-rows').replaceChildren();
 for(const [id,proof] of Object.entries(scene.registre)){
  const row=document.createElement('div');
  row.className='proof '+(proof.reussi?'pass':'fail');
  const strong=document.createElement('b');
  strong.textContent=(proof.reussi?'✓ ':'× ')+id+' · '+proof.test;
  const small=document.createElement('small');
  small.textContent='Révision '+proof.revision+' · '+(proof.reussi?'Réussi':'ÉCHEC');
  row.append(strong,small);$('registry-rows').appendChild(row);
 }
 $('audit-log').replaceChildren();
 log('Mission SPÉCIFIÉE : périmètre et tests obligatoires enregistrés.');
 $('effect').textContent='Mission spécifiée : aucun déplacement.';
 $('proofs-status').textContent='Aucune preuve vérifiée';
 updateStatus('Rapport non contrôlé. Aucune action autorisée.');
 updateBoard();
}
function execute(){
 if(state!=='VALIDÉE')return;
 if(pos[0]===0&&pos[1]===1){
  pos=[1,1];$('effect').textContent='Action autorisée après validation : un déplacement réel d’une case.';
  log('Monde : Microduck avance exactement d’une case vers l’est.');
  updateBoard(true);
 }
}
function next(){
 if(state==='SPÉCIFIÉE'){
  state='EN VÉRIFICATION';
  updateStatus('Comparaison du rapport avec le périmètre et les preuves indépendantes.');
  $('proofs-status').textContent='Vérification en cours…';
  log('Transition SPÉCIFIÉE → EN VÉRIFICATION.');
  return;
 }
 if(state!=='EN VÉRIFICATION')return;
 const answer=verify(scene.mission,scene.rapport,scene.registre);
 state=answer.etat;updateStatus(answer.motif);
 $('proofs-status').textContent=answer.etat==='BLOQUÉE'?
  'Preuves insuffisantes ou contradictoires':
  answer.verified+' / '+scene.mission.tests_requis.length+' tests vérifiés dans le registre';
 log('Transition EN VÉRIFICATION → '+state+' : '+answer.motif);
 if(state==='VALIDÉE')execute();
 else if(state==='BLOQUÉE')$('effect').textContent='Mission BLOQUÉE : Microduck reste immobile.';
 else $('effect').textContent='ATTENTE_HUMAINE : aucune action avant la décision explicite.';
}
function human(approved){
 if(state!=='ATTENTE_HUMAINE')return;
 scene.mission.decision_humaine=approved;
 if(approved){
  const result=verify(scene.mission,scene.rapport,scene.registre);
  state=result.etat;
  updateStatus('Accord humain simulé : '+result.motif);
  log('Une personne a autorisé une fois cette action (simulation).');
  if(state==='VALIDÉE')execute();
 }else{
  state='BLOQUÉE';
  updateStatus('Une personne a explicitement refusé la demande.');
  $('effect').textContent='Mission bloquée par refus humain : aucun déplacement.';
  log('Décision humaine : REFUS. Aucune action.');
 }
}
function setTheme(theme){
 if(!['light','dark','projection'].includes(theme))return;
 document.body.dataset.theme=theme;
 document.querySelectorAll('.themes button').forEach(x=>
  x.setAttribute('aria-pressed',String(x.dataset.theme===theme)));
 try{localStorage.setItem('orchestra-t05-theme',theme);}catch(_){}
}
function remember(){
 try{localStorage.setItem('orchestra-t05-draft',
  JSON.stringify({code:$('python-code').value,justification:$('justification').value}));}catch(_){}
}
function invalidate(){
 remember();
 if(validated!==null||submitted!==null){
  validated=null;results=null;
  $('score').textContent='— / 19';
  $('result-summary').textContent='Code modifié : anciens résultats invalidés. Relance les tests.';
  $('result-cases').replaceChildren();$('student-proof').hidden=true;
 }
}
async function loadStarter(){
 try{
  const response=await fetch('eleve.py',{cache:'no-store'});
  if(!response.ok)throw Error('eleve.py HTTP '+response.status);
  starter=await response.text();
  let saved=null;try{saved=JSON.parse(localStorage.getItem('orchestra-t05-draft')||'null');}catch(_){}
  $('python-code').value=saved&&typeof saved.code==='string'?saved.code:starter;
  if(saved&&typeof saved.justification==='string')$('justification').value=saved.justification;
  const theme=localStorage.getItem('orchestra-t05-theme');if(theme)setTheme(theme);
 }catch(error){$('python-status').textContent='Squelette indisponible : '+error.message;}
}
function closeWorker(){
 if(worker){worker.terminate();worker=null;}
 clearTimeout(runTimer);runTimer=null;ready=false;$('run-python').disabled=true;
}
function bootWorker(){
 closeWorker();const requestGeneration=++generation;
 if(typeof Worker==='undefined'){$('python-status').textContent='Web Worker indisponible.';return;}
 worker=new Worker('python-worker.js');
 worker.onmessage=({data})=>{
  if(requestGeneration!==generation)return;
  if(data.type==='ready'){
   ready=true;$('run-python').disabled=false;
   $('python-status').textContent=data.source==='local'?'Python prêt · distribution locale':'Python prêt · secours réseau';
  }else if(data.type==='error'){
   if(data.stage==='run'&&data.id!==runId)return;
   submitted=null;validated=null;results=null;
   clearTimeout(runTimer);runTimer=null;$('run-python').disabled=!ready;
   $('python-status').textContent='Erreur Python : '+data.message;
   $('result-summary').textContent='Exécution interrompue, aucun verdict attribué.';
   if(data.stage==='load')closeWorker();
  }else if(data.type==='result'){
   if(data.id!==runId)return;
   clearTimeout(runTimer);runTimer=null;$('run-python').disabled=false;
   if(submitted===null||$('python-code').value!==submitted){
    submitted=null;validated=null;
    $('result-summary').textContent='Code modifié pendant le contrôle : résultat ignoré.';
    return;
   }
   validated=submitted;submitted=null;
   showResults(data.data);
   $('python-status').textContent='Exécution Python terminée · résultats authentiques';
  }
 };
 worker.onerror=()=>{$('python-status').textContent='Erreur moteur Python';closeWorker();};
 $('python-status').textContent='Chargement de Pyodide…';
}
function showResults(data){
 results=data.results||[];
 $('score').textContent=(data.passed??0)+' / '+(data.total??19);
 $('result-summary').textContent=data.error||(
  data.success?'19 contrôles réussis. Termine par une justification écrite.':
  'Certaines missions sont mal classées : consulte les écarts et corrige ton code.');
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 results.forEach(result=>{
  const row=document.createElement('article');row.className='test-row'+(result.ok?'':' failed');
  const labels=document.createElement('div'),title=document.createElement('strong'),message=document.createElement('small');
  title.textContent=(result.ok?'✓ ':'× ')+result.name;message.textContent=result.message;
  labels.append(title,message);row.appendChild(labels);
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
 if(!ready||!worker)return;
 submitted=$('python-code').value;validated=null;results=null;
 const id=++runId;$('run-python').disabled=true;
 $('score').textContent='— / 19';
 $('result-summary').textContent='Tests Python en cours : aucun score anticipé.';
 $('result-cases').replaceChildren();$('student-proof').hidden=true;
 worker.postMessage({type:'run',id,source:submitted});
 clearTimeout(runTimer);
 runTimer=setTimeout(()=>{
  if(submitted===null)return;
  submitted=null;validated=null;closeWorker();
  $('python-status').textContent='Délai dépassé : moteur relancé.';
  $('result-summary').textContent='Le programme n’a pas terminé : aucun verdict attribué.';
  bootWorker();
 },12000);
}
function init(){
 for(let y=0;y<3;y++)for(let x=0;x<6;x++){
  const cell=document.createElement('div');cell.className='cell';cell.dataset.x=x;cell.dataset.y=y;
  $('board').appendChild(cell);
 }
 sprite=document.createElement('img');sprite.className='board-microduck';
 sprite.src='../../assets/microduck-idle-east.webp';sprite.alt='';
 sprite.draggable=false;sprite.setAttribute('aria-hidden','true');$('board').appendChild(sprite);
 reset();
 for(let i=0;i<3;i++){const frame=new Image();frame.src='../../assets/microduck-east-'+i+'.webp';}
 $('scenario').addEventListener('change',reset);
 $('reset').addEventListener('click',reset);
 $('next').addEventListener('click',next);
 $('approve').addEventListener('click',()=>human(true));
 $('deny').addEventListener('click',()=>human(false));
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
