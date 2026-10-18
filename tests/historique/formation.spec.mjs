import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';

test('accueil vers module, séance complète et parcours enseignant',async({page})=>{
 await page.goto('/');await page.getByRole('link',{name:'Module 01',exact:true}).click();
 await expect(page.getByRole('heading',{level:1})).toContainText('Fondements');
 await expect(page.getByText('S04 · À venir')).toBeVisible();
 await page.getByRole('link',{name:'Suivre S01 →',exact:true}).click();
 await expect(page.locator('article>section')).toHaveCount(10);
 await expect(page.locator('#etape-4')).toContainText('Autonomie');
 await expect(page.locator('#etape-4')).toContainText('Chatbot de FAQ');
 await expect(page.locator('#etape-6')).toContainText('mur initial');
 await page.getByRole('link',{name:'Enseignants',exact:true}).click();
 await expect(page.locator('#formaliser')).toContainText('π');
 await expect(page.locator('#production')).toContainText('Deux commandes, un déplacement');
 await expect(page.locator('#correction')).toContainText('S01_CORRECTION_OK');
 await expect(page.locator('#references')).toContainText('Russell');
});

test('prédiction, trace réelle, saisie persistée et export',async({page})=>{
 await page.goto('/seance01.html');
 await page.locator('#compare-prediction').click();await expect(page.locator('#comparison')).toContainText('Écrivez');
 await page.locator('#prediction').fill('Droite deux fois, mais un déplacement seulement.');
 await page.locator('#compare-prediction').click();await expect(page.locator('#comparison')).toContainText('au moins une étape');
 const lab=page.frameLocator('#observation-lab');
 await lab.locator('#step').click();await lab.locator('#step').click();
 await expect(lab.locator('#position')).toHaveText('1,2');await expect(lab.locator('#state')).toHaveText('Bloqué');
 await page.locator('#compare-prediction').click();await expect(page.locator('#comparison')).toContainText('mouvement refusé');
 await page.locator('#reponse-2').fill('La commande est choisie, puis le moteur refuse le mur.');
 const download=page.waitForEvent('download');await page.locator('#export-notes').click();
 const file=await download;const data=JSON.parse(await readFile(await file.path(),'utf8'));
 expect(data.reponses['reponse-2']).toContain('refuse le mur');
 await page.reload();await expect(page.locator('#reponse-2')).toHaveValue(/refuse le mur/);
});

test('diagnostic et bilan argumenté : retours explicites, sans fausse certification',async({page})=>{
 await page.goto('/seance01.html');await page.locator('#diagnostic-check').click();
 await expect(page.locator('#diagnostic-feedback')).toContainText('None');
 await page.locator('#check-learning').click();await expect(page.locator('#learning-feedback')).toContainText('trois questions');
 await page.locator('[name=definition][value=b]').check();await page.locator('[name=transition][value=c]').check();await page.locator('[name=preuve][value=a]').check();
 await page.locator('#check-learning').click();await expect(page.locator('#learning-feedback')).toContainText('3/3');await expect(page.locator('#learning-feedback')).toContainText('Ajoutez');
 await page.locator('#bilan-raisonnement').fill('Sans LLM : règle sur les coordonnées. Test cible à gauche.');
 await page.locator('#check-learning').click();await expect(page.locator('#learning-feedback')).toContainText('pas évalué automatiquement');
});

test('atelier S01 : Python réel, modification, console distincte de grille, erreur, Stop et reprise',async({page})=>{
 test.setTimeout(120000);await page.goto('/seance01.html');
 await page.locator('#python-lab').scrollIntoViewIfNeeded();
 const lab=page.frameLocator('#python-lab');
 await lab.locator('#py-run').click();await expect(lab.locator('#py-output')).toContainText('(0, 2) arrêt',{timeout:25000});
 await expect(lab.locator('#position')).toHaveText('0,2');
 const solution=await readFile('docs/pedagogie/module-01/python/s01_solution_interface.py','utf8');
 await lab.locator('#code').fill(solution);await lab.locator('#py-run').click();
 await expect(lab.locator('#py-output')).toContainText('S01_CORRECTION_OK');
 await expect(lab.locator('#position')).toHaveText('0,2');
 await lab.locator('#policy').selectOption('python');await lab.locator('#step').click();await expect(lab.locator('#position')).toHaveText('1,2');
 await lab.locator('#step').click();await expect(lab.locator('#state')).toHaveText('Bloqué');
 await lab.locator('#code').fill('raise ValueError("S01_ERREUR")');await lab.locator('#py-run').click();await expect(lab.locator('#py-output')).toContainText('S01_ERREUR');
 await lab.locator('#code').fill('while True:\n    pass');await lab.locator('#py-run').click();await lab.locator('#py-stop').click();
 await expect(lab.locator('#py-output')).toHaveText('Exécution Python arrêtée.');
 await lab.locator('#py-reset').click();await expect(lab.locator('#code')).toHaveValue(/return "arrêt"/);
 await lab.locator('#code').fill('print("S01_REPRISE_OK")');await lab.locator('#py-run').click();await expect(lab.locator('#py-output')).toContainText('S01_REPRISE_OK',{timeout:25000});
});

