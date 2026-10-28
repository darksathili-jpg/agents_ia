"""Régression : les variantes aléatoires ne doivent PAS rejeter le BFS correct."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'terminale'))
import runner
from test_redressement import REFERENCE

class RandomizedScenarioTests(unittest.TestCase):
    def test_reference_passes_all_variants(self):
        for seed in (0,1,2,3,5,7,11,17,42,2026,12345678):
            with self.subTest(seed=seed):
                result=runner.evaluate_source(REFERENCE,variant_seed=seed)
                self.assertEqual(result['passed'],9,
                    [(r['id'],r['message']) for r in result['results'] if not r['ok']])
                self.assertEqual(result['variant_seed'],seed)

    def test_seeded_variant_has_two_real_searches(self):
        for seed in (1,5,11,42):
            report=runner.evaluate_source(REFERENCE,seed)
            dynamic=next(c for c in report['results'] if c['id']=='dynamic')
            self.assertEqual(len(dynamic['searches']),2)
            self.assertEqual(dynamic['searches'][1]['reason'],'obstacle')
            self.assertEqual(dynamic['trace'][2]['obstacles'][0],list(runner.cases_for_seed(seed)[3]['dynamic_at']))

if __name__=='__main__':unittest.main()
