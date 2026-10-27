"""ORCHESTRA Terminale T01 — évaluateur pédagogique (CPython / Pyodide).

Important : le cloisonnement des noms et les vues du monde réduisent les
contournements accidentels ; ils ne constituent PAS un bac à sable sûr pour
du code Python hostile. Le Worker doit être utilisé sous supervision.
"""
import ast
import builtins
import json
from random import Random
from monde import Monde


def _seeded_case(seed, id, name):
    rng = Random(seed)
    blocks = [(x, y) for x in range(1, 6) for y in range(5)]
    rng.shuffle(blocks)
    # Garantit l'existence d'une route par au moins un couloir horizontal.
    obstacles = tuple(sorted(block for block in blocks[:9] if block[1] != 2))
    return {"id": id, "name": name, "width": 7, "height": 5,
            "start": (0, 2), "goal": (6, 2), "obstacles": obstacles}


CASES = [
    {"id": "direct", "name": "Trajet direct", "width": 7, "height": 5, "start": (0,2), "goal": (6,2), "obstacles": ()},
    {"id": "detour", "name": "Détour obligatoire", "width": 7, "height": 5, "start": (0,2), "goal": (6,2), "obstacles": ((3,1),(3,2),(3,3))},
    {"id": "unreachable", "name": "Cible inaccessible", "width": 3, "height": 3, "start": (0,0), "goal": (2,2), "obstacles": ((0,1),(1,0))},
    {"id": "dynamic", "name": "Obstacle imprévu", "width": 7, "height": 5, "start": (0,2), "goal": (6,2), "obstacles": (), "dynamic_at": (2,2)},
    {"id": "limit", "name": "Départ = arrivée", "width": 4, "height": 4, "start": (1,1), "goal": (1,1), "obstacles": ()},
    _seeded_case(21, "seeded", "Terrain reproductible A"),
    {"id": "blocked_start", "name": "Départ bloqué", "width": 4, "height": 4, "start": (0,0), "goal": (3,3), "obstacles": ((0,0),)},
    {"id": "blocked_goal", "name": "Cible bloquée", "width": 4, "height": 4, "start": (0,0), "goal": (3,3), "obstacles": ((3,3),)},
    _seeded_case(71, "seeded_secondary", "Terrain reproductible B"),
]


class VueMonde:
    """API consultable par l'élève, séparée du Monde de référence.

    obstacles renvoie un frozenset. Modifier l'objet élève, même en utilisant
    l'introspection, ne modifie pas le Monde contrôlé par le vérificateur.
    """
    __slots__ = ("largeur", "hauteur", "__obstacles", "__audit", "__operations")

    def __init__(self, monde, audit=None, operations=None):
        self.largeur = monde.largeur
        self.hauteur = monde.hauteur
        self.__obstacles = frozenset(monde.obstacles)
        self.__audit = audit
        self.__operations = operations

    @property
    def obstacles(self):
        return self.__obstacles

    def dans_grille(self, case):
        try:
            x, y = case
            return (type(x) is int and type(y) is int and
                    0 <= x < self.largeur and 0 <= y < self.hauteur)
        except (TypeError, ValueError):
            return False

    def est_libre(self, case):
        return self.dans_grille(case) and tuple(case) not in self.__obstacles

    def voisins(self, case):
        if self.__audit is not None:
            self.__audit.append(tuple(case))
        if self.__operations is not None:
            self.__operations.append(('voisins',tuple(case),None))
        if not self.dans_grille(case):
            return []
        x, y = case
        return [p for p in ((x,y-1),(x+1,y),(x,y+1),(x-1,y)) if self.est_libre(p)]


def _shortest(monde, start, target):
    """Oracle interne du moteur : inaccessible par l'import autorisé de l'élève."""
    if not monde.est_libre(start) or not monde.est_libre(target):
        return None
    queue = [(start, 0)]
    tete = 0
    seen = {start}
    while tete < len(queue):
        point, distance = queue[tete]
        tete += 1
        if point == target:
            return distance
        for nxt in monde.voisins(point):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt,distance+1))
    return None


