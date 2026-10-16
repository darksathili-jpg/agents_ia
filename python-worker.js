"use strict";
let pyPromise;
async function python() {
  if (!pyPromise) {
    pyPromise = (async () => {
      importScripts("https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js");
      return loadPyodide({indexURL:"https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"});
    })();
  }
  return pyPromise;
}
self.onmessage = async ({data}) => {
  const {id,kind,code,position,goal,obstacles} = data;
  try {
    const py = await python();
    let lines=[];
    py.setStdout({batched:s=>lines.push(s)});
    py.setStderr({batched:s=>lines.push(s)});
    if(kind==="run"){
      await py.runPythonAsync(code);
      self.postMessage({id,ok:true,output:lines.join("\n") || "Exécution terminée (aucun affichage)."});
    } else if(kind==="decide"){
      // Fresh namespace per decision prevents stale functions from influencing behaviour.
      const globals=py.globals.get("dict")();
      try {
        await py.runPythonAsync(code,{globals});
        const f=globals.get("decider");
        if(!f) throw Error("Définissez une fonction decider(position, objectif, obstacles).");
        try {
          globals.set("__position",position);
          globals.set("__goal",goal);
          globals.set("__obstacles",obstacles);
          // Convert JavaScript arrays to genuine Python tuples for consistent comparisons.
          await py.runPythonAsync("__result = decider(tuple(__position), tuple(__goal), [tuple(p) for p in __obstacles])",{globals});
          const result=globals.get("__result");
          const action=result===null?null:String(result);
          if(result&&typeof result.destroy==="function")result.destroy();
          if(!["droite","gauche","haut","bas","arrêt",null].includes(action))throw Error("Action non reconnue : "+action);
          self.postMessage({id,ok:true,action,output:lines.join("\\n")});
        } finally {if(f.destroy)f.destroy();}

      } finally {globals.destroy();}
    } else throw Error("Commande inconnue");
  } catch(err) {self.postMessage({id,ok:false,error:String(err)});}
};