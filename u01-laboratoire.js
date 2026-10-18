"use strict";
(()=>{
const parameters=new URLSearchParams(location.search);
const pythonMode=parameters.get('u01')==='python';
document.querySelector('#navigation-lab').hidden=pythonMode;
document.querySelector('#python-panel').hidden=!pythonMode;
const embedded=parent!==window;
if(embedded)document.body.classList.add('embedded');
function applyTheme(value){
 if(!['light','dark','projector'].includes(value))return;
 document.body.className=value+(embedded?' embedded':'');document.querySelector('#display').value=value;
}
applyTheme(document.querySelector('#display').value);
document.querySelector('#display').addEventListener('change',e=>applyTheme(e.target.value));
window.addEventListener('message',event=>{if(event.origin===location.origin&&event.source===parent&&event.data?.type==='academy-theme')applyTheme(event.data.value)});
const editor=document.querySelector('#code');const initial=editor.value;
document.querySelector('#py-reset').addEventListener('click',()=>editor.value=initial);
// Noms A–G : simple correspondance visuelle, sans changer les règles de déplacement.
function labelRow(){
 const cells=document.querySelectorAll('#grid .cell');
 for(let x=0;x<7;x++){
  const cell=cells[14+x];if(!cell||cell.querySelector('.case-label'))continue;
  const label=document.createElement('span');label.className='case-label';label.textContent='ABCDEFG'[x];label.setAttribute('aria-hidden','true');cell.append(label);
 }
}
new MutationObserver(labelRow).observe(document.querySelector('#grid'),{childList:true});labelRow();
if(embedded){
 let height=0;
 const report=()=>{const next=Math.ceil(document.querySelector('main').getBoundingClientRect().height)+8;if(next!==height){height=next;parent.postMessage({type:'academy-lab-height',height},location.origin)}};
 new ResizeObserver(report).observe(document.querySelector('main'));report();
}
})();
