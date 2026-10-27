"""Tests anti-contournement sans intégration du corrigé Terminale au site."""
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'terminale'))
import runner
from monde import Monde

BASE='''class File:
    def __init__(self): self.elements=[]
    def enfiler(self,v): self.elements.append(v)
    def defiler(self): return self.elements.pop(0)
    def est_vide(self): return not self.elements
class AgentPlanificateur:
    def __init__(self,position):
        self.position=position
        self.plan=[]
    def planifier(self,monde,objectif):
        file=File(); file.enfiler(self.position); file.defiler()
        return []
    def pas_suivant(self,monde,objectif):
        return None
'''

class HardeningTests(unittest.TestCase):
    def test_private_evaluator_import_refused(self):
        candidate="import runner\n"+BASE
        result=runner.evaluate_source(candidate)
        self.assertFalse(result['success']);self.assertIn('Aucun import',result['error'])
    def test_module_alias_import_refused(self):
        candidate="from runner import _shortest\n"+BASE
        result=runner.evaluate_source(candidate)
        self.assertFalse(result['success']);self.assertIn('Aucun import',result['error'])
    def test_private_world_unchanged_when_view_is_modified(self):
        original=Monde(5,5,[(1,1)])
        public=runner.VueMonde(original)
        with self.assertRaises((AttributeError,TypeError)):
            public.obstacles.clear()
        # Même en bricolant l'attribut privé de la vue, la référence reste intacte.
        object.__setattr__(public,'_VueMonde__obstacles',frozenset())
        self.assertFalse(original.est_libre((1,1)))
    def test_world_view_obstacles_property_read_only(self):
        public=runner.VueMonde(Monde(3,3,[(1,1)]))
        with self.assertRaises(AttributeError):public.obstacles=set()
    def test_duplicate_fixed_grid_replaced_by_seeded_grids(self):
        self.assertEqual(len(runner.CASES),9)
        self.assertIn('blocked_start',[c['id'] for c in runner.CASES])
        self.assertIn('blocked_goal',[c['id'] for c in runner.CASES])
        self.assertNotEqual(next(c for c in runner.CASES if c['id']=='seeded')['obstacles'],
                            next(c for c in runner.CASES if c['id']=='seeded_secondary')['obstacles'])
    def test_plan_errors_separate_from_movement_errors(self):
        result=runner.evaluate_source(BASE)
        self.assertEqual(result['total'],9)
        first=result['results'][0]
        self.assertFalse(first['phases']['planifier']['ok'])
        self.assertFalse(first['phases']['pas_suivant']['ok'])
        self.assertIn('Chemin',first['message'])
        self.assertIn('Déplacements',first['message'])
    def test_importing_sys_for_monkeypatch_is_refused(self):
        result=runner.evaluate_source('import sys\n'+BASE)
        self.assertFalse(result['success'])
    def test_no_reference_answer_bundled(self):
        self.assertFalse((ROOT/'terminale/solution_reference.py').exists())
        self.assertFalse((ROOT/'tests/_reference_solution.py').exists())
    def test_worker_supports_local_distribution_then_cdn(self):
        for section in ['premiere','terminale']:
            worker=(ROOT/section/'python-worker.js').read_text()
            self.assertIn("../pyodide/",worker)
            self.assertIn('https://cdn.jsdelivr.net/pyodide/v0.27.7/full/',worker)
            self.assertIn('Pyodide',worker)
    def test_terminal_editor_scroll_fix(self):
        code=(ROOT/'terminale/app.js').read_text()
        self.assertIn("gutter.style.height=`${source.clientHeight}px`",code)
        self.assertIn('gutter.scrollTop=source.scrollTop',code)
        self.assertIn('ResizeObserver',code)

if __name__=='__main__':unittest.main()
