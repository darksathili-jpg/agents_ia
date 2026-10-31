"""T06 — audit enseignant, contre-exemples, effets nuls sans validation.
La solution témoin n'est pas publiée avec le site élève.
"""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'/'t06'))
import runner_t06

REFERENCE='''def decider_reprise(mission, incident, correctif, registre):
    def conclusion(etat, motif):
        return {"etat": etat, "motif": motif}

    if type(mission) is not dict or set(mission) != {
        "revision_cible", "fichiers_autorises", "tests_requis",
        "approbation_requise", "decision_humaine", "position_reprise"
    }:
        return conclusion("BLOQUÉE","Mission mal formée")
    if type(incident) is not dict or set(incident) != {
        "etat", "revision", "position_sure", "cause"
    }:
        return conclusion("BLOQUÉE","Incident mal formé")
    if type(correctif) is not dict or set(correctif) != {
        "revision", "fichiers_modifies", "preuves", "succes_annonce"
    }:
        return conclusion("BLOQUÉE","Correctif mal formé")
    if type(registre) is not dict:
        return conclusion("BLOQUÉE","Registre absent")

    nouvelle = mission["revision_cible"]
    ancienne = incident["revision"]
    autorises = mission["fichiers_autorises"]
    requis = mission["tests_requis"]
    if (type(nouvelle) is not str or not nouvelle
        or type(ancienne) is not str or not ancienne
        or ancienne == nouvelle
        or type(incident["cause"]) is not str or not incident["cause"]
        or incident["etat"] != "BLOQUÉE"
        or type(autorises) is not set or type(requis) is not set
        or not requis
        or any(type(v) is not str or not v for v in autorises | requis)
        or type(mission["approbation_requise"]) is not bool
        or type(mission["decision_humaine"]) not in (type(None), bool)):
        return conclusion("BLOQUÉE","Révision ou contrat invalide")

    for point in (mission["position_reprise"], incident["position_sure"]):
        if (type(point) is not tuple or len(point) != 2 or
            type(point[0]) is not int or type(point[1]) is not int or
            not (0 <= point[0] < 6 and 0 <= point[1] < 3)):
            return conclusion("BLOQUÉE","Point sûr incorrect")
    if mission["position_reprise"] != incident["position_sure"]:
        return conclusion("BLOQUÉE","Désaccord sur le point sûr")

    if (type(correctif["revision"]) is not str
        or correctif["revision"] != nouvelle
        or type(correctif["succes_annonce"]) is not bool
        or correctif["succes_annonce"] is not True):
        return conclusion("BLOQUÉE","Correctif non conforme")

    fichiers = correctif["fichiers_modifies"]
    if (type(fichiers) is not list or not fichiers
        or any(type(f) is not str or not f for f in fichiers)
        or len(set(fichiers)) != len(fichiers)
        or not set(fichiers).issubset(autorises)):
        return conclusion("BLOQUÉE","Modifications hors périmètre")

    identifiants = correctif["preuves"]
    if (type(identifiants) is not list or not identifiants
        or any(type(p) is not str or not p for p in identifiants)
        or len(set(identifiants)) != len(identifiants)):
        return conclusion("BLOQUÉE","Liste des preuves incorrecte")
    tests_ok = set()
    for identifiant in identifiants:
        preuve = registre.get(identifiant)
        if type(preuve) is not dict or set(preuve) != {"test", "revision", "reussi"}:
            return conclusion("BLOQUÉE","Preuve inconnue")
        if (type(preuve["test"]) is not str or not preuve["test"]
            or type(preuve["revision"]) is not str
            or type(preuve["reussi"]) is not bool
            or preuve["reussi"] is not True
            or preuve["revision"] != nouvelle
            or preuve["test"] not in requis or preuve["test"] in tests_ok):
            return conclusion("BLOQUÉE","Preuve périmée ou test échoué")
        tests_ok.add(preuve["test"])
    if tests_ok != requis:
        return conclusion("BLOQUÉE","Tests obligatoires incomplets")
    if mission["approbation_requise"]:
        if mission["decision_humaine"] is None:
            return conclusion("ATTENTE_HUMAINE","Approbation indépendante nécessaire")
        if mission["decision_humaine"] is False:
            return conclusion("BLOQUÉE","Refus humain")
    return conclusion("REPRISE_AUTORISÉE","Correctif vérifié sur la nouvelle révision")
'''

class T06RecoveryTests(unittest.TestCase):
    def test_reference_19_for_multiple_seeds(self):
        for seed in (0,17,4242,2**32-1):
            with self.subTest(seed=seed):
                result=runner_t06.evaluate_source(REFERENCE,seed)
                self.assertTrue(result["success"],result)
                self.assertEqual(result["passed"],19)

    def test_incident_and_stale_proof_block_reprise(self):
        rows=runner_t06.evaluate_source(REFERENCE)["results"]
        self.assertEqual(rows[0]["trace"]["etat"],"REPRISE_AUTORISÉE")
        for idx in (1,2,3,4,5,6,7,8,9,10,11,15,17):
            self.assertEqual(rows[idx]["trace"]["etat"],"BLOQUÉE",rows[idx])

    def test_human_is_independent_and_mandatory(self):
        rows=runner_t06.evaluate_source(REFERENCE)["results"]
        self.assertEqual(rows[12]["trace"]["etat"],"ATTENTE_HUMAINE")
        self.assertEqual(rows[13]["trace"]["etat"],"BLOQUÉE")
        self.assertEqual(rows[14]["trace"]["etat"],"REPRISE_AUTORISÉE")
        self.assertEqual(rows[18]["trace"]["etat"],"ATTENTE_HUMAINE")

    def test_skeleton_is_incomplete_and_cheat_does_not_pass(self):
        source=(ROOT/'terminale'/'t06'/'eleve.py').read_text(encoding='utf-8')
        self.assertEqual(runner_t06.evaluate_source(source)["passed"],0)
        cheat='def decider_reprise(mission,incident,correctif,registre):\n    return {"etat":"REPRISE_AUTORISÉE","motif":"tout va bien"}'
        self.assertLess(runner_t06.evaluate_source(cheat)["passed"],19)

    def test_student_must_not_modify_input(self):
        wrong=REFERENCE.replace('    def conclusion(etat, motif):',
          '    correctif["preuves"].append("inventée")\n    def conclusion(etat, motif):')
        self.assertEqual(runner_t06.evaluate_source(wrong)["passed"],0)

    def test_import_is_forbidden(self):
        result=runner_t06.evaluate_source("import os\n"+REFERENCE)
        self.assertFalse(result["success"])

    def test_bool_is_not_a_position(self):
        m,i,c,r=runner_t06.baseline()
        m["position_reprise"]=(False,1)
        self.assertEqual(runner_t06.oracle(m,i,c,r),"BLOQUÉE")

    def test_oracle_validates_new_revision(self):
        m,i,c,r=runner_t06.baseline()
        self.assertEqual(runner_t06.oracle(m,i,c,r),"REPRISE_AUTORISÉE")
        r["p2"]["revision"]="r1"
        self.assertEqual(runner_t06.oracle(m,i,c,r),"BLOQUÉE")

if __name__=="__main__":
    unittest.main()
