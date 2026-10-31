"""Terminale T04 — banc de vérification des appels d'outils Microduck.

Le contrôle des autorisations appartient à l'orchestrateur, pas à l'agent.
La réponse Python de l'élève est comparée à une politique indépendante.
Un accord humain dans les tests est SIMULÉ explicitement par le banc de
vérification : aucun accord réel ni effet sur un système externe.

Worker Pyodide : usage scolaire supervisé ; ce n'est pas une sandbox.
"""
from __future__ import annotations
import ast
import builtins
import copy
import json

WIDTH, HEIGHT = 6, 3
VALID_DIRECTIONS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "O": (-1, 0)}
ALLOWED = frozenset(("observer", "avancer", "ouvrir_porte"))
STATES = frozenset(("AUTORISÉ", "ATTENTE_HUMAINE", "REFUSÉ"))

def _valid_position(pos):
    return (type(pos) is tuple and len(pos) == 2
            and all(type(n) is int for n in pos)
            and 0 <= pos[0] < WIDTH and 0 <= pos[1] < HEIGHT)

def expected_status(call, permissions):
    """Référence politique indépendante ; échoue fermé pour toute anomalie."""
    if type(call) is not dict or set(call) != {"outil", "arguments"}:
        return "REFUSÉ"
    tool, arguments = call["outil"], call["arguments"]
    if type(tool) is not str or type(arguments) is not dict:
        return "REFUSÉ"
    if tool not in ALLOWED or tool not in permissions:
        return "REFUSÉ"
    if tool == "observer":
        return "AUTORISÉ" if not arguments else "REFUSÉ"
    if tool == "avancer":
        return ("AUTORISÉ" if set(arguments) == {"direction"}
                and type(arguments["direction"]) is str
                and arguments["direction"] in VALID_DIRECTIONS else "REFUSÉ")
    if tool == "ouvrir_porte":
        return ("ATTENTE_HUMAINE" if set(arguments) == {"position"}
                and _valid_position(arguments["position"]) else "REFUSÉ")
    return "REFUSÉ"

CASES = (
    {"name":"Observation autorisée", "call":{"outil":"observer","arguments":{}},
     "rights":("observer",)},
    {"name":"Déplacement autorisé", "call":{"outil":"avancer","arguments":{"direction":"E"}},
     "rights":("avancer",)},
    {"name":"Permission absente", "call":{"outil":"avancer","arguments":{"direction":"N"}},
     "rights":("observer",)},
    {"name":"Outil inconnu", "call":{"outil":"effacer_journal","arguments":{}},
     "rights":("observer","avancer","effacer_journal")},
    {"name":"Argument invalide", "call":{"outil":"avancer","arguments":{"direction":"NORD"}},
     "rights":("avancer",)},
    {"name":"Approbation nécessaire", "call":{"outil":"ouvrir_porte","arguments":{"position":(2,1)}},
     "rights":("ouvrir_porte",), "walls":((2,1),)},
    {"name":"Refus humain", "call":{"outil":"ouvrir_porte","arguments":{"position":(2,1)}},
     "rights":("ouvrir_porte",), "walls":((2,1),), "human":False},
    {"name":"Accord humain simulé", "call":{"outil":"ouvrir_porte","arguments":{"position":(2,1)}},
     "rights":("ouvrir_porte",), "walls":((2,1),), "human":True},
    {"name":"Droit d'ouvrir absent", "call":{"outil":"ouvrir_porte","arguments":{"position":(2,1)}},
     "rights":("observer",), "walls":((2,1),), "human":True},
    {"name":"Fausse auto-approbation", "call":{"outil":"ouvrir_porte","arguments":{"position":(2,1)},
      "approuve":True}, "rights":("ouvrir_porte",), "walls":((2,1),), "human":True},
    {"name":"Téléportation interdite", "call":{"outil":"teleporter","arguments":{"position":(5,1)}},
     "rights":("teleporter","observer")},
    {"name":"Collision évitée par le monde", "call":{"outil":"avancer","arguments":{"direction":"E"}},
     "rights":("avancer",), "walls":((1,1),)},
    {"name":"Booléen interdit en coordonnée", "call":{"outil":"ouvrir_porte",
     "arguments":{"position":(True,1)}}, "rights":("ouvrir_porte",)},
)
LIMIT = 12000
SAFE = (
    "__build_class__", "object", "abs", "all", "any", "bool", "dict",
    "enumerate", "int", "isinstance", "len", "list", "max", "min",
    "range", "set", "sorted", "str", "sum", "tuple", "type", "zip",
    "Exception", "ValueError", "TypeError", "KeyError", "NotImplementedError",
)

