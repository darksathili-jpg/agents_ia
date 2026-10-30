"""Recette Chromium T03 : visibilité, accessibilité de base, Pyodide réel local,
trace de l'élève, invalidation et absence de bandes de trois sprites."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qa_enseignant'))
from test_t03 import REFERENCE

def test_browser():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):
            pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/terminale/t03/'
    errors=[]
    strips=[]
    try:
        with sync_playwright() as play:
            browser=play.chromium.launch(headless=True)
            page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.on('console',lambda msg:errors.append('Console : '+msg.text) if msg.type=='error' else None)
            page.on('response',lambda res:errors.append('HTTP '+str(res.status)+' '+res.url) if res.status>=400 else None)
            page.on('request',lambda req:strips.append(req.url) if '/assets/microduck-walk-' in req.url else None)
            page.route('https://cdn.jsdelivr.net/**',lambda route:route.abort())
            assert page.goto(base,wait_until='domcontentloaded').status==200
            assert page.locator('#board .cell').count()==18
            assert page.locator('#board img.board-microduck').count()==1
            assert 'DÉMONSTRATION' in page.locator('#source-label').inner_text()
            assert page.locator('#board .cell.wall').count()==0
            for width,height in ((1440,900),(900,700),(390,844)):
                page.set_viewport_size({'width':width,'height':height})
                page.wait_for_timeout(100)
                dimensions=page.evaluate('() => ({scroll:document.documentElement.scrollWidth,viewport:innerWidth})')
                assert dimensions['scroll']<=dimensions['viewport']+2, (width,dimensions)
            for theme in ('dark','projection','light'):
                page.locator(f'.themes button[data-theme="{theme}"]').click()
                assert page.locator('body').get_attribute('data-theme')==theme
            page.locator('#scenario').select_option('1')
            assert int(page.locator('#timeline').get_attribute('max'))>=7
            page.locator('#next').click()
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            page.locator('#timeline').evaluate('el => {el.value="3";el.dispatchEvent(new Event("input",{bubbles:true}));}')
            assert '(3, 1)' in page.locator('#memory').inner_text()
            page.locator('#scenario').select_option('5')
            assert page.locator('#decision').inner_text().startswith('None')
            assert page.locator('#board img.board-microduck').count()==1
            page.locator('#scenario').select_option('1')
            page.emulate_media(reduced_motion='no-preference')
            page.locator('#next').click()
            sprite=page.locator('#board img.board-microduck')
            assert sprite.get_attribute('src').endswith('microduck-east-0.webp')
            page.wait_for_function(
                "() => document.querySelector('#board .board-microduck').getAttribute('src').endsWith('microduck-east-1.webp')",
                timeout=1400)
            page.wait_for_function(
                "() => document.querySelector('#board .board-microduck').getAttribute('src').endsWith('microduck-idle-east.webp')",
                timeout=1400)
            assert not strips, strips
            page.wait_for_function(
                "() => /Python prêt|Erreur Python|indisponible/.test(document.querySelector('#python-status').textContent)",
                timeout=40_000)
            assert 'Python prêt · distribution locale' in page.locator('#python-status').inner_text(),errors
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '0 / 7'",
                timeout=45_000)
            assert page.locator('#result-cases button').count()==0
            page.locator('#python-code').fill(REFERENCE)
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '7 / 7'",
                timeout=50_000)
            assert page.locator('#result-cases button').count()==7
            page.locator('#result-cases button').nth(1).click()
            assert 'CODE ÉLÈVE' in page.locator('#source-label').inner_text()
            page.locator('#timeline').evaluate(
                'el => {el.value="3";el.dispatchEvent(new Event("input",{bubbles:true}));}')
            assert '(3, 1)' in page.locator('#memory').inner_text()
            assert page.locator('#board img.board-microduck').count()==1
            page.locator('#python-code').fill(REFERENCE+'\n# modification après validation')
            assert page.locator('#score').inner_text()=='— / 7'
            assert 'DÉMONSTRATION' in page.locator('#source-label').inner_text()
            assert not errors,errors
            browser.close()
            print('T03 : Chromium, poses unitaires, 7/7 vrai Pyodide et trace élève : OK')
    finally:
        server.shutdown()
        server.server_close()

if __name__=='__main__':
    test_browser()
