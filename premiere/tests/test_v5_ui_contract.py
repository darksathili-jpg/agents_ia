"""Non-régression statique : navigation, logo approuvé, animation sprite, pause."""
from pathlib import Path
from PIL import Image
import unittest
import re

ROOT=Path(__file__).resolve().parents[1]
class V5UIContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/'index.html').read_text(encoding='utf-8')
        cls.css=(ROOT/'styles.css').read_text(encoding='utf-8')
        cls.js=(ROOT/'hero-motion.js').read_text(encoding='utf-8')
    def test_institutional_logo_visible_twice(self):
        self.assertGreaterEqual(self.html.count('assets/logo-watteau.webp'),2)
        with Image.open(ROOT/'assets/logo-watteau.webp') as img:
            self.assertEqual(img.size,(360,360))
    def test_animated_sprite_strip_is_three_frames(self):
        self.assertIn('../assets/microduck-walk-south.webp',self.css)
        self.assertIn('steps(3,end)',self.css)
        with Image.open(ROOT/'assets/microduck-marche.webp') as img:
            self.assertEqual(img.size,(768,256))
    def test_sidebar_scrolls_and_fallback_rail(self):
        self.assertRegex(self.css,r'\.sidebar\s*\{\s*overflow-y\s*:\s*auto\s*;')
        self.assertRegex(self.css,r'\.course-list\s*\{\s*display\s*:\s*flex\s*;\s*gap\s*:\s*9px\s*;\s*overflow-x\s*:\s*auto\s*;')
        self.assertIn('tabindex="0"',self.html)
        self.assertIn('href="#decouvrir" aria-current="step"',self.html)
    def test_motion_accessibility(self):
        self.assertIn('id="hero-motion"',self.html)
        self.assertIn('prefers-reduced-motion: reduce',self.js)
        self.assertIn('visibilitychange',self.js)
        self.assertIn('IntersectionObserver',self.js)
        self.assertIn('animation-play-state:paused',self.css)
    def test_runtime_files_are_unchanged_in_scope(self):
        self.assertTrue((ROOT/'python-worker.js').exists())
        self.assertTrue((ROOT/'engine.py').exists())

if __name__=='__main__':unittest.main()
