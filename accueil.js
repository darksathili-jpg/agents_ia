"use strict";
const display=document.querySelector('#home-display');
function applyTheme(value){document.body.className='home '+value;display.value=value;}
const saved=localStorage.getItem('agent-academy-display');
applyTheme(['light','dark','projector'].includes(saved)?saved:'light');
display.addEventListener('change',()=>{applyTheme(display.value);localStorage.setItem('agent-academy-display',display.value)});
const mission = {
  observer: {
    bubble: 'On teste ? Observe avant de choisir !',
    note: 'L’agent connaît sa position, la cible et les obstacles. Le chemin direct est coupé par un mur.'
  },
  decider: {
    bubble: 'Tout droit… ou un détour ? Comparons !',
    note: 'La politique gloutonne bute sur le mur. BFS recherche un chemin libre. Le détour bleu illustre un trajet possible, parmi d’autres.'
  },
  agir: {
    bubble: 'À toi ! Un pas, puis on vérifie.',
    note: 'L’environnement accepte un déplacement libre et refuse un mur. Dans le laboratoire, exécute une étape puis lis le journal.'
  }
};
const robotMessage = document.querySelector('#robot-message');
let selectedStep = 'observer';
document.querySelectorAll('[data-mission-step]').forEach(button => {
  button.addEventListener('click', () => {
    selectedStep = button.dataset.missionStep;
    document.querySelectorAll('[data-mission-step]').forEach(item => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    robotMessage.textContent = mission[selectedStep].bubble;
    document.querySelector('#mission-note').textContent = mission[selectedStep].note;
  });
});
document.querySelectorAll('.lab-link').forEach(link => {
  const welcomeMessage = document.querySelector('#welcome-message');
  const isWelcome = Boolean(link.closest('.intro'));
  const invite = () => {
    if(isWelcome) welcomeMessage.firstChild.nodeValue = 'On y va ? Je te guide !';
    else robotMessage.textContent = 'Prêt à programmer ton premier agent ?';
  };
  const restore = () => {
    if(isWelcome) welcomeMessage.firstChild.nodeValue = 'Bienvenue dans le labo !';
    else robotMessage.textContent = mission[selectedStep].bubble;
  };
  link.addEventListener('pointerenter', invite);
  link.addEventListener('pointerleave', () => { if(document.activeElement !== link) restore(); });
  link.addEventListener('focus', invite);
  link.addEventListener('blur', restore);
});
