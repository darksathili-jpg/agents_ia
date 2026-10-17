import {createServer} from 'node:http';
import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {resolve, extname, sep} from 'node:path';
import {chromium} from '@playwright/test';

// Static, local-only visual review. Each run owns and closes its server.
const phase=process.argv[2];
if(!['avant','apres'].includes(phase))throw Error('Usage: node scripts/capture-art.mjs avant|apres');
const root=resolve('.');
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.svg':'image/svg+xml','.ttf':'font/ttf'};
const server=createServer(async(req,res)=>{
 try{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const file=resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
  if(!file.startsWith(root+sep))throw Error('Invalid path');
  res.setHeader('Content-Type',types[extname(file)]||'application/octet-stream');
  res.end(await readFile(file));
 }catch{res.writeHead(404);res.end();}
});
await new Promise(done=>server.listen(0,'127.0.0.1',done));
const base=`http://127.0.0.1:${server.address().port}`;
const dir=`docs/art/captures/v2/${phase}`;
await mkdir(dir,{recursive:true});
let browser;
try{
 browser=await chromium.launch();
 const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 for(const mode of ['light','dark','projector']){
  await page.goto(base);await page.locator('#home-display').selectOption(mode);await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:`${dir}/accueil-${mode}.png`,fullPage:true});
  if(mode==='light'){
   await page.locator('.intro').screenshot({path:`${dir}/microduck-bienvenue.png`});
   await page.locator('#laboratoire').screenshot({path:`${dir}/microduck-mission.png`});
   await page.locator('#parcours').screenshot({path:`${dir}/parcours.png`});
   await page.locator('.method').screenshot({path:`${dir}/methode.png`});
  }
 }
 await page.goto(`${base}/laboratoire.html`);await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:`${dir}/laboratoire-projector.png`,fullPage:true});
 await page.goto(base);await page.locator('#home-display').selectOption('light');
 for(const width of [390,768]){
  await page.setViewportSize({width,height:900});await page.screenshot({path:`${dir}/accueil-${width}.png`,fullPage:true});
  if(width===390)await page.locator('.intro').screenshot({path:`${dir}/microduck-mobile.png`});
 }
 console.log(`11 captures : ${dir}`);
 if(phase==='apres'){
  const subjects=[['accueil-light','Accueil clair'],['accueil-dark','Accueil sombre'],['accueil-projector','Accueil vidéoprojecteur'],['accueil-390','Mobile 390 px'],['accueil-768','Tablette 768 px'],['microduck-bienvenue','Microduck — bienvenue'],['microduck-mission','Microduck — mission'],['parcours','Parcours pédagogique'],['methode','Apprendre avec méthode'],['laboratoire-projector','Laboratoire vidéoprojecteur']];
  await writeFile('docs/art/captures/v2/index.html',`<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Agent Academy — Comparaison V1 / V2</title><style>body{font:17px/1.6 system-ui;background:#fff8ef;color:#1f2a44;max-width:1500px;margin:auto;padding:24px}h1{font-size:28px}details{border-top:1px solid #65748d;padding:18px 0}summary{font-weight:700;cursor:pointer}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}figure{margin:20px 0}img{width:100%;height:auto;border:1px solid #65748d}a{color:#254d94}@media(max-width:700px){.pair{grid-template-columns:1fr}}</style><h1>Agent Academy — Revue artistique V2</h1><p>Captures à 1440 px, sauf mobile et tablette. Animations réduites pour une comparaison stable. Cliquer sur une image ouvre sa résolution originale.</p>${subjects.map(([file,label])=>`<details ${file.startsWith('microduck')?'open':''}><summary>${label}</summary><div class="pair">${[['avant','Avant — V1'],['apres','Après — V2']].map(([folder,caption])=>`<figure><figcaption>${caption}</figcaption><a href="${folder}/${file}.png"><img loading="lazy" src="${folder}/${file}.png" alt="${label} : ${caption}"></a></figure>`).join('')}</div></details>`).join('')}</html>`);
 }
}finally{await browser?.close();server.close();}
