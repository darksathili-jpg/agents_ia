"use strict";
const display = document.querySelector('#formation-display');
const state = document.querySelector('#save-status');
let storageOK = true;
function read(key) { try { return localStorage.getItem(key); } catch { storageOK=false; return null; } }
function write(key,value) { try { localStorage.setItem(key,value); } catch { storageOK=false; } }
function setTheme(value){
 document.body.className='home formation '+value;display.value=value;
 document.querySelectorAll('iframe').forEach(frame=>frame.contentWindow?.postMessage({type:'academy-theme',value},location.origin));
}
const saved=read('agent-academy-display');setTheme(['light','dark','projector'].includes(saved)?saved:'light');
display.addEventListener('change',()=>{setTheme(display.value);write('agent-academy-display',display.value)});
document.querySelectorAll('iframe').forEach(frame=>frame.addEventListener('load',()=>setTheme(display.value)));
window.addEventListener('message',event=>{
 if(event.origin!==location.origin||event.data?.type!=='academy-lab-height')return;
 const frame=[...document.querySelectorAll('iframe')].find(item=>item.contentWindow===event.source);
 if(frame&&Number.isFinite(event.data.height)&&event.data.height>=300&&event.data.height<20000)frame.style.height=event.data.height+'px';
});
document.querySelectorAll('[data-save]').forEach(input=>{
 const key='academy-s01:'+input.dataset.save;const savedValue=read(key);
 if(savedValue!==null)input.value=savedValue;
 input.addEventListener('input',()=>{write(key,input.value);if(state)state.textContent=storageOK?'Réponses enregistrées dans ce navigateur.':'Enregistrement indisponible : exportez vos réponses avant de fermer.'});
});
if(state&&!storageOK)state.textContent='Enregistrement indisponible : exportez vos réponses avant de fermer.';
document.querySelector('#export-notes')?.addEventListener('click',()=>{
 const notes={seance:'S01',date:new Date().toISOString(),reponses:{}};
 document.querySelectorAll('[data-save]').forEach(input=>notes.reponses[input.dataset.save]=input.value);
 const url=URL.createObjectURL(new Blob([JSON.stringify(notes,null,2)],{type:'application/json'}));
 const link=document.createElement('a');link.href=url;link.download='agent-academy-s01-reponses.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
document.querySelector('#compare-prediction')?.addEventListener('click',()=>{
 const frame=document.querySelector('#observation-lab'),doc=frame.contentDocument;
 const log=doc?.querySelector('#log')?.textContent||'';
 const prediction=document.querySelector('#prediction').value.trim();
 document.querySelector('#comparison').textContent=!prediction?'Écrivez votre prédiction avant de comparer.':!log.includes('Étape ')?'Exécutez au moins une étape dans le laboratoire ci-dessous.':`Votre prédiction : ${prediction}\nTrace réellement produite :\n${log}\nComparez commande choisie et déplacement accepté. Expliquez les écarts dans votre réponse.`;
});
document.querySelector('#diagnostic-check')?.addEventListener('click',()=>{
 document.querySelector('#diagnostic-feedback').textContent='Attendus : droite ; gauche ; arrêt ; annoncer() affiche haut mais retourne None ; après (2,1) puis droite : (3,1). Si print et return sont confondus, exécutez le diagnostic dans la console avant le TP. Ce diagnostic n’est pas noté.';
});
document.querySelector('#check-learning')?.addEventListener('click',()=>{
 const answers={definition:'b',transition:'c',preuve:'a'};let correct=0,filled=0;
 for(const [name,value] of Object.entries(answers)){
  const selected=document.querySelector(`input[name="${name}"]:checked`);if(selected)filled++;if(selected?.value===value)correct++;
 }
 const justification=document.querySelector('#bilan-raisonnement').value.trim();
 document.querySelector('#learning-feedback').textContent=filled<3?'Répondez aux trois questions avant de vérifier.':`${correct}/3 réponses de repérage correctes.\nUn agent peut agir sans LLM ; le moteur refuse la seconde commande droite ; une cible à gauche départage retour constant et comparaison.\n${justification?'Votre justification reste à discuter avec l’enseignant : le texte libre n’est pas évalué automatiquement.':'Ajoutez votre justification et un cas de test : les choix seuls ne suffisent pas.'}\nReprenez le journal si vous confondez commande et mouvement. Aucun score ne certifie à lui seul la compréhension.`;
});
const links=[...document.querySelectorAll('.contents a')];
if('IntersectionObserver' in window){
 const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){links.forEach(link=>{if(link.hash==='#'+entry.target.id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')})}},{rootMargin:'0px 0px -65% 0px'});
 document.querySelectorAll('article>section[id]').forEach(section=>observer.observe(section));
}
