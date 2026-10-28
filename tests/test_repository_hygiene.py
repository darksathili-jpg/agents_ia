"""Contrôle de propreté des fichiers suivis par Git, pour la CI G0.

Ce test vérifie les artefacts générés ; il ne garantit ni la confidentialité
historique d'un dépôt public ni le bon fonctionnement de Pyodide.
"""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryHygieneTests(unittest.TestCase):
    @unittest.skipUnless((ROOT / ".git").exists(), "Contrôle réservé à une copie Git")
    def test_generated_artifacts_are_not_tracked(self):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z"],
            capture_output=True, check=True,
        )
        files = [
            p.decode("utf-8", errors="replace")
            for p in result.stdout.split(bytes([0])) if p
        ]
        unwanted = [
            path for path in files
            if path.startswith(("node_modules/", "test-results/"))
            or path.endswith((".pyc", ".pyo"))
            or "/__pycache__/" in path
            or path == "debug.log"
        ]
        self.assertEqual(
            unwanted, [], "Artefacts suivis par Git : " + ", ".join(unwanted[:20])
        )


if __name__ == "__main__":
    unittest.main()