def _check_path(path, world, start, target):
    if type(path) is not list:
        raise AssertionError('planifier doit renvoyer une liste de cases.')
    distance = _shortest(world,start,target)
    if distance is None:
        if path: raise AssertionError('Cible inaccessible : le chemin doit être [].')
        return
    if not path: raise AssertionError('Un chemin existe, mais planifier renvoie [].')
    if any(type(p) is not tuple or len(p)!=2 or type(p[0]) is not int or type(p[1]) is not int for p in path):
        raise AssertionError('Chaque case du chemin doit être un tuple de deux entiers (x, y).')
    if path[0]!=start or path[-1]!=target:
        raise AssertionError('Le chemin doit commencer au départ et finir à la cible.')
    if not all(world.est_libre(p) for p in path):
        raise AssertionError('Le chemin passe par une case bloquée ou hors grille.')
    if any(b not in world.voisins(a) for a,b in zip(path,path[1:])):
        raise AssertionError('Le chemin doit suivre des cases adjacentes.')
    if len(path)-1!=distance:
        raise AssertionError(f'Le chemin n’est pas minimal : attendu {distance} déplacements, obtenu {len(path)-1}.')


def _snapshot(agent, world, action, step, event=None, explored=()):
    plan = getattr(agent, 'plan', [])
    if not isinstance(plan, (tuple,list)):
        plan=[]
    return {'step':step, 'position':list(agent.position), 'action':action,
            'obstacles':[list(x) for x in sorted(world.obstacles)],
            'plan':[list(x) for x in plan if type(x) is tuple and len(x)==2][:35],
            'explored':[list(x) for x in explored][:120], 'event':event}


