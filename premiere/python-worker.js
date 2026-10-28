/* Exécute le moteur Python et le code élève dans Pyodide, hors du fil UI.
 * Un Web Worker n'est PAS une frontière de sécurité contre du code hostile.
 * L'interface détruit le Worker en cas de blocage ou de réinitialisation. */
const ALLOW_CDN_FALLBACK = true;
const BASE = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
const LOCAL = new URL('../pyodide/',self.location.href).href;
let pyodide = null;
async function boot() {
  for (const base of [LOCAL, ...(ALLOW_CDN_FALLBACK ? [BASE] : [])]) {
    try {
      const response = await fetch(base+'pyodide.js',{method:'HEAD',cache:'no-store'});
      if (!response.ok) throw Error('Pyodide absent');
      importScripts(base+'pyodide.js');
      return await loadPyodide({indexURL:base});
    } catch(error) { console.warn('Pyodide non disponible depuis',base,error); }
  }
  throw Error('Python ne peut pas démarrer. Vérifie la connexion ou demande une installation locale de Pyodide à ton enseignant.');
}
(async () => {
  try {
    postMessage({type: 'loading', text: 'Préparation du moteur Python…'});
    pyodide = await boot();
    const response = await fetch('engine.py', {cache: 'no-store'});
    if (!response.ok) throw new Error(`Moteur Python absent : HTTP ${response.status}`);
    pyodide.FS.writeFile('/home/pyodide/engine.py', await response.text());
    pyodide.runPython("import sys\nsys.path.insert(0, '/home/pyodide')\nimport engine");
    postMessage({type: 'ready'});
  } catch (error) {
    postMessage({type: 'error', stage: 'load', text: String(error?.message || error)});
  }
})();
onmessage = async event => {
  const {type, source, id} = event.data || {};
  if (type !== 'run' || !pyodide) return;
  try {
    pyodide.globals.set('student_source', source);
    const raw = await pyodide.runPythonAsync('engine.evaluate_source_json(student_source)');
    postMessage({type: 'result', id, data: JSON.parse(raw)});
  } catch (error) {
    postMessage({type: 'error', stage: 'run', id, text: String(error?.message || error)});
  }
};
