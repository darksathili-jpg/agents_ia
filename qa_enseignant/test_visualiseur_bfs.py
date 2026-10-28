"""Audits d'événements v1.4. Ne pas publier cette source enseignant."""
import json, sys, unittest, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'terminale'))
import runner
from test_redressement import REFERENCE

class VisualizerTraceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = runner.evaluate_source(REFERENCE)
        cls.dynamic = next(r for r in cls.report['results'] if r['id']=='dynamic')

    def test_reference_and_two_searches(self):
        self.assertEqual(self.report['passed'],9)
        searches=self.dynamic['searches']
        self.assertEqual(len(searches),2)
        self.assertEqual([s['reason'] for s in searches],['initial','obstacle'])
        self.assertEqual(searches[1]['obstacles'],[[2,2]])
        self.assertEqual(searches[1]['start'],[1,2])
        self.assertTrue(any(e['operation']=='enfiler' for e in searches[1]['operations']))
        self.assertTrue(any(e['operation']=='defiler' for e in searches[1]['operations']))
        self.assertTrue(any(e['operation']=='voisins' for e in searches[1]['operations']))
        self.assertGreater(len(searches[1]['path']),2)

    def test_events_match_current_instrumentation(self):
        js=(ROOT/'terminale/demo-bfs.js').read_text()
        payload=json.loads(js.split('window.ORCHESTRA_DEMO_BFS = ',1)[1].rstrip(';\n'))
        for prop in ('trace','searches','world'):
            self.assertEqual(payload[prop],json.loads(json.dumps(self.dynamic[prop])))

    def test_reference_does_not_ship_in_student_code(self):
        student=(ROOT/'terminale/eleve_a_completer.py').read_text()
        self.assertIn('raise NotImplementedError',student)
        self.assertNotIn('while not file.est_vide()',student)

    def test_no_old_static_diagram(self):
        html=(ROOT/'terminale/index.html').read_text()
        self.assertNotIn('grid-before',html)
        self.assertNotIn('grid-after',html)
        for marker in ('bfs-lesson-grid','bfs-queue','bfs-mode-student','bfs-next','bfs-slider'):
            self.assertIn(marker,html)

    def test_javascript_syntax(self):
        for filename in ('terminale/app.js','terminale/bfs-visualizer.js','terminale/demo-bfs.js'):
            result=subprocess.run(['node','--check',str(ROOT/filename)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0, result.stderr)

if __name__=='__main__':unittest.main()