def _run_case(cls, case):
    """Vérifie séparément la sécurité du trajet et la réutilisation du plan.

    Les actions restent comparées au monde privé ; les règles méthodologiques
    sont consignées séparément pour ne jamais masquer une réussite de trajet.
    """
    world = Monde(case['width'], case['height'], case['obstacles'])
    start, goal = case['start'], case['goal']
    agent = cls(start)
    if not hasattr(agent, 'position') or not hasattr(agent, 'plan'):
        raise AssertionError('La classe doit posséder position et plan.')
    trace = [_snapshot(agent, world, 'DÉPART', 0)]
    original_planifier = cls.planifier
    planning = {'count': 0, 'events': []}

    def counted_planifier(self, monde, objectif):
        planning['count'] += 1
        return original_planifier(self, monde, objectif)

    # Restauré après l'épreuve, même si la solution de l'élève lève une erreur.
    cls.planifier = counted_planifier
    method_errors = []
    try:
        if not world.est_libre(start) or not world.est_libre(goal) or _shortest(world,start,goal) is None or start == goal:
            if agent.pas_suivant(VueMonde(world), goal) is not None:
                raise AssertionError('Aucun déplacement autorisé lorsque la cible est inaccessible ou déjà atteinte.')
            return {'trace': trace, 'steps': 0, 'memory_ok': True,
                    'memory_message': 'Aucun déplacement nécessaire.', 'planifications': planning['count']}
        for step in range(1, 71):
            event = None
            if case.get('dynamic_at') and step == 2:
                world.ajouter_obstacle(case['dynamic_at'])
                event = 'Obstacle apparu : le plan précédent peut être invalide.'
                trace.append(_snapshot(agent, world, 'OBSTACLE APPARU', step-1, event))
            previous = agent.position
            count_before = planning['count']
            audit = []
            moved = agent.pas_suivant(VueMonde(world, audit), goal)
            count_after = planning['count']
            if moved is None:
                if agent.position != goal:
                    raise AssertionError('Arrêt prématuré : la cible reste accessible.')
                break
            if type(moved) is not tuple or len(moved) != 2 or any(type(q) is not int for q in moved):
                raise AssertionError('pas_suivant doit renvoyer un tuple de deux entiers (x, y).')
            if moved not in world.voisins(previous):
                raise AssertionError('Collision, sortie de grille ou déplacement non adjacent.')
            if agent.position != moved:
                raise AssertionError('Actualise self.position après chaque déplacement.')
            plan = getattr(agent, 'plan', None)
            if type(plan) is not list:
                method_errors.append('self.plan doit être une liste mémorisant le trajet restant.')
            elif moved != goal:
                # La liste doit décrire un itinéraire réel et complet à partir de
                # la position actuelle (ou de la prochaine case, selon le contrat).
                remaining = list(plan) if plan and plan[0] == moved else [moved]+plan
                if not plan or remaining[-1] != goal:
                    method_errors.append('Le plan ne rejoint pas la cible.')
                elif (any(type(q) is not tuple or len(q)!=2 or
                          type(q[0]) is not int or type(q[1]) is not int for q in remaining)
                      or not all(world.est_libre(q) for q in remaining)
                      or any(b not in world.voisins(a) for a,b in zip(remaining,remaining[1:]))):
                    method_errors.append('Le plan mémorisé ne correspond pas à un trajet praticable.')
            if event and isinstance(plan, list) and case['dynamic_at'] in plan:
                method_errors.append('Plan périmé : l’obstacle apparu est encore dans self.plan.')
            if count_after == 0 and step == 1:
                method_errors.append('La méthode planifier doit être appelée pour calculer le premier chemin.')
            if step > 1 and not event and count_after != count_before:
                method_errors.append('Le plan est recalculé alors que l’environnement n’a pas changé.')
            if event and count_after == count_before:
                method_errors.append('Obstacle apparu : le plan doit être recalculé.')
            trace.append(_snapshot(agent,world,'AVANCER',step,event,explored=audit))
            if agent.position == goal:
                break
        else:
            raise AssertionError('70 décisions dépassées : la cible n’est pas atteinte.')
        if agent.position != goal:
            raise AssertionError('La cible n’est pas atteinte.')
        if agent.pas_suivant(VueMonde(world),goal) is not None:
            raise AssertionError('L’agent doit s’arrêter à la cible.')
        if planning['count'] < 1:
            method_errors.append('Aucun appel réel à planifier n’a été observé.')
        return {'trace':trace, 'steps':sum(row['action']=='AVANCER' for row in trace),
                'memory_ok':not method_errors,
                'memory_message':'; '.join(dict.fromkeys(method_errors)) or 'Plan mémorisé et réutilisé.',
                'planifications':planning['count']}
    finally:
        cls.planifier = original_planifier


