"""Validation documentaire et supports locaux, sans dépendance supplémentaire."""
import ast
import os
from pathlib import Path
import re
import subprocess
import sys

DOSSIER = Path(__file__).resolve().parent.parent
liens = 0
for fichier in DOSSIER.glob("*.md"):
    texte = fichier.read_text(encoding="utf-8-sig")
    for lien in re.findall(r"\]\(([^)]+)\)", texte):
        if not lien.startswith(("http://", "https://", "#")):
            assert (fichier.parent / lien.split("#")[0]).exists(), (fichier, lien)
            liens += 1
    assert texte.count("```") % 2 == 0, fichier
for fichier in (DOSSIER / "python").glob("*.py"):
    ast.parse(fichier.read_text(encoding="utf-8"), filename=str(fichier))
objectifs = (DOSSIER / "OBJECTIFS_ET_PREREQUIS.md").read_text(encoding="utf-8")
exercices = (DOSSIER / "TP_ET_EXPERIENCES.md").read_text(encoding="utf-8")
assert set(re.findall(r"\| (O\d+) \|", objectifs)) == {f"O{i}" for i in range(1, 11)}
assert set(re.findall(r"\| (E\d+) /", exercices)) == {f"E{i:02}" for i in range(1, 16)}
assert len(re.findall(r"^## TP\d\d", exercices, re.M)) == 5
for numero in range(2, 6):
    assert not (DOSSIER / f"SEANCE_{numero:02}.md").exists(), "Point d'arrêt humain dépassé"
environnement = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
for numero in range(1, 6):
    fichier = DOSSIER / "python" / f"tp{numero:02}_depart.py"
    resultat = subprocess.run([sys.executable, str(fichier)], capture_output=True,
                              encoding="utf-8", errors="replace", env=dict(environnement, PYTHONIOENCODING="utf-8"), check=True)
    marqueur = "DEPART_TP01_OK" if numero == 1 else f"A_COMPLETER_TP{numero:02}"
    assert marqueur in resultat.stdout, fichier
subprocess.run([sys.executable, str(DOSSIER / "python" / "tests_experiences.py")],
               env=environnement, check=True)
print(f"DOSSIER_OK : {liens} liens locaux, syntaxe Python, 10 objectifs, 15 exercices, 5 TP, 5 départs")
