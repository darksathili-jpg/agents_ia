"""T05 — vérifier les rapports non fiables par des preuves indépendantes.
Le registre est construit par le banc de vérification, jamais par l'agent.
Aucune action externe. Pyodide n'est pas une sandbox.
"""
import ast, builtins, copy, json
from random import Random

ETATS=("BLOQUÉE","ATTENTE_HUMAINE","VALIDÉE")
MISSION_KEYS={"revision","fichiers_autorises","tests_requis","approbation_requise","decision_humaine"}
REPORT_KEYS={"revision","fichiers_modifies","preuves","succes_annonce"}
PROOF_KEYS={"test","revision","reussi"}

def baseline():
    return (
        {"revision":"r105","fichiers_autorises":{"robot.py"},
         "tests_requis":{"test_un_pas","test_collision"},
         "approbation_requise":False,"decision_humaine":None},
        {"revision":"r105","fichiers_modifies":["robot.py"],
         "preuves":["p1","p2"],"succes_annonce":True},
        {"p1":{"test":"test_un_pas","revision":"r105","reussi":True},
         "p2":{"test":"test_collision","revision":"r105","reussi":True}}
    )

def cases_for_seed(seed=0):
    rng=Random(seed)
    items=[]
    def add(name,transform):
        m,r,p=baseline()
        transform(m,r,p)
        items.append({"name":name,"mission":m,"rapport":r,"registre":p})
    add("Rapport conforme",lambda m,r,p:None)
    add("Agent annonce un faux succès",lambda m,r,p:p["p2"].update(reussi=False))
    add("Fichier modifié hors périmètre",lambda m,r,p:r["fichiers_modifies"].append("secrets.txt"))
    add("Rapport d'une autre révision",lambda m,r,p:r.update(revision="r104"))
    add("Preuve d'une autre révision",lambda m,r,p:p["p1"].update(revision="r104"))
    add("Test obligatoire absent",lambda m,r,p:r["preuves"].remove("p2"))
    add("Identifiant de preuve inventé",lambda m,r,p:r["preuves"].append("p999"))
    add("Même preuve citée deux fois",lambda m,r,p:r["preuves"].append("p1"))
    add("Accord humain nécessaire",lambda m,r,p:m.update(approbation_requise=True))
    add("Approbation humaine refusée",lambda m,r,p:m.update(approbation_requise=True,decision_humaine=False))
    add("Approbation humaine accordée",lambda m,r,p:m.update(approbation_requise=True,decision_humaine=True))
    add("Agent déclare son propre accord",lambda m,r,p:r.update(accord_humain=True))
    add("Rapport indique un échec",lambda m,r,p:r.update(succes_annonce=False))
    add("Preuve d'un test non requis",lambda m,r,p:p["p2"].update(test="test_inconnu"))
    add("Liste des fichiers vide",lambda m,r,p:r.update(fichiers_modifies=[]))
    add("Aucune preuve disponible",lambda m,r,p:r.update(preuves=[]))
    for i in range(3):
        m,r,p=baseline()
        rev=f"r{rng.randrange(200,999)}"
        filename=f"mission_{rng.randrange(1000,9999)}.py"
        a=f"controle_{rng.randrange(100,999)}"
        b=f"verif_{rng.randrange(100,999)}"
        m.update(revision=rev,fichiers_autorises={filename},tests_requis={a,b})
        r.update(revision=rev,fichiers_modifies=[filename])
        p["p1"].update(test=a,revision=rev)
        p["p2"].update(test=b,revision=rev)
        if i==1:p["p2"]["reussi"]=False
        if i==2:m["approbation_requise"]=True
        items.append({"name":f"Contrôle variable {i+1}","mission":m,"rapport":r,"registre":p})
    return tuple(items)

