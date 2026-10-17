// Vérification des supports via le laboratoire existant, sans le modifier.
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {chromium} from '@playwright/test';
const root=process.cwd();
const dir=resolve(root,'docs/pedagogie/module-01/python');
const source=await readFile(resolve(dir,'corriges.py'),'utf8');
const tests=await readFile(resolve(dir,'tests_experiences.py'),'utf8');
const serveur=createServer(async(req,res)=>{
 try{
  const path=resolve(root,'.'+new URL(req.url,'http://localhost').pathname);
  if(!path.startsWith(root+sep))throw Error();
  const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.ttf':'font/ttf','.png':'image/png'};
  res.setHeader('Content-Type',mime[extname(path)]||'application/octet-stream');
  res.end(await readFile(path));
 }catch{res.writeHead(404);res.end();}
});
await new Promise(done=>serveur.listen(0,'127.0.0.1',done));
let browser;
try{
 browser=await chromium.launch();
 const page=await browser.newPage();
 await page.goto(`http://127.0.0.1:${serveur.address().port}/laboratoire.html`);
 async function executer(code,attendu){
  await page.locator('#code').fill(code);await page.locator('#py-run').click();
  await page.waitForFunction(text=>document.querySelector('#py-output').textContent.includes(text),attendu,{timeout:25000});
  console.log(attendu);
 }
 for(let numero=1;numero<=5;numero++){
  const id=String(numero).padStart(2,'0');
  const depart=await readFile(resolve(dir,`tp${id}_depart.py`),'utf8');
  await executer(depart,numero===1?'DEPART_TP01_OK':`A_COMPLETER_TP${id}`);
 }
 const code=`import sys, types\nmodule = types.ModuleType("corriges")\nexec(${JSON.stringify(source)}, module.__dict__)\nsys.modules["corriges"] = module\nexec(${JSON.stringify(tests)})`;
 await executer(code,'SUPPORTS_MODULE01_OK 9');
 // Les démonstrations imprimées sont exécutées aussi, pas seulement importées.
 await executer(source+'\nprint("DEMONSTRATIONS_PYODIDE_OK")','DEMONSTRATIONS_PYODIDE_OK');
 console.log('Pyodide réel : 5 départs, 9 tests et démonstrations TP01–05 réussis.');
 const modules=['s01_diagnostic','s02_corrige','s02_observation_masquee'];
 let montage='import sys, types\n';
 for(const nom of modules){
  const contenu=await readFile(resolve(dir,nom+'.py'),'utf8');
  montage+=`module = types.ModuleType(${JSON.stringify(nom)})\nexec(${JSON.stringify(contenu)}, module.__dict__)\nsys.modules[${JSON.stringify(nom)}] = module\n`;
 }
 const testsJalon=await readFile(resolve(dir,'tests_s01_s02.py'),'utf8');
 await executer(montage+`exec(${JSON.stringify(testsJalon)})`,'TESTS_S01_S02_OK 7');
 for(const [nom,marqueur] of [['s01_diagnostic','DIAGNOSTIC_S01_OK'],['s02_obstacle_depart','A_COMPLETER_S02'],['s02_observation_masquee','OBSERVATION_MASQUEE_S02_OK'],['s02_corrige','CORRIGE_S02_OK']]){
  await executer(await readFile(resolve(dir,nom+'.py'),'utf8'),marqueur);
 }
 console.log('Jalon S01.1/S02 : 7 tests et 4 scripts exécutés dans Pyodide réel.');
}finally{await browser?.close();serveur.close();}
