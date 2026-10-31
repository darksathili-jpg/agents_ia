"""Recette Chromium T06 : reprise impossible sans preuves ni action explicite.
Exécute le moteur Pyodide local ; aucun score simulé.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qa_enseignant'))
from test_t06 import REFERENCE
OUT=ROOT/'test-results'/'t06'

def main():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):pass
    srv=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    errors=[];strips=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            page.on('response',lambda res:errors.append('HTTP '+str(res.status)+' '+res.url)
                    if res.status>=400 else None)
            page.on('request',lambda req:strips.append(req.url)
                    if '/assets/microduck-walk-' in req.url else None)
            page.route('https://cdn.jsdelivr.net/**',lambda route:route.abort())
            url=f'http://127.0.0.1:{srv.server_port}/terminale/t06/'
            assert page.goto(url,wait_until='domcontentloaded').status==200
            assert page.locator('#board .cell').count()==18
            assert page.locator('#board img.board-microduck').count()==1
            for width,height in ((1440,900),(900,700),(390,844)):
                page.set_viewport_size({'width':width,'height':height})
                page.wait_for_timeout(100)
                dims=page.evaluate('() => ({scroll:document.documentElement.scrollWidth,viewport:innerWidth})')
                assert dims['scroll']<=dims['viewport']+2,(width,dims)
                if width!=900:
                    OUT.mkdir(parents=True,exist_ok=True)
                    page.screenshot(path=str(OUT/f't06_{width}.png'),full_page=True)
            for theme in ('dark','projection','light'):
                page.locator(f'.themes button[data-theme="{theme}"]').click()
                assert page.locator('body').get_attribute('data-theme')==theme
                if theme!='dark':
                    rgb=page.locator('#python-code').evaluate(
                        'e=>getComputedStyle(e).backgroundColor')
                    vals=[int(float(v)) for v in rgb.replace('rgba(','').replace('rgb(','').replace(')','').split(',')[:3]]
                    assert min(vals)>210,(theme,rgb)

            # L'incident commence sans autorisation de reprise.
            page.locator('#scenario').select_option('1')
            assert page.locator('#status').inner_text()=='INCIDENT_DÉTECTÉ'
            assert page.locator('#resume').is_disabled()
            for expected in ('BLOQUÉE','CORRECTIF_PROPOSÉ','EN_REVÉRIFICATION','BLOQUÉE'):
                page.locator('#next').click()
                assert page.locator('#status').inner_text()==expected
                assert page.locator('#position-label').inner_text()=='(0, 1)'
                assert page.locator('#resume').is_disabled()
            assert page.locator('#next').is_disabled()
            # Correctif conforme : ne bouge pas sans clic de reprise.
            page.locator('#scenario').select_option('0')
            page.emulate_media(reduced_motion='no-preference')
            for _ in range(4):page.locator('#next').click()
            assert page.locator('#status').inner_text()=='REPRISE_AUTORISÉE'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            assert page.locator('#resume').is_enabled()
            page.locator('#resume').click()
            assert page.locator('#status').inner_text()=='REPRISE_EXÉCUTÉE'
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            assert page.locator('#board img.board-microduck').get_attribute('src').endswith('microduck-east-0.webp')
            page.wait_for_function(
                "() => document.querySelector('#board .board-microduck').getAttribute('src').endsWith('microduck-idle-east.webp')",
                timeout=1500)
            assert page.locator('#resume').is_disabled()

            for scenario in ('2','3','4','5','7','8'):
                page.locator('#scenario').select_option(scenario)
                for _ in range(4):page.locator('#next').click()
                assert page.locator('#status').inner_text()=='BLOQUÉE',scenario
                assert page.locator('#position-label').inner_text()=='(0, 1)',scenario
                assert page.locator('#resume').is_disabled()

            page.locator('#scenario').select_option('6')
            for _ in range(4):page.locator('#next').click()
            assert page.locator('#status').inner_text()=='ATTENTE_HUMAINE'
            assert page.locator('#resume').is_disabled()
            assert page.locator('#approval').is_visible()
            page.locator('#deny').click()
            assert page.locator('#status').inner_text()=='BLOQUÉE'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            page.locator('#reset').click()
            for _ in range(4):page.locator('#next').click()
            page.locator('#approve').click()
            assert page.locator('#status').inner_text()=='REPRISE_AUTORISÉE'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            page.locator('#resume').click()
            assert page.locator('#status').inner_text()=='REPRISE_EXÉCUTÉE'
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            assert page.locator('#board img.board-microduck').count()==1
            assert not strips,strips

            page.wait_for_function(
                "() => /Python prêt|Erreur Python|indisponible/.test(document.querySelector('#python-status').textContent)",
                timeout=45_000)
            assert 'Python prêt · distribution locale' in page.locator('#python-status').inner_text(),errors
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '0 / 19'",
                timeout=45_000)
            assert page.locator('#result-cases button').count()==0
            page.locator('#python-code').fill(REFERENCE)
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '19 / 19'",
                timeout=50_000)
            assert page.locator('#result-cases button').count()==19
            page.locator('#result-cases button').nth(3).click()
            assert page.locator('#student-proof').is_visible()
            assert '"etat": "BLOQUÉE"' in page.locator('#student-proof-data').inner_text()
            page.locator('#python-code').fill(REFERENCE+'\n# modification')
            assert page.locator('#score').inner_text()=='— / 19'
            assert page.locator('#student-proof').is_hidden()
            assert not errors,errors
            OUT.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(OUT/'t06_python_19_sur_19.png'),full_page=True)
            browser.close()
            print('T06 Chromium : blocage, preuves fraîches, reprise explicite, vrai Pyodide 19/19 : OK')
    finally:
        srv.shutdown();srv.server_close()

if __name__=='__main__':
    main()
