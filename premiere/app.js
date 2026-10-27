'use strict';
// ORCHESTRA — UI de la séance pilote. Les verdicts proviennent exclusivement
// du moteur Python (engine.py), exécuté dans Pyodide via python-worker.js.
const $ = id => document.getElementById(id);
const code = $('code');
const STARTER = code.value;
const SOLUTION = `def decider(observation):
    # Le robot a atteint le colis : il doit s'arrêter.
    if observation["arrive"]:
        return "STOP"

    # Ne jamais avancer si la case devant est bloquée.
    if not observation["devant_libre"]:
        return "TOURNER_DROITE"

    # La balise indique la direction du prochain déplacement.
    if observation["orientation"] == observation["balise"]:
        return "AVANCER"

    # Sinon, le robot tourne et observera à nouveau.
    return "TOURNER_DROITE"`;
const HINTS = [
  'Indice 1 — Distingue trois situations : cible atteinte, obstacle devant, direction à choisir. Dans quel ordre faut-il les tester ?',
  'Indice 2 — Si observation["arrive"] vaut True, renvoie "STOP". Si observation["devant_libre"] vaut False, tourne pour éviter une collision.',
  'Indice 3 — Compare observation["orientation"] et observation["balise"]. Si les chaînes sont identiques ET si la case est libre, avance ; sinon, tourne.'
];
const SCENARIOS = [
  {id:'direct',name:'Trajet direct',start:[0,2],goal:[5,2],orientation:'E',walls:[]},
  {id:'obstacle',name:'Obstacle qui apparaît',start:[0,2],goal:[6,2],orientation:'E',walls:[[3,2],[3,1],[4,1]],dynamic_wall:[1,2]},
  {id:'labyrinthe',name:'Changer de direction',start:[0,4],goal:[6,0],orientation:'N',walls:[[2,4],[2,3],[2,2],[4,1],[4,2],[5,2]]},
  {id:'surprise',name:'Terrain surprise',start:[0,2],goal:[6,2],orientation:'N',walls:[[0,1],[0,4],[1,3],[2,0],[3,0],[3,1],[3,2],[3,3],[6,0],[6,4]]}
];
const DIRECTION_SPRITES = {N:'north',E:'east',S:'south',O:'west'};
let worker = null, ready = false, running = false, runId = 0, timer = null;
let attempts = 0, hints = 0, result = null, scenarioIndex = 0, traceIndex = -1, playTimer = null;
let lastError = null, previousResults = [], distinctAttemptHashes = [];
const DRAFT_KEY = 'orchestra-agent-lab-v51-draft';
// Empreinte non cryptographique : elle sert uniquement à compter les versions
// réellement différentes soumises par l'élève, pas à sécuriser des données.
// L'identité d'une tentative est calculée par l'AST Python côté moteur.
// Les espaces, les commentaires et les retours à la ligne ne suffisent pas
// pour débloquer les solutions.

