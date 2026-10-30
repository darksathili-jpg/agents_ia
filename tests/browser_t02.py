"""Recette T02 dans un vrai Chromium et avec Pyodide local — aucun Worker simulé.

Lancée séparément par GitHub Actions (pas par pytest), avec :
  python -m playwright install --with-deps chromium
  python tests/browser_t02.py
"""
from __future__ import annotations

from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import contextlib
import os
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "test-results" / "t02"
sys.path.insert(0, str(ROOT / "qa_enseignant"))
from reference_t02 import REFERENCE


def test_browser():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)
        def log_message(self, format, *args):
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/terminale/t02/"
    errors = []
    strip_requests = []
    try:
        with sync_playwright() as play:
            browser = play.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("request", lambda req: strip_requests.append(req.url)
                    if "/assets/microduck-walk-" in req.url else None)
            page.on("requestfailed", lambda request: errors.append("REQ " + request.url + " " + str(request.failure)) if "ERR_ABORTED" not in str(request.failure) else None)
            page.on("response", lambda response: errors.append("HTTP " + str(response.status) + " " + response.url) if response.status >= 400 else None)
            page.on("console", lambda message: errors.append("console: "+message.text) if message.type == "error" else None)
            page.route("https://cdn.jsdelivr.net/**", lambda route: route.abort())
            assert page.goto(base, wait_until="domcontentloaded").status == 200
            page.wait_for_selector("#board-bfs .cell")
            assert page.locator("#board-bfs .cell").count() == 35
            assert page.locator("#board-dfs .cell").count() == 35
            assert page.locator("#board-bfs .board-microduck").count() == 1
            assert page.locator("#board-dfs .board-microduck").count() == 1
            assert page.locator("#phase-bfs").inner_text().startswith("EXPLORATION")
            assert page.locator(".hero-art .microduck").get_attribute("src").endswith("microduck-idle-east.webp")
            for width, height in ((1440, 900), (900, 700), (390, 844)):
                page.set_viewport_size({"width": width, "height": height})
                page.wait_for_timeout(180)
                horizontal = page.evaluate(
                    "() => ({scroll:document.documentElement.scrollWidth, viewport:innerWidth})"
                )
                assert horizontal["scroll"] <= horizontal["viewport"] + 2, (width, horizontal)
                if width != 900:
                    OUT.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(OUT / f"t02_{width}.png"), full_page=True)
            for theme in ("dark", "projection", "light"):
                page.locator(f".themes button[data-theme='{theme}']").click()
                assert page.locator("body").get_attribute("data-theme") == theme
            page.locator("#scenario").select_option("difference")
            page.locator("#step").click()
            assert page.locator("#count-bfs").inner_text() == "1"
            assert page.locator("#count-dfs").inner_text() == "1"
            page.locator("#timeline").evaluate(
                "el => {el.value=el.max;el.dispatchEvent(new Event('input',{bubbles:true}));}"
            )
            bfs = int(page.locator("#length-bfs").inner_text())
            dfs = int(page.locator("#length-dfs").inner_text())
            assert dfs > bfs, (bfs, dfs)
            assert page.locator("#phase-bfs").inner_text().startswith("DÉPLACEMENT")
            assert page.locator("#phase-dfs").inner_text().startswith("DÉPLACEMENT")
            for method in ("bfs", "dfs"):
                sprite = page.locator(f"#board-{method} .board-microduck")
                source = sprite.get_attribute("src")
                assert source.endswith(tuple(f"microduck-idle-{d}.webp"
                                            for d in ("east", "west", "north", "south"))), source
                # La position du personnage doit coïncider avec la case arrivée :
                # vérifier les coordonnées réelles du sprite dans le DOM.
                coords = page.evaluate("""(method) => {
                    const board=document.querySelector('#board-'+method);
                    const image=board.querySelector('.board-microduck');
                    const goal=board.querySelector('.cell[data-x="6"][data-y="2"]');
                    return {x:parseFloat(image.style.left),y:parseFloat(image.style.top),
                        expectedX:goal.offsetLeft+goal.offsetWidth/2,
                        expectedY:goal.offsetTop+goal.offsetHeight/2,
                        loaded:image.complete&&image.naturalWidth>0};
                }""", method)
                assert coords["loaded"], coords
                assert abs(coords["x"]-coords["expectedX"]) <= 1.5, coords
                assert abs(coords["y"]-coords["expectedY"]) <= 1.5, coords
            page.locator("#board-bfs .cell[data-x='1'][data-y='2']").click()
            assert "wall" not in page.locator("#board-bfs .cell[data-x='1'][data-y='2']").get_attribute("class")

            # Test de la marche non simulée avec motion autorisé : une pose
            # unitaire à la fois, puis retour à l'immobilité sur une case.
            page.emulate_media(reduced_motion="no-preference")
            page.locator("#scenario").select_option("direct")
            for _ in range(80):
                if page.locator("#phase-bfs").inner_text().startswith("DÉPLACEMENT"):
                    break
                assert page.locator("#step").is_enabled(), "Le BFS ne déclenche aucun déplacement."
                page.locator("#step").click()
            else:
                raise AssertionError("Le BFS n'a pas atteint la phase déplacement.")

            bfs_sprite=page.locator("#board-bfs .board-microduck")
            assert bfs_sprite.get_attribute("src").endswith("microduck-east-0.webp")
            page.wait_for_function(
                "() => document.querySelector('#board-bfs .board-microduck').getAttribute('src').endsWith('microduck-east-1.webp')",
                timeout=1500
            )
            page.wait_for_function(
                "() => document.querySelector('#board-bfs .board-microduck').getAttribute('src').endsWith('microduck-east-2.webp')",
                timeout=1500
            )
            page.wait_for_function(
                "() => document.querySelector('#board-bfs .board-microduck').getAttribute('src').endsWith('microduck-idle-east.webp')",
                timeout=1500
            )
            assert page.locator("#board-bfs img.board-microduck").count() == 1
            assert page.locator("#board-dfs img.board-microduck").count() == 1
            assert not strip_requests, "Bande complète utilisée comme image : " + str(strip_requests)

            # Pyodide réel, distribution locale, pas de secours CDN.
            page.wait_for_function(
                "() => /Python prêt|Erreur Python|indisponible/.test(document.querySelector('#python-status').textContent)",
                timeout=35_000,
            )
            status = page.locator("#python-status").inner_text()
            assert "Python prêt · distribution locale" in status, {"status":status,"errors":errors}
            page.locator("#run-python").click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent !== '— / 7'",
                timeout=50_000,
            )
            assert page.locator("#score").inner_text() == "0 / 7"

            # Corrigé exclusivement chargé par la recette enseignante, jamais
            # dans la distribution destinée aux élèves.
            page.locator("#python-code").fill(REFERENCE)
            page.locator("#run-python").click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '7 / 7'",
                timeout=60_000,
            )
            assert page.locator(".case.failed").count() == 0
            assert page.locator("#student-trace").is_visible()
            # Une réussite ne doit jamais rester valide après une modification
            # de la source. Le même principe s'applique aux traces.
            page.locator("#python-code").fill(REFERENCE+"\n# modification après validation\n")
            assert page.locator("#score").inner_text() == "— / 7"
            assert "Code modifié" in page.locator("#result-summary").inner_text()
            assert page.locator("#student-trace").is_hidden()
            page.locator("#run-python").click()
            page.wait_for_function(
                "() => document.querySelector('#score').textContent === '7 / 7'",
                timeout=60_000,
            )
            assert not errors, errors
            OUT.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(OUT / "t02_python_reel.png"), full_page=True)
            browser.close()
            print("T02 Chromium + vrai Pyodide local + code témoin 7/7 : OK")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    test_browser()
