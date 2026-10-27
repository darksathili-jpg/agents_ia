/* ORCHESTRA · Visualiseur pédagogique BFS
 * Données : une démonstration enregistrée depuis la référence CPython ou les
 * événements de File et VueMonde produits par le code exécuté de l'élève.
 * Ne déduit PAS de faux sommets explorés d'un trajet final.
 */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const key = p => Array.isArray(p) ? p.join(',') : '';
  const pretty = p => `(${Array.isArray(p) ? p.join(', ') : '—'})`;
  const valid = p => Array.isArray(p) && p.length === 2 && p.every(Number.isInteger);
  const demo = window.ORCHESTRA_DEMO_BFS;
  let student = null;
  let mode = 'demo';
  let frames = [];
  let current = 0;
  let playing = false;
  let interval = null;
  let visibilityObserver = null;
  let intersecting = true;
  const phases = ['planning', 'obstacle', 'replanning'];
  const phaseName = {planning: '01 · Explorer et planifier', obstacle: '02 · Un obstacle apparaît', replanning: '03 · Replanifier'};

  function buildFrames(record, isDemo) {
    if (!record?.world) return [];
    const w = record.world;
    const searches = Array.isArray(record.searches) ? record.searches : [];
    const trace = Array.isArray(record.trace) ? record.trace : [];
    const snapshots = [];
    const state = {
      world: w, position: [...w.start], obstacles: (w.obstacles || []).map(p => [...p]),
      path: [], queue: [], visited: [], currentVertex: null,
      phase: 'planning', searchNumber: 0, invalidQueue: false
    };
    const push = (title, detail, kind = 'info') => {
      snapshots.push({ ...state, position: [...state.position], obstacles: state.obstacles.map(p => [...p]),
        queue: state.queue.map(p => [...p]), visited: state.visited.map(p => [...p]),
        path: state.path.map(p => [...p]), currentVertex: state.currentVertex ? [...state.currentVertex] : null,
        title, detail, kind, isDemo });
    };
    push('Un objectif, une grille, des sommets.', 'Le robot doit rejoindre la cible. Les cases libres forment les sommets du graphe.');
    const done = new Set();
    let dynamicOccurred = false;
    const appendSearch = (search, index) => {
      state.phase = dynamicOccurred ? 'replanning' : 'planning';
      state.position = valid(search.start) ? [...search.start] : [...state.position];
      state.obstacles = (search.obstacles || state.obstacles).map(p => [...p]);
      state.queue = [];
      state.visited = [];
      state.path = [];
      state.currentVertex = null;
      state.invalidQueue = false;
      state.searchNumber = index + 1;
      push(dynamicOccurred ? 'Le robot cherche un nouveau chemin.' : 'Le BFS commence sa recherche.',
        dynamicOccurred ? 'Le dernier plan n’est plus praticable : une nouvelle recherche commence.' :
          'Le parcours en largeur utilise une file FIFO pour déterminer l’ordre de découverte.','search');
      for (const event of search.operations || []) {
        const v = event.value;
        if (!valid(v)) continue;
        const eventName = event.operation;
        if (eventName === 'enfiler') {
          state.queue.push([...v]);
          push(`Enfiler ${pretty(v)}`, 'Ce sommet est ajouté à la fin de la file. Il sera traité après ceux qui le précèdent.', 'enqueue');
        } else if (eventName === 'defiler') {
          // Le journal représente les opérations observées, y compris un éventuel défaut FIFO.
          if (state.queue.length && key(state.queue[0]) === key(v)) state.queue.shift();
          else { state.invalidQueue = true; const i = state.queue.findIndex(p => key(p) === key(v)); if (i >= 0) state.queue.splice(i, 1); }
          state.currentVertex = [...v];
          push(`Défiler ${pretty(v)}`, 'Ce sommet est retiré de la file pour être examiné.', 'dequeue');
        } else if (eventName === 'voisins') {
          state.currentVertex = [...v];
          if (!state.visited.some(p => key(p) === key(v))) state.visited.push([...v]);
          push(`Explorer les voisins de ${pretty(v)}`, 'Le programme appelle monde.voisins() : il étudie les arêtes issues de ce sommet.', 'explore');
        }
      }
      state.path = (search.path || []).filter(valid).map(p => [...p]);
      push(state.path.length ? 'Chemin reconstruit.' : 'Aucun chemin reconstruit.',
        state.path.length ? `La recherche a produit ${state.path.length - 1} déplacement(s) potentiels.` :
          'Aucun chemin n’a été produit par cette recherche.', 'path');
    };
    const runSearches = step => {
      searches.forEach((s,i) => { if (!done.has(i) && s.step === step) { done.add(i); appendSearch(s,i); } });
    };
    for (const row of trace.slice(1)) {
      if (row.action === 'OBSTACLE APPARU') {
        dynamicOccurred = true;
        state.phase = 'obstacle';
        state.obstacles = (row.obstacles || state.obstacles).map(p => [...p]);
        state.position = valid(row.position) ? [...row.position] : [...state.position];
        // Ne pas effacer l'ancien trajet : il montre précisément le conflit.
        push('Attention : le chemin prévu est bloqué !',
          'Un nouvel obstacle occupe une case du trajet. L’agent doit vérifier son plan avant de poursuivre.', 'obstacle');
      } else if (row.action === 'AVANCER') {
        runSearches(row.step);
        state.phase = dynamicOccurred ? 'replanning' : 'planning';
        state.obstacles = (row.obstacles || state.obstacles).map(p => [...p]);
        if (valid(row.position)) state.position = [...row.position];
        if (Array.isArray(row.plan) && row.plan.length) state.path = row.plan.filter(valid).map(p => [...p]);
        push(`Microduck avance vers ${pretty(state.position)}`, 'Le déplacement et la position proviennent du moteur Python.', 'move');
      }
    }
    // Certaines solutions appellent planifier dans un scénario sans déplacement.
    searches.forEach((s,i) => { if (!done.has(i)) appendSearch(s,i); });
    if (!trace.length || (trace.length === 1 && searches.length === 0)) {
      push('Aucune exploration enregistrée.', 'Aucun calcul de chemin ni déplacement n’a été observé pour cette situation.');
    }
    return snapshots;
  }

  function stop() {
    playing = false;
    if (interval !== null) { clearTimeout(interval); interval = null; }
    const b = $('bfs-play');
    b.textContent = '▶ Lire'; b.setAttribute('aria-pressed', 'false');
  }
  function schedule() {
    if (!playing || !intersecting || document.hidden) { stop(); return; }
    if (current >= frames.length - 1) { stop(); return; }
    const kind = frames[current]?.kind;
    const delay = kind === 'obstacle' ? 1150 : kind === 'path' ? 600 : kind === 'move' ? 450 : 105;
    interval = setTimeout(() => { interval = null; go(current + 1); schedule(); }, delay);
  }
  function togglePlay() {
    if (playing) { stop(); return; }
    if (current >= frames.length - 1) go(0);
    playing = true; $('bfs-play').textContent = 'Ⅱ Pause'; $('bfs-play').setAttribute('aria-pressed', 'true');
    schedule();
  }
  function go(n) {
    if (!frames.length) return;
    current = Math.min(frames.length - 1, Math.max(0,n));
    const f = frames[current];
    $('bfs-counter').textContent = `${current+1} / ${frames.length}`;
    $('bfs-slider').value = String(current);
    $('bfs-previous').disabled = current === 0;
    $('bfs-next').disabled = current === frames.length - 1;
    $('bfs-phase-label').textContent = phaseName[f.phase]?.toUpperCase() ?? '';
    $('bfs-action').textContent = f.title;
    $('bfs-explanation').textContent = f.detail;
    $('bfs-search-count').textContent = String(f.searchNumber);
    $('bfs-visited-count').textContent = String(f.visited.length);
    $('bfs-plan-count').textContent = f.path.length ? String(f.path.length) : '—';
    const queue = $('bfs-queue'); queue.replaceChildren();
    f.queue.slice(0,17).forEach((p,i) => {
      const cell = document.createElement('span');
      cell.className = 'bfs-queue-pill'+(i===0?' bfs-first':'');
      cell.textContent = pretty(p); queue.appendChild(cell);
    });
    if(f.queue.length > 17){const el=document.createElement('span');el.className='bfs-queue-overflow';el.textContent=`+${f.queue.length-17}`;queue.appendChild(el);}
    if (!f.queue.length){const e=document.createElement('span');e.className='bfs-empty';e.textContent='File vide';queue.appendChild(e);}
    $('bfs-queue-count').textContent = String(f.queue.length);
    $('bfs-queue-foot').textContent = f.invalidQueue ? 'Attention : l’ordre des retraits ne respecte pas les ajouts observés.' :
      f.queue.length ? `En tête de file : ${pretty(f.queue[0])}. C'est le prochain sommet à traiter.` : 'La file ne contient aucun sommet en attente.';
    $('bfs-reading').textContent = f.kind === 'obstacle' ? 'L’obstacle rouge apparaît sur l’ancienne route. Il faut calculer un nouveau chemin.' :
      f.kind === 'explore' ? 'La case bordée de bleu est un sommet effectivement exploré par monde.voisins().' :
      f.kind === 'enqueue' ? 'Une case entre dans la file FIFO : elle n’est pas encore explorée.' :
      f.kind === 'dequeue' ? 'La file retire son premier élément : le programme peut examiner ce sommet.' :
      f.kind === 'move' ? 'Ce pas du robot est issu de l’exécution Python, et non d’une animation prédessinée.' :
      f.kind === 'path' ? 'Le chemin en turquoise provient de la méthode planifier() du programme.' :
      'Le graphe et la file représentent le même état de la recherche.';
    document.querySelectorAll('[data-bfs-phase]').forEach(b=>{
      b.classList.toggle('selected',b.dataset.bfsPhase===f.phase);
      b.setAttribute('aria-pressed',String(b.dataset.bfsPhase===f.phase));
      b.disabled = !frames.some(x=>x.phase===b.dataset.bfsPhase);
    });
    renderGrid(f);
  }

  function renderGrid(f) {
    const grid = $('bfs-lesson-grid');
    const w = f.world.width, h = f.world.height;
    grid.style.setProperty('--bfs-cols', String(w));
    grid.style.setProperty('--bfs-rows', String(h));
    const obstacles = new Set(f.obstacles.map(key));
    const explored = new Set(f.visited.map(key));
    const queued = new Set(f.queue.map(key));
    const route = new Map(f.path.map((p,i)=>[key(p),i]));
    const fragment = document.createDocumentFragment();
    for(let y=0;y<h;y++) for(let x=0;x<w;x++){
      const v=[x,y], k=key(v);
      const tile=document.createElement('div');
      tile.className='bfs-tile';
      if(obstacles.has(k))tile.classList.add('blocked');
      else if(explored.has(k))tile.classList.add('explored');
      if(route.has(k))tile.classList.add('planned');
      if(queued.has(k))tile.classList.add('queued');
      if(f.currentVertex && key(f.currentVertex)===k)tile.classList.add('current');
      if(route.has(k) && !obstacles.has(k)){const badge=document.createElement('span');badge.className='bfs-route-index';badge.textContent=String(route.get(k));tile.appendChild(badge);}
      if(k===key(f.world.goal)){const target=document.createElement('span');target.className='bfs-target';target.textContent='◆';target.setAttribute('aria-hidden','true');tile.appendChild(target);}
      if(k===key(f.position)){const img=document.createElement('img');img.src='../assets/avatar-east.webp';img.alt='';img.draggable=false;img.className='bfs-robot';tile.appendChild(img);}
      if(obstacles.has(k)){const block=document.createElement('span');block.className='bfs-block-x';block.textContent='×';tile.appendChild(block);}
      fragment.appendChild(tile);
    }
    grid.replaceChildren(fragment);
    grid.setAttribute('aria-label',`Grille ${w} colonnes et ${h} lignes. Robot en ${pretty(f.position)}, cible en ${pretty(f.world.goal)}. ${f.obstacles.length} obstacle(s), ${f.visited.length} sommet(s) exploré(s), ${f.queue.length} dans la file.`);
  }

  function setMode(value){
    if(value==='student' && !student)return;
    stop(); mode=value;
    const r=value==='student'?student:demo;
    frames=buildFrames(r,value==='demo');
    $('bfs-mode-demo').classList.toggle('selected',value==='demo');
    $('bfs-mode-student').classList.toggle('selected',value==='student');
    $('bfs-mode-demo').setAttribute('aria-pressed',String(value==='demo'));
    $('bfs-mode-student').setAttribute('aria-pressed',String(value==='student'));
    $('bfs-provenance').textContent=value==='demo'?'EXEMPLE GUIDÉ · Calcul de référence, pas ton programme':'MON EXÉCUTION PYTHON · Opérations réellement observées';
    $('bfs-slider').max=String(Math.max(0,frames.length-1));
    go(0);
  }
  function setResults(results){
    student = results?.results?.find(r=>r.id==='dynamic') ?? null;
    $('bfs-mode-student').disabled = !student;
    if(student)setMode('student');
    else if(mode==='student')setMode('demo');
  }
  function init(){
    if(!$('bfs-lab'))return;
    $('bfs-play').addEventListener('click',togglePlay);
    $('bfs-previous').addEventListener('click',()=>{stop();go(current-1);});
    $('bfs-next').addEventListener('click',()=>{stop();go(current+1);});
    $('bfs-restart').addEventListener('click',()=>{stop();go(0);});
    $('bfs-slider').addEventListener('input',e=>{stop();go(Number(e.target.value));});
    $('bfs-mode-demo').addEventListener('click',()=>setMode('demo'));
    $('bfs-mode-student').addEventListener('click',()=>setMode('student'));
    document.querySelectorAll('[data-bfs-phase]').forEach(b=>b.addEventListener('click',()=>{
      stop();const i=frames.findIndex(f=>f.phase===b.dataset.bfsPhase);if(i>=0)go(i);
    }));
    document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
    if('IntersectionObserver' in window){
      visibilityObserver=new IntersectionObserver(items=>{
        intersecting=items[0]?.isIntersecting ?? true;
        if(!intersecting) stop();
      },{threshold:0.02});visibilityObserver.observe($('bfs-lab'));
    }
    if(!demo) { $('bfs-action').textContent='Démonstration indisponible.'; return; }
    setMode('demo');
  }
  window.OrchestraViz = {setResults, setMode, buildFrames, getFrameCount:()=>frames.length};
  init();
})();
