"""T02 — tests contradictoires et séparation des résultats élèves."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "terminale" / "t02"))
import runner_t02
sys.path.insert(0, str(ROOT / "qa_enseignant"))
from reference_t02 import REFERENCE


class T02Tests(unittest.TestCase):
    def test_reference_success_on_varied_grids(self):
        for seed in (0, 1, 2, 7, 42, 2026, 112358):
            with self.subTest(seed=seed):
                r = runner_t02.evaluate_source(REFERENCE, seed)
                self.assertTrue(r["success"], [(v["name"], v["bfs"]["message"], v["dfs"]["message"])
                                               for v in r["results"] if not v["ok"]])
                self.assertEqual(r["passed"], 7)
                self.assertTrue(any(e["op"] == "defiler" for e in r["results"][0]["bfs"]["events"]))
                self.assertTrue(any(e["op"] == "depiler" for e in r["results"][0]["dfs"]["events"]))

    def test_bad_fifo_is_rejected(self):
        wrong = REFERENCE.replace("return self.elements.pop(0)", "return self.elements.pop()")
        r = runner_t02.evaluate_source(wrong)
        self.assertFalse(r["success"])
        self.assertTrue(any(not c["bfs"]["method_ok"] for c in r["results"]))

    def test_bad_pile_is_rejected(self):
        wrong = REFERENCE.replace("return self.elements.pop()", "return self.elements.pop(0)")
        r = runner_t02.evaluate_source(wrong)
        self.assertFalse(r["success"])
        self.assertTrue(any(not c["dfs"]["method_ok"] for c in r["results"]))

    def test_fictive_fifo_and_stack_calls_are_not_enough(self):
        """Deux parcours sur listes indépendantes ne valident pas File/Pile."""
        fake = REFERENCE.replace(
            "    file = File()\n    file.enfiler(depart)\n    parents = {depart: None}\n"
            "    while not file.est_vide():\n        actuel = file.defiler()",
            "    file = File()\n    file.enfiler(depart)\n    file.defiler()\n"
            "    en_attente = [depart]\n    parents = {depart: None}\n"
            "    while en_attente:\n        actuel = en_attente.pop(0)"
        ).replace(
            "                file.enfiler(voisin)",
            "                en_attente.append(voisin)"
        ).replace(
            "    pile = Pile()\n    pile.empiler(depart)\n    parents = {depart: None}\n"
            "    while not pile.est_vide():\n        actuel = pile.depiler()",
            "    pile = Pile()\n    pile.empiler(depart)\n    pile.depiler()\n"
            "    en_attente = [depart]\n    parents = {depart: None}\n"
            "    while en_attente:\n        actuel = en_attente.pop()"
        ).replace(
            "                pile.empiler(voisin)",
            "                en_attente.append(voisin)"
        )
        self.assertNotEqual(fake, REFERENCE)
        for seed in (0, 7):
            with self.subTest(seed=seed):
                response = runner_t02.evaluate_source(fake, seed)
                self.assertEqual(response["passed"], 1)  # départ = objectif
                for case in response["results"]:
                    if case["name"] == "Départ = arrivée":
                        self.assertTrue(case["ok"])
                    elif case["name"] != "Cible isolée":
                        self.assertTrue(case["bfs"]["path_ok"])
                        self.assertTrue(case["dfs"]["path_ok"])
                        self.assertFalse(case["bfs"]["method_ok"])
                        self.assertFalse(case["dfs"]["method_ok"])

    def test_disconnected_case_uses_empty_path(self):
        g = runner_t02.make_graph(runner_t02.BASE_CASES[2]["walls"])
        a, b = runner_t02.BASE_CASES[2]["start"], runner_t02.BASE_CASES[2]["target"]
        self.assertIsNone(runner_t02.independent_shortest(g, a, b))
        r = runner_t02.evaluate_source(REFERENCE)
        c = r["results"][2]
        self.assertEqual(c["bfs"]["path"], [])
        self.assertEqual(c["dfs"]["path"], [])

    def test_start_equals_target(self):
        r = runner_t02.evaluate_source(REFERENCE)
        c = r["results"][3]
        self.assertEqual(c["bfs"]["path"], [[1, 1]])
        self.assertEqual(c["dfs"]["path"], [[1, 1]])

    def test_nonminimal_bfs_rejected(self):
        graph = runner_t02.make_graph(())
        path = [(0, 2), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (6, 2)]
        self.assertEqual(runner_t02._path_ok(path, graph, (0, 2), (6, 2), True)[0], False)
        self.assertEqual(runner_t02._path_ok(path, graph, (0, 2), (6, 2), False)[0], True)

    def test_malformed_coordinates_produce_pedagogical_feedback(self):
        graph = runner_t02.make_graph(())
        for bad in (
            [[0, 2], (6, 2)],
            [(0, 2), [1, 2], (6, 2)],
            [(0, 2), (True, 2), (6, 2)],
            [(0, 2), (1.0, 2), (6, 2)],
        ):
            with self.subTest(path=bad):
                ok, message = runner_t02._path_ok(
                    bad, graph, (0, 2), (6, 2), False
                )
                self.assertFalse(ok)
                self.assertIn("tuple de deux entiers", message)

    def test_boolean_coordinates_rejected(self):
        graph = runner_t02.make_graph(())
        path = [(0, 2), (True, 2), (6, 2)]
        self.assertFalse(runner_t02._path_ok(path, graph, (0, 2), (6, 2), False)[0])

    def test_wrong_solutions_do_not_pass(self):
        source = (ROOT / "terminale" / "t02" / "eleve.py").read_text(encoding="utf-8")
        r = runner_t02.evaluate_source(source)
        self.assertEqual(r["passed"], 0)
        self.assertFalse(r["success"])

    def test_public_site_does_not_include_reference(self):
        self.assertFalse((ROOT / "terminale" / "t02" / "reference_t02.py").exists())
        self.assertIn("terminale/t02/runner_t02.py", (ROOT / "scripts" / "build_site.py").read_text(encoding="utf-8"))

    def test_import_restriction(self):
        r = runner_t02.evaluate_source("import sys\n" + REFERENCE)
        self.assertFalse(r["success"])
        self.assertIn("Aucun import", r["error"])

    def test_invalid_seed(self):
        for seed in (-1, True, "1", 2**40):
            with self.subTest(seed=seed), self.assertRaises(ValueError):
                runner_t02.cases_for_seed(seed)

    def test_json_results(self):
        r = json.loads(runner_t02.evaluate_source_json(REFERENCE))
        self.assertEqual(r["total"], 7)
        self.assertEqual(r["passed"], 7)


if __name__ == "__main__":
    unittest.main()
