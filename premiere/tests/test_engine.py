import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import engine
from reference_solution import REFERENCE_SOLUTION

class EngineTests(unittest.TestCase):
    def test_reference_passes_all_scenarios(self):
        result = engine.evaluate_source(REFERENCE_SOLUTION)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(len(result['tests']), 4)
        self.assertTrue(result['safety']['passed'])
        self.assertTrue(result['passed'])
        self.assertTrue(all(t['passed'] for t in result['tests']))

    def test_trace_observations_match_state(self):
        result = engine.evaluate_source(REFERENCE_SOLUTION)
        for t in result['tests']:
            for event in t['trace']:
                self.assertEqual(event['before']['orientation'], event['observation']['orientation'])
                self.assertIn(event['action'], engine.ACTIONS)

    def test_stop_immediately_is_rejected(self):
        r = engine.evaluate_source('def decider(observation):\n    return "STOP"')
        self.assertFalse(r['passed'])
        self.assertEqual(len([t for t in r['tests'] if t['passed']]), 0)

    def test_advance_always_is_rejected(self):
        r = engine.evaluate_source('def decider(observation):\n    return "AVANCER"')
        self.assertFalse(r['passed'])

    def test_invalid_action_rejected(self):
        r = engine.evaluate_source('def decider(observation):\n    return "VITE"')
        self.assertFalse(r['passed'])
        self.assertIn('autorisée',r['tests'][0]['reason'])

    def test_boolean_action_rejected(self):
        r = engine.evaluate_source('def decider(observation):\n    return True')
        self.assertFalse(r['passed'])

    def test_missing_function(self):
        r = engine.evaluate_source('pass')
        self.assertEqual(r['status'],'error')

    def test_syntax_error(self):
        r = engine.evaluate_source('def decider(:')
        self.assertEqual(r['status'],'error')
        self.assertIn('ligne',r['error'])

    def test_source_too_long(self):
        self.assertEqual(engine.evaluate_source('x'*8001)['status'],'error')

    def test_student_exception_is_failure(self):
        r = engine.evaluate_source('def decider(observation):\n    raise ValueError("test")')
        self.assertFalse(r['passed'])
        self.assertIn('ValueError',r['tests'][0]['reason'])

    def test_sys_exit_is_caught(self):
        r=engine.evaluate_source('import sys\ndef decider(o):\n    sys.exit(0)')
        self.assertEqual(r['status'],'complete')
        self.assertIn('SystemExit',r['tests'][0]['reason'])

    def test_keyboard_interrupt_is_caught(self):
        r=engine.evaluate_source('def decider(o):\n    raise KeyboardInterrupt')
        self.assertEqual(r['status'],'complete')
        self.assertIn('KeyboardInterrupt',r['tests'][0]['reason'])

    def test_hidden_scenario_rejects_naive_wall_follower(self):
        source='''def decider(o):
    if o["arrive"]: return "STOP"
    return "AVANCER" if o["devant_libre"] else "TOURNER_DROITE"'''
        r=engine.evaluate_source(source)
        self.assertTrue(all(t['passed'] for t in r['tests'][:3]))
        self.assertFalse(r['tests'][3]['passed'])

    def test_probe_rejects_ignoring_obstacle(self):
        source='''def decider(o):
    if o["arrive"]: return "STOP"
    if o["orientation"] == o["balise"]: return "AVANCER"
    return "TOURNER_DROITE"'''
        r=engine.evaluate_source(source)
        self.assertFalse(r['tests'][1]['passed'])  # obstacle réellement apparu sur le terrain 2
        self.assertFalse(r['safety']['passed'])
        self.assertFalse(r['passed'])

    def test_all_scenarios_have_path(self):
        for s in engine.SCENARIOS:
            self.assertIsNotNone(engine.next_direction(s['start'],s['goal'],set(s['walls'])))

    def test_bfs_direct(self):
        self.assertEqual(engine.next_direction((0,2),(5,2),set()),'E')

    def test_bfs_goal(self):
        self.assertIsNone(engine.next_direction((1,1),(1,1),set()))

    def test_orientation_right_cycle(self):
        self.assertEqual(engine.DIRECTIONS,('N','E','S','O'))

    def test_determinism(self):
        a=engine.evaluate_source_json(REFERENCE_SOLUTION)
        b=engine.evaluate_source_json(REFERENCE_SOLUTION)
        self.assertEqual(a,b)

    def test_success_requires_stop(self):
        r=engine.evaluate_source('''def decider(observation):
    if observation["orientation"] == observation["balise"]:
        return "AVANCER"
    return "TOURNER_DROITE"''')
        self.assertFalse(r['passed'])

    def test_safety_probes_cover_all_orientations_and_beacons(self):
        r=engine.evaluate_source(REFERENCE_SOLUTION)
        probes=r['safety']['probes']
        self.assertEqual(len(probes),16)
        self.assertEqual({p['orientation'] for p in probes},set(engine.DIRECTIONS))
        self.assertEqual({p['balise'] for p in probes},set(engine.DIRECTIONS))
        self.assertTrue(all(p['passed'] for p in probes))

    def test_original_hardcoded_safety_observation_is_not_enough(self):
        fake = """def decider(o):
    if o['arrive']: return 'STOP'
    if o['orientation']=='E' and o['balise']=='E' and not o['devant_libre']:
        return 'TOURNER_DROITE'
    if o['orientation']==o['balise']: return 'AVANCER'
    return 'TOURNER_DROITE'"""
        r=engine.evaluate_source(fake)
        self.assertFalse(r['safety']['passed'])
        self.assertGreaterEqual(len([p for p in r['safety']['probes'] if not p['passed']]),1)

    def test_stale_beacon_is_observable_in_real_trace(self):
        r=engine.evaluate_source(REFERENCE_SOLUTION)
        trace=r['tests'][1]['trace']
        events=[e for e in trace if e.get('world_event')]
        self.assertEqual(len(events),1)
        e=events[0]
        self.assertEqual(e['observation']['balise'],'E')
        self.assertEqual(e['observation']['orientation'],'E')
        self.assertIs(e['observation']['devant_libre'],False)
        self.assertEqual(e['action'],'TOURNER_DROITE')
        self.assertIn((1,2),e['walls'])
        self.assertTrue(r['tests'][1]['passed'])

    def test_no_front_sensor_fails_in_real_world_not_only_probes(self):
        source="""def decider(o):
    if o['arrive']: return 'STOP'
    if o['orientation']==o['balise']: return 'AVANCER'
    return 'TOURNER_DROITE'"""
        r=engine.evaluate_source(source)
        self.assertFalse(r['tests'][1]['passed'])
        self.assertIn('obstacle',r['tests'][1]['reason'].lower())

    def test_world_event_determinism(self):
        a=engine.evaluate_source_json(REFERENCE_SOLUTION)
        b=engine.evaluate_source_json(REFERENCE_SOLUTION)
        self.assertEqual(a,b)

    def test_ast_signature_ignores_comments_and_whitespace(self):
        a='def decider(o):\n    return "STOP"\n'
        b='def decider(o):\n\n    # simple commentaire\n        return "STOP"   \n'
        self.assertEqual(engine.ast_fingerprint(a),engine.ast_fingerprint(b))

    def test_ast_signature_detects_real_logic_change(self):
        a='def decider(o):\n    return "STOP"\n'
        b='def decider(o):\n    return "AVANCER"\n'
        self.assertNotEqual(engine.ast_fingerprint(a),engine.ast_fingerprint(b))

    def test_reference_signature_differs_from_starter(self):
        r=engine.evaluate_source(REFERENCE_SOLUTION)
        self.assertEqual(r['starter_fingerprint'],engine.ast_fingerprint(engine.STARTER_CODE))
        self.assertEqual(r['fingerprint'],engine.ast_fingerprint(REFERENCE_SOLUTION))
        self.assertNotEqual(r['fingerprint'],r['starter_fingerprint'])

    def test_no_reachable_goal(self):
        walls={(1,0),(0,1)}
        self.assertIsNone(engine.next_direction((0,0),(2,2),walls))

    def test_turning_left_valid(self):
        def decider(o):
            if o['arrive']: return 'STOP'
            if not o['devant_libre']: return 'TOURNER_GAUCHE'
            if o['orientation'] == o['balise']: return 'AVANCER'
            return 'TOURNER_GAUCHE'
        self.assertTrue(all(engine.run_scenario(decider,s)['passed'] for s in engine.SCENARIOS))

if __name__=='__main__':unittest.main(verbosity=2)
