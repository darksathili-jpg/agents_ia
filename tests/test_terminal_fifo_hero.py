"""Régressions v1.2 : exigences NSI et héros animé, sans solution de référence livrée."""
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'))
import runner

class TerminaleFIFOHeroTests(unittest.TestCase):
    def test_no_deque_in_student_entry(self):
        for file in ['terminale/eleve_a_completer.py','terminale/app.js','terminale/index.html']:
            self.assertNotIn('deque', (ROOT/file).read_text(encoding='utf-8'), file)
    def test_file_scaffold_fifo_in_actual_starter(self):
        text=(ROOT/'terminale/eleve_a_completer.py').read_text(encoding='utf-8')
        ns={}
        # Reconstitue seulement la classe File du début de fichier : pas de corrigé nécessaire.
        exec(compile(text, 'eleve_a_completer.py', 'exec'), ns)
        file=ns['File']()
        self.assertTrue(file.est_vide())
        for value in [9, 3, 7]: file.enfiler(value)
        self.assertEqual([file.defiler(),file.defiler(),file.defiler()],[9,3,7])
        self.assertTrue(file.est_vide())
    def test_reject_module_import(self):
        out=runner.evaluate_source('from collections import deque')
        self.assertFalse(out['success'])
        self.assertIn('Aucun import',out['error'])
    def test_hero_has_real_sprite_and_switch(self):
        markup=(ROOT/'terminale/index.html').read_text(encoding='utf-8')
        css=(ROOT/'terminale/styles.css').read_text(encoding='utf-8')
        js=(ROOT/'terminale/hero-motion.js').read_text(encoding='utf-8')
        self.assertIn('terminal-robot-sprite',markup)
        self.assertIn('id="hero-motion"',markup)
        self.assertIn('steps(3,end)',css)
        self.assertIn("prefers-reduced-motion",js)
        self.assertIn('IntersectionObserver',js)
        self.assertTrue((ROOT/'terminale/assets/microduck-marche.webp').is_file())
    def test_reference_cases_unchanged(self):
        self.assertEqual(len(runner.CASES),9)
        self.assertEqual([case['id'] for case in runner.CASES][:4],['direct','detour','unreachable','dynamic'])

if __name__=='__main__':unittest.main()
