"""T04 — contre-exemples de sécurité, contrat et vérité des traces Python.
Référence enseignant exclue de la distribution publique.
"""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'/'t04'))
import runner_t04

REFERENCE = '''def verifier_appel(appel, permissions):
    if type(appel) is not dict or set(appel) != {"outil", "arguments"}:
        return {"statut": "REFUSÉ", "motif": "Structure invalide"}
    outil = appel["outil"]
    arguments = appel["arguments"]
    if type(outil) is not str or type(arguments) is not dict:
        return {"statut": "REFUSÉ", "motif": "Types invalides"}
    if outil not in {"observer", "avancer", "ouvrir_porte"}:
        return {"statut": "REFUSÉ", "motif": "Outil interdit"}
    if outil not in permissions:
        return {"statut": "REFUSÉ", "motif": "Droit manquant"}
    if outil == "observer":
        if arguments:
            return {"statut": "REFUSÉ", "motif": "Arguments inattendus"}
        return {"statut": "AUTORISÉ", "motif": "Observation permise"}
    if outil == "avancer":
        if set(arguments) != {"direction"}:
            return {"statut": "REFUSÉ", "motif": "Contrat incorrect"}
        direction = arguments["direction"]
        if type(direction) is not str or direction not in ("N", "E", "S", "O"):
            return {"statut": "REFUSÉ", "motif": "Direction incorrecte"}
        return {"statut": "AUTORISÉ", "motif": "Déplacement permis"}
    if set(arguments) != {"position"}:
        return {"statut": "REFUSÉ", "motif": "Contrat incorrect"}
    position = arguments["position"]
    if type(position) is not tuple or len(position) != 2:
        return {"statut": "REFUSÉ", "motif": "Position incorrecte"}
    x, y = position
    if type(x) is not int or type(y) is not int or not (0 <= x < 6 and 0 <= y < 3):
        return {"statut": "REFUSÉ", "motif": "Coordonnées incorrectes"}
    return {"statut": "ATTENTE_HUMAINE", "motif": "Décision humaine indispensable"}
'''

class T04Tests(unittest.TestCase):
    def test_reference_passes_every_case(self):
        result=runner_t04.evaluate_source(REFERENCE)
        self.assertTrue(result["success"],result)
        self.assertEqual(result["passed"],13)
        self.assertEqual(result["total"],13)

    def test_human_agreement_does_not_automatically_authorize(self):
        result=runner_t04.evaluate_source(REFERENCE)
        pending=result["results"][5]["trace"]
        denied=result["results"][6]["trace"]
        approved=result["results"][7]["trace"]
        self.assertEqual(pending["statut"],"ATTENTE_HUMAINE")
        self.assertIsNone(pending["accord_humain_simule"])
        self.assertFalse(pending["effet"])
        self.assertFalse(denied["effet"])
        self.assertTrue(approved["effet"])
        self.assertEqual(approved["apres"]["obstacles"],[])

    def test_agent_forged_approval_is_denied_even_when_human_flag_true(self):
        result=runner_t04.evaluate_source(REFERENCE)
        forged=result["results"][9]["trace"]
        self.assertEqual(forged["statut"],"REFUSÉ")
        self.assertFalse(forged["effet"])
        self.assertEqual(forged["avant"],forged["apres"])

    def test_authorized_tool_may_be_blocked_by_world(self):
        result=runner_t04.evaluate_source(REFERENCE)
        collision=result["results"][11]["trace"]
        self.assertEqual(collision["statut"],"AUTORISÉ")
        self.assertFalse(collision["effet"])
        self.assertEqual(collision["avant"]["position"],collision["apres"]["position"])
        self.assertEqual(result["results"][1]["trace"]["apres"]["position"],[1,1])

    def test_all_auto_authorized_and_all_rejected_fail(self):
        wrong='def verifier_appel(appel, permissions):\n    return {"statut":"AUTORISÉ","motif":"oui"}'
        self.assertLess(runner_t04.evaluate_source(wrong)["passed"],13)
        wrong='def verifier_appel(appel, permissions):\n    return {"statut":"REFUSÉ","motif":"non"}'
        self.assertLess(runner_t04.evaluate_source(wrong)["passed"],13)

    def test_student_skeleton_cannot_pass(self):
        src=(ROOT/'terminale'/'t04'/'eleve.py').read_text(encoding='utf-8')
        self.assertEqual(runner_t04.evaluate_source(src)["passed"],0)

    def test_illegal_import_forged_fields_and_boolean_coordinates(self):
        self.assertFalse(runner_t04.evaluate_source("import os\n"+REFERENCE)["success"])
        for idx in (9,12):
            self.assertEqual(runner_t04.expected_status(
                runner_t04.CASES[idx]["call"],set(runner_t04.CASES[idx]["rights"])),
                "REFUSÉ")

    def test_permissions_are_not_modified(self):
        wrong=REFERENCE.replace('    outil = appel["outil"]',
             '    permissions.add("ouvrir_porte")\n    outil = appel["outil"]')
        self.assertFalse(runner_t04.evaluate_source(wrong)["success"])

    def test_wrong_output_shape_is_rejected(self):
        wrong='def verifier_appel(appel, permissions):\n    return {"statut":"AUTORISÉ"}'
        self.assertEqual(runner_t04.evaluate_source(wrong)["passed"],0)

    def test_result_json_is_serializable(self):
        import json
        data=json.loads(runner_t04.evaluate_source_json(REFERENCE))
        self.assertEqual(data["total"],13)
        self.assertEqual(data["passed"],13)

if __name__=='__main__':
    unittest.main()
