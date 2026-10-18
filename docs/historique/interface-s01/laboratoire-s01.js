// Adaptateur de présentation S01 ; le moteur et le Worker existants restent utilisés.
"use strict";
const embeddedMode=new URLSearchParams(location.search).get('s01');
if(['observation','python'].includes(embeddedMode)){
 document.body.classList.add('s01-embedded');
 const style=document.createElement('style');
 style.textContent=`.s01-embedded .top,.s01-embedded .hero,.s01-embedded .back,.s01-embedded aside,.s01-embedded .quiz,.s01-embedded .footer,.s01-embedded .skip{display:none}.s01-embedded .layout,.s01-embedded .course{grid-template-columns:1fr}.s01-embedded .shell{padding:14px}.s01-embedded .arena{grid-template-columns:1fr}.s01-embedded .grid{width:min(100%,550px);margin:auto}.s01-embedded .stats{grid-template-columns:repeat(2,minmax(0,1fr))}.s01-embedded .stat,.s01-embedded .course>section{min-width:0}`+(embeddedMode==='observation'?'.s01-embedded .course{display:none}':'');
 document.head.append(style);
 const starter=`def decider(position, objectif, obstacles):\n    # À modifier : comparer les coordonnées.\n    return "arrêt"\n\nfor position in [(0, 2), (4, 2), (2, 2)]:\n    print(position, decider(position, (2, 2), []))`;
 if(embeddedMode==='python'){
  document.querySelector('#code').value=starter;
  document.querySelector('#py-reset').textContent='Restaurer le départ S01';
  document.querySelector('#py-reset').addEventListener('click',()=>{document.querySelector('#code').value=starter});
  document.querySelector('.course>section:last-child>p').textContent='TP01 : complétez decider. Exécuter Python lance les appels console sans déplacer la grille. Pour agir sur la carte fixe, choisir Mon agent Python, Réinitialiser, puis Exécuter une étape. Le premier chargement de Pyodide nécessite Internet.';
 }
 function theme(value){if(!['light','dark','projector'].includes(value))return;document.body.className='s01-embedded '+(value==='dark'?'':value);document.querySelector('#display').value=value}
 window.addEventListener('message',event=>{if(event.origin===location.origin&&event.source===parent&&event.data?.type==='academy-theme')theme(event.data.value)});
 if(parent!==window){
  let lastHeight=0;
  const report=()=>{const height=Math.ceil(document.querySelector('.shell').getBoundingClientRect().height)+8;if(height!==lastHeight){lastHeight=height;parent.postMessage({type:'academy-lab-height',height},location.origin)}};
  new ResizeObserver(report).observe(document.querySelector('.shell'));report();
 }
}
