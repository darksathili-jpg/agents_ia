"""ORCHESTRA NSI Terminale T02 — parcours de graphes et évaluation.

L'interface utilise exclusivement les résultats de l'élève pour afficher son
chemin et ses opérations File/Pile ; la démonstration guidée est distincte.

Le code élève est exécuté dans un Worker Pyodide : ce n'est PAS un bac à sable
contre du code hostile. Usage supervisé en lycée uniquement.
"""
from __future__ import annotations

import ast
import builtins
import json
from random import Random


SIZE = (7, 5)
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
BASE_CASES = (
    {"name": "Trajet direct", "walls": (), "start": (0, 2), "target": (6, 2)},
    {"name": "Détour", "walls": ((2, 2), (3, 2), (4, 2)), "start": (0, 2), "target": (6, 2)},
    {"name": "Cible isolée", "walls": ((4, 1), (5, 2), (4, 3), (3, 2)),
     "start": (0, 2), "target": (4, 2)},
    {"name": "Départ = arrivée", "walls": (), "start": (1, 1), "target": (1, 1)},
)


def is_free(p, walls, width=7, height=5):
    return (type(p) is tuple and len(p) == 2
            and type(p[0]) is int and type(p[1]) is int
            and 0 <= p[0] < width and 0 <= p[1] < height and p not in walls)


def make_graph(walls, width=7, height=5):
    walls = frozenset(map(tuple, walls))
    vertices = [(x, y) for y in range(height) for x in range(width)
                if is_free((x, y), walls, width, height)]
    return {p: [q for dx, dy in DIRECTIONS
                if (q := (p[0] + dx, p[1] + dy)) in vertices] for p in vertices}


def independent_shortest(graph, start, target):
    """Oracle indépendant, parcours en largeur avec liste et indice de tête."""
    if start not in graph or target not in graph:
        return None
    pending = [(start, 0)]
    head = 0
    discovered = {start}
    while head < len(pending):
        p, distance = pending[head]
        head += 1
        if p == target:
            return distance
        for q in graph[p]:
            if q not in discovered:
                discovered.add(q)
                pending.append((q, distance + 1))
    return None


def cases_for_seed(seed=0):
    if type(seed) is not int or seed < 0 or seed > 2**32 - 1:
        raise ValueError("Graine de contrôle incorrecte.")
    rng = Random(seed)
    cases = list(BASE_CASES)
    # Ajoute trois grilles reproductibles mais différentes d'une tentative à l'autre.
    for index in range(3):
        obstacles = set()
        for y in range(5):
            for x in range(1, 6):
                if rng.random() < (0.16 + 0.06 * index):
                    obstacles.add((x, y))
        cases.append({
            "name": f"Contrôle {index + 1}",
            "walls": tuple(sorted(obstacles)),
            "start": (0, 2),
            "target": (6, 2),
        })
    return tuple(cases)


def _check_source(source):
    if type(source) is not str or not source.strip() or len(source) > 16000:
        raise ValueError("Code Python absent ou trop long (maximum 16 000 caractères).")
    tree = ast.parse(source, filename="t02_eleve.py")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Aucun import n'est nécessaire pour cette activité.")
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise ValueError("Accès aux attributs internes interdit.")
        if isinstance(node, ast.Name) and node.id in (
            "eval", "exec", "globals", "locals", "open", "__import__", "__builtins__",
        ):
            raise ValueError("Instruction non autorisée pour cet atelier.")
    return tree


SAFE_NAMES = (
    "__build_class__", "abs", "all", "any", "bool", "dict", "enumerate", "int",
    "isinstance", "len", "list", "max", "min", "object", "range", "reversed",
    "set", "sorted", "str", "sum", "tuple", "type", "zip",
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
    "NotImplementedError",
)


def _path_ok(path, graph, start, target, require_shortest):
    if type(path) is not list:
        return False, "Le résultat doit être une liste de cases."
    distance = independent_shortest(graph, start, target)
    if distance is None:
        return (not path, "Cible inaccessible : renvoyer [].")
    if any(type(p) is not tuple or len(p) != 2
           or type(p[0]) is not int or type(p[1]) is not int for p in path):
        return False, "Chaque case doit être un tuple de deux entiers."
    if not path or path[0] != start or path[-1] != target:
        return False, "Le chemin doit relier le départ à la cible."
    if len(set(path)) != len(path):
        return False, "Le chemin ne doit pas former de boucle."
    if any(p not in graph for p in path) or any(b not in graph[a] for a, b in zip(path, path[1:])):
        return False, "Le chemin traverse un mur ou saute une case."
    if require_shortest and len(path) - 1 != distance:
        return False, f"Le BFS doit donner un chemin minimal : {distance} déplacements attendus."
    return True, "Chemin valide" + (" et minimal." if require_shortest else ".")


