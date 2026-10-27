from pathlib import Path
import base64, re
import sys, json, traceback
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
import engine
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.expose_function('evaluateFromCPython',engine.evaluate_source)
    mock_js='''() => {
      class MockWorker {
        constructor(url) {this.onmessage=null; this.onerror=null;this.terminated=false;
          setTimeout(()=>{if(!this.terminated && this.onmessage)this.onmessage({data:{type:'ready'}})},20)}
        terminate(){this.terminated=true}
        postMessage(data){
          if(data.type==='run') {
            window.evaluateFromCPython(data.source).then(value=>{
              if(!this.terminated && this.onmessage)this.onmessage({data:{type:'result',id:data.id,data:value}})
            }).catch(err=>{if(this.onerror)this.onerror({message:String(err)})});
          }
        }
      }
      window.Worker = MockWorker;
    }'''
    page.evaluate(mock_js)
    try:
        html=(root/'index.html').read_text(encoding='utf-8')
        css=(root/'styles.css').read_text(encoding='utf-8')
        def uri(file):
            raw=(root/file).read_bytes()
            typ='image/webp' if file.endswith('webp') else 'image/png'
            return 'data:'+typ+';base64,'+base64.b64encode(raw).decode()
        for file in (root/'assets').glob('*.webp'):
            reference='assets/'+file.name
            css=css.replace(reference,uri(reference))
            html=html.replace(reference,uri(reference))
        html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
        for file in ('vendor/prism-core.min.js','vendor/prism-clike.min.js','vendor/prism-python.min.js','../shared/editor-indent.js','app.js','hero-motion.js'):
            js=(root/file).read_text(encoding='utf-8')
            # Inline original JS in the same order.
            html=html.replace('<script defer src="'+file+'"></script>', '')
            html=html.replace('</body>', '<script>'+js+'</script></body>')
        page.set_content(html,wait_until='domcontentloaded')
        page.wait_for_timeout(400)
        print('HTML loaded:',page.title())
        print('Worker UI:',page.locator('#run-label').inner_text())
        print('logo loaded:',page.evaluate("document.querySelector('.institution-card img').naturalWidth"))
        print('demo length:',page.evaluate('DEMO_CASES.length'))
        assert page.evaluate('DEMO_CASES.length')==4
        assert 'Lancer' in page.locator('#run-label').inner_text()
        # Hint gating
        page.locator('#hint').click()
        print('hint1:',page.locator('#hint-box').inner_text()[:45])
        page.locator('#hint').click()
        assert 'première version' in page.locator('#hint-box').inner_text()
        assert page.locator('#solution').is_disabled()
        page.locator('#prediction').select_option('AVANCER')
        # Starter edited ONLY with a comment: cannot count a new AST attempt
        page.locator('#code').fill(engine.STARTER_CODE+'\n# simple espace')
        page.locator('#run').click();page.wait_for_function("document.getElementById('runtime-text').textContent.includes('Résultats produits')",timeout=15000)
        page.locator('#hint').click()
        assert 'première version' in page.locator('#hint-box').inner_text()
        first='def decider(o):\n    if o["arrive"]:\n        return "STOP"\n    return "AVANCER"'
        page.locator('#code').fill(first)
        page.locator('#run').click();page.wait_for_timeout(400)
        page.locator('#hint').click()
        assert 'Indice 2' in page.locator('#hint-box').inner_text()
        # whitespace changed: AST unchanged
        page.locator('#code').fill('def decider(o):\n  # minor comment\n  if o["arrive"]:\n      return "STOP"\n  return "AVANCER"')
        page.locator('#run').click();page.wait_for_timeout(400)
        page.locator('#hint').click()
        assert 'modifie la logique' in page.locator('#hint-box').inner_text()
        assert page.locator('#solution').is_disabled()
        # second genuinely distinct version
        page.locator('#code').fill(engine.REFERENCE_SOLUTION)
        page.locator('#run').click();page.wait_for_timeout(400)
        page.locator('#hint').click()
        assert 'Indice 3' in page.locator('#hint-box').inner_text()
        assert not page.locator('#solution').is_disabled()
        # Check trace of dynamic world
        page.locator('[data-scenario="1"]').click()
        page.wait_for_timeout(200)
        print('sensor:',page.locator('#sensor-status').inner_text())
        print('trace row 1:',page.locator('#trace-body tr').first.inner_text()[:110])
        assert 'PÉRIMÉE' in page.locator('#sensor-status').inner_text()
        assert 'Obstacle apparu' in page.locator('#trace-body tr').first.inner_text()
        print('ui after reference',page.locator('#test-total').inner_text())
        # screenshot main, dark and projection
        page.locator('[data-theme-choice="light"]').click()
        page.screenshot(path=str(root/'capture_v51_reelle_clair.png'),full_page=True)
        for theme in ('dark','projection'):
            page.locator(f'[data-theme-choice="{theme}"]').click()
            assert page.locator('body').get_attribute('data-theme')==theme
            page.screenshot(path=str(root/f'capture_v51_reelle_{theme}.png'),full_page=True)
        print('horizontal overflow:',page.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth'))
        print('pageerrors:',errors)
        assert not errors
        print('BROWSER TESTS OK (Worker CPython mock; Pyodide not tested)')
    finally:
        browser.close()
