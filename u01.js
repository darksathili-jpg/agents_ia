"use strict";
const themeSelect=document.querySelector('#formation-display');
const status=document.querySelector('#save-status');
const audience=document.body.dataset.audience;
const prefix=`academy:U01.1:${audience}:`;
let storageAvailable=true;
function read(key){try{return localStorage.getItem(key)}catch{storageAvailable=false;return null}}
function write(key,value){try{localStorage.setItem(key,value)}catch{storageAvailable=false}}
function theme(value){
 if(!['light','dark','projector'].includes(value))value='light';
 document.body.className='home formation '+value;themeSelect.value=value;
 for(const frame of document.querySelectorAll('iframe'))frame.contentWindow?.postMessage({type:'academy-theme',value},location.origin);
}
theme(read('agent-academy-display'));
themeSelect.addEventListener('change',()=>{theme(themeSelect.value);write('agent-academy-display',themeSelect.value)});
for(const frame of document.querySelectorAll('iframe'))frame.addEventListener('load',()=>theme(themeSelect.value));
window.addEventListener('message',event=>{
 if(event.origin!==location.origin||event.data?.type!=='academy-lab-height')return;
 const frame=[...document.querySelectorAll('iframe')].find(item=>item.contentWindow===event.source);
 if(frame&&Number.isFinite(event.data.height)&&event.data.height>=200&&event.data.height<20000)frame.style.height=event.data.height+'px';
});
function savedStatus(){if(status)status.textContent=storageAvailable?'Réponses enregistrées uniquement dans ce navigateur.':'Stockage indisponible : exportez vos réponses avant de fermer cette page.'}
document.querySelectorAll('[data-answer]').forEach(field=>{
 const saved=read(prefix+field.dataset.answer);if(saved!==null)field.value=saved;
 field.addEventListener('input',()=>{write(prefix+field.dataset.answer,field.value);savedStatus()});
});savedStatus();
document.querySelector('#export-notes')?.addEventListener('click',()=>{
 const answers=Object.fromEntries([...document.querySelectorAll('[data-answer]')].map(field=>[field.dataset.answer,field.value]));
 const data={unite:'U01.1',reference:'fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6',reponses:answers};
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
 const link=document.createElement('a');link.href=url;link.download='agent-academy-u01-1-reponses.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
// Navigation de lecture, sans score ni validation automatique des réponses.
if(audience==='eleve'){
 const stages=[...document.querySelectorAll('.unit-stage')];
 const links=[...document.querySelectorAll('.unit-toc a')];
 function activate(focus){
  const id=location.hash.slice(1);const active=stages.find(stage=>stage.id===id)||stages[0];
  for(const stage of stages)stage.hidden=stage!==active;
  for(const link of links){if(link.hash==='#'+active.id)link.setAttribute('aria-current','step');else link.removeAttribute('aria-current')}
  if(focus){active.focus({preventScroll:true});active.scrollIntoView({block:'start'})}
 }
 addEventListener('hashchange',()=>activate(true));activate(Boolean(location.hash));
}
