// Captures locales reproductibles ; ce script possède et ferme son serveur.
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {chromium} from '@playwright/test';
const root=process.cwd(),dir='docs/visualisation-s01/captures';
const server=createServer(async(req,res)=>{
 try{
  let path=new URL(req.url,'http://localhost').pathname;if(path.endsWith('/'))path+='index.html';
  const file=resolve(root,'.'+decodeURIComponent(path));if(!file.startsWith(root+sep))throw Error('Path');
  const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png','.ttf':'font/ttf'};
  res.setHeader('Content-Type',mime[extname(file)]||'application/octet-stream');res.end(await readFile(file));
 }catch{res.writeHead(404);res.end();}
});
await new Promise(done=>server.listen(0,'127.0.0.1',done));
const base=`http://127.0.0.1:${server.address().port}`;
await mkdir(dir,{recursive:true});let browser;
try{
 browser=await chromium.launch();const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const shots=[];
 async function shot(name,caption,fullPage=false,locator=null){
  await page.evaluate(()=>document.fonts.ready);
  if(locator)await page.locator(locator).screenshot({path:`${dir}/${name}.png`});
  else await page.screenshot({path:`${dir}/${name}.png`,fullPage});
  shots.push([name,caption]);
 }
 await page.goto(base+'/module01.html');await shot('01-module','1. Ouvrir le module : S01 intégrée, S02/S03 documentaires, S04/S05 à venir.',true);
 await page.getByRole('link',{name:'Suivre S01 →',exact:true}).click();
 await page.locator('#formation-display').selectOption('light');
 await shot('02-seance-entree','2. Commencer : prérequis, réponses locales et fil de séance.');
 // Charger aussi les deux cadres à chargement différé avant la capture complète.
 await page.locator('#python-lab').scrollIntoViewIfNeeded();
 await page.frameLocator('#python-lab').locator('#code').waitFor();
 await page.locator('#observation-lab').scrollIntoViewIfNeeded();
 await page.frameLocator('#observation-lab').locator('#grid').waitFor();
 await page.locator('#prediction').fill('Deux commandes droite, un seul déplacement accepté.');
 const observe=page.frameLocator('#observation-lab');await observe.locator('#step').click();await observe.locator('#step').click();
 await page.locator('#compare-prediction').click();
 await shot('03-experience','3. Prédire, exécuter deux décisions et confronter au refus réellement journalisé.',false,'#etape-2');
 const lab=page.frameLocator('#python-lab');
 await lab.locator('#code').fill(await readFile('docs/pedagogie/module-01/python/s01_solution_interface.py','utf8'));
 await lab.locator('#py-run').click();
 await lab.locator('#py-output').filter({hasText:'S01_CORRECTION_OK'}).waitFor({timeout:25000});
 await lab.locator('#policy').selectOption('python');await lab.locator('#step').click();await lab.locator('#step').click();
 await shot('04-atelier','4. Modifier le vrai Python, vérifier les assertions en console, puis essayer la politique sur la grille.',false,'#etape-5');
 await page.locator('#bilan-raisonnement').fill('La commande reste droite ; le moteur refuse le mur. Un test avec cible à gauche départage deux hypothèses.');
 for(const [name,value] of [['definition','b'],['transition','c'],['preuve','a']])await page.locator(`[name=${name}][value=${value}]`).check();
 await page.locator('#check-learning').click();await shot('05-bilan','5. Justifier et proposer un test ; les réponses libres restent à discuter avec l’enseignant.',false,'#etape-8');
 await page.evaluate(()=>scrollTo(0,0));await shot('seance-complete-light','Leçon S01 complète, du diagnostic à la synthèse et aux adaptations.',true);
 await page.goto(base+'/enseignant-s01.html');await shot('06-enseignant','6. Préparer le cours avec un parcours distinct : formalisation, preuves, transposition et corrigés.');
 await shot('enseignant-complet','Parcours enseignant complet, références comprises.',true);
 await page.locator('#formaliser').scrollIntoViewIfNeeded();await shot('enseignant-formalisation','Définitions et problèmes : frontière, transition et critère.',false,'#formaliser');
 await page.goto(base+'/seance01.html');await page.locator('#formation-display').selectOption('dark');await shot('seance-dark','Lecture sombre : mêmes contenus et navigation.');
 await page.locator('#formation-display').selectOption('projector');await shot('seance-projector','Projection : papier clair et typographie agrandie.');
 await page.setViewportSize({width:390,height:900});await page.locator('#formation-display').selectOption('light');await shot('seance-mobile','Mobile 390 px : fil de séance et lecture sur une colonne.');
 await writeFile('docs/visualisation-s01/index.html',`<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Démonstration S01 — Agent Academy</title><style>body{font:18px/1.6 system-ui;max-width:1100px;margin:auto;padding:24px;background:#fff8ef;color:#1f2a44}img{width:100%;border:1px solid #65748d}figure{margin:35px 0}figcaption{font-weight:700;margin-bottom:12px}a{color:#254d94}</style><h1>Parcours S01 — démonstration commentée</h1><p>Captures Chromium à 1440 × 1000, sauf mobile 390 × 900. Python exécuté par le véritable Pyodide. Les images complètes s’ouvrent en résolution originale.</p><p><a href="../../module01.html">Ouvrir le module local</a> · <a href="BILAN.md">Bilan des vérifications</a></p>${shots.map(([name,caption])=>`<figure><figcaption>${caption}</figcaption><a href="captures/${name}.png"><img loading="lazy" src="captures/${name}.png" alt="${caption}"></a></figure>`).join('')}</html>`);
 console.log(`CAPTURES_S01_OK : ${shots.length} images et séquence commentée dans docs/visualisation-s01/index.html`);
}finally{await browser?.close();server.close();}
