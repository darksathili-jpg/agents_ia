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
    try:
        with sync_playwright() as play:
            browser = play.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
            page.on("pageerror", lambda error: errors.append(str(error)))
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
            assert page.locator("#board-bfs .board-microduck").get_attribute("src").endswith("microduck-idle-east.webp")
            assert page.locator("#board-dfs .board-microduck").get_attribute("src") is not None
            page.locator("#board-bfs .cell[data-x='1'][data-y='2']").click()
            assert "wall" not in page.locator("#board-bfs .cell[data-x='1'][data-y='2']").get_attribute("class")

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
