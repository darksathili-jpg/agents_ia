"""Variabilité et garde-fous des scénarios du parcours Terminale."""
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'))
import runner


class DynamicCasesTests(unittest.TestCase):
    def test_default_case_unchanged_for_reproducible_guided_demo(self):
        self.assertEqual(runner.cases_for_seed(0)[3]['dynamic_at'], (2,2))
        self.assertEqual(len(runner.cases_for_seed(0)), 9)

    def test_obstacle_changes_with_seed_without_blocking_start_or_goal(self):
        variants={runner.cases_for_seed(i)[3]['dynamic_at'] for i in range(1,30)}
        self.assertGreaterEqual(len(variants),3)
        for seed in range(1,30):
            case=runner.cases_for_seed(seed)[3]
            self.assertEqual(case['id'],'dynamic')
            self.assertNotIn(case['dynamic_at'],(case['start'],case['goal']))
            self.assertEqual(case['dynamic_at'],(2,case['start'][1]))

    def test_seed_is_reproducible(self):
        for seed in [0,1,42,2026]:
            self.assertEqual(runner.cases_for_seed(seed),runner.cases_for_seed(seed))

    def test_disallow_bad_seed(self):
        for seed in ['0',True,-1,2**40]:
            with self.assertRaises(ValueError):runner.cases_for_seed(seed)

    def test_reject_access_to_private_audit_logs(self):
        code='''class AgentPlanificateur:
    def planifier(self,monde,objectif):
        monde._VueMonde__audit.clear()
        return []
'''
        with self.assertRaises(AssertionError):runner._check_source(code)

    def test_worker_passes_changing_seed(self):
        code=(ROOT/'terminale/python-worker.js').read_text(encoding='utf-8')
        self.assertIn('getRandomValues',code)
        self.assertIn('runner.evaluate_source_json(student_source,attempt_seed)',code)

if __name__=='__main__':unittest.main()
