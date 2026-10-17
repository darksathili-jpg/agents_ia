"""Tests comportementaux du jalon S03, exécutables aussi dans Pyodide."""
import unittest
from s03_tp import (episode, retenir, oublier, ecraser, mouvement,
                    choix_stochastique, serie_actions, a_completer)


class TestsS03(unittest.TestCase):
    def test_deux_mondes_et_actions(self):
        for couleur, sortie in (("bleu", "gauche"), ("orange", "droite")):
            resultat, trace = episode(retenir, couleur)
            self.assertEqual(resultat, "réussite")
            self.assertEqual([t[3] for t in trace], ["droite", "bas", sortie])
            self.assertEqual([t[4] for t in trace], [couleur] * 3)

    def test_reactif_et_ecrasement(self):
        self.assertEqual(episode(oublier, "bleu")[0], "réussite")
        self.assertEqual(episode(oublier, "orange")[0], "mauvaise sortie")
        for couleur in ("bleu", "orange"):
            resultat, trace = episode(ecraser, couleur)
            self.assertEqual(resultat, "arrêt")
            self.assertIsNone(trace[1][4])

    def test_absence_et_memoire_erronee(self):
        self.assertEqual(episode(retenir, "bleu", False)[0], "arrêt")
        self.assertEqual(episode(retenir, "orange", False, "bleu")[0], "mauvaise sortie")
        self.assertEqual(episode(retenir, "orange", True, "bleu")[0], "réussite")

    def test_mise_a_jour_et_observation_non_modifiee(self):
        observation = {"position": (1, 1), "indice": None}
        self.assertEqual(retenir(observation, "orange"), ("droite", "orange"))
        self.assertEqual(observation, {"position": (1, 1), "indice": None})

    def test_arrets_et_budgets(self):
        self.assertEqual(episode(retenir, "bleu", budget=0), ("budget épuisé", []))
        self.assertEqual(len(episode(retenir, "bleu", budget=2)[1]), 2)
        self.assertEqual(episode(a_completer, "bleu")[0], "arrêt")
        self.assertEqual(episode(lambda o, m: ("haut", m), "bleu")[0], "refus")
        for budget in (-1, 4, 1.5):
            with self.assertRaises(ValueError):
                episode(retenir, "bleu", budget=budget)

    def test_contrats_invalides(self):
        for appel in (lambda: episode(retenir, "vert"),
                      lambda: episode(retenir, "bleu", initiale="vert"),
                      lambda: episode(lambda o, m: ("voler", m), "bleu"),
                      lambda: episode(lambda o, m: ("droite", "vert"), "bleu"),
                      lambda: mouvement((9, 9), "droite")):
            with self.assertRaises(ValueError):
                appel()

    def test_politique_stochastique_transition_fixe(self):
        self.assertEqual({choix_stochastique(i) for i in (0, 1)}, {"gauche", "droite"})
        self.assertEqual(mouvement((1, 1), "gauche"), (0, 1))
        self.assertEqual(mouvement((1, 1), "droite"), (2, 1))
        self.assertEqual(serie_actions(7), serie_actions(7))
        self.assertEqual(serie_actions(7, 0), [])
        for appel in (lambda: choix_stochastique(2), lambda: serie_actions(7, -1)):
            with self.assertRaises(ValueError):
                appel()


if __name__ == "__main__":
    resultat = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(TestsS03))
    if not resultat.wasSuccessful():
        raise SystemExit(1)
    print("TESTS_S03_OK 7")
