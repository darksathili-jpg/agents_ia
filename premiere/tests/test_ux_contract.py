"""Contrats statiques pour l'accueil pédagogique de la v2."""
import unittest
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
class UXContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT/'index.html').read_text(encoding='utf8')
        cls.js = (ROOT/'app.js').read_text(encoding='utf8')
    def test_objective_explained_before_code(self):
        h=self.html
        self.assertIn('But de la séance',h)
        self.assertIn('Pourquoi ce laboratoire ?',h)
        self.assertLess(h.index('Pourquoi ce laboratoire ?'),h.index('id="atelier"'))
    def test_llm_and_physical_device_not_faked(self):
        self.assertIn('Aucun robot physique',self.html)
        self.assertIn('agent déterministe',self.html)
        self.assertIn('un LLM',self.html)
    def test_demo_distinct_from_real_execution(self):
        self.assertIn('DÉMONSTRATION GUIDÉE · AVANT DE PROGRAMMER',self.html)
        self.assertIn('Les véritables résultats apparaîtront',self.html)
        self.assertIn('DEMO_CASES',self.js)
        self.assertIn("$('demo-next').disabled=true",self.js)
    def test_given_sprite_used_on_page_and_map(self):
        self.assertIn('src="../assets/microduck-idle-south.webp"',self.html)
        self.assertIn('avatar-${DIRECTION_SPRITES',self.js)
        for facing in ('north','south','east','west'):
            asset=ROOT/'assets'/f'avatar-{facing}.webp'
            self.assertTrue(asset.is_file(),f'{facing} manquant')
            with Image.open(asset) as image:
                self.assertEqual(image.size,(256,256))
    def test_same_engine_used(self):
        self.assertIn('new Worker(\'python-worker.js\')',self.js)
        self.assertIn("worker.postMessage({type:'run',source:code.value,id:runId})",self.js)
if __name__=='__main__':unittest.main()
