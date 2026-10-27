/* Pyodide en Worker : distribution locale prioritaire, CDN de secours.
 * Un Worker / une liste d'imports autorisés ne sécurise PAS un code hostile. */
const CDN='https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
const LOCAL=new URL('../pyodide/',self.location.href).href;
let pyodide=null;
async function boot(){
  let errors=[];
  for(const base of [LOCAL,CDN]){
    try{
      const response=await fetch(base+'pyodide.js',{method:'HEAD',cache:'no-store'});
      if(!response.ok)throw Error('Fichier Pyodide absent (HTTP '+response.status+')');
      importScripts(base+'pyodide.js');
      const python=await loadPyodide({indexURL:base});
      return python;
    }catch(error){errors.push(`${base===LOCAL?'Local':'CDN'} : ${String(error?.message||error).slice(0,130)}`)}
  }
  console.error('ORCHESTRA Pyodide :',errors.join(' / '));
  throw Error('Python ne peut pas démarrer. Le réseau bloque peut-être le téléchargement. Demande à ton enseignant d’installer Pyodide localement avec INSTALLER_PYODIDE.cmd.');
}
(async()=>{
 try{
  postMessage({type:'loading'});
  pyodide=await boot();
  for(const name of ['monde.py','runner.py']){
   const response=await fetch(name,{cache:'no-store'});
   if(!response.ok)throw Error('Le moteur Python est inaccessible : '+name+' (HTTP '+response.status+').');
   pyodide.FS.writeFile('/home/pyodide/'+name,await response.text());
  }
  pyodide.runPython("import sys\nsys.path.insert(0,'/home/pyodide')\nimport runner");
  postMessage({type:'ready'});
 }catch(error){postMessage({type:'error',stage:'load',message:String(error?.message||error)});}
})();
onmessage=async event=>{
 const {type,source,id}=event.data||{};
 if(type!=='run'||!pyodide)return;
 try{
   pyodide.globals.set('student_source',source);
   const value=await pyodide.runPythonAsync('runner.evaluate_source_json(student_source)');
   postMessage({type:'result',id,data:JSON.parse(value)});
 }catch(error){postMessage({type:'error',stage:'run',id,message:'Erreur du moteur Python : '+String(error?.message||error).slice(0,260)});}
};
