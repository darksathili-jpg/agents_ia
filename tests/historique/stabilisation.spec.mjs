import {test,expect} from '@playwright/test';

test('repères sémantiques et aller-retour entièrement au clavier',async({page})=>{
 for(const path of ['/','/laboratoire.html']){
  await page.goto(path);
  await expect(page.locator('html')).toHaveAttribute('lang','fr');
  await expect(page.getByRole('heading',{level:1})).toHaveCount(1);
  await expect(page.getByRole('main')).toHaveCount(1);
  await expect(page.getByRole('banner')).toHaveCount(1);
  await expect(page.getByRole('contentinfo')).toHaveCount(1);
  await page.keyboard.press('Tab');
  await expect(page.locator('.skip')).toBeFocused();
  await page.keyboard.press('Enter');
 }
 await expect(page.getByRole('main')).toBeFocused();
 await expect(page.getByRole('textbox',{name:'Éditeur Python'})).toBeVisible();
 await expect(page.getByRole('radiogroup')).toHaveAccessibleName(/robot choisit/);
 // Keyboard activation of navigation links, without mouse clicks.
 const back=page.getByRole('link',{name:/Retour au carnet/});
 await back.focus();await page.keyboard.press('Enter');await expect(page).toHaveURL(/\/$/);
 const start=page.getByRole('link',{name:/Commencer/});
 await start.focus();await page.keyboard.press('Enter');await expect(page).toHaveURL(/laboratoire.html$/);
});

test('ressources et navigation sous le préfixe GitHub Pages',async({page,baseURL})=>{
 const failures=[];
 page.on('response',response=>{if(response.url().startsWith(baseURL)&&response.status()>=400)failures.push(response.url());});
 page.on('requestfailed',request=>{if(request.url().startsWith(baseURL))failures.push(request.url());});
 await page.route('**/agents_ia/**',async route=>{
  const url=route.request().url().replace('/agents_ia/','/');
  await route.fulfill({response:await route.fetch({url})});
 });
 await page.goto('/agents_ia/');await page.evaluate(()=>document.fonts.ready);
 await page.getByRole('link',{name:/Commencer/}).click();
 await expect(page).toHaveURL(/\/agents_ia\/laboratoire.html$/);
 // Creation of a real Worker resolves its URL against the nested page.
 const workerPromise=page.waitForEvent('worker');
 await page.locator('#py-run').click();const worker=await workerPromise;
 expect(worker.url()).toBe(`${baseURL}/agents_ia/python-worker.js`);
 await page.locator('#py-stop').click();
 await page.getByRole('link',{name:/Retour au carnet/}).click();await expect(page).toHaveURL(/\/agents_ia\/$/);
 await page.getByRole('link',{name:'Le parcours',exact:true}).click();await expect(page).toHaveURL(/\/agents_ia\/#parcours$/);
 expect(failures).toEqual([]);
});

test('Pyodide réel : BFS complet, erreur, interruption effective et reprise',async({page})=>{
 test.setTimeout(120000);
 await page.goto('/laboratoire.html');
 await page.locator('#py-run').click();
 await expect(page.locator('#py-status')).toHaveText('Python prêt',{timeout:20000});
 await page.locator('#policy').selectOption('python');
 for(let i=0;i<35;i++){
  if(await page.locator('#state').textContent()==='Objectif atteint')break;
  await page.locator('#step').click();
  await expect(page.locator('#steps')).toHaveText(String(i+1));
 }
 await expect(page.locator('#state')).toHaveText('Objectif atteint');
 await expect(page.locator('#position')).toHaveText('6,2');
 await page.locator('#code').fill('raise ValueError("ERREUR_CONTROLEE")');await page.locator('#py-run').click();
 await expect(page.locator('#py-output')).toContainText('ERREUR_CONTROLEE');
 const worker=page.workers()[0];
 await page.locator('#code').fill('while True:\n    pass');await page.locator('#py-run').click();
 await expect(page.locator('#py-status')).toHaveText('Exécution isolée…');
 // A queued evaluation cannot complete while the Python loop monopolises this Worker.
 const pending=worker.evaluate('1+1').catch(()=>null);
 const closed=new Promise(resolve=>worker.once('close',resolve));
 await page.locator('#py-stop').click();await closed;await pending;
 await expect(page.locator('#py-output')).toHaveText('Exécution Python arrêtée.');
 await expect(page.locator('#py-run')).toBeEnabled();
 await page.locator('#code').fill('print("REPRISE_REELLE_OK")');await page.locator('#py-run').click();
 await expect(page.locator('#py-output')).toContainText('REPRISE_REELLE_OK',{timeout:20000});
});