def _analyze_fifo(cls_file, agent_class, case):
    """Observe les vrais appels File et monde.voisins pendant planifier.

    Ce contrat vérifie la cohérence des traces, PAS la compréhension humaine
    du BFS, ni l'impossibilité de programmes hostiles volontairement truqués.
    """
    world = Monde(case['width'], case['height'], case['obstacles'])
    start, goal = case['start'], case['goal']
    if not world.est_libre(start) or not world.est_libre(goal) or start == goal:
        return [], [], True, 'File non nécessaire pour ce cas limite.', []
    operations = []
    original_enfiler = cls_file.enfiler
    original_defiler = cls_file.defiler
    def observed_enfiler(self, valeur):
        result = original_enfiler(self, valeur)
        if len(operations) < 900:
            operations.append(('enfiler', valeur, id(self)))
        return result
    def observed_defiler(self):
        result = original_defiler(self)
        if len(operations) < 900:
            operations.append(('defiler', result, id(self)))
        return result
    cls_file.enfiler = observed_enfiler
    cls_file.defiler = observed_defiler
    explored = []
    try:
        agent = agent_class(start)
        path = agent.planifier(VueMonde(world,explored,operations),goal)
        _check_path(path,world,start,goal)
    finally:
        cls_file.enfiler = original_enfiler
        cls_file.defiler = original_defiler
    # L'expansion d'un sommet doit correspondre à un retrait réel de la file.
    if not any(op=='enfiler' for op,_,_ in operations) or not any(op=='defiler' for op,_,_ in operations):
        return explored, path, False, 'Aucun usage effectif de File pendant la recherche.', operations
    pending = {}
    last_retired = None
    valid = True
    for operation, value, instance in operations:
        if operation in ('enfiler','defiler'):
            if type(value) is not tuple or len(value)!=2 or any(type(i) is not int for i in value):
                valid = False
                continue
        if operation=='enfiler':
            pending.setdefault(instance,[]).append(value)
        elif operation=='defiler':
            queue = pending.setdefault(instance,[])
            if not queue or queue.pop(0)!=value:
                valid=False
            last_retired=value
        elif operation=='voisins':
            if last_retired != value:
                valid=False
    if not valid or not explored:
        return explored,path,False,'L’exploration des voisins ne suit pas les retraits FIFO observés.',operations
    # Une solution BFS peut dépiler l'objectif sans rechercher ses voisins.
    return explored,path,True,'Retraits FIFO et explorations de voisins cohérents.',operations


def _check_plan_separately(cls, case):
    """Conserve une validation de chemin indépendante des exigences de méthode."""
    world=Monde(case['width'],case['height'],case['obstacles'])
    start,goal=case['start'],case['goal']
    agent=cls(start)
    explored=[]
    path=agent.planifier(VueMonde(world,explored),goal)
    _check_path(path,world,start,goal)
    return explored,path


_SAFE_BUILTINS=('__build_class__', 'abs', 'all', 'any', 'bool', 'dict', 'enumerate', 'filter', 'float',
                'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'map', 'max', 'min',
                'next', 'object', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 'set',
                'slice', 'sorted', 'str', 'sum', 'super', 'tuple', 'type', 'zip',
                'Exception','ValueError','TypeError','RuntimeError','NotImplementedError',
                'AssertionError','IndexError','KeyError','StopIteration')


def _check_source(source):
    tree = ast.parse(source, filename='solution_eleve.py')
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            raise AssertionError('Aucun import n’est nécessaire : une classe File FIFO est déjà fournie.')
        if isinstance(n, ast.Attribute) and (n.attr.startswith('__') or n.attr in ('_shortest', 'evaluate_source', '__dict__')):
            raise AssertionError('Accès aux fonctions ou attributs internes interdit.')
        if isinstance(n, ast.Name) and n.id in ('runner','sys','inspect','__builtins__','__import__'):
            raise AssertionError('Le vérificateur et ses composants internes ne sont pas accessibles.')
    # Sondes structurelles seulement : elles ne démontrent PAS un véritable BFS.
    file_defined = any(isinstance(n, ast.ClassDef) and n.name == 'File' for n in tree.body)
    methods = {n.func.attr for n in ast.walk(tree)
               if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    instantiates_file = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                            and n.func.id == 'File' for n in ast.walk(tree))
    uses_fifo = file_defined and instantiates_file and {'enfiler', 'defiler'}.issubset(methods)
    return tree, uses_fifo


def _world_payload(case):
    return {'width':case['width'],'height':case['height'],'start':case['start'],
            'goal':case['goal'],'obstacles':case['obstacles']}


