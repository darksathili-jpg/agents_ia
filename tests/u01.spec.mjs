import {test,expect} from '@playwright/test';
import {readFile,mkdir} from 'node:fs/promises';
const captures='docs/integration-u01/captures';
test.beforeAll(()=>mkdir(captures,{recursive:true}));

test('accueil, module et anciens favoris donnent accès uniquement à U01.1',async({page})=>{
 await page.goto('/');await page.getByRole('link',{name:/Commencer U01.1/}).click();
 await expect(page).toHaveURL(/u01.html$/);await expect(page.locator('h1')).toHaveText('Commander n’est pas déplacer');
 await page.goto('/module01.html');await expect(page.getByRole('link',{name:/Commencer U01.1/})).toBeVisible();
 await expect(page.locator('body')).not.toContainText('S01');
 for(const [old,destination] of [['seance01.html','u01.html'],['enseignant-s01.html','enseignant-u01.html'],['ressources-module01.html','enseignant-u01.html']]){
  await page.goto('/'+old);await expect(page).toHaveURL(new RegExp('/'+destination+'$'));
  await expect(page.locator('body')).not.toContainText('S01_CORRECTION_OK');
  await expect(page.locator('body')).not.toContainText('Qu’est-ce qu’un agent intelligent ?');
 }
});

test('deux étapes au clavier : moteur réel, mur, arrêt puis réinitialisation',async({page})=>{
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/u01.html#essai');const lab=page.frameLocator('#u01-lab');
 await expect(lab.locator('#position')).toHaveText('0,2');await expect(lab.locator('#steps')).toHaveText('0');
 await expect(lab.locator('#policy option')).toHaveCount(1);
 await lab.locator('#step').focus();await page.keyboard.press('Enter');
 await expect(lab.locator('#position')).toHaveText('1,2');await expect(lab.locator('#steps')).toHaveText('1');
 await expect(lab.locator('#log')).toContainText('0,2 → droite → 1,2');
 await page.keyboard.press('Enter');await expect(lab.locator('#state')).toHaveText('Bloqué');
 await expect(lab.locator('#position')).toHaveText('1,2');await expect(lab.locator('#steps')).toHaveText('2');
 await expect(lab.locator('#log')).toContainText('1,2 → droite · obstacle : mouvement refusé');
 await expect(lab.locator('#step')).toBeDisabled();await expect(lab.locator('#run')).toBeHidden();
 await lab.locator('#reset').focus();await page.keyboard.press('Enter');
 await expect(lab.locator('#position')).toHaveText('0,2');await expect(lab.locator('#steps')).toHaveText('0');
 expect(errors).toEqual([]);
});

test('parcours complet : prédictions, explication différée, A1, Nora, curseur et prolongements séparés',async({page})=>{
 await page.goto('/u01.html');await expect(page.locator('#contexte')).toBeVisible();
 await expect(page.locator('#comprendre')).toBeHidden();
 await expect(page.locator('#contexte')).toContainText('La commande droite demande d’aller sur la case immédiatement à droite');
 await page.locator('#contexte .action-link').click();await expect(page.locator('#essai')).toBeFocused();
 for(const key of ['P1-justification','P2','E2','E3'])await expect(page.locator('#'+key)).toBeVisible();
 await expect(page.locator('#essai')).toContainText('Sans réinitialiser');
 await page.locator('#essai .action-link').click();await expect(page.locator('#comprendre')).toContainText('deux commandes, mais un seul déplacement');
 await page.locator('#comprendre .action-link').click();await expect(page.locator('#entrainement')).toContainText('indépendants');
 await page.locator('#entrainement .action-link').click();await expect(page.locator('#nora')).toContainText('Elle ne s’ouvre pas automatiquement');
 await expect(page.locator('#nora table textarea')).toHaveCount(4);
 await page.locator('#nora .action-link').click();await expect(page.locator('#curseur')).toContainText('le curseur ne revient pas automatiquement au début');
 await expect(page.locator('#curseur table textarea')).toHaveCount(6);
 await page.locator('#curseur .action-link').click();await expect(page.locator('#suite details')).not.toHaveAttribute('open','');
 await page.locator('#suite summary').press('Enter');await expect(page.locator('#suite')).toContainText('Maya affirme');
 await expect(page.locator('#suite')).toContainText('B1');
});

test('réponses isolées de S01, persistence locale et export fidèle sans notation',async({page})=>{
 await page.goto('/u01.html#nora');await page.evaluate(()=>localStorage.setItem('academy-s01:reponse-2','ANCIENNE REPONSE'));
 await page.locator('#T2').fill('Réponse construite pour le test technique.');
 await page.locator('#nora-ligne1-col5').fill('hall');
 await page.reload();await expect(page.locator('#T2')).toHaveValue('Réponse construite pour le test technique.');
 const download=page.waitForEvent('download');await page.locator('#export-notes').click();
 const file=await download;const data=JSON.parse(await readFile(await file.path(),'utf8'));
 expect(data.unite).toBe('U01.1');expect(data.reponses.T2).toContain('test technique');
 expect(data.reponses['nora-ligne1-col5']).toBe('hall');expect(JSON.stringify(data)).not.toContain('ANCIENNE REPONSE');
 expect(data.score).toBeUndefined();
});

