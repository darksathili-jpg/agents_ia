"""T06 — reprise contrôlée après incident, avec preuves nouvelles et point sûr.

Source indépendante : registre préparé par le banc de vérification.
Pas d'action externe, pas de preuve cryptographique, pas de sandbox hostile.
"""
import ast
import builtins
import copy
import json
from random import Random

ETATS=("BLOQUÉE","ATTENTE_HUMAINE","REPRISE_AUTORISÉE")
MISSION_KEYS={"revision_cible","fichiers_autorises","tests_requis",
              "approbation_requise","decision_humaine","position_reprise"}
INCIDENT_KEYS={"etat","revision","position_sure","cause"}
CORRECTIF_KEYS={"revision","fichiers_modifies","preuves","succes_annonce"}
PROOF_KEYS={"test","revision","reussi"}

def baseline():
    return (
        {"revision_cible":"r2","fichiers_autorises":{"robot.py"},
         "tests_requis":{"test_un_pas","test_collision"},
         "approbation_requise":False,"decision_humaine":None,
         "position_reprise":(0,1)},
        {"etat":"BLOQUÉE","revision":"r1","position_sure":(0,1),
         "cause":"collision"},
        {"revision":"r2","fichiers_modifies":["robot.py"],
         "preuves":["p1","p2"],"succes_annonce":True},
        {"p1":{"test":"test_un_pas","revision":"r2","reussi":True},
         "p2":{"test":"test_collision","revision":"r2","reussi":True}},
    )

def cases_for_seed(seed=0):
    rng=Random(seed)
    items=[]
    def add(name,change):
        m,i,c,p=baseline()
        change(m,i,c,p)
        items.append({"name":name,"mission":m,"incident":i,"correctif":c,"registre":p})
    add("Correctif conforme",lambda m,i,c,p:None)
    add("Test toujours en échec",lambda m,i,c,p:p["p2"].update(reussi=False))
    add("Fichier modifié interdit",lambda m,i,c,p:c["fichiers_modifies"].append("secret.txt"))
    add("Preuve ancienne révision",lambda m,i,c,p:p["p2"].update(revision="r1"))
    add("Test obligatoire absent",lambda m,i,c,p:c["preuves"].remove("p2"))
    add("Preuve fictive",lambda m,i,c,p:c["preuves"].append("p999"))
    add("Preuve citée deux fois",lambda m,i,c,p:c["preuves"].append("p1"))
    add("Fichier dupliqué",lambda m,i,c,p:c["fichiers_modifies"].append("robot.py"))
    add("Révision inchangée après incident",lambda m,i,c,p:m.update(revision_cible="r1"))
    add("Point de reprise altéré",lambda m,i,c,p:i.update(position_sure=(1,1)))
    add("Incident non bloqué",lambda m,i,c,p:i.update(etat="VALIDÉE"))
    add("Auto-approbation forgée",lambda m,i,c,p:c.update(accord_humain=True))
    add("Approbation humaine absente",lambda m,i,c,p:m.update(approbation_requise=True))
    add("Approbation humaine refusée",lambda m,i,c,p:m.update(approbation_requise=True,decision_humaine=False))
    add("Approbation humaine accordée",lambda m,i,c,p:m.update(approbation_requise=True,decision_humaine=True))
    add("Succès annoncé faux",lambda m,i,c,p:c.update(succes_annonce=False))
    for index in range(3):
        m,i,c,p=baseline()
        original=f"r{rng.randrange(100,400)}"
        new=f"r{rng.randrange(500,900)}"
        file=f"mission_{rng.randrange(1000,9999)}.py"
        test1=f"verifier_{rng.randrange(100,999)}"
        test2=f"tester_{rng.randrange(100,999)}"
        m.update(revision_cible=new,fichiers_autorises={file},tests_requis={test1,test2})
        i.update(revision=original)
        c.update(revision=new,fichiers_modifies=[file])
        p["p1"].update(test=test1,revision=new)
        p["p2"].update(test=test2,revision=new)
        if index==1:p["p2"]["reussi"]=False
        if index==2:m["approbation_requise"]=True
        items.append({"name":f"Contrôle variable {index+1}","mission":m,
                      "incident":i,"correctif":c,"registre":p})
    return tuple(items)

def point_valid(p):
    return (type(p) is tuple and len(p)==2 and
            type(p[0]) is int and type(p[1]) is int and
            0<=p[0]<6 and 0<=p[1]<3)

