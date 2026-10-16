import { test, expect } from "@playwright/test";

test("cours en français et contrôles accessibles", async ({page})=>{
  await page.goto("/");
  await expect(page.getByRole("heading",{name:/Comprendre l’agent/})).toBeVisible();
  await expect(page.getByRole("button",{name:/Exécuter une étape/})).toBeVisible();
  await expect(page.getByLabel("Politique :")).toBeVisible();
});
test("politique gloutonne bloquée, puis BFS aboutit",async({page})=>{
  await page.goto("/");
  await page.getByRole("button",{name:/Exécuter une étape/}).click();
  await page.getByRole("button",{name:/Exécuter une étape/}).click();
  await expect(page.locator("#state")).toHaveText("Bloqué");
  await page.locator("#policy").selectOption("bfs");
  for(let i=0;i<35;i++){
    if(await page.locator("#state").textContent()==="Objectif atteint") break;
    await page.locator("#step").click();
  }
  await expect(page.locator("#state")).toHaveText("Objectif atteint");
  await expect(page.locator("#position")).toHaveText("6,2");
});
test("évaluation et modes d'affichage",async({page})=>{
  await page.goto("/");
  await page.locator('input[value="b"]').check();
  await page.getByRole("button",{name:"Vérifier la réponse"}).click();
  await expect(page.locator("#feedback")).toContainText("Exact");
  await page.locator("#display").selectOption("light");
  await expect(page.locator("body")).toHaveClass(/light/);
  await page.reload();
  await expect(page.locator("#display")).toHaveValue("light");
  await page.locator("#display").selectOption("projector");
  await expect(page.locator("body")).toHaveClass(/projector/);
});
test("exécution Python reliée à la grille (worker de test contrôlé)",async({page})=>{
  await page.addInitScript(()=>{
    class FakeWorker{
      constructor(){this.onmessage=null;this.onerror=null;this.terminated=false}
      postMessage(msg){
        const reply=()=>{
          if(this.terminated)return;
          const x=msg.position?.[0]??0,y=msg.position?.[1]??2;
          const action=x===1&&y===2?"haut":x===1&&y===1?"haut":x===1&&y===0?"droite":x===2&&y===0?"droite":x===3&&y===0?"bas":x===3&&y===1?"bas":x===3&&y===2?"droite":x>=4&&x<6?"droite":"droite";
          this.onmessage?.({data:{id:msg.id,ok:true,action,output:""}});
        };
        setTimeout(reply,0);
      }
      terminate(){this.terminated=true}
    }
    window.Worker=FakeWorker;
  });
  await page.goto("/");
  await page.locator("#policy").selectOption("python");
  await page.locator("#step").click();
  await expect(page.locator("#position")).toHaveText("1,2");
  await page.locator("#step").click();
  await expect(page.locator("#position")).toHaveText("1,1");
});
test("bouton stop disponible même pendant une boucle",async({page})=>{
  await page.addInitScript(()=>{
    window.Worker=class{
      postMessage(){}
      terminate(){window.__terminated=true}
    };
  });
  await page.goto("/");
  await page.locator("#py-run").click();
  await page.locator("#py-stop").click();
  await expect(page.locator("#py-output")).toHaveText("Exécution Python arrêtée.");
  await expect(page.locator("#py-run")).toBeEnabled();
  expect(await page.evaluate(()=>window.__terminated)).toBe(true);
});
test("mise en page mobile sans débordement horizontal important",async({page})=>{
  await page.setViewportSize({width:390,height:844});
  await page.goto("/");
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2)).toBe(true);
});