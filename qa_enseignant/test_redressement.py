"""Batterie contradictoire côté enseignant : à retirer d'un éventuel site public.
Aucun test ici ne prouve la compréhension du BFS ni la sécurité du sandbox.
"""
import sys,re,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'))
import runner
from monde import Monde

# Source de référence réservée à la recette : ne PAS publier comme activité élève.
REFERENCE=(ROOT/'terminale/eleve_a_completer.py').read_text()
i=REFERENCE.index('    def planifier(')
REFERENCE=REFERENCE[:i]+'''    def planifier(self, monde, objectif):
        if not monde.est_libre(self.position) or not monde.est_libre(objectif):
            return []
        file = File()
        file.enfiler(self.position)
        parent = {self.position: None}
        while not file.est_vide():
            actuel = file.defiler()
            if actuel == objectif:
                chemin=[]
                while actuel is not None:
                    chemin.append(actuel)
                    actuel=parent[actuel]
                chemin.reverse()
                return chemin
            for voisin in monde.voisins(actuel):
                if voisin not in parent:
                    parent[voisin]=actuel
                    file.enfiler(voisin)
        return []

    def pas_suivant(self, monde, objectif):
        if self.position == objectif or not monde.est_libre(self.position) or not monde.est_libre(objectif):
            return None
        if len(self.plan)<2 or self.plan[0]!=self.position or not monde.est_libre(self.plan[1]):
            self.plan=self.planifier(monde,objectif)
        if len(self.plan)<2:
            return None
        prochain=self.plan[1]
        self.position=prochain
        self.plan=self.plan[1:]
        return prochain
'''

# Indépendant de la première mutation « sans File » : ici la file est réellement
# utilisée pour BFS, mais l'agent recalcule son trajet à chaque déplacement.
RECALCUL=REFERENCE.replace('if len(self.plan)<2 or self.plan[0]!=self.position or not monde.est_libre(self.plan[1]):\n            self.plan=self.planifier(monde,objectif)', 'self.plan=self.planifier(monde,objectif)')

# Mutation : la file n'est utilisée qu'en branche morte ; parcours via liste.
FICTIVE=REFERENCE.replace('file = File()\n        file.enfiler(self.position)', 'file = File()\n        if False:\n            file.enfiler(self.position)\n            file.defiler()\n        file = []\n        file.append(self.position)').replace('while not file.est_vide():\n            actuel = file.defiler()', 'while file:\n            actuel = file.pop(0)').replace('file.enfiler(voisin)', 'file.append(voisin)')

class RedressementChecks(unittest.TestCase):
    def test_reference_9_situations(self):
        result=runner.evaluate_source(REFERENCE)
        self.assertTrue(result['success'],[(x['id'],x['message']) for x in result.get('results',[]) if not x['ok']])
        self.assertEqual(result['passed'],9)
        self.assertEqual(result['functional_passed'],9)
        self.assertEqual(result['method_passed'],9)
        self.assertTrue(any(x['fifo_trace'] for x in result['results']))
    def test_file_in_dead_branch_rejected_without_erasing_functional_success(self):
        r=runner.evaluate_source(FICTIVE)
        self.assertEqual(r['functional_passed'],9)
        self.assertLess(r['method_passed'],9)
        self.assertFalse(r['success'])
        self.assertTrue(any(x['functional_ok'] and not x['method_ok'] for x in r['results']))
        self.assertTrue(any(not x['phases']['fifo']['ok'] for x in r['results']))
    def test_replanning_at_every_step_rejected_independently(self):
        r=runner.evaluate_source(RECALCUL)
        self.assertEqual(r['functional_passed'],9)
        self.assertLess(r['method_passed'],9)
        self.assertTrue(any(x['phases']['fifo']['ok'] and not x['phases']['memoire']['ok'] for x in r['results']))
    def test_float_and_bool_coordinates_rejected(self):
        m=Monde(7,5,())
        for path in [[(0.0,2.0),(1.0,2.0)],[(True,2),(2,2)]]:
            with self.subTest(path=path),self.assertRaisesRegex(AssertionError,'deux entiers'):
                runner._check_path(path,m,(0,2),(6,2))
    def test_client_metadata_generated_from_python(self):
        text=(ROOT/'terminale/cases.js').read_text()
        value=json.loads(text.split('window.ORCHESTRA_CASES = ',1)[1].rstrip(';\n'))
        self.assertEqual(set(value),{x['id'] for x in runner.CASES})
        self.assertEqual(len(value),9)
        for case in runner.CASES:
            self.assertEqual(value[case['id']]['name'],case['name'])
            self.assertEqual(value[case['id']]['obstacles'],[list(o) for o in case['obstacles']])
        self.assertIn('9 situations d’évaluation',(ROOT/'index.html').read_text())
        self.assertIn('const TEST_TOTAL=Object.keys(CASES).length',(ROOT/'terminale/app.js').read_text())
        ids=set(re.findall(r'data-case="([^"]+)"',(ROOT/'terminale/index.html').read_text()))
        self.assertEqual(ids,set(value))
    def test_editor_starter_equals_supplied_file(self):
        js=(ROOT/'terminale/app.js').read_text()
        start=js.split('const STARTER=`',1)[1].split('`;',1)[0]
        self.assertEqual(start.strip(),(ROOT/'terminale/eleve_a_completer.py').read_text().strip())
        self.assertNotIn('bibliothèque non étudiée',start)
    def test_phases_and_trace_rendered_in_ui(self):
        js=(ROOT/'terminale/app.js').read_text()
        for string in ('FIFO observée','Plan conservé','functional_passed','method_passed','function renderFIFO()'):
            self.assertIn(string,js)
        h=(ROOT/'terminale/index.html').read_text()
        for marker in ('lesson-path-title','obstacle-demo-title','fifo-trace','score-breakdown'):
            self.assertIn(marker,h)
    def test_missing_file_is_a_clear_contract_error(self):
        source='class AgentPlanificateur:\n    def __init__(self,p):self.position=p;self.plan=[]'
        result=runner.evaluate_source(source)
        self.assertIn('File',result['error'])
    def test_runner_not_importable(self):
        result=runner.evaluate_source('import runner\n'+REFERENCE)
        self.assertFalse(result['success']);self.assertIn('Aucun import',result['error'])
    def test_source_returns_only_functional_and_method_evidence(self):
        r=runner.evaluate_source(REFERENCE)
        self.assertIn('ne',r['structure']['message']) # phrase limitative explicite
        self.assertIn('pas de preuve formelle',r['limits'])

if __name__=='__main__': unittest.main()
