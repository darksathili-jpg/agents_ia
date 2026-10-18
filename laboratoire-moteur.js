"use strict";
const $=id=>document.getElementById(id);
const W=7,H=5,start=[0,2],goal=[6,2],walls=new Set(["2,1","2,2","2,3","4,0","4,1","4,3","4,4"]);
let busy=false,epoch=0;let pos=[...start],history=[],visited=new Set(["0,2"]),timer=null,mode="ready",last="Position initiale.";
const key=p=>p.join(","),eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const moves=[["droite",[1,0]],["bas",[0,1]],["haut",[0,-1]],["gauche",[-1,0]]];
const valid=p=>p[0]>=0&&p[0]<W&&p[1]>=0&&p[1]<H&&!walls.has(key(p));
function bfs(from){const q=[[from,[]]],seen=new Set([key(from)]);while(q.length){const [p,path]=q.shift();if(eq(p,goal))return path[0]||null;for(const [name,d] of moves){const n=[p[0]+d[0],p[1]+d[1]];if(valid(n)&&!seen.has(key(n))){seen.add(key(n));q.push([n,[...path,name]])}}}return null}
function naive(p){const [x,y]=p;if(x<goal[0])return "droite";if(x>goal[0])return "gauche";if(y<goal[1])return "bas";if(y>goal[1])return "haut";return null}
function append(message){history.push(message);if(history.length>80)history.shift();$("log").textContent=history.join("\n");$("log").scrollTop=$("log").scrollHeight}
function stop(){if(timer!==null){clearInterval(timer);timer=null}$("run").textContent="▶ Exécution auto"}
function draw(){const grid=$("grid");grid.replaceChildren();for(let y=0;y<H;y++)for(let x=0;x<W;x++){const p=[x,y],cell=document.createElement("div");cell.className="cell"+(walls.has(key(p))?" wall":"")+(eq(p,goal)?" goal":"")+(visited.has(key(p))?" visited":"");const center=document.createElement("span");center.textContent=eq(pos,p)?"◆":eq(p,goal)?"◎":walls.has(key(p))?"■":"";if(eq(pos,p))center.className="agent";else if(eq(p,goal))center.className="goalmark";cell.append(center);cell.title=walls.has(key(p))?"Obstacle":eq(p,goal)?"Objectif":'Case '+x+','+y;grid.append(cell)}$("position").textContent=key(pos);$("steps").textContent=String(Math.max(0,history.filter(s=>s.startsWith("Étape ")).length));$("state").textContent=mode==="won"?"Objectif atteint":mode==="blocked"?"Bloqué":mode==="running"?"En cours":"Prêt";$("statuspill").textContent=mode==="won"?"● Mission réussie":mode==="blocked"?"● Action impossible":mode==="running"?"● En cours":"● En attente";$("observation").textContent=last;$("step").disabled=mode==="won"||mode==="blocked" }
async function step(){if(busy||mode==="won"||mode==="blocked")return;busy=true;const revision=epoch;const policy=$("policy").value;let action;try{action=policy==="python"?(await requestPython("decide",{code:$("code").value,position:pos,goal,obstacles:[...walls].map(s=>s.split(",").map(Number))},12000)).action:policy==="bfs"?bfs(pos):naive(pos)}catch(e){if(revision===epoch){mode="blocked";last="Erreur Python : "+String(e.message||e);append(last);stop();draw()}busy=false;return}if(revision!==epoch){busy=false;return}busy=false;const n=history.filter(s=>s.startsWith("Étape ")).length+1;const before=key(pos);$("explain").textContent="Observation : position "+before+", cible "+key(goal)+". Politique : "+policy+". Décision : "+String(action)+". Vérification de l’action en cours.";if(action===null){mode=eq(pos,goal)?"won":"blocked";last="Aucune action disponible.";append("Fin : "+last);stop();draw();return}if(action==="arrêt"){mode=eq(pos,goal)?"won":"blocked";last=mode==="won"?"Objectif déjà atteint.":"La politique a demandé l’arrêt avant d’atteindre l’objectif.";append("Étape "+n+" · décision : arrêt · "+last);stop();draw();return}if(!moves.some(m=>m[0]===action)){mode="blocked";last="Action inconnue : "+String(action);append(last);stop();draw();return}const delta=moves.find(m=>m[0]===action)[1],next=[pos[0]+delta[0],pos[1]+delta[1]];if(!valid(next)){mode="blocked";last="Mur détecté devant l’agent.";append("Étape "+n+" · "+before+" → "+action+" · obstacle : mouvement refusé.");stop()}else{pos=next;visited.add(key(pos));mode=eq(pos,goal)?"won":"running";last="Observation : position "+key(pos)+", cible "+key(goal);append("Étape "+n+" · "+before+" → "+action+" → "+key(pos)+(mode==="won"?" · OBJECTIF ATTEINT":""));if(mode==="won")stop()}draw()}
function reset(){epoch++;stop();$("explain").textContent="L’agent observe sa position et la cible. Une politique détermine l’action ; l’environnement vérifie ensuite si elle est autorisée.";pos=[...start];visited=new Set([key(start)]);history=[];mode="ready";last="Position initiale.";append("Nouvelle expérience. Objectif : "+key(goal)+".");draw()}
$("step").addEventListener("click",step);$("reset").addEventListener("click",reset);$("policy").addEventListener("change",reset);$("run").addEventListener("click",()=>{if(timer!==null){stop();return}if(mode==="won"||mode==="blocked")reset();timer=setInterval(()=>{if(!busy)step()},650);$("run").textContent="⏸ Pause"});$("check").addEventListener("click",()=>{const selected=document.querySelector('input[name="quiz"]:checked');$("feedback").textContent=!selected?"Choisissez une réponse.":selected.value==="b"?"✓ Exact. Un agent n’a pas besoin d’un LLM : il lui faut une politique d’action et des interactions avec un environnement.":"À revoir : l’utilisation d’un LLM ou l’apprentissage en ligne ne sont pas des conditions nécessaires pour définir un agent."});
$("display").addEventListener("change",e=>{document.body.className=e.target.value==="dark"?"":e.target.value;localStorage.setItem("agent-academy-display",e.target.value)});const saved=localStorage.getItem("agent-academy-display");if(["dark","light","projector"].includes(saved)){$("display").value=saved;document.body.className=saved==="dark"?"":saved}
const initial=$("code").value;
$("py-reset").addEventListener("click",()=>{$("code").value=initial});
let worker=null,seq=0,runGeneration=0,pending=new Map();
function terminatePython(reason="Interrompu"){
  if(worker){worker.terminate();worker=null}
  for(const [id,item] of pending){clearTimeout(item.timeout);item.reject(new Error(reason))}
  pending.clear();
}
function requestPython(kind,args,timeoutMs=12000){
  if(!worker){
    worker=new Worker("./python-worker.js");
    worker.onmessage=({data})=>{
      const item=pending.get(data.id);if(!item)return;
      pending.delete(data.id);clearTimeout(item.timeout);
      if(data.ok)item.resolve(data);else item.reject(new Error(data.error));
    };
    worker.onerror=e=>{terminatePython(e.message||"Erreur du Web Worker")};
  }
  return new Promise((resolve,reject)=>{
    const id=++seq;
    const timeout=setTimeout(()=>terminatePython("Temps limite dépassé : exécution interrompue."),timeoutMs);
    pending.set(id,{resolve,reject,timeout});
    worker.postMessage({id,kind,...args});
  });
}
$("py-stop").addEventListener("click",()=>{
  epoch++;runGeneration++;stop();terminatePython("Arrêt demandé");busy=false;
  $("py-status").textContent="Interrompu";
  $("py-output").textContent="Exécution Python arrêtée.";
  $("py-run").disabled=false;
  reset();
});
$("py-run").addEventListener("click",async()=>{
  const button=$("py-run");const generation=++runGeneration;button.disabled=true;
  $("py-status").textContent="Exécution isolée…";
  $("py-output").textContent="Initialisation de Python dans le Web Worker…";
  try{
    const result=await requestPython("run",{code:$("code").value},12000);
    if(generation===runGeneration){$("py-status").textContent="Python prêt";$("py-output").textContent=result.output;}
  }catch(e){if(generation===runGeneration){$("py-status").textContent="Erreur / interruption";$("py-output").textContent=String(e.message||e)}}
  finally{button.disabled=false}
});
reset();
