import {test,expect} from '@playwright/test';
for(const theme of ['light','dark','projector']){
 test(`accueil et laboratoire ${theme}`,async({page},testInfo)=>{
  await page.goto('/');await page.locator('#home-display').selectOption(theme);
  await expect(page.getByRole('heading',{level:1})).toContainText('apprivoise');
  expect(await page.locator('.classroom img').evaluate(el=>el.complete&&el.naturalWidth>0)).toBe(true);
  await page.screenshot({path:testInfo.outputPath(`accueil-${theme}.png`),fullPage:true});
  await page.getByRole('link',{name:/Commencer/}).click();
  await expect(page).toHaveURL(/laboratoire.html/);await expect(page.locator('#display')).toHaveValue(theme);
  if(theme==='projector')for(const selector of ['body','.panel','#code','#py-output','#grid']){
   expect(await page.locator(selector).first().evaluate(el=>getComputedStyle(el).backgroundColor.match(/\d+/g).slice(0,3).map(Number).every(v=>v>230))).toBe(true);
  }
  await page.screenshot({path:testInfo.outputPath(`laboratoire-${theme}.png`),fullPage:true});
  await page.getByRole('link',{name:/Retour au carnet/}).click();await expect(page).toHaveURL(/\/$/);
 });
}
for(const width of [390,768,1440])test(`responsive ${width}`,async({page},testInfo)=>{
 await page.setViewportSize({width,height:900});await page.goto('/');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.getByRole('link',{name:'Le parcours',exact:true}).click();await expect(page.locator('#parcours')).toBeInViewport();
 if(width===390)await page.screenshot({path:testInfo.outputPath('accueil-mobile.png'),fullPage:true});
});
test('mouvement réduit et clavier',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');
 expect(await page.locator('.mascot').evaluate(el=>getComputedStyle(el).animationName)).toBe('none');
 await page.keyboard.press('Tab');await expect(page.locator('.skip')).toBeFocused();
 await page.keyboard.press('Enter');await expect(page).toHaveURL(/#parcours$/);
});
test('chapitres et références',async({page})=>{
 await page.goto('/');await expect(page.locator('.journey ol a')).toHaveCount(0);
 expect(await page.locator('.sources a').evaluateAll(nodes=>nodes.map(n=>n.href))).toEqual([
 'https://huggingface.co/learn/agents-course/fr/unit0/introduction','https://arxiv.org/abs/2210.03629','https://www.anthropic.com/engineering/building-effective-agents']);
});