def _checked_source(source):
    if type(source) is not str or not source.strip() or len(source) > LIMIT:
        raise ValueError("Code absent ou trop long (12 000 caractères maximum).")
    tree = ast.parse(source, filename="t04_eleve.py")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Aucun import n'est nécessaire.")
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise ValueError("Accès aux attributs internes interdit.")
        if isinstance(node, ast.Name) and node.id in (
            "exec", "eval", "compile", "open", "__import__", "globals",
            "locals", "vars", "getattr", "setattr", "__builtins__",
        ):
            raise ValueError("Instruction non autorisée pour cet atelier.")
    return tree

def _execute_world(case, status):
    """Seul le monde réalise l'effet, après la décision et l'accord éventuel."""
    position = (0, 1)
    walls = set(case.get("walls", ()))
    before = {"position": list(position), "obstacles": [list(x) for x in sorted(walls)]}
    approved = case.get("human", None)
    effective = status == "AUTORISÉ" or (status == "ATTENTE_HUMAINE" and approved is True)
    call = case["call"]
    changed = False
    if effective and call["outil"] == "avancer":
        dx, dy = VALID_DIRECTIONS[call["arguments"]["direction"]]
        candidate = position[0] + dx, position[1] + dy
        if _valid_position(candidate) and candidate not in walls:
            position = candidate
            changed = True
    elif effective and call["outil"] == "ouvrir_porte":
        wall = call["arguments"]["position"]
        if wall in walls:
            walls.remove(wall)
            changed = True
    after = {"position": list(position), "obstacles": [list(x) for x in sorted(walls)]}
    return before, after, changed

def evaluate_source(source):
    try:
        tree = _checked_source(source)
        safe = {name: getattr(builtins, name) for name in SAFE}
        ns = {"__builtins__": safe, "__name__": "t04_student"}
        exec(compile(tree, "t04_eleve.py", "exec"), ns)
        verify = ns.get("verifier_appel")
        if not callable(verify):
            raise ValueError("Définis la fonction verifier_appel(appel, permissions).")
    except BaseException as error:
        return {"success": False, "passed": 0, "total": len(CASES),
                "error": type(error).__name__ + " : " + str(error)[:240], "results": []}

    results = []
    for case in CASES:
        call = copy.deepcopy(case["call"])
        rights = set(case["rights"])
        initial_call, initial_rights = copy.deepcopy(call), rights.copy()
        expected = expected_status(initial_call, initial_rights)
        try:
            response = verify(call, rights)
            if type(response) is not dict or set(response) != {"statut", "motif"}:
                raise AssertionError("Renvoyer un dictionnaire contenant exactement statut et motif.")
            if type(response["statut"]) is not str or response["statut"] not in STATES:
                raise AssertionError("Statut attendu : AUTORISÉ, ATTENTE_HUMAINE ou REFUSÉ.")
            if type(response["motif"]) is not str or not response["motif"].strip():
                raise AssertionError("Le motif doit être une chaîne non vide.")
            if call != initial_call or rights != initial_rights:
                raise AssertionError("La vérification doit laisser l'appel et les permissions inchangés.")
            if response["statut"] != expected:
                raise AssertionError("Décision incorrecte : attendu " + expected + ".")
            before, after, changed = _execute_world(case, expected)
            results.append({"name": case["name"], "ok": True,
                            "message": "Contrat et permission vérifiés.",
                            "trace": {"appel": initial_call, "permissions": sorted(rights),
                                      "statut": response["statut"], "motif": response["motif"],
                                      "accord_humain_simule": case.get("human", None),
                                      "avant": before, "apres": after, "effet": changed}})
        except BaseException as error:
            results.append({"name": case["name"], "ok": False,
                            "message": type(error).__name__ + " : " + str(error)[:220],
                            "trace": None})
    passed = sum(item["ok"] for item in results)
    return {"success": passed == len(CASES), "passed": passed,
            "total": len(CASES), "results": results,
            "limits": "Accord humain simulé dans le banc de test. Aucune action externe, aucune sandbox de sécurité."}

def evaluate_source_json(source):
    return json.dumps(evaluate_source(source), ensure_ascii=False)