for(const width of [390,768,1440])test(`formation : responsive, thèmes et clavier à ${width}px`,async({page})=>{
 await page.setViewportSize({width,height:900});
 for(const path of ['/module01.html','/seance01.html','/enseignant-s01.html']){
  await page.goto(path);await page.keyboard.press('Tab');await expect(page.locator('.skip')).toBeFocused();await page.keyboard.press('Enter');await expect(page.getByRole('main')).toBeFocused();
  for(const theme of ['light','dark','projector']){
   await page.locator('#formation-display').selectOption(theme);
   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${path}/${theme}`).toBe(true);
   if(theme==='projector'){
    expect(await page.locator('.sheet').first().evaluate(el=>getComputedStyle(el).backgroundColor.match(/\d+/g).slice(0,3).map(Number).every(v=>v>=230))).toBe(true);
    expect(await page.locator('body').evaluate(el=>parseFloat(getComputedStyle(el).fontSize))).toBeGreaterThanOrEqual(20);
   }
  }
 }
});

test('GitHub Pages : parcours, documents HTML et ressources sous préfixe',async({page,baseURL})=>{
 const errors=[];page.on('response',r=>{if(r.url().startsWith(baseURL)&&r.status()>=400)errors.push(r.url())});
 await page.route('**/agents_ia/**',async route=>{
  const response=await route.fetch({url:route.request().url().replace('/agents_ia/','/')});
  const body=await response.body();await route.fulfill({status:response.status(),headers:response.headers(),body});
 });
 await page.goto('/agents_ia/module01.html');await page.getByRole('link',{name:'Lire les documents S02 →'}).click();
 await expect(page).toHaveURL(/agents_ia\/ressources-module01.html#seance_02$/);await expect(page.locator('#seance_02')).toContainText('Environnement');
 await page.goto('/agents_ia/seance01.html');
 const lab=page.frameLocator('#observation-lab');await lab.locator('#step').click();await expect(lab.locator('#position')).toHaveText('1,2');
 await page.getByRole('link',{name:'Enseignants',exact:true}).click();await expect(page).toHaveURL(/agents_ia\/enseignant-s01.html$/);
 await page.evaluate(()=>document.fonts.ready);await page.unrouteAll({behavior:'wait'});
 expect(errors).toEqual([]);
});

test('contrôles de la séance au clavier, exécution auto, pause et réinitialisation',async({page})=>{
 await page.goto('/seance01.html');
 const diagnostic=page.locator('#diagnostic-check');await diagnostic.focus();await page.keyboard.press('Enter');
 await expect(page.locator('#diagnostic-feedback')).toContainText('Attendus');
 await page.locator('#observation-lab').scrollIntoViewIfNeeded();const lab=page.frameLocator('#observation-lab');
 await lab.locator('#run').focus();await page.keyboard.press('Enter');await expect(lab.locator('#steps')).toHaveText('1');
 await lab.locator('#run').click();await expect(lab.locator('#run')).toHaveText('▶ Exécution auto');
 await lab.locator('#reset').focus();await page.keyboard.press('Enter');await expect(lab.locator('#position')).toHaveText('0,2');await expect(lab.locator('#steps')).toHaveText('0');
 const hints=page.locator('#etape-5 summary');await hints.focus();await page.keyboard.press('Enter');await expect(page.locator('#etape-5 details')).toHaveAttribute('open','');
});

test('projection de l’atelier : code et console clairs, lisibles et sans débordement',async({page})=>{
 await page.goto('/seance01.html');await page.locator('#python-lab').scrollIntoViewIfNeeded();const lab=page.frameLocator('#python-lab');
 await lab.locator('#code').waitFor();await page.locator('#formation-display').selectOption('projector');
 await expect(lab.locator('body')).toHaveClass(/projector/);
 for(const width of [390,768,1440]){
  await page.setViewportSize({width,height:900});
  expect(await lab.locator('html').evaluate(el=>el.scrollWidth<=innerWidth)).toBe(true);
 }
 for(const selector of ['#code','#py-output','#log']){
  const metrics=await lab.locator(selector).evaluate(el=>{
   const s=getComputedStyle(el),rgb=v=>v.match(/[\d.]+/g).slice(0,3).map(Number);
   const lum=arr=>arr.map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
   const bg=rgb(s.backgroundColor),a=lum(bg),b=lum(rgb(s.color));
   return {background:bg,size:parseFloat(s.fontSize),contrast:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
  });
  expect(metrics.background.every(v=>v>=230)).toBe(true);expect(metrics.size).toBeGreaterThanOrEqual(20);expect(metrics.contrast).toBeGreaterThanOrEqual(4.5);
 }
});
