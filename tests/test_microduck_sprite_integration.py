"""Contrats de rendu Microduck : pas d'influence sur les verdicts du moteur."""
from pathlib import Path
import unittest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class SpriteIntegrationTests(unittest.TestCase):
    def test_all_four_directions_three_poses(self):
        for direction in ('north','east','south','west'):
            strip=ROOT/'assets'/f'microduck-walk-{direction}.webp'
            with self.subTest(direction=direction), Image.open(strip) as im:
                self.assertEqual(im.size,(768,256))
                self.assertEqual(im.mode,'RGBA')
            for phase in range(3):
                with self.subTest(direction=direction,pose=phase), Image.open(ROOT/'assets'/f'microduck-{direction}-{phase}.webp') as im:
                    self.assertEqual(im.size,(256,256))
                    self.assertIsNotNone(im.getchannel('A').getbbox())
    def test_engine_not_used_by_decorative_hero(self):
        for route in ('premiere','terminale'):
            js=(ROOT/route/'hero-motion.js').read_text()
            self.assertNotIn('postMessage(',js)
            self.assertIn('visibilitychange',js)
            self.assertIn('IntersectionObserver',js)
    def test_both_visualizers_use_shared_helper(self):
        self.assertIn('window.MicroduckSprite?.frame', (ROOT/'premiere/app.js').read_text())
        self.assertIn('window.MicroduckSprite?.frame', (ROOT/'terminale/app.js').read_text())
        self.assertIn('window.MicroduckSprite?.frame', (ROOT/'terminale/bfs-visualizer.js').read_text())
        for route in ('premiere','terminale'):
            self.assertIn('../shared/microduck-sprite.js',(ROOT/route/'index.html').read_text())
    def test_manifest_references_public_helper(self):
        self.assertIn("'shared/microduck-sprite.js'",(ROOT/'scripts/build_site.py').read_text())
if __name__=='__main__':unittest.main()
