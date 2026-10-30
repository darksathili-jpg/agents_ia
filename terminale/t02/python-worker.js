/* ORCHESTRA T02 : le résultat n'est produit que par runner_t02.py exécuté dans Pyodide.
 * Le Worker n'est pas un environnement sûr contre du code Python hostile. */
const LOCAL = new URL('../../pyodide/', self.location.href).href;
const CDN = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
const ALLOW_CDN_FALLBACK = true;
let python = null;
async function boot() {
  for (const root of [LOCAL, ...(ALLOW_CDN_FALLBACK ? [CDN] : [])]) {
    try {
      const check = await fetch(root + 'pyodide.js', {method:'HEAD'});
      if (!check.ok) throw Error('Pyodide HTTP ' + check.status);
      importScripts(root + 'pyodide.js');
      python = await loadPyodide({indexURL:root});
      const response = await fetch('runner_t02.py', {cache:'no-store'});
      if (!response.ok) throw Error('runner_t02.py HTTP ' + response.status);
      python.FS.writeFile('/home/pyodide/runner_t02.py', await response.text());
      python.runPython("import sys\nsys.path.insert(0,'/home/pyodide')\nimport runner_t02");
      postMessage({type:'ready', source:root===LOCAL?'local':'cdn'});
      return;
    } catch (e) {
      if (root === CDN || !ALLOW_CDN_FALLBACK) throw e;
    }
  }
}
(async () => {try {await boot();} catch(e) {postMessage({type:'error', stage:'load', message:String(e?.message||e)});}})();
onmessage = async ({data}) => {
  if (!data || data.type !== 'run' || !python) return;
  try {
    python.globals.set('student_source', data.source);
    const seed = (self.crypto && self.crypto.getRandomValues)
      ? self.crypto.getRandomValues(new Uint32Array(1))[0] : 0;
    python.globals.set('scenario_seed', seed || 1);
    const json = await python.runPythonAsync('runner_t02.evaluate_source_json(student_source, scenario_seed)');
    postMessage({type:'result', id:data.id, data:JSON.parse(json)});
  } catch(e) {
    postMessage({type:'error', stage:'run', id:data.id, message:String(e?.message||e)});
  }
};