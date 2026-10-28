"""G1 — tests contradictoires pour les contrats observables des deux parcours.

Ces contrôles ne démontrent ni la compréhension du BFS ni l'existence d'un
bac à sable sécurisé contre du code Python volontairement hostile.
"""
from collections import deque
from pathlib import Path
from random import Random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "premiere"))
import engine
sys.path.insert(0, str(ROOT / "terminale"))
import runner
from monde import Monde
sys.path.insert(0, str(ROOT / "qa_enseignant"))
from test_redressement import REFERENCE, FICTIVE, RECALCUL


class G1ContractTests(unittest.TestCase):
    def test_reference_terminal_passes_distinct_seeds(self):
        for seed in (0, 1, 2, 7, 42, 2026):
            with self.subTest(seed=seed):
                result = runner.evaluate_source(REFERENCE, seed)
                self.assertTrue(result["success"])
                self.assertEqual(result["passed"], 9)
                self.assertEqual(result["functional_passed"], 9)
                self.assertEqual(result["method_passed"], 9)

    def test_alternative_shortest_path_order_is_accepted(self):
        alternative = REFERENCE.replace(
            "for voisin in monde.voisins(actuel):",
            "for voisin in reversed(monde.voisins(actuel)):"
        )
        self.assertNotEqual(alternative, REFERENCE)
        for seed in (0, 7, 42):
            with self.subTest(seed=seed):
                r = runner.evaluate_source(alternative, seed)
                self.assertTrue(r["success"], [(x["id"], x["message"]) for x in r["results"] if not x["ok"]])

    def test_lifo_stack_cannot_replace_fifo(self):
        source = REFERENCE.replace(
            "return self.elements.pop(0)", "return self.elements.pop()"
        )
        self.assertNotEqual(source, REFERENCE)
        for seed in (0, 7):
            with self.subTest(seed=seed):
                r = runner.evaluate_source(source, seed)
                self.assertFalse(r["success"])
                self.assertLess(r["method_passed"], r["total"])

    def test_unused_file_is_detected_without_erasing_correct_paths(self):
        r = runner.evaluate_source(FICTIVE, 0)
        self.assertFalse(r["success"])
        self.assertEqual(r["functional_passed"], 9)
        self.assertLess(r["method_passed"], 9)
        self.assertTrue(any(x["functional_ok"] and not x["method_ok"] for x in r["results"]))

    def test_unnecessary_replanning_is_detected_separately(self):
        r = runner.evaluate_source(RECALCUL, 0)
        self.assertFalse(r["success"])
        self.assertEqual(r["functional_passed"], 9)
        self.assertLess(r["method_passed"], 9)
        self.assertTrue(any(not x["phases"]["memoire"]["ok"] for x in r["results"]))

    def test_result_aggregation_matches_per_case_phases(self):
        for source in (REFERENCE, FICTIVE, RECALCUL):
            with self.subTest(source=source[:35]):
                r = runner.evaluate_source(source, 7)
                self.assertEqual(r["passed"], sum(x["ok"] for x in r["results"]))
                self.assertEqual(r["functional_passed"], sum(x["functional_ok"] for x in r["results"]))
                self.assertEqual(r["method_passed"], sum(x["method_ok"] for x in r["results"]))
                self.assertEqual(r["success"], all(x["ok"] for x in r["results"]))
                for x in r["results"]:
                    phases = x["phases"]
                    self.assertEqual(x["functional_ok"], phases["planifier"]["ok"] and phases["pas_suivant"]["ok"])
                    self.assertEqual(x["method_ok"], phases["fifo"]["ok"] and phases["memoire"]["ok"])
                    self.assertEqual(x["ok"], x["functional_ok"] and x["method_ok"])

    def test_path_oracle_matches_independent_search_on_seeded_grids(self):
        rng = Random(1327)
        for case in range(60):
            start, goal = (0, 0), (3, 3)
            obstacles = frozenset((x, y) for y in range(4) for x in range(4)
                                  if (x, y) not in (start, goal) and rng.random() < 0.31)
            world = Monde(4, 4, obstacles)
            queue = deque([(start, 0)])
            seen = {start}
            expected = None
            while queue:
                pos, distance = queue.popleft()
                if pos == goal:
                    expected = distance
                    break
                x, y = pos
                for nxt in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
                    if nxt not in seen and world.est_libre(nxt):
                        seen.add(nxt)
                        queue.append((nxt, distance + 1))
            with self.subTest(case=case):
                self.assertEqual(runner._shortest(world, start, goal), expected)

    def test_invalid_coordinates_rejected_including_boolean(self):
        world = Monde(4, 4, ())
        for path in ([(0, 0), (1.0, 0)], [(0, 0), (True, 0)], [(0, 0), [1, 0]]):
            with self.subTest(path=path), self.assertRaisesRegex(AssertionError, "deux entiers"):
                runner._check_path(path, world, (0, 0), (3, 3))

    def test_private_imports_and_audit_attributes_rejected(self):
        for source in ("import runner", "from runner import _shortest",
                       "monde._VueMonde__audit.clear()", "import sys"):
            with self.subTest(source=source), self.assertRaises(AssertionError):
                runner._check_source(source)

    def test_premiere_safety_is_observable_in_a_real_scenario(self):
        source = """def decider(o):
    if o["arrive"]: return "STOP"
    if o["orientation"] == o["balise"]: return "AVANCER"
    return "TOURNER_DROITE"
"""
        r = engine.evaluate_source(source)
        self.assertEqual(r["status"], "complete")
        self.assertFalse(r["tests"][1]["passed"])
        self.assertFalse(r["safety"]["passed"])
        self.assertTrue(any(p["orientation"] == "E" and not p["passed"] for p in r["safety"]["probes"]))

    def test_premiere_reference_accepts_both_safe_turns_in_scenarios(self):
        def left(o):
            if o["arrive"]: return "STOP"
            if not o["devant_libre"]: return "TOURNER_GAUCHE"
            if o["orientation"] == o["balise"]: return "AVANCER"
            return "TOURNER_GAUCHE"
        for scenario in engine.SCENARIOS:
            with self.subTest(scenario=scenario["id"]):
                self.assertTrue(engine.run_scenario(left, scenario)["passed"])


if __name__ == "__main__":
    unittest.main()
