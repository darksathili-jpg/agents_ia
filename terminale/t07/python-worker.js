/* T07 — résultats exclusivement produits par runner_t07.py dans Pyodide.
 * Ce Worker n'est pas une sandbox contre du code hostile. */
const LOCAL = new URL('../../pyodide/', self.location.href).href;
const CDN = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
const ALLOW_CDN_FALLBACK = true;
let python = null;
(async () => {
  const failures = [];
  for (const root of [LOCAL, ...(ALLOW_CDN_FALLBACK ? [CDN] : [])]) {
    try {
      const check = await fetch(root+'pyodide.js', {method:'HEAD'});
      if(!check.ok) throw Error('Pyodide HTTP '+check.status);
      importScripts(root+'pyodide.js');
      python = await loadPyodide({indexURL:root});
      const source = await fetch('runner_t07.py', {cache:'no-store'});
      if(!source.ok) throw Error('runner_t07.py HTTP '+source.status);
      python.FS.writeFile('/home/pyodide/runner_t07.py', await source.text());
      python.runPython("import sys\nsys.path.insert(0,'/home/pyodide')\nimport runner_t07");
      postMessage({type:'ready',source:root===LOCAL?'local':'cdn'});
      return;
    } catch(error) {
      failures.push((root===LOCAL?'Local':'CDN')+' : '+String(error.message||error));
    }
  }
  postMessage({type:'error',stage:'load',message:failures.join(' ; ')});
})();
onmessage = async ({data}) => {
  if(!data || data.type!=='run' || !python)return;
  try {
    python.globals.set('student_source',data.source);
    const seed=(self.crypto&&self.crypto.getRandomValues)?self.crypto.getRandomValues(new Uint32Array(1))[0]:1;
    python.globals.set('scenario_seed',seed);
    const result=await python.runPythonAsync('runner_t07.evaluate_source_json(student_source, scenario_seed)');
    postMessage({type:'result',id:data.id,data:JSON.parse(result)});
  } catch(error) {
    postMessage({type:'error',stage:'run',id:data.id,message:String(error.message||error)});
  }
};
