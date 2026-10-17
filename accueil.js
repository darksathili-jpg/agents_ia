"use strict";
const display=document.querySelector('#home-display');
function applyTheme(value){document.body.className='home '+value;display.value=value;}
const saved=localStorage.getItem('agent-academy-display');
applyTheme(['light','dark','projector'].includes(saved)?saved:'light');
display.addEventListener('change',()=>{applyTheme(display.value);localStorage.setItem('agent-academy-display',display.value)});
document.querySelectorAll('.lab-link').forEach(link=>{link.addEventListener('pointerenter',()=>document.querySelector('#robot-message').textContent='Prêt à programmer ton premier agent ?');link.addEventListener('pointerleave',()=>document.querySelector('#robot-message').textContent='On teste ?');link.addEventListener('focus',()=>document.querySelector('#robot-message').textContent='Bienvenue dans le labo !')});
