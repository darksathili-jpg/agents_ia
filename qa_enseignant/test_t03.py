"""Recette T03 : contrats de la classe, trace réelle, mémoire persistante et contre-exemples."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'/'t03'))
import runner_t03

REFERENCE = '''class AgentMicroduck:
    def __init__(self, position):
        self.position = position
        self.memoire = set()

    def percevoir(self, observation):
        self.position = observation["position"]
        for obstacle in observation["obstacles"]:
            self.memoire.add(obstacle)

    def decider(self, objectif):
        if self.position == objectif:
            return None
        x, y = self.position
        voisins = ((x+1,y),(x,y-1),(x,y+1),(x-1,y))
        possibilites = []
        for case in voisins:
            if 0 <= case[0] < 6 and 0 <= case[1] < 3 and case not in self.memoire:
                possibilites.append(case)
        if not possibilites:
            return None
        return min(possibilites,
                   key=lambda p: abs(p[0]-objectif[0])+abs(p[1]-objectif[1]))
'''

class T03AgentTests(unittest.TestCase):
    def test_reference_seven_cases(self):
        result=runner_t03.evaluate_source(REFERENCE)
        self.assertTrue(result["success"],result)
        self.assertEqual(result["passed"],7)
        self.assertEqual(result["total"],7)
        self.assertEqual(result["results"][1]["trace"][2]["position"],[2,1])
        self.assertIn([3,1],result["results"][1]["trace"][3]["memory"])
        self.assertEqual(result["results"][4]["trace"][0]["decision"],None)
        self.assertEqual(result["results"][5]["trace"][0]["decision"],None)

    def test_missing_methods_and_incorrect_code_fail_closed(self):
        source=(ROOT/'terminale'/'t03'/'eleve.py').read_text(encoding='utf-8')
        result=runner_t03.evaluate_source(source)
        self.assertFalse(result["success"])
        self.assertEqual(result["passed"],0)
        self.assertFalse(any(x["trace"] for x in result["results"]))
        self.assertEqual(runner_t03.evaluate_source("pass")["passed"],0)

    def test_memory_is_not_reset_at_each_observation(self):
        wrong=REFERENCE.replace('self.position = observation["position"]\n        for obstacle',
                                'self.position = observation["position"]\n        self.memoire = set()\n        for obstacle')
        result=runner_t03.evaluate_source(wrong)
        self.assertFalse(result["success"])
        self.assertFalse(result["results"][1]["ok"])

    def test_decision_cannot_change_position(self):
        wrong=REFERENCE.replace('return min(possibilites,',
          'self.position = (0, 0)\n        return min(possibilites,')
        self.assertFalse(runner_t03.evaluate_source(wrong)["success"])

    def test_naive_agent_cannot_ignore_obstacles(self):
        wrong=REFERENCE.replace('case not in self.memoire:', 'True:')
        result=runner_t03.evaluate_source(wrong)
        self.assertFalse(result["success"])

    def test_import_and_private_access_rejected(self):
        for bad in ('import os\n'+REFERENCE,
                    REFERENCE+'\nprint(AgentMicroduck.__mro__)'):
            self.assertFalse(runner_t03.evaluate_source(bad)["success"])

    def test_oracle_excludes_walls_and_respects_priority(self):
        self.assertEqual(runner_t03.oracle((2,1),(5,1),{(3,1)}),(2,0))
        self.assertEqual(runner_t03.oracle((3,1),(3,1),set()),None)
        self.assertEqual(runner_t03.oracle((2,1),(5,1),
            {(1,1),(3,1),(2,0),(2,2)}),None)

if __name__=='__main__':
    unittest.main()