def evaluate_source(source):
    if not isinstance(source,str) or len(source)>20000:
        return {'success':False,'error':'Code absent ou trop long.','results':[], 'total':len(CASES),'passed':0}
    try:
        tree, structural_hint = _check_source(source)
        safe={name:getattr(builtins,name) for name in _SAFE_BUILTINS}
        ns={'__builtins__':safe,'__name__':'student_solution'}
        exec(compile(tree,'solution_eleve.py','exec'),ns)
        cls=ns.get('AgentPlanificateur')
        if not isinstance(cls,type):
            raise AssertionError('Définis une classe AgentPlanificateur.')
        file_cls=ns.get('File')
        if not isinstance(file_cls,type) or not all(callable(getattr(file_cls,n,None)) for n in ('enfiler','defiler')):
            raise AssertionError('La classe File doit posséder enfiler() et defiler().')
    except BaseException as exc:
        return {'success':False,'error':f'{type(exc).__name__} : {str(exc)[:280]}',
                'results':[], 'total':len(CASES),'passed':0}
    results=[]
    for case in CASES:
        phases={}; errors=[]; exploration=[];plan=[];fifo_operations=[]
        try:
            exploration,plan=_check_plan_separately(cls,case)
            phases['planifier']={'ok':True,'message':'Le chemin est valide et minimal.'}
        except BaseException as exc:
            msg=f'{type(exc).__name__} : {str(exc)[:190]}'
            phases['planifier']={'ok':False,'message':msg}
            errors.append('Chemin : '+msg)
        if phases['planifier']['ok']:
            try:
                observed,_,fifo_ok,fifo_msg,fifo_operations=_analyze_fifo(file_cls,cls,case)
                exploration=observed
                phases['fifo']={'ok':fifo_ok,'message':fifo_msg}
            except BaseException as exc:
                phases['fifo']={'ok':False,'message':f'{type(exc).__name__} : {str(exc)[:160]}'}
        else:
            phases['fifo']={'ok':False,'message':'Vérifie d’abord le chemin calculé.'}
        try:
            data=_run_case(cls,case)
            phases['pas_suivant']={'ok':True,'message':'Déplacements sûrs et cible atteinte.'}
            phases['memoire']={'ok':data['memory_ok'],'message':data['memory_message']}
        except BaseException as exc:
            msg=f'{type(exc).__name__} : {str(exc)[:190]}'
            phases['pas_suivant']={'ok':False,'message':msg}
            phases['memoire']={'ok':False,'message':'À vérifier après correction des déplacements.'}
            errors.append('Déplacements : '+msg)
            data={'trace':[],'steps':0,'planifications':0}
        if data['trace']:
            data['trace'][0]['explored']=[list(x) for x in exploration][:120]
            data['trace'][0]['plan']=[list(x) for x in plan if type(x) is tuple and len(x)==2][:35]
        functional_ok = phases['planifier']['ok'] and phases['pas_suivant']['ok']
        method_ok = phases['fifo']['ok'] and phases['memoire']['ok']
        all_ok = functional_ok and method_ok
        messages = errors+[f"FIFO : {phases['fifo']['message']}" for _ in [0] if not phases['fifo']['ok']]+[f"Plan : {phases['memoire']['message']}" for _ in [0] if not phases['memoire']['ok'] and phases['pas_suivant']['ok']]
        results.append({'id':case['id'],'name':case['name'], 'ok':all_ok,
                        'functional_ok':functional_ok,'method_ok':method_ok,
                        'message':' ; '.join(messages) or 'Trajet et méthode conformes aux tests.',
                        'phases':phases,'world':_world_payload(case),
                        'fifo_trace':[{'operation':op,'valeur':list(value) if type(value) is tuple else str(value)} for op,value,_ in fifo_operations if op!='voisins'][:160],
                        **data})
    return {'success':bool(results) and all(r['ok'] for r in results),
            'results':results,'total':len(results),
            'passed':sum(r['ok'] for r in results),
            'functional_passed':sum(r['functional_ok'] for r in results),
            'method_passed':sum(r['method_ok'] for r in results),
            'structure':{'fifo':structural_hint,'message':'Présence de File détectée dans le code : seul le comportement observé est évalué ; une justification humaine reste nécessaire.'},
            'limits':'Tests indicatifs, pas de preuve formelle de compréhension ni de sandbox hostile.'}


def evaluate_source_json(source):
    return json.dumps(evaluate_source(source),ensure_ascii=False)
