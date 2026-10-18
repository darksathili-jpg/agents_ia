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
// Lecture seule du moteur et de sa trace : aucune nouvelle décision ni transition.
function describeAttempt(){
 const rows=document.querySelector('#log').textContent.split('\n');
 const line=rows.filter(row=>row.startsWith('Étape ')).at(-1);
 const match=line?.match(/^Étape (\d+) · (\d+),(\d+) → (droite|gauche|haut|bas)(?: → (\d+),(\d+)| · obstacle : mouvement refusé\.)/);
 const values=document.querySelector('#detail-values');
 document.querySelector('#detail-empty').hidden=Boolean(match);
 values.hidden=!match;
 if(!match){document.querySelector('#detail-title').textContent='Lire la tentative';for(const dd of values.querySelectorAll('dd'))dd.textContent='';return}
 const before=[Number(match[2]),Number(match[3])];
 const command=match[4];
 const after=document.querySelector('#position').textContent.split(',').map(Number);
 const delta=moves.find(([name])=>name===command)[1];
 const requested=[before[0]+delta[0],before[1]+delta[1]];
 const name=point=>point[1]===2&&point[0]>=0&&point[0]<7?`${'ABCDEFG'[point[0]]} (${point.join(',')})`:`(${point.join(',')})`;
 // L'explication est conditionnée par la commande effectivement journalisée.
 let reason='La trace ne correspond pas à la règle gloutonne attendue : vérification nécessaire.';
 if(naive(before)===command){
  const horizontal=before[0]!==goal[0];
  const direction=horizontal?(before[0]<goal[0]?'à droite':'à gauche'):(before[1]<goal[1]?'plus bas':'plus haut');
  reason=horizontal?`L’arrivée ${name(goal)} est ${direction} de ${name(before)}. La règle choisit ${command} avant d’examiner haut/bas, sans consulter les murs.`:`Le robot et l’arrivée sont dans la même colonne ; l’arrivée est ${direction}. La règle choisit ${command}, sans consulter les murs.`;
 }
 const inside=requested[0]>=0&&requested[0]<W&&requested[1]>=0&&requested[1]<H;
 const allowed=valid(requested);
 const check=!inside?`${name(requested)} est hors de la grille : mouvement refusé.`:walls.has(key(requested))?`${name(requested)} contient un mur : mouvement refusé.`:`${name(requested)} est dans la grille et libre : mouvement autorisé.`;
 document.querySelector('#detail-title').textContent=`Tentative ${match[1]} — commande et résultat`;
 document.querySelector('#detail-command').textContent=`${command} : demande la case ${name(requested)} depuis ${name(before)}.`;
 document.querySelector('#detail-reason').textContent=reason;
 document.querySelector('#detail-check').textContent=check;
 document.querySelector('#detail-effect').textContent=eq(before,after)?`${name(before)} → ${name(after)} : aucun déplacement. La commande choisie reste ${command}.`:`${name(before)} → ${name(after)} : déplacement d’une case.`;
 if(allowed!==!eq(before,after))document.querySelector('#detail-check').textContent+=' Écart entre la vérification attendue et la position observée : à examiner.';
}
new MutationObserver(describeAttempt).observe(document.querySelector('#log'),{childList:true,characterData:true,subtree:true});describeAttempt();
if(embedded){
 let height=0;
 const report=()=>{const next=Math.ceil(document.querySelector('main').getBoundingClientRect().height)+8;if(next!==height){height=next;parent.postMessage({type:'academy-lab-height',height},location.origin)}};
 new ResizeObserver(report).observe(document.querySelector('main'));report();
}
})();