test('préparation enseignante intégrale, symboles expliqués, corrigés repliés',async({page})=>{
 await page.goto('/enseignant-u01.html');
 await expect(page.locator('#preparation')).toContainText('aucune connaissance préalable de la théorie des agents');
 for(const text of ['La première composante','des quatre états possibles','Une valeur hors de ces listes déclenche','Les quatre lignes sont des appels indépendants','J4','Poole','réponse initialement autonome']){
  await expect(page.locator('main')).toContainText(text);
 }
 await expect(page.locator('#corriges details')).not.toHaveAttribute('open','');
 await page.locator('#corriges summary').press('Enter');await expect(page.locator('#corriges')).toContainText('J4');
 await expect(page.locator('#evaluation')).toContainText('non observable');
});

for(const theme of ['light','dark','projector'])test(`affichage réel ${theme}, focus et capture du laboratoire`,async({page})=>{
 await page.setViewportSize({width:1440,height:1000});await page.goto('/u01.html');
 await page.locator('#formation-display').selectOption(theme);
 await page.screenshot({path:`${captures}/eleve-${theme}.png`,fullPage:true});
 await page.locator('.unit-toc a[href="#essai"]').click();
 const lab=page.frameLocator('#u01-lab');await expect(lab.locator('body')).toHaveClass(new RegExp(theme));
 await lab.locator('#step').click();await lab.locator('#step').click();
 await page.locator('#experience').scrollIntoViewIfNeeded();
 await page.screenshot({path:`${captures}/experience-${theme}.png`});
 await lab.locator('#reset').focus();
 expect(await lab.locator('#reset').evaluate(e=>parseFloat(getComputedStyle(e).outlineWidth))).toBeGreaterThanOrEqual(3);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 if(theme==='projector'){
  expect(await lab.locator('#log').evaluate(e=>parseFloat(getComputedStyle(e).fontSize))).toBeGreaterThanOrEqual(20);
 }
 await page.getByRole('link',{name:'Parcours enseignant',exact:true}).click();
 await expect(page.locator('body')).toHaveClass(new RegExp(theme));
 await page.locator('#python').scrollIntoViewIfNeeded();await page.screenshot({path:`${captures}/enseignant-${theme}.png`});
});

for(const width of [390,768])test(`lecture mobile ${width}, table accessible et clavier`,async({page})=>{
 await page.setViewportSize({width,height:900});await page.goto('/u01.html');
 await page.keyboard.press('Tab');await expect(page.locator('.skip')).toBeFocused();await page.keyboard.press('Enter');
 for(const key of ['contexte','essai','entrainement','nora','curseur']){
  await page.locator(`.unit-toc a[href="#${key}"]`).click();
  await expect(page.locator('#'+key)).toBeVisible();
  await expect(page.locator('#'+key)).toBeFocused();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 }
 await page.locator('#curseur .table-scroll').focus();await expect(page.locator('#curseur .table-scroll')).toBeFocused();
 await page.screenshot({path:`${captures}/curseur-mobile-${width}.png`,fullPage:true});
});

test('chemins relatifs sous /agents_ia/, grille et Worker du même sous-dossier',async({page})=>{
 await page.route('**/agents_ia/**',async route=>{
  const response=await route.fetch({url:route.request().url().replace('/agents_ia/','/')});
  await route.fulfill({response});
 });
 await page.goto('/agents_ia/u01.html#essai');
 const lab=page.frameLocator('#u01-lab');await lab.locator('#step').click();await lab.locator('#step').click();
 await expect(lab.locator('#steps')).toHaveText('2');
 await page.getByRole('link',{name:'Parcours enseignant',exact:true}).click();
 await expect(page).toHaveURL(/\/agents_ia\/enseignant-u01.html$/);
 await page.goto('/agents_ia/laboratoire.html?u01=python');
 const worker=page.waitForEvent('worker');await page.locator('#py-run').click();
 expect((await worker).url()).toContain('/agents_ia/python-worker.js');await page.locator('#py-stop').click();
});

test('Nora et curseur affichés sans corrigé ni extension prématurée',async({page})=>{
 for(const key of ['nora','curseur']){
  await page.goto('/u01.html#'+key);await expect(page.locator('#suite')).toBeHidden();
  await page.screenshot({path:`${captures}/${key}.png`,fullPage:true});
 }
});

test('Python réel de la porte : quatre sorties, erreur, interruption et reprise',async({page})=>{
 test.setTimeout(120000);
 await page.goto('/laboratoire.html?u01=python');
 await page.locator('#py-run').click();await expect(page.locator('#py-status')).toHaveText('Python prêt',{timeout:45000});
 const output=await page.locator('#py-output').textContent();
 expect(output.trim().split('\n')).toHaveLength(4);
 expect(output).toContain("('hall', 'fermée') AVANCER -> ('hall', 'fermée')");
 expect(output).toContain("('hall', 'ouverte') AVANCER -> ('bureau', 'ouverte')");
 expect(output).toContain("('bureau', 'fermée') AVANCER -> ('bureau', 'fermée')");
 expect(output).toContain("('bureau', 'ouverte') AVANCER -> ('bureau', 'ouverte')");
 await page.screenshot({path:`${captures}/python-reel.png`,fullPage:true});
 await page.locator('#code').fill('raise ValueError("CONTROLE_U01")');await page.locator('#py-run').click();await expect(page.locator('#py-output')).toContainText('CONTROLE_U01');
 await page.locator('#code').fill('while True:\n    pass');await page.locator('#py-run').click();await page.locator('#py-stop').click();
 await expect(page.locator('#py-status')).toHaveText('Interrompu');
 await page.locator('#py-reset').click();await page.locator('#py-run').click();await expect(page.locator('#py-status')).toHaveText('Python prêt',{timeout:45000});
});
