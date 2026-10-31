"""T07 : Chromium, auditeur visuel, rejeu explicite et Python réel Pyodide."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qa_enseignant'))
from test_t07 import REFERENCE
OUT=ROOT/'test-results'/'t07'

def main():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    failures=[]
    strips=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
            page.on('pageerror',lambda e:failures.append(str(e)))
            page.on('console',lambda m:failures.append(m.text) if m.type=='error' else None)
            page.on('response',lambda res:failures.append(f'HTTP {res.status} {res.url}')
                    if res.status>=400 else None)
            page.on('request',lambda req:strips.append(req.url)
                    if '/assets/microduck-walk-' in req.url else None)
            page.route('https://cdn.jsdelivr.net/**',lambda route:route.abort())
            uri=f'http://127.0.0.1:{server.server_port}/terminale/t07/'
            assert page.goto(uri,wait_until='domcontentloaded').status==200
            assert page.locator('#board .cell').count()==18
            assert page.locator('#board img.board-microduck').count()==1

            for w,h in ((1440,900),(900,700),(390,844)):
                page.set_viewport_size({'width':w,'height':h})
                page.wait_for_timeout(130)
                dim=page.evaluate('() => ({scroll:document.documentElement.scrollWidth,viewport:innerWidth})')
                assert dim['scroll']<=dim['viewport']+2,(w,dim)
                if w!=900:
                    OUT.mkdir(parents=True,exist_ok=True)
                    page.screenshot(path=str(OUT/f't07_{w}.png'),full_page=True)
            for mode in ('dark','projection','light'):
                page.locator(f'.themes button[data-theme="{mode}"]').click()
                assert page.locator('body').get_attribute('data-theme')==mode
                if mode!='dark':
                    rgb=page.locator('#python-code').evaluate('el => getComputedStyle(el).backgroundColor')
                    values=[int(float(v)) for v in rgb.replace('rgba(','').replace('rgb(','').replace(')','').split(',')[:3]]
                    assert min(values)>210,(mode,rgb)

            # Les traces non attestées sont BLOQUÉES sans rejeu.
            for option in ('1','2','3','4','5','7','8'):
                page.locator('#scenario').select_option(option)
                assert page.locator('#status').inner_text()=='JOURNAL_REÇU'
                assert page.locator('#replay').is_disabled()
                page.locator('#audit').click()
                assert page.locator('#status').inner_text()=='AUDIT_EN_COURS'
                assert page.locator('#replay').is_disabled()
                page.locator('#audit').click()
                assert page.locator('#status').inner_text()=='ANOMALIE',option
                assert page.locator('#position-label').inner_text()=='(0, 1)'
                assert page.locator('#replay').is_disabled()

            # Rejouer six événements : deux mouvements et non six.
            page.locator('#scenario').select_option('0')
            page.emulate_media(reduced_motion='no-preference')
            page.locator('#audit').click()
            page.locator('#audit').click()
            assert page.locator('#status').inner_text()=='CONFORME'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            page.locator('#replay').click()  # DEBUT
            page.locator('#replay').click()  # OBSERVATION
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            page.locator('#replay').click()  # Premier DEPLACEMENT
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            assert page.locator('#board img.board-microduck').get_attribute('src').endswith('microduck-east-0.webp')
            page.wait_for_function(
                "() => document.querySelector('#board .board-microduck').getAttribute('src').endsWith('microduck-idle-east.webp')",
                timeout=1500)
            page.locator('#replay').click()  # OBSERVATION
            assert page.locator('#position-label').inner_text()=='(1, 1)'
            page.locator('#replay').click()  # Second DEPLACEMENT
            assert page.locator('#position-label').inner_text()=='(2, 1)'
            page.locator('#replay').click()  # FIN
            assert page.locator('#status').inner_text()=='REJEU_TERMINÉ'
            assert page.locator('#position-label').inner_text()=='(2, 1)'
            assert page.locator('#replay').is_disabled()

            # Attente humaine sans action, refus et accord indépendants.
            page.locator('#scenario').select_option('6')
            page.locator('#audit').click()
            page.locator('#audit').click()
            assert page.locator('#status').inner_text()=='ATTENTE_HUMAINE'
            assert page.locator('#replay').is_disabled()
            assert page.locator('#approval').is_visible()
            page.locator('#deny').click()
            assert page.locator('#status').inner_text()=='ANOMALIE'
            assert page.locator('#replay').is_disabled()
            page.locator('#reset').click()
            page.locator('#audit').click()
            page.locator('#audit').click()
            page.locator('#approve').click()
            assert page.locator('#status').inner_text()=='CONFORME'
            assert page.locator('#position-label').inner_text()=='(0, 1)'
            assert page.locator('#replay').is_enabled()
            assert page.locator('#board img.board-microduck').count()==1
            assert not strips,strips

            # Le score ne vient que de la véritable exécution du code Python.
            page.wait_for_function(
                "() => /Python prêt|Erreur Python|indisponible/.test(document.querySelector('#python-status').textContent)",
                timeout=45_000)
            assert 'Python prêt · distribution locale' in page.locator('#python-status').inner_text(),failures
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '0 / 19'",
                timeout=50_000)
            assert page.locator('#result-cases button').count()==0
            page.locator('#python-code').fill(REFERENCE)
            page.locator('#run-python').click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '19 / 19'",
                timeout=50_000)
            assert page.locator('#result-cases button').count()==19
            page.locator('#result-cases button').nth(1).click()
            assert page.locator('#student-proof').is_visible()
            assert '"etat": "ANOMALIE"' in page.locator('#student-proof-data').inner_text()
            page.locator('#python-code').fill(REFERENCE+'\n# édition après validation')
            assert page.locator('#score').inner_text()=='— / 19'
            assert page.locator('#student-proof').is_hidden()
            assert not failures,failures
            OUT.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(OUT/'t07_python_19_sur_19.png'),full_page=True)
            browser.close()
            print('T07 Chromium : anomalies bloquées, deux déplacements, Pyodide local 19/19 : OK')
    finally:
        server.shutdown();server.server_close()

if __name__=='__main__':
    main()
