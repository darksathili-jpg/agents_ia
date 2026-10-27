import re
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import engine
ROOT = Path(__file__).resolve().parents[1]

class StructureTests(unittest.TestCase):
    def test_all_runtime_files_exist(self):
        for name in ('index.html','styles.css','app.js','python-worker.js','engine.py','README.md','../LANCER_ORCHESTRA.cmd'):
            with self.subTest(name=name):self.assertTrue((ROOT/name).is_file())

    def test_no_fake_success_in_ui(self):
        app=(ROOT/'app.js').read_text()
        self.assertIn('data.tests.filter(t=>t.passed)',app)
        self.assertIn("worker.postMessage({type:'run'",app)
        self.assertIn("data.type === 'result'",app)

    def test_python_worker_loads_real_engine(self):
        worker=(ROOT/'python-worker.js').read_text()
        self.assertIn("fetch('engine.py'",worker)
        self.assertIn('loadPyodide',worker)
        self.assertIn('engine.evaluate_source_json(student_source)',worker)

    def test_ui_scenarios_match_engine(self):
        text=(ROOT/'app.js').read_text()
        for s in engine.SCENARIOS:
            self.assertIn("id:'"+s['id']+"'",text)
            self.assertIn('start:['+','.join(map(str,s['start']))+']',text)
            self.assertIn('goal:['+','.join(map(str,s['goal']))+']',text)
            self.assertIn('walls:['+','.join('['+','.join(map(str,w))+']' for w in s['walls'])+']',text)

    def test_three_themes_and_hidden_terrain_are_present(self):
        h=(ROOT/'index.html').read_text()
        css=(ROOT/'styles.css').read_text()
        js=(ROOT/'app.js').read_text()
        for mode in ('light','dark','projection'):
            self.assertIn(f'data-theme-choice="{mode}"',h)
        self.assertIn('body[data-theme="dark"]',css)
        self.assertIn('body[data-theme="projection"]',css)
        self.assertIn('data-scenario="3" aria-pressed="false" hidden',h)
        self.assertIn('distinctAttemptHashes.length>=2',js)
        self.assertIn('localStorage.setItem(DRAFT_KEY',js)
        self.assertIn('9 secondes',js)

    def test_html_references_present(self):
        html=(ROOT/'index.html').read_text()
        js=(ROOT/'app.js').read_text()
        ids=set(re.findall(r'\bid="([^"]+)"',html))
        used=set(re.findall(r"\$\('([^']+)'\)",js))
        self.assertFalse(used-ids,used-ids)

    def test_html_has_no_fake_test_results(self):
        html=(ROOT/'index.html').read_text()
        self.assertNotIn('Tous les tests sont réussis',html)
        self.assertIn('EN ATTENTE',html)

if __name__=='__main__':unittest.main(verbosity=2)
