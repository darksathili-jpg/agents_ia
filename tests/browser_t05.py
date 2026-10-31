"""Recette Chromium T05 : vérité des preuves, machine à états et Pyodide réel."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qa_enseignant'))
from test_t05 import REFERENCE
OUT=ROOT/'test-results'/'t05'

def main():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):pass
    srv=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    errors=[]
    strips=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            page.on('response',lambda res:errors.append('HTTP '+str(res.status)+' '+res.url)
                    if res.status>=400 else None)
            page.on('request',lambda req:strips.append(req.url) if '/assets/microduck-walk-' in req.url else None)
            page.route('https://cdn.jsdelivr.net/**',lambda route:route.abort())
            address=f'http://127.0.0.1:{srv.server_port}/terminale/t05/'
            assert page.goto(address,wait_until='domcontentloaded').status==200
            assert page.locator('#board .cell').count()==18
            assert page.locator('#board img.board-microduck').count()==1
            for width,height in ((1440,900),(900,700),(390,844)):
                page.set_viewport_size({'width':width,'height':height})
                page.wait_for_timeout(110)
                d=page.evaluate('() => ({scroll:document.documentElement.scrollWidth,viewport:innerWidth})')
                assert d['scroll']<=d['viewport']+2,(width,d)
                if width!=900:
                    OUT.mkdir(parents=True,exist_ok=True)
                    page.screenshot(path=str(OUT/f't05_{width}.png'),full_page=True)
            for theme in ('dark','projection','light'):
                page.locator(f'.themes button[data-theme="{theme}"]').click()
                assert page.locator('body').get_attribute('data-theme')==theme
                if theme!='dark':
                    rgb=page.locator('#python-code').evaluate('e=>getComputedStyle(e).backgroundColor')
                    channels=[int(float(n)) for n in rgb.replace('rgb(','').replace('rgba(','').replace(')','').split(',')[:3]]
                    assert min(channels)>210,(theme,rgb)

            # Rapport trompeur : aucune possibilité de déplacement.
            page.locator('#scenario').select_option('1')
            assert page.locator('#status').inner_text()=='SPÉCIFIÉE'
            page.locator('#next').click()
            assert page.locator('#status').inner_text()=='EN VÉRIFICATION'
            page.locator('#next').click()
            assert page.locator('#status').inner_text()=='BLOQUÉE'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            assert page.locator('#approval').is_hidden()
            assert page.locator('#next').is_disabled()

            # Un rapport honnête et deux tests indépendants réussis autorisent un seul pas.
            page.locator('#scenario').select_option('0')
            page.emulate_media(reduced_motion='no-preference')
            page.locator('#next').click()
            page.locator('#next').click()
            assert page.locator('#status').inner_text()=='VALIDÉE'
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            assert page.locator('#board img.board-microduck').get_attribute('src').endswith('microduck-east-0.webp')
            page.wait_for_function(
                "() => document.querySelector('#board .board-microduck').getAttribute('src').endsWith('microduck-idle-east.webp')",
                timeout=1500)

            # Preuve inventée et auto-approbation de l'agent : blocage.
            for scenario in ('3','6'):
                page.locator('#scenario').select_option(scenario)
                page.locator('#next').click()
                page.locator('#next').click()
                assert page.locator('#status').inner_text()=='BLOQUÉE'
                assert page.locator('#position-label').inner_text()=='(0, 1)'

            # Accord humain externe à la requête : ni présumé ni automatique.
            page.locator('#scenario').select_option('5')
            page.locator('#next').click()
            page.locator('#next').click()
            assert page.locator('#status').inner_text()=='ATTENTE_HUMAINE'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            assert page.locator('#approval').is_visible()
            page.locator('#deny').click()
            assert page.locator('#status').inner_text()=='BLOQUÉE'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            page.locator('#reset').click()
            page.locator('#next').click()
            page.locator('#next').click()
            page.locator('#approve').click()
            assert page.locator('#status').inner_text()=='VALIDÉE'
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            assert page.locator('#board img.board-microduck').count()==1
            assert not strips,strips

            # Vrai Pyodide local, sans CDN. Squelette -> échec, référence -> réussite.
            page.wait_for_function(
                "() => /Python prêt|Erreur Python|indisponible/.test(document.querySelector('#python-status').textContent)",
                timeout=40_000)
            assert 'Python prêt · distribution locale' in page.locator('#python-status').inner_text(),errors
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '0 / 19'",timeout=50_000)
            assert page.locator('#result-cases button').count()==0
            page.locator('#python-code').fill(REFERENCE)
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '19 / 19'",timeout=50_000)
            assert page.locator('#result-cases button').count()==19
            page.locator('#result-cases button').nth(1).click()
            assert page.locator('#student-proof').is_visible()
            assert '"etat": "BLOQUÉE"' in page.locator('#student-proof-data').inner_text()
            page.locator('#python-code').fill(REFERENCE+'\n# changement')
            assert page.locator('#score').inner_text()=='— / 19'
            assert page.locator('#student-proof').is_hidden()
            assert not errors,errors
            OUT.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(OUT/'t05_python.png'),full_page=True)
            browser.close()
            print('T05 : Chromium, états et agent trompeur, vrai Pyodide local 19/19 : OK')
    finally:
        srv.shutdown()
        srv.server_close()

if __name__=='__main__':
    main()