def _run_algorithm(namespace, name, graph, start, target, method):
    fn = namespace[name]
    cls = namespace["File" if method == "bfs" else "Pile"]
    push_name, pop_name = (("enfiler", "defiler") if method == "bfs" else ("empiler", "depiler"))
    events, shadow = [], {}
    popped_vertices, neighbor_reads = [], []
    fifo_ok = True
    old_push, old_pop = getattr(cls, push_name), getattr(cls, pop_name)

    def tracked_push(self, vertex):
        result = old_push(self, vertex)
        shadow.setdefault(id(self), []).append(vertex)
        if len(events) < 240:
            events.append({"op": push_name, "vertex": list(vertex) if type(vertex) is tuple else str(vertex)})
        return result

    def tracked_pop(self):
        nonlocal fifo_ok
        result = old_pop(self)
        q = shadow.setdefault(id(self), [])
        expected = q.pop(0 if method == "bfs" else -1) if q else None
        if expected is None or result != expected:
            fifo_ok = False
        popped_vertices.append(result)
        if len(events) < 240:
            events.append({"op": pop_name, "vertex": list(result) if type(result) is tuple else str(result)})
        return result

    class ObservedGraph(dict):
        """Observe les consultations des voisins, pas les métadonnées du graphe."""
        def __getitem__(self, vertex):
            result = super().__getitem__(vertex)
            neighbor_reads.append(vertex)
            return result

        def get(self, vertex, default=None):
            if vertex in self:
                neighbor_reads.append(vertex)
            return super().get(vertex, default)

    setattr(cls, push_name, tracked_push)
    setattr(cls, pop_name, tracked_pop)
    try:
        path = fn(ObservedGraph({p: list(v) for p, v in graph.items()}), start, target)
    finally:
        setattr(cls, push_name, old_push)
        setattr(cls, pop_name, old_pop)
    path_ok, message = _path_ok(path, graph, start, target, method == "bfs")
    distance = independent_shortest(graph, start, target)
    # Le départ et l'objectif sont deux sommets distincts : même lorsque la
    # cible est inaccessible, il faut réellement explorer pour le constater.
    needs_structure = start in graph and target in graph and start != target
    used = (any(e["op"] == push_name for e in events)
            and any(e["op"] == pop_name for e in events))
    # L'utilisation fictive d'une File/Pile isolée ne valide pas la méthode :
    # les voisins consultés doivent correspondre à des sommets retirés
    # effectivement de la structure observée. Une solution sans lecture du
    # graphe ne satisfait pas une recherche non triviale.
    exploration_correlated = (
        bool(neighbor_reads)
        and all(vertex in popped_vertices for vertex in neighbor_reads)
    )
    method_ok = fifo_ok and (
        (used and exploration_correlated) if needs_structure else True
    )
    if not method_ok:
        detail = (
            "File FIFO : les sommets dont les voisins sont lus doivent provenir "
            "des retraits réels de la file."
            if method == "bfs" else
            "Pile LIFO : les sommets dont les voisins sont lus doivent provenir "
            "des retraits réels de la pile."
        )
        message = (message + " " if message else "") + detail
    return {
        "ok": path_ok and method_ok,
        "path_ok": path_ok,
        "method_ok": method_ok,
        "message": message,
        "path": [list(p) for p in path] if type(path) is list
            and all(type(p) is tuple and len(p) == 2 for p in path) else [],
        "events": events,
        "distance": distance,
        "explored": sum(e["op"] == pop_name for e in events),
    }


def evaluate_source(source, seed=0):
    try:
        tree = _check_source(source)
        cases = cases_for_seed(seed)
        safe = {name: getattr(builtins, name) for name in SAFE_NAMES}
        ns = {"__builtins__": safe, "__name__": "t02_student"}
        exec(compile(tree, "t02_eleve.py", "exec"), ns)
        for cl, funcs in (("File", ("enfiler", "defiler")),
                          ("Pile", ("empiler", "depiler"))):
            if not isinstance(ns.get(cl), type) or not all(callable(getattr(ns[cl], f, None)) for f in funcs):
                raise ValueError(f"La classe {cl} doit définir {', '.join(funcs)}.")
        if not all(callable(ns.get(n)) for n in ("chercher_largeur", "chercher_profondeur")):
            raise ValueError("Définis chercher_largeur et chercher_profondeur.")
    except BaseException as exc:
        return {"success": False, "error": f"{type(exc).__name__} : {str(exc)[:220]}", "results": [], "total": 7, "passed": 0}

    results = []
    for case in cases:
        graph = make_graph(case["walls"])
        item = {
            "name": case["name"], "start": list(case["start"]), "target": list(case["target"]),
            "walls": [list(p) for p in case["walls"]],
        }
        for algo, name in (("bfs", "chercher_largeur"), ("dfs", "chercher_profondeur")):
            try:
                item[algo] = _run_algorithm(ns, name, graph, case["start"], case["target"], algo)
            except BaseException as exc:
                item[algo] = {"ok": False, "path_ok": False, "method_ok": False,
                              "message": f"{type(exc).__name__} : {str(exc)[:160]}",
                              "events": [], "path": [], "distance": independent_shortest(graph, case["start"], case["target"]),
                              "explored": 0}
        item["ok"] = item["bfs"]["ok"] and item["dfs"]["ok"]
        results.append(item)

    return {
        "success": all(item["ok"] for item in results),
        "passed": sum(item["ok"] for item in results), "total": len(results),
        "results": results, "seed": seed,
        "limits": "Les traces proviennent des appels File/Pile observés ; cela n'est pas une preuve formelle de BFS/DFS ni une sandbox sécurisée.",
    }


def evaluate_source_json(source, seed=0):
    return json.dumps(evaluate_source(source, seed), ensure_ascii=False)
