"""ORCHESTRA — moteur de référence de la séance 01.

Le moteur est déterministe. Il ne contient aucun LLM. Les décisions sont
prises par la fonction Python decider(observation) écrite par l'élève.
"""
from __future__ import annotations

import contextlib
import io
import json
import ast
import hashlib
from collections import deque

WIDTH, HEIGHT = 7, 5
DIRECTIONS = ("N", "E", "S", "O")
VECTORS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "O": (-1, 0)}
ACTIONS = ("AVANCER", "TOURNER_DROITE", "TOURNER_GAUCHE", "STOP")
MAX_STEPS = 48
# Empreinte structurelle du programme de départ, pour ne pas compter des
# variantes purement typographiques comme un nouveau raisonnement.
STARTER_CODE = 'def decider(observation):\n    # Écris ici les conditions qui choisissent une action.\n    return "STOP"'


def ast_fingerprint(source):
    """SHA256 de l'AST Python : ignore espaces et commentaires seulement."""
    tree = ast.parse(source, filename="solution_eleve.py")
    canonical = ast.dump(tree, annotate_fields=True, include_attributes=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


SCENARIOS = (
    {"id": "direct", "name": "01 · Trajet direct", "start": (0, 2), "goal": (5, 2), "orientation": "E", "walls": ()},
    {"id": "obstacle", "name": "02 · Contourner un obstacle", "start": (0, 2), "goal": (6, 2), "orientation": "E", "walls": ((3, 2), (3, 1), (4, 1)), "dynamic_wall": (1, 2)},
    {"id": "labyrinthe", "name": "03 · Changer de direction", "start": (0, 4), "goal": (6, 0), "orientation": "N", "walls": ((2, 4), (2, 3), (2, 2), (4, 1), (4, 2), (5, 2))},
    {"id": "surprise", "name": "04 · Terrain surprise (inconnu avant le test)", "start": (0, 2), "goal": (6, 2), "orientation": "N", "walls": ((0, 1), (0, 4), (1, 3), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (6, 0), (6, 4))},
)


def is_free(x, y, walls):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT and (x, y) not in walls


def next_direction(position, goal, walls):
    """Capteur de balise : premier pas d'un plus court chemin (BFS)."""
    if position == goal:
        return None
    queue = deque([(position, None)])
    seen = {position}
    while queue:
        (x, y), first = queue.popleft()
        for direction in DIRECTIONS:
            dx, dy = VECTORS[direction]
            new = (x + dx, y + dy)
            if new in seen or not is_free(*new, walls):
                continue
            if new == goal:
                return first or direction
            seen.add(new)
            queue.append((new, first or direction))
    return None


def observation(position, orientation, goal, walls):
    dx, dy = VECTORS[orientation]
    return {
        "arrive": position == goal,
        "orientation": orientation,
        "balise": next_direction(position, goal, walls),
        "devant_libre": is_free(position[0] + dx, position[1] + dy, walls),
    }


def run_scenario(decider, scenario):
    walls = set(map(tuple, scenario["walls"]))
    position = tuple(scenario["start"])
    goal = tuple(scenario["goal"])
    orientation = scenario["orientation"]
    trace = []
    dynamic_wall = scenario.get("dynamic_wall")
    for step in range(1, MAX_STEPS + 1):
        # La balise a été calculée avec les obstacles précédemment connus.
        obs = observation(position, orientation, goal, walls)
        event = None
        # Événement dynamique unique, déterministe et visible dans la trace :
        # un obstacle est signalé entre le calcul de la balise et la décision.
        if step == 1 and dynamic_wall is not None:
            walls.add(tuple(dynamic_wall))
            dx, dy = VECTORS[orientation]
            obs["devant_libre"] = is_free(position[0] + dx, position[1] + dy, walls)
            event = "Obstacle apparu : la balise précédente peut être périmée."
        before = {"x": position[0], "y": position[1], "orientation": orientation}
        try:
            action = decider(dict(obs))
        except BaseException as exc:
            return {"passed": False, "reason": f"Erreur Python : {type(exc).__name__} — {exc}", "trace": trace}
        if type(action) is not str or action not in ACTIONS:
            trace.append({"step": step, "observation": obs, "before": before, "action": repr(action)[:90], "after": before, "outcome": "Action non autorisée", "walls": sorted(walls), "world_event": event})
            return {"passed": False, "reason": "L'agent doit renvoyer une des quatre actions autorisées.", "trace": trace}
        outcome = ""
        if action == "STOP":
            success = position == goal
            outcome = "Objectif atteint : arrêt validé" if success else "Arrêt prématuré"
            trace.append({"step": step, "observation": obs, "before": before, "action": action, "after": before, "outcome": outcome, "walls": sorted(walls), "world_event": event})
            return {"passed": success, "reason": outcome, "trace": trace}
        if position == goal:
            trace.append({"step": step, "observation": obs, "before": before, "action": action, "after": before, "outcome": "L'agent doit s'arrêter sur la cible", "walls": sorted(walls), "world_event": event})
            return {"passed": False, "reason": "Sur la cible, l'action attendue est STOP.", "trace": trace}
        if action == "TOURNER_DROITE":
            orientation = DIRECTIONS[(DIRECTIONS.index(orientation) + 1) % 4]
            outcome = "Rotation de 90° à droite"
        elif action == "TOURNER_GAUCHE":
            orientation = DIRECTIONS[(DIRECTIONS.index(orientation) - 1) % 4]
            outcome = "Rotation de 90° à gauche"
        elif action == "AVANCER":
            dx, dy = VECTORS[orientation]
            new_position = (position[0] + dx, position[1] + dy)
            if not is_free(*new_position, walls):
                trace.append({"step": step, "observation": obs, "before": before, "action": action, "after": before, "outcome": "Collision ou sortie du terrain", "walls": sorted(walls), "world_event": event})
                return {"passed": False, "reason": "Déplacement refusé : obstacle ou limite du terrain.", "trace": trace}
            position = new_position
            outcome = "Déplacement autorisé"
        after = {"x": position[0], "y": position[1], "orientation": orientation}
        trace.append({"step": step, "observation": obs, "before": before, "action": action, "after": after, "outcome": outcome, "walls": sorted(walls), "world_event": event})
    return {"passed": False, "reason": "Limite de 48 décisions atteinte : l'agent ne termine pas.", "trace": trace}


def evaluate_source(source):
    if not isinstance(source, str) or len(source) > 8000:
        return {"status": "error", "error": "Code absent ou trop long (maximum 8 000 caractères)."}
    try:
        compiled = compile(source, "solution_eleve.py", "exec")
        code_fingerprint = ast_fingerprint(source)
    except SyntaxError as exc:
        return {"status": "error", "error": f"Syntaxe Python, ligne {exc.lineno} : {exc.msg}"}
    tests = []
    output = io.StringIO()
    for scenario in SCENARIOS:
        namespace = {"__name__": "__student__"}
        try:
            with contextlib.redirect_stdout(output):
                exec(compiled, namespace, namespace)
            decider = namespace.get("decider")
            if not callable(decider):
                return {"status": "error", "error": "Définis une fonction decider(observation)."}
            with contextlib.redirect_stdout(output):
                result = run_scenario(decider, scenario)
        except BaseException as exc:
            result = {"passed": False, "reason": f"Erreur Python : {type(exc).__name__} — {exc}", "trace": []}
        tests.append({"id": scenario["id"], "name": scenario["name"], "passed": result["passed"], "reason": result["reason"], "steps": len(result["trace"]), "trace": result["trace"], "scenario": scenario})
    # Matrice de sûreté : quatre orientations × quatre indications de balise.
    # Ce test de fonction n'est pas un terrain supplémentaire, et aucun nombre
    # fini de sondes ne démontre la sûreté pour tout programme arbitraire.
    probes = []
    for orientation in DIRECTIONS:
        for balise in DIRECTIONS:
            probe_observation = {"arrive": False, "orientation": orientation,
                                 "balise": balise, "devant_libre": False}
            try:
                namespace = {"__name__": "__student__"}
                with contextlib.redirect_stdout(output):
                    exec(compiled, namespace, namespace)
                    action = namespace["decider"](dict(probe_observation))
                passed = type(action) is str and action in ("TOURNER_DROITE", "TOURNER_GAUCHE", "STOP")
                # Un arrêt face à un obstacle est sûr physiquement, mais n'est
                # pas une réponse correcte ici : l'objectif n'est pas atteint.
                passed = passed and action != "STOP"
                reason = ("Rotation sûre face à l'obstacle." if passed else
                          f"Devant bloqué en orientation {orientation}, balise {balise} : tourner est obligatoire.")
            except BaseException as exc:
                passed = False
                reason = f"Erreur Python dans la sonde : {type(exc).__name__} — {exc}"
            probes.append({"orientation": orientation, "balise": balise,
                           "passed": passed, "reason": reason})
    safety_passed = all(p["passed"] for p in probes)
    failed = next((p for p in probes if not p["passed"]), None)
    safety = {"name": "Sûreté · 16 observations d’obstacle", "passed": safety_passed,
              "reason": "16 orientations/balises : aucun déplacement dangereux." if safety_passed else failed["reason"],
              "probes": probes}
    return {"status": "complete", "passed": all(t["passed"] for t in tests) and safety_passed,
            "tests": tests, "safety": safety, "stdout": output.getvalue()[:800],
            "fingerprint": code_fingerprint,
            "starter_fingerprint": ast_fingerprint(STARTER_CODE)}


def evaluate_source_json(source):
    return json.dumps(evaluate_source(source), ensure_ascii=False)


REFERENCE_SOLUTION = '''def decider(observation):
    if observation["arrive"]:
        return "STOP"
    if not observation["devant_libre"]:
        return "TOURNER_DROITE"
    if observation["orientation"] == observation["balise"]:
        return "AVANCER"
    return "TOURNER_DROITE"
'''

if __name__ == "__main__":
    print(json.dumps(evaluate_source(REFERENCE_SOLUTION), ensure_ascii=False, indent=2))
