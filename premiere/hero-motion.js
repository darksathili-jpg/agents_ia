
/* Animation décorative 3 frames : aucun rapport artificiel avec les actions Python. */
(()=>{
  'use strict';
  const hero=document.querySelector('.hero');
  const control=document.querySelector('#hero-motion');
  if(!hero || !control) return;
  const reduced=window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let userPlaying=!reduced;
  let visible=true;
  function render(){
    const playing=userPlaying && visible && !document.hidden;
    hero.dataset.motion=playing ? 'playing' : 'paused';
    control.setAttribute('aria-pressed',String(userPlaying));
    control.setAttribute('aria-label', userPlaying ? 'Mettre l’animation du robot en pause' : 'Relancer l’animation du robot');
    control.textContent=userPlaying?'Ⅱ Pause animation':'▶ Animer le robot';
  }
  control.addEventListener('click',()=>{userPlaying=!userPlaying;render()});
  document.addEventListener('visibilitychange',render);
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;render()},{threshold:.02});
    observer.observe(hero);
  }
  render();
})();