def oracle(mission,report,registre):
    try:
        if (type(mission) is not dict or set(mission)!=MISSION_KEYS or
            type(report) is not dict or set(report)!=REPORT_KEYS or
            type(registre) is not dict):
            return "BLOQUÉE"
        revision=mission["revision"]
        allowed,required=mission["fichiers_autorises"],mission["tests_requis"]
        if (type(revision) is not str or not revision or
            type(allowed) is not set or type(required) is not set or not required or
            any(type(n) is not str or not n for n in allowed|required) or
            type(mission["approbation_requise"]) is not bool or
            mission["decision_humaine"] not in (None,True,False) or
            type(report["revision"]) is not str or report["revision"]!=revision or
            type(report["succes_annonce"]) is not bool or
            report["succes_annonce"] is not True):
            return "BLOQUÉE"
        files,proofs=report["fichiers_modifies"],report["preuves"]
        if (type(files) is not list or not files or
            any(type(v) is not str or not v for v in files) or
            len(set(files))!=len(files) or not set(files).issubset(allowed) or
            type(proofs) is not list or not proofs or
            any(type(v) is not str or not v for v in proofs) or
            len(set(proofs))!=len(proofs)):
            return "BLOQUÉE"
        checked=set()
        for proof_id in proofs:
            proof=registre.get(proof_id)
            if (type(proof) is not dict or set(proof)!=PROOF_KEYS or
                type(proof["test"]) is not str or
                type(proof["revision"]) is not str or
                type(proof["reussi"]) is not bool or
                proof["revision"]!=revision or proof["reussi"] is not True or
                proof["test"] not in required or proof["test"] in checked):
                return "BLOQUÉE"
            checked.add(proof["test"])
        if checked!=required:return "BLOQUÉE"
        if mission["approbation_requise"]:
            if mission["decision_humaine"] is None:return "ATTENTE_HUMAINE"
            if mission["decision_humaine"] is False:return "BLOQUÉE"
        return "VALIDÉE"
    except (KeyError,TypeError,ValueError):
        return "BLOQUÉE"

SAFE=("__build_class__","abs","all","any","bool","dict","enumerate","int",
      "isinstance","len","list","max","min","object","range","set",
      "sorted","str","sum","tuple","type","zip","Exception","ValueError",
      "TypeError","KeyError","NotImplementedError")

def checked_ast(source):
    if type(source) is not str or not source.strip() or len(source)>16000:
        raise ValueError("Code absent ou trop long (16 000 caractères maximum).")
    tree=ast.parse(source,filename="t05_eleve.py")
    for node in ast.walk(tree):
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            raise ValueError("Aucun import n'est nécessaire.")
        if isinstance(node,ast.Attribute) and node.attr.startswith("_"):
            raise ValueError("Accès interne interdit.")
        if isinstance(node,ast.Name) and node.id in (
            "exec","eval","compile","open","__import__","__builtins__",
            "globals","locals","getattr","setattr","vars"):
            raise ValueError("Instruction interdite.")
    return tree

def evaluate_source(source,seed=0):
    try:
        if type(seed) is not int or not (0<=seed<2**32):
            raise ValueError("Graine invalide.")
        namespace={"__builtins__":{x:getattr(builtins,x) for x in SAFE},
                   "__name__":"t05_student"}
        exec(compile(checked_ast(source),"t05_eleve.py","exec"),namespace)
        fn=namespace.get("controler_mission")
        if not callable(fn):raise ValueError("Définis controler_mission(mission, rapport, registre).")
    except BaseException as e:
        return {"passed":0,"total":19,"success":False,"results":[],
                "error":type(e).__name__+" : "+str(e)[:220]}
    results=[]
    for case in cases_for_seed(seed):
        mission,report,registre=(copy.deepcopy(case[k]) for k in ("mission","rapport","registre"))
        original=copy.deepcopy((mission,report,registre))
        expected=oracle(mission,report,registre)
        try:
            answer=fn(mission,report,registre)
            if (type(answer) is not dict or set(answer)!={"etat","motif"} or
                type(answer["etat"]) is not str or answer["etat"] not in ETATS or
                type(answer["motif"]) is not str or not answer["motif"].strip()):
                raise AssertionError("Renvoyer exactement etat et motif ; motif non vide.")
            if (mission,report,registre)!=original:
                raise AssertionError("Les entrées ne doivent pas être modifiées.")
            if answer["etat"]!=expected:
                raise AssertionError("État incorrect : attendu "+expected+".")
            results.append({"name":case["name"],"ok":True,
                "message":{"BLOQUÉE":"Blocage conforme : preuves ou contrat non valides.",
                           "ATTENTE_HUMAINE":"Attente conforme : accord humain nécessaire.",
                           "VALIDÉE":"Validation conforme : registre indépendant vérifié."}[expected],
                "trace":{"revision":original[0]["revision"],
                         "reussite_annoncee":original[1]["succes_annonce"],
                         "preuves_declarees":original[1]["preuves"],
                         "registre_consulte":sorted(original[2]),
                         "etat":answer["etat"],"motif":answer["motif"],
                         "decision_humaine_simulee":original[0]["decision_humaine"]}})
        except BaseException as e:
            results.append({"name":case["name"],"ok":False,
                            "message":type(e).__name__+" : "+str(e)[:200],"trace":None})
    passed=sum(row["ok"] for row in results)
    return {"passed":passed,"total":len(results),"success":passed==len(results),
            "results":results,
            "limits":"Le registre indépendant est simulé, pas une attestation cryptographique."}

def evaluate_source_json(source,seed=0):
    return json.dumps(evaluate_source(source,seed),ensure_ascii=False)
