"""Audit enseignant T05 : références, faux rapport et preuves indépendantes.
La référence reste dans qa_enseignant, exclu du site élève.
"""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'/'t05'))
import runner_t05

REFERENCE = '''def controler_mission(mission, rapport, registre):
    def decision(etat, raison):
        return {"etat":etat,"motif":raison}

    if type(mission) is not dict or set(mission) != {
        "revision","fichiers_autorises","tests_requis",
        "approbation_requise","decision_humaine"
    }:
        return decision("BLOQUÉE","Mission incorrecte")
    if type(rapport) is not dict or set(rapport) != {
        "revision","fichiers_modifies","preuves","succes_annonce"
    }:
        return decision("BLOQUÉE","Rapport incorrect")
    if type(registre) is not dict:
        return decision("BLOQUÉE","Registre absent")

    revision = mission["revision"]
    autorises = mission["fichiers_autorises"]
    requis = mission["tests_requis"]
    if (type(revision) is not str or not revision
        or type(autorises) is not set or type(requis) is not set
        or not requis
        or any(type(v) is not str or not v for v in autorises | requis)
        or type(mission["approbation_requise"]) is not bool
        or mission["decision_humaine"] not in (None, True, False)):
        return decision("BLOQUÉE","Contrat de la mission incorrect")

    if (type(rapport["revision"]) is not str
        or rapport["revision"] != revision
        or type(rapport["succes_annonce"]) is not bool
        or rapport["succes_annonce"] is not True):
        return decision("BLOQUÉE","Rapport non conforme à la révision")

    fichiers = rapport["fichiers_modifies"]
    if (type(fichiers) is not list or not fichiers
        or any(type(f) is not str or not f for f in fichiers)
        or len(set(fichiers)) != len(fichiers)
        or not set(fichiers).issubset(autorises)):
        return decision("BLOQUÉE","Fichier interdit ou dupliqué")

    identifiants = rapport["preuves"]
    if (type(identifiants) is not list or not identifiants
        or any(type(p) is not str or not p for p in identifiants)
        or len(set(identifiants)) != len(identifiants)):
        return decision("BLOQUÉE","Preuves insuffisantes ou dupliquées")

    tests_valides = set()
    for identifiant in identifiants:
        preuve = registre.get(identifiant)
        if type(preuve) is not dict or set(preuve) != {"test","revision","reussi"}:
            return decision("BLOQUÉE","Preuve inconnue ou mal formée")
        if (type(preuve["test"]) is not str
            or type(preuve["revision"]) is not str
            or type(preuve["reussi"]) is not bool
            or preuve["revision"] != revision
            or preuve["reussi"] is not True
            or preuve["test"] not in requis
            or preuve["test"] in tests_valides):
            return decision("BLOQUÉE","Preuve incorrecte ou test échoué")
        tests_valides.add(preuve["test"])
    if tests_valides != requis:
        return decision("BLOQUÉE","Tests obligatoires incomplets")

    if mission["approbation_requise"]:
        if mission["decision_humaine"] is None:
            return decision("ATTENTE_HUMAINE","Accord humain nécessaire")
        if mission["decision_humaine"] is False:
            return decision("BLOQUÉE","Refus humain")
    return decision("VALIDÉE","Preuves et autorisations conformes")
'''

class T05Tests(unittest.TestCase):
    def test_reference_19_scenarios(self):
        for seed in (0,17,999,2**32-1):
            with self.subTest(seed=seed):
                result=runner_t05.evaluate_source(REFERENCE,seed)
                self.assertTrue(result["success"],result)
                self.assertEqual(result["passed"],19)
                self.assertEqual(result["total"],19)

    def test_lie_is_blocked_even_if_report_says_success(self):
        rows=runner_t05.evaluate_source(REFERENCE)["results"]
        self.assertEqual(rows[1]["trace"]["etat"],"BLOQUÉE")
        self.assertTrue(rows[1]["trace"]["reussite_annoncee"])
        self.assertEqual(rows[0]["trace"]["etat"],"VALIDÉE")

    def test_approval_cannot_be_self_declared(self):
        rows=runner_t05.evaluate_source(REFERENCE)["results"]
        self.assertEqual(rows[8]["trace"]["etat"],"ATTENTE_HUMAINE")
        self.assertEqual(rows[9]["trace"]["etat"],"BLOQUÉE")
        self.assertEqual(rows[10]["trace"]["etat"],"VALIDÉE")
        self.assertEqual(rows[11]["trace"]["etat"],"BLOQUÉE")

    def test_permissions_and_forged_evidence_fail_closed(self):
        rows=runner_t05.evaluate_source(REFERENCE)["results"]
        for i in (2,3,4,5,6,7,11,13,14,15):
            self.assertEqual(rows[i]["trace"]["etat"],"BLOQUÉE",rows[i])

    def test_missing_code_and_skeleton_do_not_pass(self):
        source=(ROOT/'terminale'/'t05'/'eleve.py').read_text(encoding='utf-8')
        self.assertEqual(runner_t05.evaluate_source(source)["passed"],0)
        self.assertFalse(runner_t05.evaluate_source("pass")["success"])

    def test_always_claim_validated_fails(self):
        cheat='def controler_mission(mission, rapport, registre):\n    return {"etat":"VALIDÉE","motif":"tout va bien"}'
        self.assertLess(runner_t05.evaluate_source(cheat)["passed"],19)

    def test_mutating_report_and_registry_is_forbidden(self):
        wrong=REFERENCE.replace('    def decision(etat, raison):',
            '    rapport["preuves"].append("fausse")\n    def decision(etat, raison):')
        result=runner_t05.evaluate_source(wrong)
        self.assertLess(result["passed"],19)

    def test_banned_import(self):
        self.assertFalse(runner_t05.evaluate_source("import os\n"+REFERENCE)["success"])

    def test_oracle_independent_of_declared_success(self):
        m,r,p=runner_t05.baseline()
        self.assertEqual(runner_t05.oracle(m,r,p),"VALIDÉE")
        p["p2"]["reussi"]=False
        self.assertEqual(runner_t05.oracle(m,r,p),"BLOQUÉE")
        p["p2"]["reussi"]=True
        m["approbation_requise"]=True
        self.assertEqual(runner_t05.oracle(m,r,p),"ATTENTE_HUMAINE")
        m["decision_humaine"]=False
        self.assertEqual(runner_t05.oracle(m,r,p),"BLOQUÉE")

if __name__=='__main__':
    unittest.main()
