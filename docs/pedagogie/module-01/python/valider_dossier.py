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
assert (DOSSIER / "SEANCE_02.md").exists()
assert (DOSSIER / "SEANCE_03.md").exists()
for numero in range(4, 6):
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
subprocess.run([sys.executable, str(DOSSIER / "python" / "tests_s01_s02.py")],
               env=environnement, check=True)
seance1 = (DOSSIER / "SEANCE_01.md").read_text(encoding="utf-8")
seance2 = (DOSSIER / "SEANCE_02.md").read_text(encoding="utf-8")
subprocess.run([sys.executable, str(DOSSIER / "python" / "tests_s03.py")],
               env=environnement, check=True)
for nom, marqueur in (("s03_depart.py", "DEPART_S03_OK"), ("s03_tp.py", "TP03_S03_OK")):
    resultat = subprocess.run([sys.executable, str(DOSSIER / "python" / nom)],
                              capture_output=True, encoding="utf-8", errors="replace",
                              env=dict(environnement, PYTHONIOENCODING="utf-8"), check=True)
    assert marqueur in resultat.stdout, nom
seance3 = (DOSSIER / "SEANCE_03.md").read_text(encoding="utf-8")
plages1 = re.findall(r"^##.*?— (\d+) à (\d+) min", seance1, re.M)
plages2 = re.findall(r"^\| (\d+)–(\d+) \|", seance2, re.M)
plages3 = re.findall(r"^\| (\d+)–(\d+) \|", seance3, re.M)
for plages in (plages1, plages2, plages3):
    fin = 0
    for debut, arret in plages:
        assert int(debut) == fin and int(arret) > fin, plages
        fin = int(arret)
    assert fin == 120, plages
assert ("45", "85") in plages1, "40 minutes de programmation non préservées"
assert ("40", "80") in plages3, "40 minutes de TP03 non préservées"
for fichier in DOSSIER.glob("*.md"):
    for fragment in re.findall(r"```python\n(.*?)```", fichier.read_text(encoding="utf-8-sig"), re.S):
        ast.parse(fragment, filename=str(fichier))
print("JALON_S03_OK : 120 min par séance, TP01 40 min, blocs Python valides, arrêt avant S04")
print(f"DOSSIER_OK : {liens} liens locaux, syntaxe Python, 10 objectifs, 15 exercices, 5 TP, 5 départs")
