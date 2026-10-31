/* T04 — résultats exclusivement produits par runner_t04.py dans Pyodide.
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
      const source = await fetch('runner_t04.py', {cache:'no-store'});
      if(!source.ok) throw Error('runner_t04.py HTTP '+source.status);
      python.FS.writeFile('/home/pyodide/runner_t04.py', await source.text());
      python.runPython("import sys\nsys.path.insert(0,'/home/pyodide')\nimport runner_t04");
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
    const result=await python.runPythonAsync('runner_t04.evaluate_source_json(student_source)');
    postMessage({type:'result',id:data.id,data:JSON.parse(result)});
  } catch(error) {
    postMessage({type:'error',stage:'run',id:data.id,message:String(error.message||error)});
  }
};
