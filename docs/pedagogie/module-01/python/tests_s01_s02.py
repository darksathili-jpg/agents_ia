"""Contrats et contre-exemples du jalon, à exécuter aussi dans Pyodide réel."""
import contextlib
import io
import unittest
from s01_diagnostic import choisir_x, annoncer
from s02_corrige import appliquer, appliquer_avec_glissement, essais_glissement, MURS
from s02_observation_masquee import observer, avancer, historique


class JalonS01S02(unittest.TestCase):
    def test_diagnostic(self):
        self.assertEqual([choisir_x(1, 4), choisir_x(4, 1), choisir_x(2, 2)],
                         ["droite", "gauche", "arrêt"])
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            self.assertIsNone(annoncer())
        self.assertEqual(sortie.getvalue(), "haut\n")

    def test_obstacle_trace(self):
        position, resultat = appliquer((0, 2), "droite", MURS)
        self.assertEqual((position, resultat), ((1, 2), "accepte"))
        self.assertEqual(appliquer(position, "droite", MURS), ((1, 2), "refuse"))

    def test_bords_et_arrivee(self):
        for position, action in [((0, 0), "haut"), ((0, 0), "gauche"),
                                  ((6, 4), "bas"), ((6, 4), "droite")]:
            self.assertEqual(appliquer(position, action, []), (position, "refuse"))
        self.assertEqual(appliquer((6, 2), "arrêt", MURS), ((6, 2), "arret"))

    def test_entrees_invalides(self):
        for position, action in [((-1, 0), "droite"), ((2, 2), "droite"), ((0, 2), "voler")]:
            with self.assertRaises(ValueError):
                appliquer(position, action, MURS)
        with self.assertRaises(ValueError):
            appliquer_avec_glissement((0, 2), "droite", [], 3)
        with self.assertRaises(ValueError):
            observer((2, 0), "bleu")

    def test_indiscernabilite(self):
        bleu, orange = historique("bleu"), historique("orange")
        self.assertEqual(len(bleu), 3)
        self.assertNotEqual(bleu[0], orange[0])
        self.assertEqual(bleu[1:], orange[1:])
        self.assertIsNone(bleu[-1]["indice"])
        self.assertEqual(bleu[-1]["position"], (1, 1))

    def test_contre_exemple(self):
        observation = observer((1, 1), "bleu")
        self.assertEqual(observation, observer((1, 1), "orange"))
        # Pour cette tâche de sortie immédiate, aucune action autorisée unique
        # ne garantit les deux mondes ; on ne généralise pas à toutes les tâches.
        for action in ("gauche", "droite", "bas", "haut", "arrêt"):
            finale = avancer(observation["position"], action)
            reussites = [finale == (0, 1), finale == (2, 1)]
            self.assertLessEqual(sum(reussites), 1)

    def test_stochasticite_controlee(self):
        self.assertEqual(appliquer_avec_glissement((0, 2), "droite", [], 0), ((0, 2), "patine"))
        self.assertEqual(appliquer_avec_glissement((0, 2), "droite", [], 1), ((1, 2), "accepte"))
        for tirage in (0, 1):
            self.assertEqual(appliquer_avec_glissement((1, 2), "droite", MURS, tirage), ((1, 2), "refuse"))
        self.assertEqual(essais_glissement(7), essais_glissement(7))
        self.assertEqual(len(essais_glissement(7)), 8)
        self.assertEqual(essais_glissement(7, 0), [])


if __name__ == "__main__":
    resultat = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(JalonS01S02))
    assert resultat.wasSuccessful()
    print("TESTS_S01_S02_OK", resultat.testsRun)
