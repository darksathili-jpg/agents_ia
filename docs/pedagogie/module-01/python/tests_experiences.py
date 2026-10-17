"""Validation des supports documentaires, pas des nouveaux composants web."""
import unittest
from corriges import (decider, appliquer, executer, MURS, CAS, observer_case,
                      decider_memoire, episode_memoire, chemin_bfs,
                      politique_bfs, comparer, politique_aleatoire, decider_prudent)


class SupportsScientifiques(unittest.TestCase):
    def test_reactions(self):
        for position, attendu in [((0, 2), "droite"), ((4, 2), "gauche"),
                                  ((2, 1), "bas"), ((2, 3), "haut"),
                                  ((2, 2), "arrêt")]:
            self.assertEqual(decider(position, (2, 2), []), attendu)
        self.assertEqual(decider_prudent((1, 2), (6, 2), MURS), "arrêt")
        self.assertEqual(decider_prudent((0, 2), (6, 2), MURS), "droite")
        self.assertEqual(decider_prudent((6, 2), (6, 2), MURS), "arrêt")

    def test_refus_et_bord(self):
        self.assertEqual(appliquer((1, 2), "droite", MURS), ((1, 2), "refuse"))
        self.assertEqual(appliquer((0, 0), "haut", []), ((0, 0), "refuse"))
        with self.assertRaises(ValueError):
            appliquer((0, 0), "voler", [])

    def test_trace_obstacle(self):
        r = executer(decider, (0, 2), (6, 2), MURS)
        self.assertEqual((r["etat"], r["position"], r["tentatives"], r["deplacements"]),
                         ("bloque", (1, 2), 2, 1))

    def test_terminaison(self):
        self.assertEqual(executer(decider, (0, 0), (0, 0), [], 0)["etat"], "reussite")
        self.assertEqual(executer(decider, (0, 0), (6, 2), [], 0)["etat"], "limite")
        self.assertEqual(executer(lambda *args: "arrêt", (0, 0), (6, 2), [])["etat"], "arret")
        with self.assertRaises(ValueError):
            executer(decider, (-1, 0), (6, 2), [])

    def test_observation_masquee(self):
        self.assertNotEqual(observer_case((0, 0), "bleu"), observer_case((0, 0), "orange"))
        self.assertEqual(observer_case((1, 1), "bleu"), observer_case((1, 1), "orange"))
        observation = observer_case((1, 1), "bleu")
        self.assertEqual(decider_memoire(observation, "bleu")[0], "gauche")
        self.assertEqual(decider_memoire(observation, "orange")[0], "droite")
        with self.assertRaises(ValueError):
            decider_memoire(observation, None)

    def test_memoire(self):
        for indice in ["bleu", "orange"]:
            reussite, trace = episode_memoire(indice)
            self.assertTrue(reussite)
            self.assertEqual(len(trace), 3)
            self.assertIsNone(trace[-1][0]["indice"])
            self.assertEqual(trace[-1][1], indice)

    def test_bfs_oracles(self):
        for nom, depart, objectif, obstacles, longueur in CAS:
            with self.subTest(cas=nom):
                chemin = chemin_bfs(depart, objectif, obstacles)
                if longueur is None:
                    self.assertIsNone(chemin)
                else:
                    self.assertEqual(len(chemin), longueur)
                    position = depart
                    for action in chemin:
                        position, effet = appliquer(position, action, obstacles)
                        self.assertEqual(effet, "accepte")
                    self.assertEqual(position, objectif)
                    r = executer(politique_bfs, depart, objectif, obstacles)
                    self.assertEqual(r["etat"], "reussite")

    def test_tableau(self):
        lignes = comparer()
        self.assertEqual(len(lignes), 12)
        self.assertEqual(sum(l[2] == "reussite" for l in lignes if l[0] == "bfs"), 5)
        self.assertEqual(sum(l[2] == "reussite" for l in lignes if l[0] == "locale"), 3)
        for ligne in lignes:
            self.assertEqual(ligne[-1], 0 if ligne[2] == "reussite" else None)

    def test_hasard_reproductible(self):
        a = executer(politique_aleatoire(7), (0, 2), (6, 2), MURS)
        b = executer(politique_aleatoire(7), (0, 2), (6, 2), MURS)
        self.assertEqual(a, b)
        self.assertLessEqual(a["tentatives"], 35)


if __name__ == "__main__":
    resultat = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(SupportsScientifiques))
    assert resultat.wasSuccessful()
    print("SUPPORTS_MODULE01_OK", resultat.testsRun)
