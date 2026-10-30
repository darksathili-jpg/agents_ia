"""T03 — évaluation d'un agent perceptif à mémoire.
Chaque trace affichée résulte de l'exécution du code élève. Le Worker Pyodide
n'est pas un bac à sable contre du code hostile : usage scolaire supervisé.
"""
import ast
import builtins
import json

WIDTH, HEIGHT = 6, 3
DIRECTIONS = ((1, 0), (0, -1), (0, 1), (-1, 0))
CASES = (
    {"name": "Route libre", "start": (0, 1), "goal": (5, 1), "walls": ()},
    {"name": "Obstacle découvert", "start": (0, 1), "goal": (5, 1), "walls": ((3, 1),)},
    {"name": "Obstacle dès le départ", "start": (0, 1), "goal": (5, 1), "walls": ((1, 1),)},
    {"name": "Mémoire après déplacement", "start": (2, 1), "goal": (5, 1), "walls": ((3, 1),)},
    {"name": "Objectif au départ", "start": (3, 1), "goal": (3, 1), "walls": ()},
    {"name": "Agent encerclé", "start": (2, 1), "goal": (5, 1),
     "walls": ((1, 1), (3, 1), (2, 0), (2, 2))},
    {"name": "Déplacement vers l'ouest", "start": (5, 2), "goal": (0, 2), "walls": ()},
)

def valid(point):
    return (type(point) is tuple and len(point) == 2
            and type(point[0]) is int and type(point[1]) is int
            and 0 <= point[0] < WIDTH and 0 <= point[1] < HEIGHT)

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def oracle(position, goal, known):
    """Politique locale indépendante de la classe de l'élève ; pas un BFS."""
    if position == goal:
        return None
    available = []
    for dx, dy in DIRECTIONS:
        neighbor = position[0] + dx, position[1] + dy
        if valid(neighbor) and neighbor not in known:
            available.append(neighbor)
    return min(available, key=lambda p: distance(p, goal)) if available else None

def check_source(source):
    if type(source) is not str or not source.strip() or len(source) > 14000:
        raise ValueError("Le code Python est absent ou trop long (14 000 caractères maximum).")
    tree = ast.parse(source, filename="t03_eleve.py")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Aucun import n'est nécessaire dans cet atelier.")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise ValueError("Accès aux attributs spéciaux interdit.")
        if isinstance(node, ast.Name) and node.id in (
            "eval", "exec", "open", "compile", "__import__", "globals", "locals",
            "__builtins__", "getattr", "setattr", "vars",
        ):
            raise ValueError("Instruction interdite dans cet atelier.")
    return tree

SAFE = (
    "__build_class__", "object", "abs", "all", "any", "bool", "dict", "enumerate",
    "int", "len", "list", "max", "min", "range", "set", "sorted", "str",
    "sum", "tuple", "zip", "isinstance", "Exception", "ValueError",
    "TypeError", "NotImplementedError",
)

def run_case(cls, case):
    pos, goal, walls = case["start"], case["goal"], set(case["walls"])
    agent = cls(pos)
    observed = set()
    trace = []
    for step in range(15):
        visible = tuple(sorted(p for p in walls if distance(pos, p) == 1))
        observation = {"position": pos, "obstacles": visible}
        agent.percevoir(observation)
        observed.update(visible)
        if getattr(agent, "position", None) != pos:
            raise AssertionError("La méthode percevoir doit actualiser self.position.")
        memory = getattr(agent, "memoire", None)
        if type(memory) is not set or memory != observed:
            raise AssertionError("self.memoire doit être un ensemble des obstacles observés, sans oubli ni invention.")
        before = (agent.position, memory.copy())
        next_position = agent.decider(goal)
        if (agent.position, memory) != before:
            raise AssertionError("decider ne doit modifier ni la position ni la mémoire.")
        expected = oracle(pos, goal, observed)
        if next_position != expected or (next_position is not None and not valid(next_position)):
            raise AssertionError(
                "Décision incorrecte : examiner les voisins libres, puis minimiser la distance de Manhattan "
                "avec priorité Est, Nord, Sud, Ouest ; renvoyer None au but ou si aucun voisin n'est libre."
            )
        trace.append({
            "step": step, "position": list(pos),
            "visible": [list(p) for p in visible],
            "memory": [list(p) for p in sorted(memory)],
            "decision": list(next_position) if next_position is not None else None,
        })
        if next_position is None:
            return {"ok": True, "message": "Arrêt conforme : aucune action lorsque nécessaire.", "trace": trace}
        if distance(pos, next_position) != 1 or next_position in walls:
            raise AssertionError("Action bloquée : sortie du terrain, saut ou collision.")
        pos = next_position
        if pos == goal:
            # Le cycle final est observé : contrôle explicite de l'arrêt sur l'objectif.
            continue
    raise AssertionError("L'agent ne s'arrête pas en moins de 15 cycles.")

def evaluate_source(source):
    try:
        tree = check_source(source)
        safe = {key: getattr(builtins, key) for key in SAFE}
        ns = {"__builtins__": safe, "__name__": "t03_student"}
        exec(compile(tree, "t03_eleve.py", "exec"), ns)
        cls = ns.get("AgentMicroduck")
        if not isinstance(cls, type):
            raise ValueError("Définis la classe AgentMicroduck.")
        for method in ("percevoir", "decider"):
            if not callable(getattr(cls, method, None)):
                raise ValueError("Méthode manquante : " + method)
    except BaseException as exc:
        return {"success": False, "passed": 0, "total": len(CASES),
                "error": type(exc).__name__ + " : " + str(exc)[:240], "results": []}
    results = []
    for case in CASES:
        try:
            data = run_case(cls, case)
            results.append({"name": case["name"], **data})
        except BaseException as exc:
            results.append({"name": case["name"], "ok": False,
                            "message": type(exc).__name__ + " : " + str(exc)[:240],
                            "trace": []})
    passed = sum(case["ok"] for case in results)
    return {"success": passed == len(CASES), "passed": passed,
            "total": len(CASES), "results": results,
            "limits": "Contrôles fonctionnels sur sept situations ; ni preuve formelle ni environnement sécurisé."}

def evaluate_source_json(source):
    return json.dumps(evaluate_source(source), ensure_ascii=False)
