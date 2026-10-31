"""T07 — référence enseignant hors site élève : preuve et séquence indépendante."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'/'t07'))
import runner_t07

REFERENCE='''def auditer_journal(mission, journal, registre):
    def sortie(etat, motif):
        return {"etat":etat,"motif":motif}

    if type(mission) is not dict or set(mission) != {
        "revision","depart","objectif","outils_autorises",
        "accord_requis","decision_humaine"
    }:
        return sortie("ANOMALIE","Mission invalide")
    if type(journal) is not list or len(journal) < 4 or type(registre) is not dict:
        return sortie("ANOMALIE","Données invalides")

    def position_valide(p):
        return (type(p) is tuple and len(p)==2
            and type(p[0]) is int and type(p[1]) is int
            and 0 <= p[0] < 6 and 0 <= p[1] < 3)

    revision=mission["revision"]
    debut=mission["depart"]
    cible=mission["objectif"]
    droits=mission["outils_autorises"]
    if (type(revision) is not str or not revision
        or not position_valide(debut) or not position_valide(cible)
        or type(droits) is not set
        or any(type(n) is not str for n in droits)
        or not {"observer","avancer"}.issubset(droits)
        or type(mission["accord_requis"]) is not bool
        or type(mission["decision_humaine"]) not in (type(None),bool)):
        return sortie("ANOMALIE","Contrat de mission invalide")

    position=debut
    precedent=None
    preuves_utilisees=set()
    nb_deplacements=0
    for numero, evenement in enumerate(journal):
        if type(evenement) is not dict or set(evenement) != {
            "sequence","type","revision","position","preuve"
        }:
            return sortie("ANOMALIE","Événement mal formé")
        genre=evenement["type"]
        point=evenement["position"]
        preuve_id=evenement["preuve"]
        if (type(evenement["sequence"]) is not int
            or evenement["sequence"] != numero
            or type(genre) is not str
            or type(evenement["revision"]) is not str
            or evenement["revision"] != revision
            or not position_valide(point)):
            return sortie("ANOMALIE","Séquence ou révision incorrecte")

        if numero == 0:
            if genre != "DEBUT" or point != debut or preuve_id is not None:
                return sortie("ANOMALIE","Départ incorrect")
        elif numero == len(journal)-1:
            if (genre != "FIN" or point != cible or
                point != position or preuve_id is not None or
                nb_deplacements == 0):
                return sortie("ANOMALIE","Fin incorrecte")
        elif genre == "OBSERVATION":
            if (point != position or preuve_id is not None
                or precedent not in ("DEBUT","DEPLACEMENT")):
                return sortie("ANOMALIE","Observation incorrecte")
        elif genre == "DEPLACEMENT":
            if (precedent != "OBSERVATION"
                or abs(position[0]-point[0])+abs(position[1]-point[1]) != 1
                or type(preuve_id) is not str or not preuve_id
                or preuve_id in preuves_utilisees):
                return sortie("ANOMALIE","Déplacement incorrect")
            preuve=registre.get(preuve_id)
            if (type(preuve) is not dict
                or set(preuve) != {"revision","outil","origine","destination","reussi"}):
                return sortie("ANOMALIE","Preuve absente")
            if (type(preuve["revision"]) is not str
                or preuve["revision"] != revision
                or preuve["outil"] != "avancer"
                or type(preuve["reussi"]) is not bool
                or preuve["reussi"] is not True
                or not position_valide(preuve["origine"])
                or not position_valide(preuve["destination"])
                or preuve["origine"] != position
                or preuve["destination"] != point):
                return sortie("ANOMALIE","Preuve non conforme")
            preuves_utilisees.add(preuve_id)
            position=point
            nb_deplacements+=1
        else:
            return sortie("ANOMALIE","Événement inconnu")
        precedent=genre

    if mission["accord_requis"]:
        if mission["decision_humaine"] is None:
            return sortie("ATTENTE_HUMAINE","Accord humain manquant")
        if mission["decision_humaine"] is False:
            return sortie("ANOMALIE","Refus humain")
    return sortie("CONFORME","Trace et preuves corroborées")
'''

class T07Tests(unittest.TestCase):
    def test_reference_19_cases_different_seeds(self):
        for seed in (0,12,555,2**32-1):
            with self.subTest(seed=seed):
                result=runner_t07.evaluate_source(REFERENCE,seed)
                self.assertTrue(result["success"],result)
                self.assertEqual(result["passed"],19)

    def test_forged_journal_is_anomalous(self):
        rows=runner_t07.evaluate_source(REFERENCE)["results"]
        self.assertEqual(rows[0]["trace"]["etat"],"CONFORME")
        for k in (1,2,3,4,5,6,7,8,9,10,11,13,15,17):
            self.assertEqual(rows[k]["trace"]["etat"],"ANOMALIE",rows[k])

    def test_human_gate_never_self_approves(self):
        rows=runner_t07.evaluate_source(REFERENCE)["results"]
        self.assertEqual(rows[12]["trace"]["etat"],"ATTENTE_HUMAINE")
        self.assertEqual(rows[13]["trace"]["etat"],"ANOMALIE")
        self.assertEqual(rows[14]["trace"]["etat"],"CONFORME")
        self.assertEqual(rows[18]["trace"]["etat"],"ATTENTE_HUMAINE")

    def test_reference_skeleton_fails(self):
        source=(ROOT/'terminale'/'t07'/'eleve.py').read_text(encoding='utf-8')
        self.assertEqual(runner_t07.evaluate_source(source)["passed"],0)

    def test_cheat_always_conform_is_rejected(self):
        code='def auditer_journal(mission,journal,registre):\n    return {"etat":"CONFORME","motif":"oui"}'
        self.assertLess(runner_t07.evaluate_source(code)["passed"],19)

    def test_mutating_inputs_not_allowed(self):
        code=REFERENCE.replace('    def sortie(etat, motif):',
            '    journal.append({"non":"autorisé"})\n    def sortie(etat, motif):')
        self.assertEqual(runner_t07.evaluate_source(code)["passed"],0)

    def test_oracle_uses_independent_proof(self):
        m,j,r=runner_t07.base()
        self.assertEqual(runner_t07.oracle(m,j,r),"CONFORME")
        r["p2"]["reussi"]=False
        self.assertEqual(runner_t07.oracle(m,j,r),"ANOMALIE")

    def test_actual_bool_invalid_coordinate(self):
        m,j,r=runner_t07.base()
        j[2]["position"]=(True,1)
        self.assertEqual(runner_t07.oracle(m,j,r),"ANOMALIE")

    def test_imports_rejected(self):
        self.assertFalse(runner_t07.evaluate_source('import os\n'+REFERENCE)["success"])

if __name__=="__main__":
    unittest.main()
