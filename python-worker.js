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
        const result=f(position,goal,obstacles);
        const action=result===null?null:String(result);
        if(result&&typeof result.destroy==="function")result.destroy();
        if(f.destroy)f.destroy();
        if(!["droite","gauche","haut","bas","arrêt",null].includes(action))throw Error("Action non reconnue : "+action);
        self.postMessage({id,ok:true,action,output:lines.join("\n")});
      } finally {globals.destroy();}
    } else throw Error("Commande inconnue");
  } catch(err) {self.postMessage({id,ok:false,error:String(err)});}
};