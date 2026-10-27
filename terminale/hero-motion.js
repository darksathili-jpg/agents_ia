/* Animation décorative indépendante de l'exécution Python de l'élève. */
(()=>{
  'use strict';
  const hero=document.querySelector('.hero');
  const control=document.querySelector('#hero-motion');
  if(!hero || !control)return;
  const reduced=window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let requested=!reduced;
  let visible=true;
  function refresh(){
    const playing=requested && visible && !document.hidden;
    hero.dataset.motion=playing?'playing':'paused';
    control.setAttribute('aria-pressed',String(requested));
    control.setAttribute('aria-label',requested?'Mettre Microduck en pause':'Relancer l’animation de Microduck');
    control.textContent=requested?'Ⅱ Pause Microduck':'▶ Animer Microduck';
  }
  control.addEventListener('click',()=>{requested=!requested;refresh()});
  document.addEventListener('visibilitychange',refresh);
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;refresh()},{threshold:.05});
    observer.observe(hero);
  }
  refresh();
})();
