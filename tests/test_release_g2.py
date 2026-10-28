"""G2 — Recette stricte du site construit, sans accès réseau.

Exige l'ancien jeu Pyodide 0.27.7 + manifeste SHA-256 pour publier.
Avec une copie dépourvue de binaires, exige l'échec fermé et laisse
les autres travaux de développement tester leurs parcours.
"""
from pathlib import Path
import importlib.util
import hashlib
import json
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("orchestra_build_site_g2", ROOT / "scripts/build_site.py")
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)


class StrictDeploymentTests(unittest.TestCase):
    def test_strict_publication_is_verifiable_or_refused(self):
        has_local = (ROOT / "pyodide" / "MANIFEST_INSTALLATION.json").is_file()
        old_output = publication.OUTPUT
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "_site"
            publication.OUTPUT = site
            try:
                if not has_local:
                    with self.assertRaisesRegex(RuntimeError, "Pyodide local absent"):
                        publication.build(require_local=True)
                    self.assertFalse(site.exists())
                    return
                report = publication.build(require_local=True)
                self.assertTrue(report["pyodide_local_verified"])
                manifest = json.loads((ROOT / "pyodide" / "MANIFEST_INSTALLATION.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["version"], "0.27.7")
                for filename, spec in manifest["files"].items():
                    with self.subTest(filename=filename):
                        actual = site / "pyodide" / filename
                        self.assertTrue(actual.is_file(), filename)
                        self.assertEqual(hashlib.sha256(actual.read_bytes()).hexdigest(), spec["sha256"])
                        self.assertEqual(actual.stat().st_size, spec["bytes"])
                for section in ("premiere", "terminale"):
                    text = (site / section / "python-worker.js").read_text(encoding="utf-8")
                    self.assertIn("const ALLOW_CDN_FALLBACK = false;", text)
                self.assertFalse((site / "premiere/tests/reference_solution.py").exists())
                self.assertFalse((site / "qa_enseignant").exists())
                self.assertFalse((site / "node_modules").exists())
                provenance = json.loads((site / "orchestra-build.json").read_text(encoding="utf-8"))
                self.assertEqual(provenance["mode"], "pyodide-local-verifie")
                self.assertRegex(provenance["source_commit"], r"^(?:[0-9a-f]{40}|inconnue)$")
                self.assertEqual(provenance["index_sha256"], hashlib.sha256((site / "index.html").read_bytes()).hexdigest())
            finally:
                publication.OUTPUT = old_output


if __name__ == "__main__":
    unittest.main()