def oracle(mission,incident,correctif,registre):
    """Oracle indépendant de la fonction écrite par l'élève."""
    try:
        if (type(mission) is not dict or set(mission)!=MISSION_KEYS or
            type(incident) is not dict or set(incident)!=INCIDENT_KEYS or
            type(correctif) is not dict or set(correctif)!=CORRECTIF_KEYS or
            type(registre) is not dict):
            return "BLOQUÉE"
        revision=mission["revision_cible"]
        initial=incident["revision"]
        allowed,required=mission["fichiers_autorises"],mission["tests_requis"]
        if (type(revision) is not str or not revision or
            type(initial) is not str or not initial or revision==initial or
            type(incident["cause"]) is not str or not incident["cause"] or
            incident["etat"]!="BLOQUÉE" or
            not point_valid(mission["position_reprise"]) or
            not point_valid(incident["position_sure"]) or
            mission["position_reprise"]!=incident["position_sure"] or
            type(allowed) is not set or type(required) is not set or not required or
            any(type(t) is not str or not t for t in allowed|required) or
            type(mission["approbation_requise"]) is not bool or
            type(mission["decision_humaine"]) not in (type(None),bool) or
            type(correctif["revision"]) is not str or
            correctif["revision"]!=revision or
            type(correctif["succes_annonce"]) is not bool or
            correctif["succes_annonce"] is not True):
            return "BLOQUÉE"
        files,proof_ids=correctif["fichiers_modifies"],correctif["preuves"]
        if (type(files) is not list or not files or
            any(type(x) is not str or not x for x in files) or
            len(set(files))!=len(files) or not set(files).issubset(allowed) or
            type(proof_ids) is not list or not proof_ids or
            any(type(x) is not str or not x for x in proof_ids) or
            len(set(proof_ids))!=len(proof_ids)):
            return "BLOQUÉE"
        passed=set()
        for proof_id in proof_ids:
            proof=registre.get(proof_id)
            if (type(proof) is not dict or set(proof)!=PROOF_KEYS or
                type(proof["test"]) is not str or not proof["test"] or
                type(proof["revision"]) is not str or
                type(proof["reussi"]) is not bool or proof["reussi"] is not True or
                proof["revision"]!=revision or proof["test"] not in required or
                proof["test"] in passed):
                return "BLOQUÉE"
            passed.add(proof["test"])
        if passed!=required:return "BLOQUÉE"
        if mission["approbation_requise"]:
            if mission["decision_humaine"] is None:return "ATTENTE_HUMAINE"
            if mission["decision_humaine"] is False:return "BLOQUÉE"
        return "REPRISE_AUTORISÉE"
    except (KeyError,TypeError,ValueError):
        return "BLOQUÉE"

SAFE=("__build_class__","abs","all","any","bool","dict","enumerate",
      "int","isinstance","len","list","max","min","object","range",
      "set","sorted","str","sum","tuple","type","zip","Exception",
      "ValueError","TypeError","KeyError","NotImplementedError")

def checked_ast(source):
    if type(source) is not str or not source.strip() or len(source)>18000:
        raise ValueError("Code absent ou trop long (maximum 18 000 caractères).")
    tree=ast.parse(source,filename="t06_eleve.py")
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            raise ValueError("Aucun import n'est nécessaire.")
        if isinstance(node,ast.Attribute) and node.attr.startswith("_"):
            raise ValueError("Accès aux attributs internes interdit.")
        if isinstance(node,ast.Name) and node.id in ("eval","exec","open",
            "compile","__import__","__builtins__","globals","locals",
            "getattr","setattr","vars"):
            raise ValueError("Instruction non autorisée.")
    return tree

def evaluate_source(source,seed=0):
    try:
        if type(seed) is not int or not (0<=seed<2**32):
            raise ValueError("Graine de contrôle invalide.")
        safe={key:getattr(builtins,key) for key in SAFE}
        ns={"__builtins__":safe,"__name__":"t06_student"}
        exec(compile(checked_ast(source),"t06_eleve.py","exec"),ns)
        fn=ns.get("decider_reprise")
        if not callable(fn):
            raise ValueError("Définis decider_reprise(mission, incident, correctif, registre).")
    except BaseException as e:
        return {"success":False,"passed":0,"total":19,"results":[],
                "error":type(e).__name__+" : "+str(e)[:220]}
    results=[]
    for case in cases_for_seed(seed):
        m,i,c,r=(copy.deepcopy(case[k]) for k in ("mission","incident","correctif","registre"))
        before=copy.deepcopy((m,i,c,r))
        expected=oracle(m,i,c,r)
        try:
            ans=fn(m,i,c,r)
            if (type(ans) is not dict or set(ans)!={"etat","motif"} or
                type(ans["etat"]) is not str or ans["etat"] not in ETATS or
                type(ans["motif"]) is not str or not ans["motif"].strip()):
                raise AssertionError("Résultat attendu : dictionnaire etat / motif, motif non vide.")
            if before!=(m,i,c,r):
                raise AssertionError("Une vérification ne doit jamais modifier ses entrées.")
            if ans["etat"]!=expected:
                raise AssertionError("État incorrect : attendu "+expected+".")
            results.append({"name":case["name"],"ok":True,
                "message":{"BLOQUÉE":"Blocage conforme : incident non résolu ou preuves invalides.",
                           "ATTENTE_HUMAINE":"Attente conforme : validation humaine indispensable.",
                           "REPRISE_AUTORISÉE":"Reprise conforme : nouveau correctif et preuves vérifiés."}[expected],
                "trace":{"etat":ans["etat"],"motif":ans["motif"],
                         "revision_initiale":i["revision"],
                         "revision_cible":m["revision_cible"],
                         "preuves_annoncees":c["preuves"],
                         "preuves_registre":sorted(r.keys()),
                         "point_sure":list(i["position_sure"]),
                         "decision_humaine_simulee":m["decision_humaine"]}})
        except BaseException as e:
            results.append({"name":case["name"],"ok":False,
                            "message":type(e).__name__+" : "+str(e)[:200],"trace":None})
    passed=sum(row["ok"] for row in results)
    return {"success":passed==len(results),"passed":passed,"total":len(results),
            "results":results,
            "limits":"Registre et approbation simulés ; aucun changement Git ni privilège réel."}

def evaluate_source_json(source,seed=0):
    return json.dumps(evaluate_source(source,seed),ensure_ascii=False)
