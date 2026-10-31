"""Tests du périmètre élève et de la confidentialité des ressources web."""
import importlib.util
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_site', ROOT/'scripts/build_site.py')
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


class SitePublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = publication.build(require_local=False)
        cls.site = ROOT/'_site'

    def test_publication_list_is_explicit_and_small(self):
        self.assertGreater(self.report['files'], 30)
        self.assertLess(self.report['files'], 100)
        self.assertTrue((self.site/'terminale/python-worker.js').exists())
        self.assertTrue((self.site/'premiere/python-worker.js').exists())
        self.assertTrue((self.site/'terminale/bfs-visualizer.js').exists())
        self.assertTrue((self.site/'terminale/t04/runner_t04.py').exists())
        self.assertTrue((self.site/'terminale/t04/lab.js').exists())

    def test_no_teacher_data_or_build_artifacts(self):
        forbidden = ['tests','scripts','.github','RAPPORT_VALIDATION_V14.md',
                     'premiere/GUIDE_ENSEIGNANT.md','terminale/GUIDE_ENSEIGNANT.md',
                     'premiere/tests/reference_solution.py','LANCER_ORCHESTRA.cmd']
        for path in forbidden:
            with self.subTest(path=path):
                self.assertFalse((self.site/path).exists())
        for file in self.site.rglob('*'):
            if file.is_file():
                self.assertNotIn('tests', file.relative_to(self.site).parts)
                self.assertNotIn('.github', file.relative_to(self.site).parts)
                self.assertNotIn(file.suffix, ('.md','.cmd','.pyc'))

    def test_no_public_reference_solution(self):
        for relative in ['premiere/app.js','premiere/engine.py']:
            text = (self.site/relative).read_text(encoding='utf-8')
            self.assertNotIn('REFERENCE_SOLUTION',text)
            self.assertNotIn('const SOLUTION =',text)

    def test_no_google_font_request(self):
        for file in self.site.rglob('*'):
            if file.suffix in {'.css','.html'}:
                content = file.read_text(encoding='utf-8')
                self.assertNotIn('fonts.googleapis.com',content)
                self.assertNotIn('fonts.gstatic.com',content)

    def test_control_terrain_is_not_called_secret(self):
        for path in ['premiere/app.js','premiere/index.html','premiere/engine.py']:
            content=(self.site/path).read_text(encoding='utf-8').lower()
            self.assertNotIn('terrain caché',content)
            self.assertNotIn('terrain surprise',content)

    def test_css_rule_parsing_tolerates_whitespace(self):
        css = (self.site/'premiere/styles.css').read_text(encoding='utf-8')
        # Structural assertion independent of formatting of the CSS file.
        self.assertRegex(css, r'\.sidebar\s*\{\s*overflow-y\s*:\s*auto\s*;')

    def test_legacy_workflow_deploying_dot_is_rejected(self):
        old_root = publication.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / '.github' / 'workflows'
            folder.mkdir(parents=True)
            (folder / 'legacy.yml').write_text("steps:\n - uses: actions/upload-pages-artifact@v3\n   with:\n     path: '.'\n", encoding='utf-8')
            publication.ROOT = root
            try:
                with self.assertRaisesRegex(RuntimeError, 'Ancien workflow'):
                    publication.guard_legacy_deployments()
            finally:
                publication.ROOT = old_root

    def test_required_local_pyodide_fails_closed_if_missing(self):
        folder = ROOT/'pyodide'
        if (folder/'pyodide.js').exists():
            self.skipTest('La copie locale est déjà installée ; test conditionnel non applicable')
        old_output = publication.OUTPUT
        with tempfile.TemporaryDirectory() as tmp:
            publication.OUTPUT = Path(tmp) / '_site'
            try:
                with self.assertRaises(RuntimeError):
                    publication.build(require_local=True)
            finally:
                publication.OUTPUT = old_output


if __name__=='__main__':
    unittest.main()
