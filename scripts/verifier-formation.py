"""Liens et cohérence de publication des pages statiques du prototype S01."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import ast
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGES = ("module01.html", "seance01.html", "enseignant-s01.html", "ressources-module01.html")


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.h1 = [], [], 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])


pages = {name: Page((ROOT / name).read_text(encoding="utf-8")) for name in PAGES}
count = 0
for name, page in pages.items():
    assert page.h1 == 1, name
    assert len(page.ids) == len(set(page.ids)), name
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = ROOT / unquote(url.path or name)
        if target.is_dir():
            target /= "index.html"
        assert target.exists(), (name, link)
        if url.fragment and target.suffix == ".html":
            dest = pages.get(target.name) or Page(target.read_text(encoding="utf-8"))
            assert unquote(url.fragment) in dest.ids, (name, link)
        count += 1
assert all(f"etape-{i}" in pages["seance01.html"].ids for i in range(10))
assert not (ROOT / "docs/pedagogie/module-01/SEANCE_04.md").exists()
assert not (ROOT / "docs/pedagogie/module-01/SEANCE_05.md").exists()
for filename in ("scripts/construire-formation.py", "scripts/verifier-formation.py"):
    ast.parse((ROOT / filename).read_text(encoding="utf-8"))
subprocess.run([sys.executable, str(ROOT / "docs/pedagogie/module-01/python/s01_solution_interface.py")], check=True)
print(f"FORMATION_STATIQUE_OK : {count} liens/ressources locaux, ancres, un h1 par page, 10 étapes S01, correction Python")
