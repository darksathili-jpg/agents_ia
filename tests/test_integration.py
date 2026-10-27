"""Tests d'intégrité des deux parcours, sans solution Terminale embarquée."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'))
import runner

class IntegrationTests(unittest.TestCase):
    def test_routes_present(self):
        for path in ('index.html','site.css','premiere/index.html','premiere/engine.py','premiere/python-worker.js','terminale/index.html','terminale/runner.py','terminale/monde.py','terminale/python-worker.js'):
            with self.subTest(path=path):self.assertTrue((ROOT/path).is_file())
    def test_navigation_links(self):
        self.assertIn('href="premiere/"',(ROOT/'index.html').read_text())
        self.assertIn('href="terminale/"',(ROOT/'index.html').read_text())
        self.assertIn('../terminale/',(ROOT/'premiere/index.html').read_text())
        self.assertIn('../premiere/',(ROOT/'terminale/index.html').read_text())
    def test_wrong_code_is_rejected(self):
        src="class File:\n    def enfiler(self,x): pass\n    def defiler(self): return None\nclass AgentPlanificateur:\n    def __init__(self,position):\n        self.position=position\n        self.plan=[]\n    def planifier(self,monde,objectif):\n        return []\n    def pas_suivant(self,monde,objectif):\n        return None\n"
        out=runner.evaluate_source(src)
        self.assertEqual(len(out['results']),9)
        self.assertFalse(out['success'])
        self.assertLess(out['passed'],9)
    def test_system_exit_is_handled(self):
        out=runner.evaluate_source('raise SystemExit(4)')
        self.assertFalse(out['success'])
        self.assertIn('SystemExit',out['error'])
    def test_invalid_class_is_handled(self):
        out=runner.evaluate_source('a=1')
        self.assertFalse(out['success'])
        self.assertIn('AgentPlanificateur',out['error'])
    def test_no_reference_solution_in_public_root(self):
        self.assertFalse((ROOT/'terminale/solution_reference.py').exists())
        self.assertFalse((ROOT/'terminale/test_reference.py').exists())

if __name__=='__main__':unittest.main()
