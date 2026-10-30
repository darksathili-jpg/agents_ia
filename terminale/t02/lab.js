/* ORCHESTRA NSI T02 — démonstration guidée et exécution Python séparées.
 * Une animation de référence ne représente PAS le code de l'élève. */
(function () {
  'use strict';
  const WIDTH = 7, HEIGHT = 5, START = [0, 2], GOAL = [6, 2];
  const PRESETS = {
    difference: [[1,2],[2,3],[4,2],[4,4],[5,3]],
    direct: [],
    barrier: [[2,2],[3,2],[4,2]],
    isolated: [[5,2],[6,1],[6,3]]
  };
  const ORDER = {
    ESON: [[1,0],[0,1],[-1,0],[0,-1]],
    NOSE: [[0,-1],[-1,0],[0,1],[1,0]]
  };
  const key = point => point.join(',');
  const point = value => value.split(',').map(Number);
  function reconstruct(parents, targetKey) {
    const result = [];
    let vertex = targetKey;
    while(vertex != null) {
      result.push(point(vertex));
      vertex = parents.get(vertex);
    }
    return result.reverse();
  }
  function traverse(walls, order, method) {
    const vectors = ORDER[order] || ORDER.ESON;
    const blocked = new Set(walls.map(key));
    const src = key(START), dst = key(GOAL);
    const frontier = [src], discovered = new Set([src]), examined = [];
    const parents = new Map([[src, null]]);
    const frames = [{
      current: null, examined: [], discovered: [src],
      frontier: [src], path: [], finished: false,
      explanation: 'La recherche démarre : départ inséré dans ' + (method === 'bfs' ? 'la file.' : 'la pile.')
    }];
    let path = [];
    while(frontier.length) {
      const current = frontier.splice(method === 'bfs' ? 0 : frontier.length - 1, 1)[0];
      examined.push(current);
      if(current === dst) {
        path = reconstruct(parents, current);
        frames.push({
          current, examined: examined.slice(), discovered: [...discovered],
          frontier: frontier.slice(), path: path.map(key), finished: true,
          explanation: 'Cible retirée de ' + (method === 'bfs' ? 'la file' : 'la pile') + '. Chemin reconstruit.'
        });
        break;
      }
      const [x,y] = point(current);
      const vectorsToPush = method === 'dfs' ? [...vectors].reverse() : vectors;
      for (const [dx,dy] of vectorsToPush) {
        const next = [x+dx,y+dy], nextKey = key(next);
        if(next[0] < 0 || next[0] >= WIDTH || next[1] < 0 || next[1] >= HEIGHT
            || blocked.has(nextKey) || discovered.has(nextKey)) continue;
        discovered.add(nextKey);
        parents.set(nextKey,current);
        frontier.push(nextKey);
      }
      frames.push({
        current, examined: examined.slice(), discovered: [...discovered],
        frontier: frontier.slice(), path: [], finished: false,
        explanation: 'Sommet (' + current + ') traité. ' + frontier.length
          + ' sommet(s) en attente dans ' + (method === 'bfs' ? 'la file.' : 'la pile.')
      });
    }
    if(!path.length) {
      frames.push({
        current:null,examined:examined.slice(),discovered:[...discovered],
        frontier:[],path:[],finished:true,
        explanation:'Aucun chemin : la structure est vide et la cible n’a pas été atteinte.'
      });
    }
    return {frames, path, examined:examined.length, found:!!path.length};
  }
  function analyze(walls, order='ESON') {
    return {bfs:traverse(walls,order,'bfs'), dfs:traverse(walls,order,'dfs')};
  }
  const api = {traverse, analyze, PRESETS, WIDTH, HEIGHT};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;

  const $ = id => document.getElementById(id);
  let walls = PRESETS.difference.map(p => p.slice());
  let state = analyze(walls), stepIndex = 0, timer = null, worker = null,
      workerReady = false, taskId = 0, runTimer = null, sourceStarter = null;

  function framesTotal() {
    return Math.max(state.bfs.frames.length,state.dfs.frames.length);
  }
  function stop() {
    if(timer !== null) clearInterval(timer);
    timer = null;
    $('play').textContent='▶ Lire';
    $('play').setAttribute('aria-pressed','false');
  }
  function makeCell(method,x,y) {
    const c=document.createElement('button');
    c.type='button';c.className='cell';c.dataset.x=x;c.dataset.y=y;
    c.setAttribute('aria-label','Case ('+x+', '+y+') : cliquer pour modifier le mur');
    c.addEventListener('click',()=>{
      if ((x===START[0]&&y===START[1])||(x===GOAL[0]&&y===GOAL[1]))return;
      const n=key([x,y]);
      walls=walls.some(p=>key(p)===n)?walls.filter(p=>key(p)!==n):[...walls,[x,y]];
      recompute();
    });
    return c;
  }
  function initBoards(){
    for (const method of ['bfs','dfs']){
      const host=$('board-'+method);
      for(let y=0;y<HEIGHT;y++)for(let x=0;x<WIDTH;x++)host.append(makeCell(method,x,y));
    }
  }
  function draw(method) {
    const result=state[method];
    const frame=result.frames[Math.min(stepIndex,result.frames.length-1)];
    const visited=new Set(frame.examined), discovered=new Set(frame.discovered);
    const route=new Set(frame.path), blocked=new Set(walls.map(key));
    for(const cell of $('board-'+method).children) {
      const x=+cell.dataset.x,y=+cell.dataset.y,k=key([x,y]);
      const isStart=x===START[0]&&y===START[1],isGoal=x===GOAL[0]&&y===GOAL[1];
      cell.className='cell';
      if(blocked.has(k))cell.classList.add('wall');
      else if(route.has(k))cell.classList.add('route');
      else if(frame.current===k)cell.classList.add('active');
      else if(visited.has(k))cell.classList.add('active','seen');
      else if(discovered.has(k))cell.classList.add('seen');
      if (isStart)cell.classList.add('fixed','start');
      if (isGoal)cell.classList.add('fixed','target');
      cell.replaceChildren();
      if(isStart||isGoal){
        const text=document.createElement('span');
        text.textContent=isStart?'D':'A';
        cell.appendChild(text);
      } else if(frame.current===k&&!blocked.has(k)) {
        const text=document.createElement('span');text.textContent='●';cell.appendChild(text);
      }
      cell.setAttribute('aria-label','Case ('+x+', '+y+')'+
        (blocked.has(k)?' mur':isStart?' départ':isGoal?' arrivée':
         frame.current===k?' sommet traité':route.has(k)?' chemin':visited.has(k)?' traité':
         discovered.has(k)?' découvert':' libre'));
    }
    $('count-'+method).textContent=String(frame.examined.length);
    $('length-'+method).textContent=frame.finished?
      (frame.path.length?String(frame.path.length-1):'∅'):'—';
    const host=$('frontier-'+method);host.replaceChildren();
    for (const n of frame.frontier.slice(0,35)) {
      const tag=document.createElement('span');tag.textContent='('+n+')';host.appendChild(tag);
    }
    if(!frame.frontier.length)host.textContent='Aucune case';
    $('event-'+method).textContent=frame.explanation;
  }
  function render() {
    draw('bfs');draw('dfs');
    $('step-number').textContent=stepIndex+' / '+(framesTotal()-1);
    $('timeline').max=Math.max(1,framesTotal()-1);
    $('timeline').value=String(stepIndex);
    const atEnd=stepIndex>=framesTotal()-1;
    $('step').disabled=atEnd;
    if(atEnd)stop();
    const left=state.bfs,right=state.dfs;
    if(!atEnd){
      $('compare-result').textContent='Démonstration guidée, calculée localement : '
        +'les opérations sont synchronisées par rang de traitement, pas par durée.';
    }else if(!left.found){
      $('compare-result').textContent='La cible est inaccessible : aucun des deux parcours ne trouve de chemin.';
    }else {
      const b=left.path.length-1,d=right.path.length-1;
      $('compare-result').textContent='BFS : '+b+' déplacement(s) ; DFS : '+d+
        ' déplacement(s). '+(b===d?'Ils obtiennent ici la même longueur.':
          'BFS trouve ici un chemin plus court.')+
        ' Les deux chemins sont valides.';
    }
  }
  function recompute(){
    stop();stepIndex=0;
    state=analyze(walls,$('order').value);
    render();
  }
  function next(){if(stepIndex<framesTotal()-1){stepIndex++;render();}}
  function togglePlay(){
    if(timer!==null){stop();return;}
    if(stepIndex>=framesTotal()-1)stepIndex=0;
    $('play').textContent='Ⅱ Pause';
    $('play').setAttribute('aria-pressed','true');
    timer=setInterval(()=>{if(stepIndex>=framesTotal()-1)stop();else next();},500);
    render();
  }
  function setTheme(theme){
    if(!['light','dark','projection'].includes(theme))return;
    document.body.dataset.theme=theme;
    for(const button of document.querySelectorAll('[data-theme]')) {
      if(button.tagName==='BUTTON')button.setAttribute('aria-pressed',String(button.dataset.theme===theme));
    }
    try{localStorage.setItem('orchestra-t02-theme',theme);}catch(_){}
  }
  function loadDraft(){
    try{
      const draft=JSON.parse(localStorage.getItem('orchestra-t02-draft')||'null');
      if(draft&&typeof draft.code==='string')$('python-code').value=draft.code;
      if(draft&&typeof draft.justification==='string')$('justification').value=draft.justification;
      const theme=localStorage.getItem('orchestra-t02-theme');
      if(theme)setTheme(theme);
    }catch(_){}
  }
  function save(){
    try{localStorage.setItem('orchestra-t02-draft',JSON.stringify({
      code:$('python-code').value,justification:$('justification').value
    }));}catch(_){}
  }
  async function loadStarter(){
    try{
      const response=await fetch('eleve.py',{cache:'no-store'});
      if(!response.ok)throw Error('Code de départ non accessible');
      sourceStarter=await response.text();
      if(!$('python-code').value)$('python-code').value=sourceStarter;
    }catch(e){$('python-status').textContent='Le code de départ est inaccessible : '+e.message;}
  }
  function workerStop(){
    if(worker){worker.terminate();worker=null;}
    workerReady=false;clearTimeout(runTimer);runTimer=null;
    $('run-python').disabled=true;
  }
  function newWorker(){
    workerStop();
    const id=++taskId;
    if(typeof Worker==='undefined'){
      $('python-status').textContent='Web Worker indisponible dans ce navigateur.';return;
    }
    worker=new Worker('python-worker.js');
    worker.onmessage=({data})=>{
      if(id!==taskId)return;
      if(data.type==='ready'){
        workerReady=true;$('python-status').textContent=
          data.source==='local'?'Python prêt · distribution locale':'Python prêt · secours réseau';
        $('run-python').disabled=false;
      }
      if(data.type==='error'){
        $('python-status').textContent='Erreur Python : '+data.message;
        clearTimeout(runTimer);$('run-python').disabled=false;
        if(data.stage==='load')workerStop();
      }
      if(data.type==='result'){
        if(data.id!==taskId)return;
        clearTimeout(runTimer);runTimer=null;
        $('python-status').textContent='Exécution terminée';
        $('run-python').disabled=false;
        showResult(data.data);
      }
    };
    worker.onerror=e=>{$('python-status').textContent='Erreur du moteur Python';workerStop();};
    $('python-status').textContent='Préparation de Pyodide…';
  }
  function appendText(host,tag,text,klass){
    const node=document.createElement(tag);
    if(klass)node.className=klass;
    node.textContent=text;host.appendChild(node);
    return node;
  }
  function showResult(data){
    const cases=$('result-cases');cases.replaceChildren();
    $('score').textContent=(data.passed??0)+' / '+(data.total??7);
    if(data.error){
      $('result-summary').textContent=data.error;
      $('student-trace').hidden=true;return;
    }
    $('result-summary').textContent=data.success?
      'Tous les contrôles sont réussis. Explique maintenant ton choix dans la dernière activité.':
      'Les chemins et les structures sont contrôlés séparément. Lis les retours ci-dessous.';
    for(const result of data.results||[]){
      const row=document.createElement('article');row.className='case'+(result.ok?'':' failed');
      appendText(row,'span',result.ok?'✓':'×','status-icon');
      const main=document.createElement('div');
      appendText(main,'strong',result.name);
      appendText(main,'small','BFS : '+result.bfs.message);
      appendText(main,'small','DFS : '+result.dfs.message);
      row.appendChild(main);
      appendText(row,'span',(result.ok?'2':'—')+' parcours','scores');
      cases.appendChild(row);
    }
    const first=(data.results||[]).find(r=>r.bfs.events.length||r.dfs.events.length);
    if(first){
      $('student-trace').hidden=false;
      const entries=['FILE · appels Python observés',
        ...first.bfs.events.slice(0,15).map(e=>e.op+' ('+e.vertex.join(',')+')'),
        'PILE · appels Python observés',
        ...first.dfs.events.slice(0,15).map(e=>e.op+' ('+e.vertex.join(',')+')')];
      $('student-trace-lines').textContent=entries.join('\n');
    }else $('student-trace').hidden=true;
  }
  function run(){
    if(!workerReady||!worker)return;
    const id=++taskId;
    // taskId identifie l'exécution ; le handler conserve l'identifiant du Worker.
    // Ne pas incrémenter le jeton du Worker lors d'une simple exécution.
    taskId=id-1;
    $('run-python').disabled=true;
    $('python-status').textContent='Exécution des 7 situations…';
    worker.postMessage({type:'run',source:$('python-code').value,id:taskId});
    clearTimeout(runTimer);
    runTimer=setTimeout(()=>{
      $('python-status').textContent='Exécution interrompue après 9 secondes. Worker redémarré.';
      newWorker();
    },9000);
  }
  function init(){
    initBoards();render();
    $('scenario').addEventListener('change',()=>{walls=PRESETS[$('scenario').value].map(p=>p.slice());recompute();});
    $('order').addEventListener('change',recompute);
    $('reset').addEventListener('click',()=>{walls=PRESETS[$('scenario').value].map(p=>p.slice());recompute();});
    $('step').addEventListener('click',()=>{stop();next();});
    $('play').addEventListener('click',togglePlay);
    $('timeline').addEventListener('input',()=>{stop();stepIndex=Number($('timeline').value);render();});
    for(const button of document.querySelectorAll('.themes button'))button.addEventListener('click',()=>setTheme(button.dataset.theme));
    $('python-code').addEventListener('input',save);
    $('justification').addEventListener('input',save);
    $('restore').addEventListener('click',()=>{
      if(sourceStarter!==null&&window.confirm('Effacer ton code et restaurer le départ ?')){
        $('python-code').value=sourceStarter;save();
      }
    });
    $('run-python').addEventListener('click',run);
    $('python-code').addEventListener('keydown',e=>{
      if(!window.OrchestraIndent)return;
      const action=e.key==='Tab'?(e.shiftKey?'unindent':'indent'):
                   e.key==='Enter'?'enter':e.key==='Backspace'?'backspace':null;
      if(action&&window.OrchestraIndent.applyToTextarea(e.currentTarget,action)){e.preventDefault();}
    });
    loadDraft();loadStarter();newWorker();
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)stop();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
  else init();
})();