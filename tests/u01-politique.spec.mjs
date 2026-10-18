import {test,expect} from '@playwright/test';
import {mkdir} from 'node:fs/promises';
const captures='docs/correction-u01-politique/captures';
test.beforeAll(()=>mkdir(captures,{recursive:true}));

test('code réel : priorité horizontale, verticale seulement ensuite et refus du moteur',async({page})=>{
 await page.goto('/laboratoire.html');
 const rules=await page.evaluate(()=>({
  initial:naive([0,2]),afterFirst:naive([1,2]),above:naive([6,1]),below:naive([6,3]),atGoal:naive([6,2]),
  free:valid([1,2]),wall:valid([2,2]),left:valid([-1,2]),right:valid([7,2]),top:valid([0,-1]),bottom:valid([0,5])
 }));
 expect(rules).toEqual({initial:'droite',afterFirst:'droite',above:'bas',below:'haut',atGoal:null,free:true,wall:false,left:false,right:false,top:false,bottom:false});
});

test('explication avant la prédiction et la manipulation, sans résultats préremplis',async({page})=>{
 await page.goto('/u01.html#essai');
 const explanation=page.locator('#essai #regle-explication');
 await expect(explanation).toBeVisible();
 await expect(explanation).toContainText('ne recherche pas de chemin');
 await expect(explanation).toContainText('ne consulte pas les murs');
 await expect(explanation).toContainText('le mot « gloutonne » ne signifie pas que toutes');
 const beforePrediction=await explanation.evaluate(e=>Boolean(e.compareDocumentPosition(document.querySelector('#P1-justification'))&Node.DOCUMENT_POSITION_FOLLOWING));
 expect(beforePrediction).toBe(true);
 await expect(page.locator('#P1-justification')).toBeEmpty();
 const lab=page.frameLocator('#u01-lab');await expect(lab.locator('#detail-values')).toBeHidden();
 await expect(lab.locator('#steps')).toHaveText('0');
 await page.screenshot({path:`${captures}/apres-avant-manipulation.png`,fullPage:true});
});

for(const theme of ['light','dark','projector'])test(`deux décompositions fidèles et remise à zéro — ${theme}`,async({page})=>{
 await page.setViewportSize({width:1440,height:1000});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/laboratoire.html');await page.locator('#display').selectOption(theme);
 await page.locator('#step').focus();await page.keyboard.press('Enter');
 await expect(page.locator('#detail-title')).toContainText('Tentative 1');
 await expect(page.locator('#detail-command')).toHaveText('droite : demande la case B (1,2) depuis A (0,2).');
 await expect(page.locator('#detail-reason')).toContainText('G (6,2) est à droite de A (0,2)');
 await expect(page.locator('#detail-reason')).toContainText('sans consulter les murs');
 await expect(page.locator('#detail-check')).toHaveText('B (1,2) est dans la grille et libre : mouvement autorisé.');
 await expect(page.locator('#detail-effect')).toHaveText('A (0,2) → B (1,2) : déplacement d’une case.');
 await page.locator('#decision-detail').scrollIntoViewIfNeeded();await page.screenshot({path:`${captures}/apres-etape1-${theme}.png`,fullPage:true});
 await page.locator('#step').focus();await page.keyboard.press('Enter');
 await expect(page.locator('#detail-title')).toContainText('Tentative 2');
 await expect(page.locator('#detail-command')).toHaveText('droite : demande la case C (2,2) depuis B (1,2).');
 await expect(page.locator('#detail-reason')).toContainText('G (6,2) est à droite de B (1,2)');
 await expect(page.locator('#detail-check')).toHaveText('C (2,2) contient un mur : mouvement refusé.');
 await expect(page.locator('#detail-effect')).toHaveText('B (1,2) → B (1,2) : aucun déplacement. La commande choisie reste droite.');
 await expect(page.locator('#steps')).toHaveText('2');await expect(page.locator('#step')).toBeDisabled();
 await page.screenshot({path:`${captures}/apres-etape2-${theme}.png`,fullPage:true});
 if(theme==='projector')expect(await page.locator('#detail-effect').evaluate(e=>parseFloat(getComputedStyle(e).fontSize))).toBeGreaterThanOrEqual(20);
 await page.locator('#reset').focus();await page.keyboard.press('Enter');
 await expect(page.locator('#detail-values')).toBeHidden();await expect(page.locator('#detail-effect')).toBeEmpty();
 await expect(page.locator('#steps')).toHaveText('0');expect(errors).toEqual([]);
});

test('tableau explicatif en cadre et mobile : visible, sans débordement, focus conservé',async({page})=>{
 await page.setViewportSize({width:390,height:900});await page.goto('/u01.html#essai');
 const lab=page.frameLocator('#u01-lab');await lab.locator('#step').click();await lab.locator('#step').click();
 await expect(lab.locator('#detail-check')).toContainText('C (2,2) contient un mur');
 await expect(lab.locator('#regle-explication')).toBeHidden();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 expect(await lab.locator('body').evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await lab.locator('#reset').focus();await expect(lab.locator('#reset')).toBeFocused();
 await page.screenshot({path:`${captures}/apres-mobile.png`,fullPage:true});
});
