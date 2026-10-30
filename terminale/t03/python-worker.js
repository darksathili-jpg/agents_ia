/* T03 : seuls les résultats de runner_t03.py exécuté par Pyodide sont affichés.
 * Ne pas exécuter de code non fiable : le Worker n'est pas une sandbox. */
const LOCAL = new URL('../../pyodide/', self.location.href).href;
const CDN = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
const ALLOW_CDN_FALLBACK = true;
let python = null;
(async () => {
  const problems = [];
  for (const root of [LOCAL, ...(ALLOW_CDN_FALLBACK ? [CDN] : [])]) {
    try {
      const response = await fetch(root + 'pyodide.js', {method:'HEAD'});
      if (!response.ok) throw Error('Pyodide HTTP '+response.status);
      importScripts(root+'pyodide.js');
      python = await loadPyodide({indexURL:root});
      const runner = await fetch('runner_t03.py', {cache:'no-store'});
      if (!runner.ok) throw Error('runner_t03.py HTTP '+runner.status);
      python.FS.writeFile('/home/pyodide/runner_t03.py', await runner.text());
      python.runPython("import sys\nsys.path.insert(0,'/home/pyodide')\nimport runner_t03");
      postMessage({type:'ready', source:root===LOCAL?'local':'cdn'});
      return;
    } catch (error) {
      problems.push((root===LOCAL?'local':'CDN')+' : '+String(error.message||error));
    }
  }
  postMessage({type:'error', stage:'load', message:problems.join(' ; ')});
})();
onmessage = async ({data}) => {
  if (!data || data.type!=='run' || !python) return;
  try {
    python.globals.set('student_source', data.source);
    const result = await python.runPythonAsync('runner_t03.evaluate_source_json(student_source)');
    postMessage({type:'result',id:data.id,data:JSON.parse(result)});
  } catch (error) {
    postMessage({type:'error',stage:'run',id:data.id,message:String(error.message||error)});
  }
};
