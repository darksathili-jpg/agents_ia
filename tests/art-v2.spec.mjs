import {test,expect} from '@playwright/test';

test('Microduck explique les trois étapes au clavier et conserve le choix',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/');
 const decide=page.getByRole('button',{name:'2. Décider',exact:true});
 await decide.scrollIntoViewIfNeeded();await decide.press('Space');
 await expect(decide).toBeFocused();await expect(decide).toHaveAttribute('aria-pressed','true');
 await expect(page.locator('#mission-note')).toContainText('case immédiatement à droite');
 await expect(page.locator('#robot-message')).toContainText('Une commande');
 await expect(page.locator('[aria-pressed="true"]')).toHaveCount(1);
 await page.locator('.mascot').hover();await expect(page.locator('#robot-message')).toContainText('Prêt');
 await page.locator('.mission-heading').hover();await expect(page.locator('#robot-message')).toContainText('Une commande');
 await page.getByRole('button',{name:'3. Agir',exact:true}).click();
 await expect(page.locator('#mission-note')).toContainText('refuse un mur');
 await page.locator('#home-display').selectOption('dark');
 await expect(page.locator('[data-mission-step="agir"]')).toHaveAttribute('aria-pressed','true');
 await page.getByRole('button',{name:'1. Observer',exact:true}).focus();
 await page.keyboard.press('Tab');
 await expect(decide).toBeFocused();
 expect(await decide.evaluate(el=>getComputedStyle(el).outlineStyle)).toBe('solid');
 expect(await decide.evaluate(el=>parseFloat(getComputedStyle(el).outlineWidth))).toBeGreaterThanOrEqual(3);
 await page.locator('.mascot').click();await expect(page).toHaveURL(/laboratoire.html/);
});

// Resolve inherited transparent surfaces and use actual browser colours, not CSS strings.
async function textMetrics(locator){
 return locator.evaluate(el=>{
  const rgb=value=>value.match(/[\d.]+/g).map(Number);
  let background=[255,255,255];
  for(let node=el;node;node=node.parentElement){
   const value=rgb(getComputedStyle(node).backgroundColor);
   if(value.length<4||value[3]===1){background=value.slice(0,3);break;}
  }
  const lum=values=>values.map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
  const style=getComputedStyle(el),foreground=rgb(style.color),a=lum(foreground.slice(0,3)),b=lum(background);
  return {ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),size:parseFloat(style.fontSize),background};
 });
}

test('projection : contraste réel et taille des textes de l’accueil et du labo',async({page})=>{
 await page.goto('/');await page.locator('#home-display').selectOption('projector');
 for(const selector of ['.brand-subtitle','.masthead nav>a','.masthead label','#home-display','.issue','.classroom figcaption','.welcome-bubble span','.guide-signature','.annotation','.chapter-status','.journey li small','.mission-heading>span','.mission-steps button','#mission-note','.experiment figcaption','.experiment code','.sources a span','.home-footer small']){
  const metrics=await textMetrics(page.locator(selector).first());
  expect(metrics.ratio,selector).toBeGreaterThanOrEqual(4.5);
  expect(metrics.size,selector).toBeGreaterThanOrEqual(18);
 }
 for(const selector of ['body','.opening','.bubble','.experiment']){
  expect((await textMetrics(page.locator(selector).first())).background.every(v=>v>=230),selector).toBe(true);
 }
 await page.goto('/laboratoire.html');
 for(const selector of ['.stats span','#log','#policy','#step']){
  const metrics=await textMetrics(page.locator(selector).first());
  expect(metrics.ratio,selector).toBeGreaterThanOrEqual(4.5);
  expect(metrics.size,selector).toBeGreaterThanOrEqual(18);
 }
 for(const selector of ['body','#log','#grid']){
  expect((await textMetrics(page.locator(selector).first())).background.every(v=>v>=230),selector).toBe(true);
 }
});

for(const width of [390,768,1440])test(`V2 : trois thèmes et bulles à ${width}px`,async({page})=>{
 await page.setViewportSize({width,height:900});await page.goto('/');
 for(const theme of ['light','dark','projector']){
  await page.locator('#home-display').selectOption(theme);
  for(const step of ['observer','decider','agir']){
   await page.locator(`[data-mission-step="${step}"]`).click();
   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${theme}/${step}`).toBe(true);
  }
  await expect(page.locator('.brand-title')).toBeVisible();
  expect(await page.locator('.brand-title').evaluate(el=>getComputedStyle(el).fontFamily)).toContain('Henny Penny');
 }
});

test('animations finies, réduction du mouvement et focus visible dans les trois modes',async({page})=>{
 await page.goto('/');
 expect(await page.locator('.mascot').evaluate(el=>Number(getComputedStyle(el).animationIterationCount))).toBeLessThanOrEqual(3);
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const theme of ['light','dark','projector']){
  await page.locator('#home-display').selectOption(theme);
  expect(await page.locator('.robot-picture').first().evaluate(el=>getComputedStyle(el,'::after').animationName)).toBe('none');
  expect(await page.locator('.mascot').evaluate(el=>getComputedStyle(el).animationName)).toBe('none');
  await page.getByRole('link',{name:'Le parcours',exact:true}).focus();
  expect(await page.getByRole('link',{name:'Le parcours',exact:true}).evaluate(el=>getComputedStyle(el).outlineStyle)).toBe('solid');
 }
});