function loadDraft() {
  try {
    const raw=localStorage.getItem(DRAFT_KEY);
    if (raw) {
      const saved=JSON.parse(raw);
      if (typeof saved.code==='string' && saved.code.length<10000) code.value=saved.code;
      if (Number.isInteger(saved.attempts) && saved.attempts>=0) attempts=Math.min(saved.attempts,10000);
      if (Array.isArray(saved.history)) previousResults=saved.history.slice(-20);
      if (Array.isArray(saved.distinctAttempts)) distinctAttemptHashes=saved.distinctAttempts.filter(x=>typeof x==='string').slice(-30);
      if (typeof saved.prediction==='string') $('prediction').value=saved.prediction;
      $('draft-status').textContent='Brouillon retrouvé : ton code et tes essais sont conservés.';
    }
  } catch (_) {$('draft-status').textContent='Stockage local indisponible : exporte ton bilan régulièrement.';}
  updateAttempts();updateSolutionAccess();
}
function updateAttempts() {$('attempt-count').textContent=`${attempts} essai${attempts>1?'s':''}`;}
function saveDraft() {
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify({code:code.value,attempts,prediction:$('prediction').value,history:previousResults.slice(-20),distinctAttempts:distinctAttemptHashes.slice(-30)}));
    $('draft-status').textContent='Brouillon enregistré sur cet appareil.';
  } catch (_) {$('draft-status').textContent='Stockage local indisponible : exporte ton bilan régulièrement.';}
}
function appendHistory(data) {
  if (data?.status === 'complete' && data.tests?.some(t=>t.trace?.length) && $('prediction').value) {
    const fp=data.fingerprint;
    if (typeof fp==='string' && fp!==data.starter_fingerprint && !distinctAttemptHashes.includes(fp))
      distinctAttemptHashes.push(fp);
    distinctAttemptHashes=distinctAttemptHashes.slice(-30);
  }
  previousResults.push({date:new Date().toISOString(),attempt:attempts,prediction:$('prediction').value,
    predictedAction:data?.tests?.[0]?.trace?.[0]?.action || null,passed:!!data?.passed,
    tests:data?.tests?.map(t=>({id:t.id,passed:t.passed,reason:t.reason,steps:t.steps})) || [],
    safety:data?.safety || null,error:data?.error || null});
  previousResults=previousResults.slice(-20);saveDraft();updateAttempts();updateSolutionAccess();
}
function exportReport() {
  const report={format:'orchestra-nsi-lab-v5.1',export_date:new Date().toISOString(),level:'Première NSI',
    purpose:'Première NSI · Agent réflexe Python, observation → décision → action → vérification',
    code:code.value,attempts,prediction:$('prediction').value,history:previousResults,
    latest:result?{passed:result.passed,tests:result.tests.map(t=>({id:t.id,passed:t.passed,reason:t.reason,steps:t.steps})),safety:result.safety}:null};
  const blob=new Blob([JSON.stringify(report,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob);
  const a=document.createElement('a');a.href=url;a.download='orchestra-bilan-agent.json';a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}

function runtime(text, status='waiting') {
  $('runtime-text').textContent = text;
  $('runtime-dot').className = `runtime-dot ${status}`;
  $('run').disabled = status !== 'ready' || running;
  $('run-label').textContent = status === 'ready' ? 'Lancer 5 vérifications' : status === 'error' ? 'Python indisponible' : 'Charger Python…';
}
function stopPlay() {
  if (playTimer) clearInterval(playTimer);
  playTimer = null;
  $('play').textContent = '▶ Rejouer';
}
function startWorker() {
  if (worker) worker.terminate();
  worker = null; ready = false; running = false;
  clearTimeout(timer);
  runtime('Initialisation de Python dans le navigateur…');
  if (!window.Worker) { runtime('Ce navigateur ne prend pas en charge les Web Workers.', 'error'); return; }
  try { worker = new Worker('python-worker.js'); }
  catch (err) { runtime(`Impossible de créer le Worker : ${err.message}`, 'error'); return; }
  const activeWorker=worker;
  timer = setTimeout(() => {
    if (worker!==activeWorker) return;
    runtime('Chargement impossible après 90 s. Vérifie Internet puis clique sur Redémarrer Python.', 'error');
    worker?.terminate(); worker = null;
  }, 90000);
  worker.onmessage = ({data}) => {
    if (worker !== activeWorker) return;
    if (data.type === 'loading') { runtime(data.text); return; }
    if (data.type === 'ready') {
      clearTimeout(timer); ready = true; running = false;
      runtime('Python prêt. Ton code sera exécuté dans Pyodide.', 'ready'); return;
    }
    if (data.type === 'error') {
      if (data.stage === 'run' && data.id !== runId) return;
      clearTimeout(timer); running = false;
      runtime(`Erreur ${data.stage === 'load' ? 'de chargement' : 'd’exécution'} : ${data.text}`, 'error');
      showFailure(`Erreur technique : ${data.text}`);
      lastError=data.text;appendHistory({status:'error',error:data.text});
      return;
    }
    if (data.type === 'result' && data.id === runId) {
      clearTimeout(timer); running = false;
      runtime('Python prêt. Résultats produits par le moteur.', 'ready');
      showResult(data.data);
      appendHistory(data.data);
    }
  };
  worker.onerror = event => {
    if (worker !== activeWorker) return;
    clearTimeout(timer); running = false;
    runtime(`Erreur du Worker : ${event.message || 'chargement impossible'}`, 'error');
    showFailure('Impossible de démarrer le moteur Python.');
  };
}
// L'édition est assurée par un vrai textarea (clavier, sélection, lecteur d'écran).
// Prism colore sa réplique visuelle locale ; aucun service externe n'est requis.
const syntaxView = $('syntax-highlight');
const syntaxCode = $('syntax-code');
function syncEditorScroll() {
  syntaxView.style.transform = `translate(${-code.scrollLeft}px, ${-code.scrollTop}px)`;
  $('line-number-content').style.transform = `translateY(${-code.scrollTop}px)`;
}
function setEditorLines() {
  const count = Math.max(8, code.value.split('\n').length);
  $('line-number-content').innerHTML = Array.from({length:count}, (_,i)=>i+1).join('<br>');
  if (window.Prism && Prism.languages && Prism.languages.python) {
    syntaxCode.innerHTML = Prism.highlight(code.value + (code.value.endsWith('\n')?' ':'') , Prism.languages.python, 'python');
    $('code-shell').classList.add('syntax-ready');
  } else {
    // Échec de Prism : le textarea reste lisible en texte brut.
    $('code-shell').classList.remove('syntax-ready');
  }
  syncEditorScroll();
}
function showHint(text) { $('hint-box').hidden = false; $('hint-box').textContent = text; updateSolutionAccess(); }
function reset() {
  if (!window.confirm('Effacer le code actuel et remettre l’exercice au début ? Le bilan des essais déjà effectués sera conservé.')) return;
  stopPlay(); result = null; scenarioIndex = 0; traceIndex = -1; hints = 0;
  code.value = STARTER; setEditorLines(); saveDraft();
  $('hint-box').hidden = true; $('hint-box').textContent = '';
  $('prediction').value = ''; $('prediction-feedback').textContent = '';
  document.querySelectorAll('.world-tab').forEach((tab,i) => {tab.classList.toggle('active',i===0);tab.setAttribute('aria-pressed',String(i===0));});
  clearVerdict(); renderTrace(); renderMap();
  if (!ready) startWorker();
}
function clearVerdict() {
  $('test-total').textContent = '0 / 5';
  $('test-results').replaceChildren();
  for (const s of SCENARIOS) addTestRow(s.name, null, s.id==='surprise' ? 'TERRAIN CACHÉ' : 'EN ATTENTE');
  addTestRow('Sûreté : 16 observations de blocage',null,'EN ATTENTE');
  const v=$('verdict'); v.className='verdict'; v.replaceChildren();
  const icon=document.createElement('span');icon.textContent='✦';
  const p=document.createElement('p');const b=document.createElement('strong');b.textContent='Prêt pour l’expérience ?';p.append(b,document.createElement('br'),'Écris ton programme puis lance les cinq vérifications.');v.append(icon,p);
}
function addTestRow(name, passed, label) {
  const row=document.createElement('div');row.className='test-item';
  const icon=document.createElement('span');icon.className=`test-icon ${passed===null?'neutral':passed?'pass':'fail'}`;icon.textContent=passed===null?'○':passed?'✓':'×';
  const title=document.createElement('span');title.textContent=name;
  const status=document.createElement('small');status.textContent=label;
  row.append(icon,title,status);$('test-results').append(row);
}
function showFailure(text) {
  const v=$('verdict');v.className='verdict failure';v.replaceChildren();
  const icon=document.createElement('span');icon.textContent='!';
  const p=document.createElement('p');const b=document.createElement('strong');b.textContent='Exécution interrompue';p.append(b,document.createElement('br'),text);v.append(icon,p);
}
function showResult(data) {
  stopPlay();
  if (!data || data.status !== 'complete' || !Array.isArray(data.tests) || data.tests.length!==4 || !data.safety) {
    result = null; clearVerdict(); showFailure(data?.error || 'Résultat Python inattendu.');renderTrace();renderMap();return;
  }
  result = data;
  document.querySelector('[data-scenario="3"]').hidden=false;
  const prediction = $('prediction').value;
  const firstAction = data.tests[0]?.trace?.[0]?.action;
  $('prediction-feedback').textContent = prediction && firstAction ? (prediction === firstAction ? `✓ Hypothèse confirmée : ton code a renvoyé ${firstAction}.` : `↗ Hypothèse à revoir : tu avais prévu ${prediction}, mais ton code a renvoyé ${firstAction}.`) : '';
  $('test-results').replaceChildren();
  for (const t of data.tests) addTestRow(t.name.replace(/^\d+\s*·\s*/,''),t.passed,t.passed?`OK · ${t.steps} PAS`:'À CORRIGER');
  if(data.safety) addTestRow('Sûreté : 16 observations de blocage',data.safety.passed,data.safety.passed?'16/16 SÛRS':'À CORRIGER');
  const passed=data.tests.filter(t=>t.passed).length+(data.safety?.passed ? 1 : 0);
  $('test-total').textContent=`${passed} / ${data.tests.length+1}`;
  const v=$('verdict');v.className=`verdict ${data.passed?'success':'failure'}`;v.replaceChildren();
  const icon=document.createElement('span');icon.textContent=data.passed?'✓':'!';
  const p=document.createElement('p');const b=document.createElement('strong');b.textContent=data.passed?'Bravo, ton agent atteint ses objectifs !':'Ton agent a encore besoin de toi.';
  p.append(b,document.createElement('br'),data.passed?'Quatre terrains et une vérification de sûreté réussis. Explore les décisions ci-dessous.':`${passed}/${data.tests.length+1} vérifications réussies. ${data.tests.find(t=>!t.passed)?.reason || (!data.safety?.passed?data.safety?.reason:'')}`);
  v.append(icon,p);
  scenarioIndex = Math.max(0,data.tests.findIndex(t=>!t.passed));
  traceIndex=0;
  document.querySelectorAll('.world-tab').forEach((tab,i)=>{tab.classList.toggle('active',i===scenarioIndex);tab.setAttribute('aria-pressed',String(i===scenarioIndex));});
  renderTrace();renderMap();
}
function selectedTrace() {return result?.tests?.[scenarioIndex]?.trace || [];}
function renderTrace() {
  const rows=$('trace-body');rows.replaceChildren();
  const trace=selectedTrace();
  $('trace-count').textContent=`${trace.length} ÉVÉNEMENT${trace.length>1?'S':''}`;
  if (!trace.length) {
    const tr=document.createElement('tr');tr.className='empty-row';const td=document.createElement('td');td.colSpan=4;td.textContent=result?'Aucune décision enregistrée pour ce terrain.':'Lance ton programme pour afficher les décisions de l’agent.';tr.append(td);rows.append(tr);
  } else trace.forEach((item,i)=>{
    const tr=document.createElement('tr');if (i===traceIndex) tr.className='selected';
    const obs=item.observation;
    const values=[String(item.step).padStart(2,'0'),`orient. ${obs.orientation} · balise ${obs.balise ?? '—'} · libre ${obs.devant_libre}`,item.action,(item.world_event ? '⚠ '+item.world_event+' ' : '')+item.outcome];
    for(const value of values){const td=document.createElement('td');td.textContent=value;tr.append(td);}
    tr.tabIndex=0;tr.setAttribute('aria-label',`Voir l’étape ${item.step}`);
    tr.addEventListener('click',()=>selectStep(i));tr.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectStep(i);}});
    rows.append(tr);
  });
  $('step-label').textContent=trace.length?`DÉCISION ${traceIndex+1} / ${trace.length}`:'Aucune décision';
  $('previous').disabled=traceIndex<=0;
  $('next').disabled=!trace.length||traceIndex>=trace.length-1;
  $('play').disabled=trace.length<2;
}
function selectStep(index) {
  stopPlay(); const trace=selectedTrace(); if(!trace.length)return;
  traceIndex=Math.max(0,Math.min(trace.length-1,index));renderTrace();renderMap();
}
function renderMap() {
  const scenario = result?.tests?.[scenarioIndex]?.scenario || SCENARIOS[scenarioIndex];
  const trace=selectedTrace();const current=trace[traceIndex];
  const position=current?current.before:{x:scenario.start[0],y:scenario.start[1],orientation:scenario.orientation};
  const map=$('map');map.replaceChildren();
  const NS='http://www.w3.org/2000/svg';
  function node(tag,attrs={},parent=map){const el=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));parent.append(el);return el;}
  const ox=29,oy=29,dx=62,dy=56;
  for(let y=0;y<5;y++)for(let x=0;x<7;x++){
    const effectiveWalls=current?.walls || scenario.walls;
    const isWall=effectiveWalls.some(w=>w[0]===x&&w[1]===y);
    const tile=node('rect',{x:ox+x*dx,y:oy+y*dy,width:56,height:50,rx:9,fill:isWall?'#9eb5c8':(x+y)%2===0?'#ffffff':'#f6fbff',stroke:isWall?'#7993ab':'#d7e7f0','stroke-width':1.3});tile.classList.add('map-tile');
    if(isWall){node('path',{d:`M${ox+x*dx+12} ${oy+y*dy+25}h32 M${ox+x*dx+28} ${oy+y*dy+11}v28`,stroke:'#7b94a9','stroke-width':2,opacity:.5});}
  }
  const gx=ox+scenario.goal[0]*dx+28,gy=oy+scenario.goal[1]*dy+25;
  node('circle',{cx:gx,cy:gy,r:23,fill:'#ffe8aa',stroke:'#edbb4d','stroke-width':2,'stroke-dasharray':'4 3'});
  const pack=node('g',{transform:`translate(${gx},${gy})`});
  node('path',{d:'M-12-7 0-14 12-7 0 0Z',fill:'#ffe59a',stroke:'#b98928','stroke-width':1.5},pack);
  node('path',{d:'M-12-7 0 0 0 14-12 7Z',fill:'#e7a938',stroke:'#b98928','stroke-width':1.5},pack);
  node('path',{d:'M12-7 0 0 0 14 12 7Z',fill:'#f5c65c',stroke:'#b98928','stroke-width':1.5},pack);
  node('path',{d:'M-4-11 8-4 8 3',stroke:'#fff4c7','stroke-width':3,fill:'none'},pack);
  const rx=ox+position.x*dx+28,ry=oy+position.y*dy+25;
  node('ellipse',{cx:rx,cy:ry+18,rx:21,ry:7,fill:'#173652',opacity:'.13'});
  node('circle',{cx:rx,cy:ry,r:23,fill:'#fffdf2',stroke:'#ffa92d','stroke-width':2.5});
  const robot=node('image',{href:`assets/avatar-${DIRECTION_SPRITES[position.orientation] || 'south'}.webp`,x:rx-27,y:ry-30,width:54,height:58,'preserveAspectRatio':'xMidYMid meet'});
  robot.classList.add('avatar-map-sprite');
  const indicator=node('g',{transform:`translate(${rx},${ry})`});
  node('path',{d:'M-5-24 0-32 5-24Z',fill:'#fb7f3f',stroke:'#fff','stroke-width':1.4,transform:`rotate(${({N:0,E:90,S:180,O:270})[position.orientation]})`},indicator);
  const obs=current?.observation;
  $('sensor-status').textContent=current?(current.world_event ? `⚠ ÉTAPE ${current.step} · BALISE PÉRIMÉE` : `ÉTAPE ${current.step} · AVANT ACTION`):'AVANT EXÉCUTION';
  $('sensor-arrive').textContent=obs?String(obs.arrive):'—';
  $('sensor-orientation').textContent=obs?String(obs.orientation):'—';
  $('sensor-balise').textContent=obs?String(obs.balise):'—';
  $('sensor-free').textContent=obs?String(obs.devant_libre):'—';
}
function run() {
  if (!ready || running || !worker) return;
  stopPlay();attempts++;updateAttempts();saveDraft();
  result=null;traceIndex=-1;clearVerdict();renderTrace();renderMap();
  running=true;runId++;
  runtime('Exécution réelle des quatre terrains et du contrôle de sûreté en Python…');
  $('run').disabled=true;
  const activeRun=runId;
  timer=setTimeout(()=>{
    if (activeRun!==runId || !running) return;
    running=false;ready=false;worker?.terminate();worker=null;
    showFailure('Temps dépassé : boucle infinie possible. Le code est conservé. Python redémarre automatiquement.');
    lastError='Dépassement du temps d’exécution (9 secondes).';
    appendHistory({status:'error',error:lastError});
    startWorker();
  },9000);
  worker.postMessage({type:'run',source:code.value,id:runId});
}
$('run').addEventListener('click',run);
$('reset').addEventListener('click',reset);
$('restart-python').addEventListener('click',()=>{stopPlay();saveDraft();startWorker();});
$('export').addEventListener('click',exportReport);
$('prediction').addEventListener('change',saveDraft);
$('hint').addEventListener('click',()=>{
  if (hints===1 && distinctAttemptHashes.length<1) {
    showHint('Pour obtenir le deuxième indice : choisis ta prédiction puis teste une première version de code qui diffère du programme de départ.');return;
  }
  if (hints===2 && distinctAttemptHashes.length<2) {
    showHint('Pour obtenir le troisième indice : modifie la logique de ta fonction, prédis son action puis exécute une nouvelle version. Les seuls espaces et commentaires ne comptent pas.');return;
  }
  showHint(HINTS[Math.min(hints,HINTS.length-1)]);
  if (hints < HINTS.length) hints++;
  saveDraft();
});
$('solution').addEventListener('click',()=>{if(distinctAttemptHashes.length>=2 && hints>=2)showHint('Solution commentée (à comparer avec ton programme) :\n\n'+SOLUTION);});
function updateSolutionAccess(){ $('solution').disabled = !(distinctAttemptHashes.length>=2 && hints>=2); } 
// Modes clair / sombre / vidéoprojecteur, mémorisés sans modifier les missions.
const THEMES = ['light','dark','projection'];
function setTheme(theme) {
  if (!THEMES.includes(theme)) theme = 'light';
  document.body.dataset.theme = theme;
  document.body.classList.toggle('projection', theme === 'projection');
  document.querySelectorAll('[data-theme-choice]').forEach(button => {
    const chosen = button.dataset.themeChoice === theme;
    button.classList.toggle('selected', chosen);
    button.setAttribute('aria-pressed', String(chosen));
  });
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#1e344b' : theme === 'projection' ? '#ffffff' : '#f6f7f5';
  try { localStorage.setItem('orchestra-display-theme', theme); } catch (_) { /* navigation privée */ }
  setEditorLines();
}
document.querySelectorAll('[data-theme-choice]').forEach(button => button.addEventListener('click', () => setTheme(button.dataset.themeChoice)));
let initialTheme = 'light';
try { initialTheme = localStorage.getItem('orchestra-display-theme') || 'light'; } catch (_) { /* stockage indisponible */ }
setTheme(initialTheme);
$('previous').addEventListener('click',()=>selectStep(traceIndex-1));
$('next').addEventListener('click',()=>selectStep(traceIndex+1));
$('play').addEventListener('click',()=>{
  if(playTimer){stopPlay();return;}
  const trace=selectedTrace();if(!trace.length)return;
  traceIndex=0;renderTrace();renderMap();$('play').textContent='Ⅱ Pause';
  playTimer=setInterval(()=>{if(traceIndex>=trace.length-1){stopPlay();return;}traceIndex++;renderTrace();renderMap();$('play').textContent='Ⅱ Pause';},550);
});
document.querySelectorAll('.world-tab').forEach(button=>button.addEventListener('click',()=>{
  stopPlay();scenarioIndex=Number(button.dataset.scenario);traceIndex=selectedTrace().length?0:-1;
  document.querySelectorAll('.world-tab').forEach(b=>{const active=b===button;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
  renderTrace();renderMap();
}));
code.addEventListener('input',()=>{setEditorLines();saveDraft();});
// Sur clavier tactile, certains navigateurs émettent beforeinput sans keydown.
code.addEventListener('beforeinput',event=>{
  if (event.inputType==='insertLineBreak' && !event.isComposing && event.cancelable) {
    event.preventDefault(); OrchestraIndent.applyToTextarea(code,'enter');
  }
});
code.addEventListener('scroll',syncEditorScroll,{passive:true});
window.addEventListener('resize',syncEditorScroll);
code.addEventListener('keydown',event=>{
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault(); run(); return;
  }
  if (event.key === 'Tab' && !event.ctrlKey && !event.altKey && !event.metaKey) {
    event.preventDefault();
    OrchestraIndent.applyToTextarea(code, event.shiftKey ? 'unindent' : 'indent');
    return;
  }
  if (event.key === 'Enter' && !event.shiftKey && !event.ctrlKey && !event.metaKey && !event.isComposing) {
    event.preventDefault(); OrchestraIndent.applyToTextarea(code, 'enter'); return;
  }
  if (event.key === 'Backspace' && !event.ctrlKey && !event.altKey && !event.metaKey) {
    if (OrchestraIndent.backspace(code.value, code.selectionStart, code.selectionEnd)) {
      event.preventDefault(); OrchestraIndent.applyToTextarea(code, 'backspace');
    }
  }
});

setEditorLines();

// Trois questions d'introduction. Il ne s'agit pas de tests Python exécutés.
const DEMO_CASES = [
  {observation:{arrive:false,orientation:'E',balise:'E',devant_libre:true},context:'Le robot regarde vers l’est ; la balise indique l’est.',answer:'AVANCER',explanation:'Les directions sont identiques et la case devant est libre : avancer.'},
  {observation:{arrive:false,orientation:'E',balise:'S',devant_libre:true},context:'Le robot regarde vers l’est ; la balise indique le sud.',answer:'TOURNER_DROITE',explanation:'Le robot doit se tourner vers le sud avant d’avancer.'},
  {observation:{arrive:false,orientation:'E',balise:'E',devant_libre:false},context:'Un obstacle vient d’apparaître à l’est. La balise indique encore l’est, mais devant_libre vaut False.',answer:'TOURNER_DROITE',explanation:'La balise a été calculée avant le nouvel obstacle : il ne faut jamais avancer lorsque devant_libre vaut False.'},
  {observation:{arrive:true,orientation:'S',balise:null,devant_libre:true},context:'Le robot est déjà arrivé au colis.',answer:'STOP',explanation:'La cible est atteinte : il faut s’arrêter sans avancer.'},
];
let demoCaseIndex = 0, demoCaseDone = false;
function renderDemo() {
  const d = DEMO_CASES[demoCaseIndex];demoCaseDone=false;
  $('demo-index').textContent=`CAS ${demoCaseIndex+1} / ${DEMO_CASES.length}`;
  $('demo-context').textContent=d.context;
  $('demo-observation').textContent='observation = '+JSON.stringify(d.observation,null,2).replace(/\btrue\b/g,'True').replace(/\bfalse\b/g,'False').replace(/\bnull\b/g,'None');
  $('demo-feedback').textContent='Choisis une action : tu peux te tromper et recommencer.';
  $('demo-feedback').className='demo-feedback';
  document.querySelectorAll('[data-demo-action]').forEach(b=>{b.disabled=false;b.classList.remove('correct','incorrect')});
  $('demo-next').disabled=true;
  $('demo-next').textContent=demoCaseIndex===DEMO_CASES.length-1?'Recommencer la démonstration ↻':'Cas suivant →';
}
document.querySelectorAll('[data-demo-action]').forEach(btn=>btn.addEventListener('click',()=>{
  const d=DEMO_CASES[demoCaseIndex];if(demoCaseDone)return;
  if(btn.dataset.demoAction===d.answer){
    demoCaseDone=true;btn.classList.add('correct');
    $('demo-feedback').className='demo-feedback correct';
    $('demo-feedback').textContent=`✓ ${d.explanation}`;
    $('demo-next').disabled=false;
    document.querySelectorAll('[data-demo-action]').forEach(b=>{if(b!==btn)b.disabled=true});
  }else{
    btn.classList.add('incorrect');
    $('demo-feedback').className='demo-feedback incorrect';
    $('demo-feedback').textContent=`Cette action ne convient pas. Relis « arrive », « orientation » et « balise », puis réessaie.`;
  }
}));
$('demo-next').addEventListener('click',()=>{demoCaseIndex=(demoCaseIndex+1)%DEMO_CASES.length;renderDemo()});
renderDemo();

loadDraft();clearVerdict();setEditorLines();renderTrace();renderMap();startWorker();
