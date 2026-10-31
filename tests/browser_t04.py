"""Recette Chromium T04 : interface, refus, approbation explicite et vrai Pyodide local."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qa_enseignant'))
from test_t04 import REFERENCE
OUT=ROOT/'test-results'/'t04'

def test_browser():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):
            pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/terminale/t04/'
    errors=[]
    strip_requests=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
            page.on('response',lambda response:errors.append('HTTP '+str(response.status)+' '+response.url)
                    if response.status>=400 else None)
            page.on('request',lambda request:strip_requests.append(request.url)
                    if '/assets/microduck-walk-' in request.url else None)
            page.route('https://cdn.jsdelivr.net/**',lambda route:route.abort())
            assert page.goto(base,wait_until='domcontentloaded').status==200
            assert page.locator('#board .cell').count()==18
            assert page.locator('#board img.board-microduck').count()==1

            # Modes et absence de débordement horizontal.
            for width,height in ((1440,900),(900,700),(390,844)):
                page.set_viewport_size({'width':width,'height':height})
                page.wait_for_timeout(140)
                sizes=page.evaluate('() => ({scroll:document.documentElement.scrollWidth,viewport:innerWidth})')
                assert sizes['scroll']<=sizes['viewport']+2,(width,sizes)
                if width != 900:
                    OUT.mkdir(parents=True,exist_ok=True)
                    page.screenshot(path=str(OUT/f't04_{width}.png'),full_page=True)
            for theme in ('dark','projection','light'):
                page.locator(f'.themes button[data-theme="{theme}"]').click()
                assert page.locator('body').get_attribute('data-theme')==theme
                if theme != 'dark':
                    rgb=page.locator('#python-code').evaluate(
                        'el => getComputedStyle(el).backgroundColor')
                    nums=[int(float(x)) for x in rgb.replace('rgba(','').replace('rgb(','').replace(')','').split(',')[:3]]
                    assert min(nums)>210,('Editeur sombre en mode clair/projection',theme,rgb)

            # Le droit d'avancer entraîne exactement un déplacement.
            page.emulate_media(reduced_motion='no-preference')
            page.locator('#scenario').select_option('1')
            page.locator('#inspect').click()
            assert page.locator('#status').inner_text()=='AUTORISÉ'
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            assert page.locator('#board img.board-microduck').get_attribute('src').endswith('microduck-east-0.webp')
            page.wait_for_function(
                "() => document.querySelector('#board .board-microduck').getAttribute('src').endsWith('microduck-idle-east.webp')",
                timeout=1400)

            page.locator('#scenario').select_option('2')
            page.locator('#inspect').click()
            assert page.locator('#status').inner_text()=='REFUSÉ'
            assert page.locator('#position-label').inner_text()=='(0, 1)'

            # Une opération sensible reste en attente sans mouvement.
            page.locator('#scenario').select_option('3')
            page.locator('#inspect').click()
            assert page.locator('#status').inner_text()=='ATTENTE_HUMAINE'
            assert page.locator('#approval').is_visible()
            assert page.locator('#board .cell.wall').count()==1
            page.locator('#deny').click()
            assert page.locator('#status').inner_text()=='REFUSÉ PAR HUMAIN'
            assert page.locator('#board .cell.wall').count()==1
            page.locator('#reset').click()
            page.locator('#inspect').click()
            page.locator('#approve').click()
            assert page.locator('#status').inner_text()=='AUTORISÉ APRÈS ACCORD'
            assert page.locator('#board .cell.wall').count()==0
            assert page.locator('#position-label').inner_text()=='(0, 1)'

            # Ni faux champ d'approbation ni téléportation ne passe.
            for option in ('4','5'):
                page.locator('#scenario').select_option(option)
                page.locator('#inspect').click()
                assert page.locator('#status').inner_text()=='REFUSÉ'
                assert page.locator('#approval').is_hidden()
                assert page.locator('#position-label').inner_text()=='(0, 1)'
            page.locator('#scenario').select_option('6')
            page.locator('#inspect').click()
            assert page.locator('#status').inner_text()=='AUTORISÉ'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            assert page.locator('#board img.board-microduck').count()==1
            assert not strip_requests,strip_requests

            # Le test réel n'utilise jamais la démonstration JS.
            page.wait_for_function(
                "() => /Python prêt|Erreur Python|indisponible/.test(document.querySelector('#python-status').textContent)",
                timeout=40_000)
            assert 'Python prêt · distribution locale' in page.locator('#python-status').inner_text(),errors
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '0 / 13'",timeout=45_000)
            assert page.locator('#result-cases button').count()==0
            page.locator('#python-code').fill(REFERENCE)
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '13 / 13'",timeout=50_000)
            assert page.locator('#result-cases button').count()==13
            page.locator('#result-cases button').nth(7).click()
            assert page.locator('#student-proof').is_visible()
            assert '"accord_humain_simule": true' in page.locator('#student-proof-data').inner_text()
            page.locator('#python-code').fill(REFERENCE+'\n# modification')
            assert page.locator('#score').inner_text()=='— / 13'
            assert page.locator('#student-proof').is_hidden()
            assert not errors,errors
            OUT.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(OUT/'t04_python_reel.png'),full_page=True)
            browser.close()
            print('T04 Chromium + Pyodide local + 13/13 + refus/approbation : OK')
    finally:
        server.shutdown()
        server.server_close()

if __name__=='__main__':
    test_browser()
