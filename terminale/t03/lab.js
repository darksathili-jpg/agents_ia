/* T03 · Orchestration de la démonstration et des résultats réels.
 * La démonstration JavaScript n'est jamais assimilée au programme de l'élève. */
(function () {
  'use strict';
  const WIDTH=6, HEIGHT=3, ORDER=[[1,0],[0,-1],[0,1],[-1,0]];
  const CASES=[
    {name:'Route libre',start:[0,1],goal:[5,1],walls:[]},
    {name:'Obstacle découvert',start:[0,1],goal:[5,1],walls:[[3,1]]},
    {name:'Obstacle dès le départ',start:[0,1],goal:[5,1],walls:[[1,1]]},
    {name:'Mémoire après déplacement',start:[2,1],goal:[5,1],walls:[[3,1]]},
    {name:'Objectif au départ',start:[3,1],goal:[3,1],walls:[]},
    {name:'Agent encerclé',start:[2,1],goal:[5,1],walls:[[1,1],[3,1],[2,0],[2,2]]},
    {name:"Déplacement vers l'ouest",start:[5,2],goal:[0,2],walls:[]}
  ];
  const key=p=>p.join(',');
  const same=(a,b)=>!!a&&!!b&&a[0]===b[0]&&a[1]===b[1];
  const dist=(a,b)=>Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1]);
  const inside=p=>p[0]>=0&&p[0]<WIDTH&&p[1]>=0&&p[1]<HEIGHT;
  function decision(position,goal,memory) {
    if(same(position,goal))return null;
    const options=ORDER.map(([dx,dy])=>[position[0]+dx,position[1]+dy])
      .filter(p=>inside(p)&&!memory.has(key(p)));
    if(!options.length)return null;
    return options.reduce((best,p)=>dist(p,goal)<dist(best,goal)?p:best);
  }
  function demonstrate(scenario) {
    let position=scenario.start.slice();
    const known=new Set(), frames=[];
    for(let step=0;step<15;step++) {
      const visible=scenario.walls.filter(p=>dist(position,p)===1);
      for(const p of visible) known.add(key(p));
      const next=decision(position,scenario.goal,known);
      frames.push({step,position:position.slice(),visible:visible.map(p=>p.slice()),
        memory:[...known].map(k=>k.split(',').map(Number)),decision:next?next.slice():null});
      if(!next)return frames;
      if(scenario.walls.some(p=>same(p,next)))throw Error('Collision du scénario de démonstration');
      position=next;
    }
    throw Error('Démonstration supérieure à quinze cycles');
  }
  const api={decision,demonstrate,CASES,WIDTH,HEIGHT};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  if(typeof document==='undefined')return;

  const $=id=>document.getElementById(id);
  let index=1,kind='guide',frames=[],step=0,lastStep=-1,lastPosition=null;
  let sprite,playTimer=null,poseTimers=[],worker=null,workerReady=false,runId=0,runTimer=null;
  let submitted=null,validated=null,results=null,starter=null,activeResult=-1;
  const FACE={east:'east',west:'west',north:'north',south:'south'};
  const reduced=()=>!!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  function stopPose(){for(const id of poseTimers)clearTimeout(id);poseTimers=[];}
  function setPose(file) {
    const url='../../assets/'+file;
    if(sprite.getAttribute('src')!==url)sprite.setAttribute('src',url);
  }
  function face(before,after) {
    if(!before||!after)return'east';
    const dx=after[0]-before[0],dy=after[1]-before[1];
    return dx>0?FACE.east:dx<0?FACE.west:dy>0?FACE.south:dy<0?FACE.north:'east';
  }
  function animateWalking(direction) {
    stopPose();
    setPose('microduck-'+direction+'-0.webp');
    poseTimers=[
      setTimeout(()=>setPose('microduck-'+direction+'-1.webp'),140),
      setTimeout(()=>setPose('microduck-'+direction+'-2.webp'),280),
      setTimeout(()=>{setPose('microduck-idle-'+direction+'.webp');poseTimers=[];},430)
    ];
  }
  function stop() {
    if(playTimer!==null)clearInterval(playTimer);
    playTimer=null;
    $('play').textContent='▶ Lire';
    $('play').setAttribute('aria-pressed','false');
  }
  function rebuild() {
    stop();stopPose();kind='guide';activeResult=-1;frames=demonstrate(CASES[index]);
    step=0;lastStep=-1;lastPosition=null;draw();
  }
  function useStudentTrace(i) {
    if(!results||!results[i]||!results[i].ok||!results[i].trace.length)return;
    stop();stopPose();activeResult=i;kind='student';index=i;
    $('scenario').value=String(i);frames=results[i].trace;
    step=0;lastStep=-1;lastPosition=null;draw();
    $('terrain').scrollIntoView({behavior:reduced()?'auto':'smooth',block:'start'});
  }
  function makeBoard() {
    const board=$('board');
    for(let y=0;y<HEIGHT;y++)for(let x=0;x<WIDTH;x++) {
      const cell=document.createElement('div');
      cell.className='cell';cell.dataset.x=x;cell.dataset.y=y;
      cell.setAttribute('aria-label','Case ('+x+', '+y+')');
      board.appendChild(cell);
    }
    sprite=document.createElement('img');
    sprite.className='board-microduck';sprite.src='../../assets/microduck-idle-east.webp';
    sprite.alt='';sprite.draggable=false;sprite.setAttribute('aria-hidden','true');
    board.appendChild(sprite);
  }
  function draw() {
    const scene=CASES[index],frame=frames[step],memory=new Set(frame.memory.map(key));
    const visible=new Set(frame.visible.map(key)),world=new Set(scene.walls.map(key));
    $('source-label').textContent=kind==='guide'
      ?'DÉMONSTRATION GUIDÉE · aucun code élève exécuté'
      :'TRACE DU CODE ÉLÈVE · Python réellement exécuté';
    $('position-label').textContent='('+frame.position.join(', ')+')';
    const board=$('board');
    for(const cell of board.querySelectorAll('.cell')) {
      const p=[+cell.dataset.x,+cell.dataset.y],k=key(p);
      cell.className='cell';
      if(memory.has(k))cell.classList.add('seen');
      else if(visible.has(k)&&world.has(k))cell.classList.add('wall');
      if(same(p,scene.start))cell.classList.add('start');
      if(same(p,scene.goal))cell.classList.add('goal');
      if(same(p,frame.position))cell.classList.add('current');
      cell.textContent=same(p,scene.goal)?'A':same(p,scene.start)?'D':'';
      cell.setAttribute('aria-label','Case ('+p.join(', ')+')'+
        (memory.has(k)?' obstacle mémorisé':same(p,scene.goal)?' arrivée':
          same(p,scene.start)?' départ':' non observée'));
    }
    const cell=board.querySelector('.cell[data-x="'+frame.position[0]+'"][data-y="'+frame.position[1]+'"]');
    const nextIsMove=step===lastStep+1&&dist(lastPosition||frame.position,frame.position)===1;
    const direction=nextIsMove?face(lastPosition,frame.position):'east';
    sprite.style.transition=nextIsMove&&!reduced()?'left 430ms linear, top 430ms linear':'none';
    sprite.style.left=(cell.offsetLeft+cell.offsetWidth/2)+'px';
    sprite.style.top=(cell.offsetTop+cell.offsetHeight/2)+'px';
    sprite.style.width=Math.max(26,Math.min(87,cell.offsetWidth*1.08))+'px';
    if(nextIsMove&&!reduced())animateWalking(direction);
    else{stopPose();setPose('microduck-idle-'+direction+'.webp');}
    lastStep=step;lastPosition=frame.position.slice();
    $('visible').textContent=frame.visible.length
      ?frame.visible.map(p=>'('+p.join(', ')+')').join(' · '):'Aucun obstacle détecté';
    $('memory').replaceChildren();
    if(!frame.memory.length) {
      const em=document.createElement('em');em.textContent='Ensemble vide';$('memory').appendChild(em);
    } else for(const p of frame.memory) {
      const b=document.createElement('b');b.textContent='('+p.join(', ')+')';$('memory').appendChild(b);
    }
    $('decision').textContent=frame.decision?'('+frame.decision.join(', ')+')':'None · attendre';
    $('decision-note').textContent=frame.decision
      ?'Action proposée : le monde vérifie le déplacement vers cette case.'
      :'Aucun déplacement demandé : cible atteinte ou aucun voisin accessible.';
    $('explanation').textContent=frame.decision
      ?'Observation enregistrée. La mémoire contient '+frame.memory.length+
       ' obstacle(s) et la décision propose un pas voisin. Clique sur « Cycle suivant » pour voir le déplacement validé.'
      :'Cycle arrêté : la méthode decider renvoie None. Le personnage reste immobile.';
    $('step-label').textContent=(step+1)+' / '+frames.length;
    $('timeline').max=String(Math.max(0,frames.length-1));$('timeline').value=String(step);
    $('next').disabled=step===frames.length-1;
    if(step===frames.length-1)stop();
  }
  function moveNext(){if(step<frames.length-1){step++;draw();}}
  function togglePlay() {
    if(playTimer!==null){stop();return;}
    if(step>=frames.length-1){step=0;lastStep=-1;lastPosition=null;}
    $('play').textContent='Ⅱ Pause';$('play').setAttribute('aria-pressed','true');
    draw();playTimer=setInterval(moveNext,570);
  }
  function setTheme(theme) {
    if(!['light','dark','projection'].includes(theme))return;
    document.body.dataset.theme=theme;
    document.querySelectorAll('.themes button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.theme===theme)));
    try{localStorage.setItem('orchestra-t03-theme',theme);}catch(_){}
  }
  function remember() {
    try{localStorage.setItem('orchestra-t03-draft',JSON.stringify({
      code:$('python-code').value,justification:$('justification').value
    }));}catch(_){}
  }
  function invalidate() {
    remember();
    if(validated!==null||submitted!==null) {
      validated=null;results=null;activeResult=-1;
      $('score').textContent='— / 7';
      $('result-summary').textContent='Code modifié : les résultats précédents sont invalidés. Relance les tests.';
      $('result-cases').replaceChildren();
      if(kind==='student')rebuild();
    }
  }
  async function loadStarter() {
    try {
      const response=await fetch('eleve.py',{cache:'no-store'});
      if(!response.ok)throw Error('Code de départ HTTP '+response.status);
      starter=await response.text();
      let saved=null;
      try{saved=JSON.parse(localStorage.getItem('orchestra-t03-draft')||'null');}catch(_){}
      $('python-code').value=saved&&typeof saved.code==='string'?saved.code:starter;
      if(saved&&typeof saved.justification==='string')$('justification').value=saved.justification;
      const theme=localStorage.getItem('orchestra-t03-theme');
      if(theme)setTheme(theme);
    } catch(error) {$('python-status').textContent='Chargement du squelette impossible : '+error.message;}
  }
  function closeWorker() {
    if(worker){worker.terminate();worker=null;}
    workerReady=false;clearTimeout(runTimer);runTimer=null;$('run-python').disabled=true;
  }
  function bootWorker() {
    closeWorker();const generation=++runId;
    if(typeof Worker==='undefined'){$('python-status').textContent='Worker indisponible.';return;}
    worker=new Worker('python-worker.js');
    worker.onmessage=({data})=>{
      if(generation!==workerGeneration)return;
      if(data.type==='ready'){
        workerReady=true;
        $('run-python').disabled=false;
        $('python-status').textContent=data.source==='local'
          ?'Python prêt · distribution locale':'Python prêt · secours réseau';
      } else if(data.type==='error'){
        if(data.stage==='run'&&data.id!==activeRun)return;
        clearTimeout(runTimer);runTimer=null;submitted=null;validated=null;
        $('run-python').disabled=!workerReady;
        $('python-status').textContent='Erreur Python : '+data.message;
        $('result-summary').textContent='Le test a échoué avant de produire des résultats exploitables.';
        if(data.stage==='load')closeWorker();
      } else if(data.type==='result'){
        if(data.id!==activeRun)return;
        clearTimeout(runTimer);runTimer=null;
        $('run-python').disabled=false;
        if(submitted===null||$('python-code').value!==submitted){
          submitted=null;validated=null;
          $('result-summary').textContent='Code modifié pendant les tests : résultat ignoré.';
          return;
        }
        validated=submitted;submitted=null;showResults(data.data);
        $('python-status').textContent='Exécution Python terminée · résultats du code affiché';
      }
    };
    worker.onerror=()=>{$('python-status').textContent='Erreur du moteur Python';closeWorker();};
    $('python-status').textContent='Préparation de Pyodide…';
  }
  let workerGeneration=0,activeRun=0;
  // Surcharge explicite de l'identifiant de génération après création.
  const originalBoot=bootWorker;
  function newWorker(){workerGeneration=runId+1;originalBoot();}
  function showResults(data) {
    $('score').textContent=(data.passed||0)+' / '+(data.total||7);
    $('result-summary').textContent=data.error||(
      data.success?'Sept contrôles réussis. Termine par la justification écrite.':
      'Lis les retours ci-dessous et corrige la méthode concernée.');
    results=data.results||[];
    $('result-cases').replaceChildren();
    results.forEach((item,i)=>{
      const line=document.createElement('div');line.className='test-row'+(item.ok?'':' failed');
      const words=document.createElement('div'),title=document.createElement('strong');
      title.textContent=(item.ok?'✓ ':'× ')+item.name;
      const detail=document.createElement('small');detail.textContent=item.message;
      words.append(title,detail);line.appendChild(words);
      if(item.ok&&item.trace.length) {
        const button=document.createElement('button');button.type='button';
        button.textContent='Voir ma trace';button.addEventListener('click',()=>useStudentTrace(i));
        line.appendChild(button);
      }
      $('result-cases').appendChild(line);
    });
  }
  function runPython() {
    if(!workerReady||!worker)return;
    submitted=$('python-code').value;validated=null;results=null;
    const id=++activeRun; $('run-python').disabled=true;
    $('score').textContent='— / 7';
    $('result-summary').textContent='Exécution en cours : aucun score anticipé.';
    $('result-cases').replaceChildren();
    worker.postMessage({type:'run',id,source:submitted});
    clearTimeout(runTimer);
    runTimer=setTimeout(()=>{
      if(submitted===null)return;
      submitted=null;validated=null;closeWorker();
      $('python-status').textContent='Temps limite dépassé : moteur relancé. Vérifie les boucles de ton code.';
      $('result-summary').textContent='Aucun verdict : le programme n\'a pas terminé.';
      newWorker();
    },12000);
  }
  function init(){
    makeBoard();rebuild();
    for(const direction of ['north','east','south','west'])
      for(let i=0;i<3;i++){const image=new Image();image.src='../../assets/microduck-'+direction+'-'+i+'.webp';}
    $('scenario').addEventListener('change',()=>{
      index=Number($('scenario').value);rebuild();
    });
    $('reset').addEventListener('click',rebuild);
    $('next').addEventListener('click',moveNext);
    $('play').addEventListener('click',togglePlay);
    $('timeline').addEventListener('input',()=>{stop();step=Number($('timeline').value);draw();});
    document.querySelectorAll('.themes button').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.theme)));
    $('python-code').addEventListener('input',invalidate);
    $('justification').addEventListener('input',remember);
    $('run-python').addEventListener('click',runPython);
    $('restore').addEventListener('click',()=>{
      if(starter===null)return;
      $('python-code').value=starter;invalidate();
    });
    if(window.ORCHESTRA_EDITOR_INDENT&&typeof window.ORCHESTRA_EDITOR_INDENT.attach==='function')
      window.ORCHESTRA_EDITOR_INDENT.attach($('python-code'));
    loadStarter();newWorker();
  }
  init();
})();
